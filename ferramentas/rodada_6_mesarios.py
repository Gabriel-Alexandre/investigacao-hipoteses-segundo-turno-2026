"""Rodada 6, H41 (24/11/2026): "o mesmo título de mesário aparece em duas cidades longe uma da outra, com segundos ou
minutos de diferença" (2 reels do Instagram de 23/11 e um comentário no YouTube).

Lê os logs baixados por rodada_6_coletar.py (dados/brutos/rodada6/logs.sqlite) e separa cada número de 12 dígitos pelo
evento em que ele aparece no log:
  mesario_registro   "Mesário N registrado" (o mesário se cadastra na urna no começo do dia)
  mesario_habilita   "Mesário N habilitou o eleitor"
  mesario_biometria  "Biometria do mesário N encontrada nos arquivos coletados"
  mesario_secao      "Mesário N é eleitor da seção" / "não é eleitor da seção"
  mesario_pedido     "Pedido de leitura da biometria do mesário N" / "Biometria coletada não é do mesário N"
  encerramento       "Título digitado para encerramento: N"
  midia              "Mídia de votação/de carga gerada pelo usuário: N" (quem gerou a mídia da urna no cartório; não é mesário)
⛔ O número nunca sai daqui: vira código por HMAC-SHA256 com a chave local (dados/chave-local.txt, fora do git).

Para cada código: em quantas seções e municípios aparece, por quais eventos, e, quando aparece em 2 municípios, a menor
distância de tempo entre um evento de um e de outro. Os pares dos reels são conferidos um a um.

Saída: resultados/RODADA6_MESARIOS.json e resultados/tabelas/r6_h41_*.csv (só códigos, nunca o número).
Uso: python ferramentas/rodada_6_mesarios.py
"""
from __future__ import annotations

import hashlib
import hmac
import io
import json
import re
import sqlite3
import zipfile
from collections import defaultdict
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
BRUTOS = RAIZ / "dados" / "brutos" / "rodada6" / "logs.sqlite"
NOMES = RAIZ.parent / "investigacao-segundo-turno-2026" / "dados" / "derivados" / "municipios_nomes.csv"
TAB = RAIZ / "resultados" / "tabelas"
DIAS = {"1": "04/10/2026", "2": "25/10/2026"}
EVENTOS = [
    ("mesario_registro", re.compile(r"Mes.rio (\d{8,}) registrado")),
    ("mesario_habilita", re.compile(r"Mes.rio (\d{8,}) habilitou o eleitor")),
    ("mesario_biometria", re.compile(r"Biometria do mes.rio (\d{8,}) encontrada")),
    ("mesario_secao", re.compile(r"Mes.rio (\d{8,}) (?:n.o )?. eleitor da se..o")),
    ("mesario_pedido", re.compile(r"(?:Pedido de leitura da biometria do mes.rio|Biometria coletada n.o . do mes.rio) (\d{8,})")),
    ("encerramento", re.compile(r"T.tulo digitado para encerramento: (\d{8,})")),
    ("midia", re.compile(r"M.dia de (?:vota..o|carga) gerada pelo usu.rio: (\d{6,})")),
]
# os pares que os reels citam (município, município, turno, o intervalo que o reel diz)
PARES = [
    ("BRAGANCA", "RIO MARIA", "1", "2 s"), ("DIADEMA", "GUARACI", "1", "6 min"), ("ATALEIA", "GOIANESIA", "1", "7 min"),
    ("MOGI MIRIM", "PETROPOLIS", "1", "16 min"), ("JOSE BONIFACIO", "SAO VICENTE", "1", "17 min"),
    ("PORTO SEGURO", "CASA NOVA", "2", "22 s"), ("CAMACAN", "JUAZEIRO", "2", "32 s"), ("ALAGOINHAS", "PORTO SEGURO", "2", "37 s"),
]


def chave() -> bytes:
    return (RAIZ / "dados" / "chave-local.txt").read_text().strip().encode()


def ler(body: bytes) -> list[str]:
    z = zipfile.ZipFile(io.BytesIO(body))
    nome = next(n for n in z.namelist() if n.lower().endswith(".dat"))
    return z.read(nome).decode("latin-1").splitlines()


def main() -> None:
    k = chave()
    cod = lambda n: hmac.new(k, n.encode(), hashlib.sha256).hexdigest()[:12]
    import unicodedata
    sa = lambda x: unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode().upper().strip()
    nomes = {k2: sa(v) for k2, v in pd.read_csv(NOMES, dtype=str).set_index(["uf", "municipio"]).nome.to_dict().items()}
    con = sqlite3.connect(f"file:{BRUTOS}?mode=ro", uri=True)
    linhas = []
    secoes = set()
    for url, body in con.execute("SELECT url, body FROM raw WHERE status=200 AND url LIKE '%.jez'"):
        p = url.split("/")
        pl, uf, mun, zona, secao = p[-8], p[-6], p[-5], p[-4], p[-3]
        turno = "1" if pl == "3220" else "2"
        secoes.add((turno, uf, mun, zona, secao))
        for l in ler(body):
            c = l.split("\t")
            if len(c) < 5:
                continue
            data_hora = c[0]
            for tipo, rx in EVENTOS:
                m = rx.search(c[4])
                if m:
                    linhas.append((turno, uf, mun, zona, secao, data_hora[:10], data_hora[11:19], tipo, cod(m.group(1)), len(m.group(1))))
                    break
    d = pd.DataFrame(linhas, columns=["turno", "uf", "mun", "zona", "secao", "data", "hora", "tipo", "codigo", "digitos"])
    d["municipio"] = [nomes.get((u, m), m) for u, m in zip(d.uf, d.mun)]
    d["no_dia"] = d.data == d.turno.map(DIAS)
    d["t"] = pd.to_timedelta(d.hora).dt.total_seconds()

    # 1. por código: quantos municípios e por quais eventos
    g = d.groupby(["turno", "codigo"]).agg(municipios=("municipio", "nunique"), secoes=("secao", lambda s: s.size),
                                         tipos=("tipo", lambda s: ",".join(sorted(set(s)))))
    g = g.reset_index()
    multi = g[g.municipios >= 2]
    por_tipo = {}
    for tipo, _ in EVENTOS:
        cods = set(d[d.tipo == tipo].codigo)
        gg = g[g.codigo.isin(cods)]
        por_tipo[tipo] = {"codigos": int(len(gg)), "em_2_ou_mais_municipios": int((gg.municipios >= 2).sum())}

    # 2. os pares dos reels: códigos de mesário (não de mídia) nos 2 municípios, e o menor intervalo
    mes = d[d.tipo.str.startswith("mesario") | (d.tipo == "encerramento")]
    pares = []
    for a, b, t, diz in PARES:
        da = mes[(mes.turno == t) & (mes.municipio.map(lambda x: x.upper()) == a)]
        db = mes[(mes.turno == t) & (mes.municipio.map(lambda x: x.upper()) == b)]
        comuns = set(da.codigo) & set(db.codigo)
        menor = None
        detalhe = []
        for c in comuns:
            ta, tb = da[da.codigo == c], db[db.codigo == c]
            dif = min(abs(x - y) for x in ta.t for y in tb.t)
            detalhe.append({"codigo": c, "menor_intervalo_s": int(dif),
                            "eventos_a": sorted(set(ta.tipo)), "eventos_b": sorted(set(tb.tipo)),
                            "secoes_a": int(ta[["zona", "secao"]].drop_duplicates().shape[0]),
                            "secoes_b": int(tb[["zona", "secao"]].drop_duplicates().shape[0])})
            menor = dif if menor is None else min(menor, dif)
        pares.append({"a": a, "b": b, "turno": t, "o_reel_diz": diz,
                      "secoes_baixadas_a": int(len({s for s in secoes if s[0] == t and nomes.get((s[1], s[2]), "").upper() == a})),
                      "secoes_baixadas_b": int(len({s for s in secoes if s[0] == t and nomes.get((s[1], s[2]), "").upper() == b})),
                      "codigos_de_mesario_em_comum": len(comuns), "menor_intervalo_s": None if menor is None else int(menor),
                      "detalhe": sorted(detalhe, key=lambda x: x["menor_intervalo_s"])[:10]})

    # 3. todo código de mesário em 2+ municípios, no conjunto inteiro: o que o número fez em cada lugar
    mm = mes.groupby(["turno", "codigo"]).agg(municipios=("municipio", "nunique"), digitos=("digitos", "max")).reset_index()
    multi = mm[mm.municipios >= 2]
    casos = []
    for r in multi.itertuples():
        x = mes[(mes.turno == r.turno) & (mes.codigo == r.codigo)]
        lugares = []
        for (mun, z, sc), y in x.groupby(["municipio", "zona", "secao"]):
            reg = y[y.tipo == "mesario_registro"]
            lugares.append({"municipio": mun, "habilitou_eleitores": int((y.tipo == "mesario_habilita").sum()),
                            "biometria_encontrada": int((y.tipo == "mesario_biometria").sum()),
                            "registros": int(len(reg)), "registro_so_no_fim_do_dia": bool(len(reg) and reg.t.min() >= 16.5 * 3600),
                            "primeiro": str(y.hora.min()), "ultimo": str(y.hora.max())})
        atuou = [l for l in lugares if l["habilitou_eleitores"] > 0 or l["biometria_encontrada"] > 0]
        munis_atuou = {l["municipio"] for l in atuou}
        casos.append({"turno": r.turno, "codigo": r.codigo, "municipios": int(r.municipios), "lugares": lugares,
                      "municipios_em_que_liberou_eleitor_ou_teve_biometria": len(munis_atuou),
                      "so_digitado_no_registro_em_algum_lugar": any(l["habilitou_eleitores"] == 0 and l["biometria_encontrada"] == 0 for l in lugares)})
    TAB.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([{"turno": c["turno"], "codigo": c["codigo"], "municipios": c["municipios"],
                   "municipios_em_que_atuou": c["municipios_em_que_liberou_eleitor_ou_teve_biometria"],
                   "lugares": "; ".join(f"{l['municipio']} hab={l['habilitou_eleitores']} bio={l['biometria_encontrada']} reg_fim={l['registro_so_no_fim_do_dia']}" for l in c["lugares"])}
                  for c in casos]).to_csv(TAB / "r6_h41_codigos_em_2_municipios.csv", index=False)
    resumo_multi = {"codigos": len(casos),
                    "atuou_em_2_ou_mais_municipios": sum(c["municipios_em_que_liberou_eleitor_ou_teve_biometria"] >= 2 for c in casos),
                    "atuou_em_1_e_so_foi_digitado_no_outro": sum(c["municipios_em_que_liberou_eleitor_ou_teve_biometria"] == 1 for c in casos),
                    "nao_atuou_em_nenhum": sum(c["municipios_em_que_liberou_eleitor_ou_teve_biometria"] == 0 for c in casos)}
    # a régua: o mesmo número em 2+ seções do MESMO município (substituição e remanejamento são permitidos)
    mesmo_mun = mes.groupby(["turno", "codigo"]).agg(secoes=("secao", lambda s: s.size), municipios=("municipio", "nunique"))
    sec = mes.drop_duplicates(["turno", "codigo", "municipio", "zona", "secao"]).groupby(["turno", "codigo"]).size()
    regua = {"codigos_em_2_ou_mais_secoes_do_mesmo_municipio": int(((sec >= 2) & (mm.set_index(["turno", "codigo"]).municipios == 1)).sum())}
    out = {"secoes_lidas": len(secoes), "eventos_lidos": int(len(d)), "eventos_fora_do_dia": int((~d.no_dia).sum()),
           "por_tipo_de_evento": por_tipo, "pares_dos_reels": pares,
           "mesario_em_2_ou_mais_municipios": resumo_multi, "casos": casos, "regua_mesmo_municipio": regua,
           "codigos_de_mesario_no_total": int(len(mm))}
    (RAIZ / "resultados" / "RODADA6_MESARIOS.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k2: v for k2, v in out.items() if k2 not in ("pares_dos_reels", "casos")}, ensure_ascii=False, indent=1))
    for p in pares:
        print(p["a"], p["b"], p["turno"], p["o_reel_diz"], p["secoes_baixadas_a"], p["secoes_baixadas_b"], p["codigos_de_mesario_em_comum"], p["menor_intervalo_s"])


if __name__ == "__main__":
    main()
