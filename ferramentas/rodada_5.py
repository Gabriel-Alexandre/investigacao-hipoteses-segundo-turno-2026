"""Rodada 5 (17/11/2026): a resposta do TRE-PE ao pedido por LAI e duas hipoteses novas dos comentarios.

H37  a resposta do TRE-PE (protocolo 82034721135306, 13/11/2026) conferida contra o log de cada urna do 1o turno:
     cobertura da resposta, impugnacoes, fiscais, caderno de votacao x liberacoes sem digital, e os casos que
     as atas e os e-mails trazem (Jatauba, Parnamirim, Condado, Jaboatao, Caruaru).
H38  "os votos de 2022 foram reescritos em 2026": a mesma secao repete em 2026 o numero de 2022?

Entradas: dados/brutos/rodada5/ (rodada_5_coletar.py), dados/lai/tre_pe_resposta_2026-11-13.csv (a resposta
transcrita, uma linha por secao do pedido), dados/copias/s2022_t2.parquet e t2_secoes.parquet.
Saidas: resultados/RODADA5.json e resultados/tabelas/r5_*.csv. Sem rede.
Uso: python ferramentas/rodada_5.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from hipoteses.log import ler_jez, ler_log  # noqa: E402

BR = RAIZ / "dados" / "brutos" / "rodada5"
LAI = RAIZ / "dados" / "lai" / "tre_pe_resposta_2026-11-13.csv"
C = RAIZ / "dados" / "copias"
OUT = RAIZ / "resultados" / "RODADA5.json"
TAB = RAIZ / "resultados" / "tabelas"
DIA = "04/10/2026"
H17 = 17 * 3600


def hhmm(s):
    if s is None or (isinstance(s, float) and np.isnan(s)):
        return None
    s = int(s)
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}"


def blocos(linhas):
    """Divide o dia em atendimentos: cada 'Aguardando digitacao do identificador' abre um."""
    ev = []
    for ln in linhas:
        if not ln.startswith(DIA):
            continue
        p = ln.split("\t")
        if len(p) > 4:
            ev.append((p[0][11:19], p[3], p[4]))
    out, cur = [], None
    reinicios = []
    for h, app, m in ev:
        if app == "VOTA" and m.startswith("Iniciando aplica"):
            reinicios.append(h)
        if app != "VOTA":
            continue
        if m.startswith("Aguardando digita"):
            if cur:
                out.append(cur)
            cur = [(h, m)]
        elif cur is not None:
            cur.append((h, m))
    if cur:
        out.append(cur)
    return out, reinicios


def ler_secao(zona, secao):
    f = BR / f"{zona}-{secao}-log.jez"
    linhas = ler_jez(f.read_bytes())
    lt = ler_log(linhas, b"rodada5", dia=DIA)
    el = pd.DataFrame(lt.eleitores, columns=["t", "tipo", "nao_confere", "mes", "tent", "ident", "susp", "hab", "suspm", "hab_s"])
    bl, reinicios = blocos(linhas)
    canceladas = sum(any("cancelada" in m for _, m in b) for b in bl)
    sem_voto_com_dado = sum(any("dado pessoal" in m for _, m in b) and not any("foi computado" in m for _, m in b) for b in bl)
    # quatro tentativas de digital sem reconhecer, em qualquer atendimento (com ou sem voto no fim)
    quatro_falhas = sum(any("Tentativa [4] de [4]" in m and m.startswith("N") for _, m in b) for b in bl)
    # leitura por um 2o caminho: contar direto os eventos de liberacao, sem o classificador
    ev_mesario = sum(1 for ln in linhas if ln.startswith(DIA) and "habilitou o eleitor" in ln)
    ev_ano = sum(1 for ln in linhas if ln.startswith(DIA) and ("Ano de nascimento digitado" in ln and "igual" in ln))
    ev_bio = sum(1 for ln in linhas if ln.startswith(DIA) and "[biom" in ln and "Tipo de habilita" in ln)
    ev_voto = sum(1 for ln in linhas if ln.startswith(DIA) and "O voto do eleitor foi computado" in ln)
    jv = [hhmm(s) for s in lt.ja_votou]
    r = {
        "zona": zona, "secao": secao,
        "votos": int(len(el)),
        "biometrica": int((el.tipo == "biometrica").sum()),
        "digital_falhou_mesario": int((el.tipo == "manual_mes").sum()),
        "sem_digital_cadastrada_ano": int((el.tipo == "manual_sem").sum()),
        "outra": int((el.tipo == "outra").sum()),
        "votos_apos_17h": int((el.t >= H17).sum()),
        "sem_digital_apos_17h": int(((el.t >= H17) & (el.tipo != "biometrica")).sum()),
        "primeiro_voto": hhmm(el.t.min()) if len(el) else None,
        "ultimo_voto": hhmm(el.t.max()) if len(el) else None,
        "votos_apos_17h10": int((el.t >= 17 * 3600 + 600).sum()),
        "habilitacoes_canceladas": int(canceladas),
        "dado_pedido_sem_voto": int(sem_voto_com_dado),
        "atendimentos_4_falhas_digital": int(quatro_falhas),
        "reinicios_no_dia": reinicios,
        "ja_votou": len(jv), "ja_votou_horas": jv,
        "segundo_caminho": {"ev_mesario_habilitou": ev_mesario, "ev_ano_igual": ev_ano, "ev_biometrica": ev_bio, "ev_voto": ev_voto},
    }
    r["deviam_assinar"] = r["digital_falhou_mesario"] + r["sem_digital_cadastrada_ano"]
    return r, el


def h37():
    tre = pd.read_csv(LAI, dtype=str).fillna("")
    linhas, por_hora = [], {}
    for _, t in tre.iterrows():
        z, s = int(t.zona), int(t.secao)
        r, el = ler_secao(z, s)
        r["municipio"] = t.municipio
        r["tipo_resposta"] = t.tipo_resposta
        linhas.append(r)
        por_hora[f"{z}-{s}"] = el
    lg = pd.DataFrame(linhas)
    x = tre.copy()
    x["zona"] = x.zona.astype(int)
    x["secao"] = x.secao.astype(int)
    m = x.merge(lg.drop(columns=["municipio", "tipo_resposta"]), on=["zona", "secao"])

    def num(col):
        return pd.to_numeric(m[col], errors="coerce")

    # cobertura
    cob = m.tipo_resposta.value_counts().to_dict()
    com_conteudo = int(m.tipo_resposta.isin(["conteudo", "ata"]).sum())
    imp = m.impugnacao_ou_protesto.value_counts().to_dict()
    fis = num("fiscais_documentados")
    fiscais = {
        "secoes_com_numero": int(fis.notna().sum()),
        "secoes_sem_fiscal": int((fis == 0).sum()),
        "secoes_com_fiscal": int((fis > 0).sum()),
        "secoes_com_fiscal_do_pl": int(m.fiscais_partidos.str.contains("PL").sum()),
        "fiscais_do_pl": int(m.fiscais_partidos.str.count(r"\bPL\b").sum()),
    }

    # caderno x log: quem precisava assinar (todo eleitor liberado sem a digital: a digital falhou ou nao existe)
    cad = []
    for _, r in m.iterrows():
        ass = pd.to_numeric(r.assinaturas_caderno, errors="coerce")
        behb = pd.to_numeric(r.behb, errors="coerce")
        cit = pd.to_numeric(r.sem_biometria_citado_pelo_cartorio, errors="coerce")
        bsem = pd.to_numeric(r.behb_sem_assinatura, errors="coerce")
        ab = pd.to_numeric(r.assinaturas_de_eleitores_com_biometria_cadastrada, errors="coerce")
        if all(pd.isna(v) for v in (ass, behb, cit, ab)) and r.todos_sem_biometria_assinaram == "":
            continue
        d = {"zona": r.zona, "secao": r.secao, "municipio": r.municipio,
             "log_digital_falhou": r.digital_falhou_mesario, "log_sem_digital_cadastrada": r.sem_digital_cadastrada_ano,
             "log_deviam_assinar": r.deviam_assinar,
             "tre_assinaturas": None if pd.isna(ass) else int(ass), "tre_behb": None if pd.isna(behb) else int(behb),
             "tre_sem_biometria_citado": None if pd.isna(cit) else int(cit),
             "tre_behb_sem_assinatura": None if pd.isna(bsem) else int(bsem),
             "tre_assinaturas_com_biometria_cadastrada": None if pd.isna(ab) else int(ab),
             "tre_todos_assinaram": r.todos_sem_biometria_assinaram,
             "secao_citada": r.secao_citada_na_resposta}
        d["behb_menos_log"] = None if pd.isna(behb) else int(behb) - int(r.digital_falhou_mesario)
        # minimo de liberacoes sem digital sem assinatura, supondo que nenhum eleitor com digital reconhecida assinou
        d["minimo_sem_assinatura"] = None if pd.isna(ass) else max(0, int(r.deviam_assinar) - int(ass))
        if not pd.isna(bsem):
            d["minimo_sem_assinatura"] = int(bsem)  # o cartorio contou direto, so dentro do BEHB
        if not pd.isna(ab):
            d["minimo_sem_assinatura"] = max(0, int(r.digital_falhou_mesario) - int(ab))  # 318: so as de quem tem digital cadastrada
        cad.append(d)
    cad = pd.DataFrame(cad)
    cad.to_csv(TAB / "r5_caderno_x_log.csv", index=False)

    # Jatauba (54/185): o relato do cartorio contra o log
    j = lg[(lg.zona == 54) & (lg.secao == 185)].iloc[0]
    elj = por_hora["54-185"]
    jat = {"votos": int(j.votos), "digital_falhou_mesario": int(j.digital_falhou_mesario),
           "pct_sem_reconhecimento": round(100 * (j.votos - j.biometrica) / j.votos, 1),
           "biometrica": int(j.biometrica), "primeiro_voto": j.primeiro_voto, "ultimo_voto": j.ultimo_voto,
           "reinicios": j.reinicios_no_dia,
           "biometricas_antes_9h21": int(((elj.tipo == "biometrica") & (elj.t < 9 * 3600 + 21 * 60)).sum()),
           "votos_entre_9h08_e_9h21": int(((elj.t >= 9 * 3600 + 8 * 60) & (elj.t < 9 * 3600 + 21 * 60)).sum())}

    # as secoes do pedido no contexto de PE e do Brasil: % de liberacao sem digital
    lg["pct_sem_digital"] = 100 * (lg.votos - lg.biometrica) / lg.votos
    lg.to_csv(TAB / "r5_log_por_secao.csv", index=False)

    sem_ass = cad.minimo_sem_assinatura.dropna()
    return {
        "secoes_no_pedido": int(len(m)),
        "cobertura": cob, "secoes_com_conteudo": com_conteudo,
        "atas_enviadas": int((m.ata_enviada == "sim").sum()),
        "impugnacao_ou_protesto": imp,
        "secoes_com_informacao_de_impugnacao": int((m.impugnacao_ou_protesto == "nao").sum()),
        "fiscais": fiscais,
        "caderno": {
            "secoes_com_dado_de_caderno": int(len(cad)),
            "secoes_com_minimo_sem_assinatura": int((sem_ass > 0).sum()),
            "soma_minimo_sem_assinatura": int(sem_ass.sum()),
            "tabela": cad.to_dict(orient="records"),
        },
        "log_bate_com_o_numero_do_cartorio": {
            "101-724_sem_digital_cadastrada": [int(m[(m.zona == 101) & (m.secao == 724)].sem_digital_cadastrada_ano.iloc[0]), 97],
            "105-356_behb": [int(m[(m.zona == 105) & (m.secao == 356)].digital_falhou_mesario.iloc[0]), 5],
            "105-247_behb": [int(m[(m.zona == 105) & (m.secao == 247)].digital_falhou_mesario.iloc[0]), 24],
            "106-321_behb": [int(m[(m.zona == 106) & (m.secao == 321)].digital_falhou_mesario.iloc[0]), 29],
            "106-325_behb": [int(m[(m.zona == 106) & (m.secao == 325)].digital_falhou_mesario.iloc[0]), 14],
        },
        "jatauba": jat,
        "secao_121_24_e_274": {k: {c: int(ler_secao(121, k)[0][c]) for c in ("votos", "digital_falhou_mesario", "sem_digital_cadastrada_ano")} for k in (24, 274)},
        "pct_sem_digital_nas_41": {"mediana": round(float(lg.pct_sem_digital.median()), 1),
                                    "min": round(float(lg.pct_sem_digital.min()), 1), "max": round(float(lg.pct_sem_digital.max()), 1)},
        "por_secao": lg.drop(columns=["segundo_caminho"]).to_dict(orient="records"),
        "segundo_caminho": {f"{r.zona}-{r.secao}": r.segundo_caminho for r in lg.itertuples()},
    }


def h38():
    """A mesma secao repete em 2026 o numero do Lula de 2022? Espelho: o Flavio repete o Bolsonaro?"""
    a = pd.read_parquet(C / "t2_secoes.parquet", columns=["uf", "municipio", "zona", "secao", "bu_lula", "bu_flavio", "bu_branco", "bu_nulo"])
    b = pd.read_parquet(C / "s2022_t2.parquet")
    for d in (a, b):
        d["uf"] = d.uf.str.lower()
        for c, n in (("municipio", 5), ("zona", 4), ("secao", 4)):
            d[c] = d[c].astype(str).str.zfill(n)
    a = a.dropna(subset=["bu_lula", "bu_flavio"])
    x = a.merge(b, on=["uf", "municipio", "zona", "secao"], how="inner")
    n = len(x)
    lula_igual = int((x.bu_lula == x.lula).sum())
    flavio_igual_bolso = int((x.bu_flavio == x.bolsonaro).sum())
    os_dois_iguais = int(((x.bu_lula == x.lula) & (x.bu_flavio == x.bolsonaro)).sum())
    boletim_igual = int(((x.bu_lula == x.lula) & (x.bu_flavio == x.bolsonaro) & (x.bu_branco == x.branco) & (x.bu_nulo == x.nulo)).sum())
    # o teste que decide: se numeros de 2022 tivessem sido copiados, a diferenca 2026 - 2022 teria um pico no zero.
    # Sem copia, o zero fica no meio da curva, com o -1 e o +1 do lado quase do mesmo tamanho.
    dl = (x.bu_lula - x.lula).astype(int).value_counts()
    df = (x.bu_flavio - x.bolsonaro).astype(int).value_counts()
    def pico(v):
        viz = np.mean([v.get(k, 0) for k in (-2, -1, 1, 2)])
        return {"no_zero": int(v.get(0, 0)), "media_vizinhos_-2_a_2": round(float(viz), 1), "razao": round(float(v.get(0, 0) / viz), 3),
                "contagem_-3_a_3": {int(k): int(v.get(k, 0)) for k in range(-3, 4)}}
    return {
        "pico_lula": pico(dl), "pico_flavio": pico(df),
        "secoes_casadas_2022_2026": n,
        "lula_2026_igual_lula_2022": lula_igual, "pct": round(100 * lula_igual / n, 2),
        "flavio_2026_igual_bolsonaro_2022": flavio_igual_bolso, "pct_espelho": round(100 * flavio_igual_bolso / n, 2),
        "os_dois_iguais": os_dois_iguais, "boletim_inteiro_igual": boletim_igual,
    }


def main():
    TAB.mkdir(parents=True, exist_ok=True)
    out = {"H37": h37(), "H38": h38()}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    r = out["H37"]
    print("cobertura", r["cobertura"], "com conteudo", r["secoes_com_conteudo"])
    print("impugnacao", r["impugnacao_ou_protesto"], "fiscais", r["fiscais"])
    print("caderno", {k: v for k, v in r["caderno"].items() if k != "tabela"})
    print(pd.DataFrame(r["caderno"]["tabela"]).to_string())
    print("bate", r["log_bate_com_o_numero_do_cartorio"])
    print("jatauba", r["jatauba"])
    print("121", r["secao_121_24_e_274"], r["pct_sem_digital_nas_41"])
    print("H38", out["H38"])


if __name__ == "__main__":
    main()
