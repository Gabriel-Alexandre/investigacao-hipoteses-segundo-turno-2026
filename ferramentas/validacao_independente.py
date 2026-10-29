"""Validação por outro caminho: os números centrais refeitos SEM importar analise.py e SEM as tabelas copiadas do
vídeo 16, a partir de arquivos que o projeto baixou por conta própria:

  votacao_secao_2026_BR.zip   a votação por seção que o TSE publica nos dados abertos (outro produto que não o boletim)
  amostra.sqlite              os logs brutos da amostra, lidos aqui com uma expressão regular simples, sem hipoteses/log.py
  perfil_eleitorado_2026.zip  o eleitorado, somado direto do CSV
  ibge (json)                 a população do Censo, somada direto das respostas da API

Cada checagem compara com o número do RESUMO.json (ou com um número público) e diz se passou.
Uso: python ferramentas/validacao_independente.py   ->  resultados/VALIDACAO.json
"""
import io
import json
import re
import sqlite3
import zipfile
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
B = RAIZ / "dados/brutos"
FUSO = {"ac": 2, "am": 1, "ro": 1, "rr": 1, "mt": 1, "ms": 1}


def votacao_secao():
    z = zipfile.ZipFile(B / "tse/votacao_secao_2026_BR.zip")
    nome = next(n for n in z.namelist() if n.lower().endswith(".csv"))
    cols = ["NR_TURNO", "SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO", "NR_ZONA", "NR_SECAO", "CD_CARGO", "NR_VOTAVEL", "QT_VOTOS"]
    partes = []
    for ch in pd.read_csv(z.open(nome), sep=";", encoding="latin1", dtype=str, usecols=lambda c: c in cols, chunksize=2_000_000, keep_default_na=False):
        ch = ch[(ch.CD_CARGO == "1") & ch.NR_VOTAVEL.isin(["13", "22"])]
        partes.append(ch)
    v = pd.concat(partes)
    v["QT_VOTOS"] = v.QT_VOTOS.astype(int)
    p = v.pivot_table(index=["NR_TURNO", "SG_UF", "CD_MUNICIPIO", "NM_MUNICIPIO", "NR_ZONA", "NR_SECAO"], columns="NR_VOTAVEL", values="QT_VOTOS", aggfunc="sum", fill_value=0).reset_index()
    p.columns.name = None
    return p.rename(columns={"13": "lula", "22": "flavio"})


def contar_17h_nos_logs():
    """Votos computados com hora a partir das 17h00 de Brasília em 25/10, contados direto no texto do log."""
    con = sqlite3.connect(B / "t2/amostra.sqlite")
    rx_url = re.compile(r"/dados/(\w\w)/(\d+)/(\d+)/(\d+)/")
    out = {}
    for url, corpo in con.execute("SELECT url, body FROM raw WHERE status=200 AND url LIKE '%-log.jez'"):
        uf, mun, zona, secao = rx_url.search(url).groups()
        z = zipfile.ZipFile(io.BytesIO(corpo))
        txt = z.read([n for n in z.namelist() if n.endswith(".dat")][0]).decode("latin-1")
        n = 0
        for ln in txt.splitlines():
            if ln.startswith("25/10/2026") and "O voto do eleitor foi computado" in ln:
                h = int(ln[11:13]) + FUSO.get(uf, 0)
                if h >= 17:
                    n += 1
        out[(uf, mun, zona, secao)] = n
    return out


def main():
    r = json.loads((RAIZ / "resultados/RESUMO.json").read_text(encoding="utf-8"))
    ch = []

    def conferir(nome, obtido, esperado, fonte):
        ch.append({"checagem": nome, "obtido": obtido, "esperado": esperado, "fonte_do_esperado": fonte, "passou": bool(obtido == esperado)})

    v = votacao_secao()
    t2 = v[v.NR_TURNO == "2"].copy()
    t1 = v[v.NR_TURNO == "1"]
    conferir("Lula no 2º turno (votação por seção dos dados abertos)", int(t2.lula.sum()), 64256232, "resultado proclamado pelo TSE")
    conferir("Flávio no 2º turno (votação por seção dos dados abertos)", int(t2.flavio.sum()), 59826041, "resultado proclamado pelo TSE")
    br = t2[t2.SG_UF != "ZZ"]
    zf = br[(br.flavio == 0) & (br.lula > 0)]
    conferir("seções sem voto do Flávio", int(len(zf)), r["H07"]["secoes"], "RESUMO.json H07")
    conferir("votos do Lula nessas seções", int(zf.lula.sum()), r["H07"]["votos_lula"], "RESUMO.json H07")
    conferir("seções sem voto do Lula", int(((br.lula == 0) & (br.flavio > 0)).sum()), r["H07"]["espelho_zero_lula"]["secoes"], "RESUMO.json H07")
    k = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO"]
    j = zf.merge(t1[k + ["flavio"]].rename(columns={"flavio": "flavio_1t"}), on=k, how="left")
    conferir("votos do Flávio no 1º turno nessas seções", int(j.flavio_1t.fillna(0).sum()), r["H07"]["flavio_no_1t_2026_nessas_votos"], "RESUMO.json H07")
    nom = br.lula + br.flavio
    conferir("seções com mais de 90% para o Lula", int((br.lula / nom > 0.9).sum()), r["H04"]["acima_90_lula"], "RESUMO.json H04")
    conferir("seções com mais de 90% para o Flávio", int((br.flavio / nom > 0.9).sum()), r["H04"]["acima_90_flavio"], "RESUMO.json H04")
    rep = int((br[nom > 0].groupby(["lula", "flavio"]).size() >= 2).sum())
    conferir("placares repetidos (Lula, Flávio)", rep, r["H08"]["placares_repetidos_2026"], "RESUMO.json H08")
    tf = t2[(t2.SG_UF == "BA") & (t2.NM_MUNICIPIO.str.upper() == "TEIXEIRA DE FREITAS")]
    conferir("Teixeira de Freitas, Flávio", int(tf.flavio.sum()), 41454, "Aos Fatos, 28/10")
    conferir("Teixeira de Freitas, Lula", int(tf.lula.sum()), 41361, "Aos Fatos, 28/10")
    fu = br[br.SG_UF.str.lower().isin(FUSO)]
    conferir("Flávio nos 6 estados com fuso (%)", round(100 * fu.flavio.sum() / (fu.lula + fu.flavio).sum(), 2),
             r["H01"]["reproducao_do_relatorio"]["flavio_pct_nessas"], "RESUMO.json H01 (só as seções do grupo até 17h, que são quase todas)")

    # logs: contagem independente de votos depois das 17h, nas seções sorteadas, contra a tabela do vídeo 16
    n17 = contar_17h_nos_logs()
    amostra = pd.read_csv(RAIZ / "dados/derivados/amostra_secoes.csv", dtype=str)
    sorteio = amostra[amostra.grupo.str.contains("sorteio")]
    tab = pd.read_parquet(RAIZ / "dados/copias/t2_secoes.parquet")
    tab = tab.merge(sorteio[["uf", "municipio", "zona", "secao"]], on=["uf", "municipio", "zona", "secao"])
    soma_tab = int(tab.log_votos_depois_17h.fillna(0).sum())
    soma_ind = int(sum(n17.get(tuple(x), 0) for x in sorteio[["uf", "municipio", "zona", "secao"]].itertuples(index=False)))
    conferir("votos depois das 17h nas 12 mil seções sorteadas (log lido de novo × tabela do vídeo 16)", soma_ind, soma_tab, "tabela do vídeo 16")

    # eleitorado e Censo
    z = zipfile.ZipFile(B / "tse/perfil_eleitorado_2026.zip")
    tot = 0
    for n in z.namelist():
        if n.lower().endswith(".csv") and not n.upper().endswith("_BRASIL.CSV"):
            for c in pd.read_csv(z.open(n), sep=";", encoding="latin1", usecols=["QT_ELEITORES"], chunksize=2_000_000):
                tot += int(c.QT_ELEITORES.sum())
    conferir("eleitorado 2026", tot, 158745463, "TSE, eleitorado apto em 2026")
    ib = json.loads((B / "ibge/censo2022_9514_total.json").read_text(encoding="utf-8"))
    pop = sum(int(s["serie"]["2022"]) for resp in ib for b in resp[0]["resultados"] for s in b["series"])
    conferir("população do Censo 2022", pop, 203080756, "IBGE, Censo 2022")

    out = {"checagens": ch, "passaram": int(sum(c["passou"] for c in ch)), "total": len(ch)}
    (RAIZ / "resultados/VALIDACAO.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    for c in ch:
        print("OK " if c["passou"] else "XX ", c["checagem"], c["obtido"], c["esperado"])
    print(out["passaram"], "de", out["total"])


if __name__ == "__main__":
    main()
