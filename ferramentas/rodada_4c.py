"""Rodada 4c (10/11/2026): mais quatro pedidos do publico, lidos nos 908 comentarios dos dias 31/10 a 10/11.

H33  secoes abertas depois das 17h contra as que fecharam no horario: o Lula cresceu igual nos dois grupos?
H34  secoes que mudaram de local de votacao entre os turnos: como votaram?
H35  onde o Flavio era mais forte no 1o turno, o Lula cresceu mais? (o desenho geral, com 2022 de espelho)
H36  conferencias de fato: voto no exterior, Santa Catarina "mais de 3 milhoes" e secao com mais votantes que eleitores

Le so o que ja esta em dados/. Escreve resultados/RODADA4C.json. Sem rede.
Uso: python ferramentas/rodada_4c.py
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from rodada_4 import C, D, RAIZ, base_secoes, boot_slope, demean, m2022, municipios, pct, slope

OUT = RAIZ / "resultados" / "RODADA4C.json"
# diferenca para Brasilia (BRT = hora local + N) no dia 25/10/2026 (sem horario de verao)
OFFSET = {"ac": 2, "am": 1, "mt": 1, "ms": 1, "ro": 1, "rr": 1}


def h33(b):
    t2 = pd.read_parquet(C / "t2_secoes.parquet", columns=["uf", "municipio", "zona", "secao", "encerramento"])
    t2["k"] = t2.uf.str.lower() + "|" + t2.municipio.astype(str).str.zfill(5) + "|" + t2.zona.astype(str).str.zfill(4) + "|" + t2.secao.astype(str).str.zfill(4)
    t2["enc"] = pd.to_datetime(t2.encerramento, errors="coerce")
    t2 = t2.dropna(subset=["enc"])
    t2["brt"] = t2.enc + pd.to_timedelta(t2.uf.str.lower().map(OFFSET).fillna(0), unit="h")
    t2["hora_brt"] = t2.brt.dt.hour + t2.brt.dt.minute / 60
    x = b.merge(t2[["k", "hora_brt", "uf"]], on="k", how="inner", suffixes=("", "_t2"))
    x = x[(x.hora_brt >= 15) & (x.hora_brt <= 21)].copy()
    x["tarde"] = x.hora_brt > 17.25
    x["dls"] = 100 * (x.ls2 - x.ls1)
    n_tarde = int(x.tarde.sum())
    # dentro do municipio: a variacao do Lula nas que fecharam tarde menos a das que fecharam no horario, nos municipios que tem os dois grupos
    g = x.groupby("mun").tarde.agg(["sum", "count"])
    ambos = g[(g["sum"] > 0) & (g["sum"] < g["count"])].index
    y = x[x.mun.isin(ambos)].copy()
    y["dls_d"] = demean(y, "dls")
    y["t"] = y.tarde.astype(float)
    y["t_d"] = demean(y, "t")
    inc = slope(y.t_d, y.dls_d)
    ci = boot_slope(y.t_d, y.dls_d, y.mun, B=200)
    # o mesmo para o 1o turno (o espelho: o Lula no 1o turno nessas secoes, contra o resto do municipio)
    y["ls1_d"] = demean(y.assign(v=100 * y.ls1), "v")
    inc_t1 = slope(y.t_d, y.ls1_d)
    cortes = {}
    for c in (17.0, 17.25, 17.5, 18.0):
        yy = y.copy()
        yy["t"] = (yy.hora_brt > c).astype(float)
        if yy.t.sum() < 200:
            continue
        yy["t_d"] = demean(yy, "t")
        cortes[f"depois_das_{c:.2f}".replace(".", "h")] = {"secoes": int(yy.t.sum()), "inclinacao": round(slope(yy.t_d, yy.dls_d), 3)}
    # histograma de horario (em BRT) das secoes
    hist = x.hora_brt.round(0).value_counts().sort_index()
    return {
        "secoes_com_horario": int(len(x)), "fecharam_depois_das_17h15_brt": n_tarde, "pct": pct(n_tarde, len(x), 2),
        "municipios_com_os_dois_grupos": int(len(ambos)),
        "variacao_media_do_lula_pontos_tarde": round(float(x[x.tarde].dls.mean()), 2), "variacao_media_do_lula_pontos_no_horario": round(float(x[~x.tarde].dls.mean()), 2),
        "diferenca_dentro_do_municipio_pontos": round(inc, 3), "intervalo_95_bootstrap": ci,
        "diferenca_no_1o_turno_pontos_(espelho)": round(inc_t1, 3),
        "outros_cortes": cortes,
        "fechamento_por_hora_brt": {f"{int(k):02d}h": int(v) for k, v in hist.items()},
    }


def h34():
    d = pd.read_parquet(D / "detalhe_secao_2026.parquet", columns=["uf", "municipio", "zona", "secao", "turno", "local", "comparecimento", "aptos"])
    d = d[d.uf != "zz"].copy()
    d["k"] = d.uf.str.lower() + "|" + d.municipio.astype(str).str.zfill(5) + "|" + d.zona.astype(str).str.zfill(4) + "|" + d.secao.astype(str).str.zfill(4)
    p = d.pivot_table(index="k", columns="turno", values="local", aggfunc="first")
    p.columns = ["l1", "l2"]
    p = p.dropna()
    p["mudou"] = p.l1 != p.l2
    b = base_secoes()
    x = b.merge(p[["mudou"]].reset_index(), on="k", how="inner")
    x["dls"] = 100 * (x.ls2 - x.ls1)
    x["m"] = x.mudou.astype(float)
    x["m_d"] = demean(x, "m")
    x["dls_d"] = demean(x, "dls")
    n = int(x.mudou.sum())
    por_uf = x.groupby(x.uf).mudou.agg(["sum", "count"])
    por_uf["pct"] = 100 * por_uf["sum"] / por_uf["count"]
    return {
        "secoes_nos_dois_turnos": int(len(x)), "mudaram_de_local": n, "pct": pct(n, len(x), 2),
        "variacao_do_lula_nas_que_mudaram_pontos": round(float(x[x.mudou].dls.mean()), 2), "variacao_do_lula_nas_que_ficaram_pontos": round(float(x[~x.mudou].dls.mean()), 2),
        "diferenca_dentro_do_municipio_pontos": round(slope(x.m_d, x.dls_d), 3), "intervalo_95_bootstrap": boot_slope(x.m_d, x.dls_d, x.mun, B=200),
        "ufs_com_mais_mudancas": [{"uf": i.upper(), "mudaram": int(r["sum"]), "de": int(r["count"]), "pct": round(float(r.pct), 2)} for i, r in por_uf.sort_values("sum", ascending=False).head(6).iterrows()],
        "comparecimento_das_que_mudaram_pct": pct((x[x.mudou].comp2).sum(), (x[x.mudou].aptos2).sum(), 1), "comparecimento_das_que_ficaram_pct": pct((x[~x.mudou].comp2).sum(), (x[~x.mudou].aptos2).sum(), 1),
    }


def h35(mu, m22):
    m = mu[mu.validos_1t > 0].copy()
    m["f1"] = 100 * m.flavio_1t / m.validos_1t
    m["dl"] = 100 * (m.lula_2t / m.validos_2t - m.lula_1t / m.validos_1t)
    # 2022: o Bolsonaro no 1o turno e a variacao do Lula, em % do comparecimento (o 1o turno de 2022 tem 11 candidatos)
    w = m22[(m22.comp_1t > 0) & (m22.comp_2t > 0)].copy()
    w["b1"] = 100 * w.bolsonaro_1t / w.comp_1t
    w["dl"] = 100 * (w.lula_2t / w.comp_2t - w.lula_1t / w.comp_1t)
    m["dl_c"] = 100 * (m.lula_2t / m.comparecimento_2t - m.lula_1t / m.comparecimento_1t)
    # mesma medida nos dois anos: a parte do Lula no comparecimento
    def blocos(df, col, dl):
        q = pd.qcut(df[col], 10, labels=False, duplicates="drop")
        t = df.groupby(q).apply(lambda g: pd.Series({"min": g[col].min(), "max": g[col].max(), "municipios": len(g), "dl": g[dl].mean()}), include_groups=False)
        return [{"decil": int(i) + 1, "forca_do_adversario_pct": f"{r['min']:.0f} a {r['max']:.0f}", "municipios": int(r.municipios), "ganho_do_lula_pontos": round(float(r.dl), 2)} for i, r in t.iterrows()]
    return {
        "2026_por_decil_da_forca_do_Flavio_no_1t": blocos(m, "f1", "dl_c"),
        "2022_por_decil_da_forca_do_Bolsonaro_no_1t": blocos(w, "b1", "dl"),
        "inclinacao_2026_pontos_do_lula_por_ponto_de_Flavio": round(slope(m.f1, m.dl_c), 3),
        "inclinacao_2022_pontos_do_lula_por_ponto_de_Bolsonaro": round(slope(w.b1, w.dl), 3),
        "municipios_2026": int(len(m)), "municipios_2022": int(len(w)),
    }


def h36(b):
    t1 = pd.read_parquet(C / "t1_secoes.parquet")
    t2 = pd.read_parquet(C / "t2_secoes.parquet", columns=["uf", "municipio", "rdv_lula", "rdv_flavio", "aptos", "comparecimento"])
    s22 = pd.read_parquet(C / "s2022_t2.parquet")
    s22a = pd.read_parquet(C / "s2022_t1.parquet")
    ext1 = t1[t1.uf == "zz"]
    ext2 = t2[t2.uf == "zz"]
    ext22_2 = s22[s22.uf.str.lower() == "zz"]
    ext22_1 = s22a[s22a.uf.str.lower() == "zz"]
    sc1 = t1[t1.uf == "sc"]
    sc2 = t2[t2.uf == "sc"]
    r = {
        "exterior": {
            "secoes_2026": int(len(ext2)),
            "lula_pct_dos_dois_1t": pct(ext1.lula.sum(), ext1.lula.sum() + ext1.flavio.sum(), 1),
            "lula_pct_dos_dois_2t": pct(ext2.rdv_lula.sum(), ext2.rdv_lula.sum() + ext2.rdv_flavio.sum(), 1),
            "lula_pct_dos_dois_2022_1t": pct(ext22_1.lula.sum(), ext22_1.lula.sum() + ext22_1.bolsonaro.sum(), 1),
            "lula_pct_dos_dois_2022_2t": pct(ext22_2.lula.sum(), ext22_2.lula.sum() + ext22_2.bolsonaro.sum(), 1),
            "votos_lula_2t": int(ext2.rdv_lula.sum()), "votos_flavio_2t": int(ext2.rdv_flavio.sum()),
        },
        "santa_catarina": {
            "lula_1t": int(sc1.lula.sum()), "lula_2t": int(sc2.rdv_lula.sum()), "ganho_do_lula": int(sc2.rdv_lula.sum() - sc1.lula.sum()),
            "flavio_1t": int(sc1.flavio.sum()), "flavio_2t": int(sc2.rdv_flavio.sum()), "ganho_do_flavio": int(sc2.rdv_flavio.sum() - sc1.flavio.sum()),
            "comparecimento_1t": int(sc1.comparecimento.sum()), "comparecimento_2t": int(sc2.comparecimento.sum()),
        },
    }
    # secao com mais votantes que eleitores aptos
    r["secoes_com_mais_votantes_que_aptos"] = {"1t": int((t1.comparecimento > t1.aptos).sum()), "2t": int((t2.comparecimento > t2.aptos).sum()), "secoes_1t": int(len(t1)), "secoes_2t": int(len(t2)),
                                               "2022_1t": int((s22a.comparecimento > s22a.aptos).sum()), "2022_2t": int((s22.comparecimento > s22.aptos).sum())}
    return r


def main():
    b = base_secoes()
    mu = municipios()
    m22 = m2022()
    out = {"H33": h33(b), "H34": h34(), "H35": h35(mu, m22), "H36": h36(b)}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=lambda o: o.item() if hasattr(o, "item") else str(o)), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))


if __name__ == "__main__":
    main()
