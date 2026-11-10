"""Rodada 4 (10/11/2026): H25 a H29, saidas dos comentarios e das mensagens que chegaram depois do video 20.

H25  Campos dos Goytacazes: "o Lula ganhou TODOS os votos nulos, brancos, abstencoes e dos outros candidatos" (post de 03/11)
H26  populacao x votos refeita: quantos dos 5.571 municipios e quanto representa em votos (post de 07/11)
H27  voto liberado sem digital: variacao de cada secao entre os turnos, contra a variacao do Lula (comentario de 31/10)
H28  pares de secoes da mesma escola: o resultado dentro da escola, 1o contra 2o turno (comentario de 10/11)
H30  urnas substituidas: dobraram do 1o para o 2o turno? (comentario de 01/11)
H29  voto pelo ausente: a queda da abstencao secao a secao contra o ganho do Lula, com 2022 de espelho (comentario de 04/11)

Le so o que ja esta em dados/ (copias e derivados). Escreve resultados/RODADA4.json. Sem rede.
Uso: python ferramentas/rodada_4.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
C = RAIZ / "dados" / "copias"
D = RAIZ / "dados" / "derivados"
OUT = RAIZ / "resultados" / "RODADA4.json"
rng = np.random.default_rng(2026)


def pct(a, b, casas=2):
    return round(100 * float(a) / float(b), casas) if b else None


def chave(df):
    return df.uf.str.lower() + "|" + df.municipio.astype(str).str.zfill(5) + "|" + df.zona.astype(str).str.zfill(4) + "|" + df.secao.astype(str).str.zfill(4)


# --------------------------------------------------------------------------- municipios
def municipios():
    mu = pd.read_csv(C / "presidente_municipio.csv", dtype={"cd_tse": str, "cd_ibge": str})
    mu = mu[mu.uf != "zz"].copy()
    ib = pd.read_csv(D / "ibge_municipio.csv", dtype={"cod_ibge": str})
    mu = mu.merge(ib[["cod_ibge", "pop_total", "pop_16_ou_mais"]], left_on="cd_ibge", right_on="cod_ibge", how="left")
    mu["gl"] = mu.lula_2t - mu.lula_1t
    mu["gf"] = mu.flavio_2t - mu.flavio_1t
    mu["outros_1t_total"] = mu.caiado_1t + mu.cury_1t + mu.renan_1t + mu.zema_1t + mu.outros_1t
    mu["bn_1t"] = mu.brancos_1t + mu.nulos_1t
    mu["bn_2t"] = mu.brancos_2t + mu.nulos_2t
    return mu


def m2022():
    out = []
    for t in (1, 2):
        s = pd.read_parquet(C / f"s2022_t{t}.parquet")
        s["uf"] = s.uf.str.lower()
        g = s.groupby(["uf", "municipio"], as_index=False).agg(
            aptos=("aptos", "sum"), comp=("comparecimento", "sum"), bolsonaro=("bolsonaro", "sum"), lula=("lula", "sum"))
        g["turno"] = t
        out.append(g)
    a = pd.concat(out)
    w = a.pivot(index=["uf", "municipio"], columns="turno", values=["aptos", "comp", "bolsonaro", "lula"])
    w.columns = [f"{c}_{t}t" for c, t in w.columns]
    w = w.reset_index()
    w["cd_tse"] = w.municipio.astype(str)
    w["gb"] = w.bolsonaro_2t - w.bolsonaro_1t
    w["gl"] = w.lula_2t - w.lula_1t
    return w


# --------------------------------------------------------------------------- H25
def h25(mu, m22):
    r = mu[(mu.uf == "rj") & (mu.municipio.str.upper() == "CAMPOS DOS GOYTACAZES")].iloc[0]
    abst_var = int(r.abstencao_2t - r.abstencao_1t)
    pool_outros = int(r.outros_1t_total)
    pool_bn = int(r.bn_1t - r.bn_2t)
    flavio_perdeu = int(-r.gf)
    pool = pool_outros + pool_bn + flavio_perdeu
    tweet = {
        "lula_ganhou": int(r.gl),
        "flavio_variou": int(r.gf),
        "brancos_e_nulos_que_sumiram": pool_bn,
        "abstencao_variou_para_cima": abst_var,
        "votos_dos_outros_candidatos_no_1t": pool_outros,
        "cury_caiado_renan_zema": int(r.cury_1t + r.caiado_1t + r.renan_1t + r.zema_1t),
        "o_pool_de_quem_podia_mudar": pool,
        "lula_ficou_com_pct_do_pool": pct(r.gl, pool, 1),
    }
    # comparacao: os municipios grandes do Brasil
    g = mu[mu.eleitores_1t >= 100000].copy()
    g["gf_pct"] = 100 * g.gf / g.flavio_1t
    g["pool"] = g.outros_1t_total + (g.bn_1t - g.bn_2t) - g.gf.clip(upper=0)
    g["lula_do_pool"] = g.gl / g.pool
    rj = g[g.uf == "rj"]
    # espelho 2022: quem liderava o 1o turno de 2022 era o Lula, o 2o turno o Bolsonaro cresceu; contar municipios grandes onde o Bolsonaro perdeu voto
    w = m22.merge(mu[["cd_tse", "uf", "eleitores_1t"]], on=["cd_tse", "uf"], how="inner")
    w = w[w.eleitores_1t >= 100000]
    out = {
        "campos": {"flavio_1t": int(r.flavio_1t), "flavio_2t": int(r.flavio_2t), "lula_1t": int(r.lula_1t), "lula_2t": int(r.lula_2t),
                   "abstencao_1t": int(r.abstencao_1t), "abstencao_2t": int(r.abstencao_2t), "eleitores": int(r.eleitores_1t)},
        "conta_do_post": tweet,
        "municipios_grandes_100mil": int(len(g)),
        "flavio_perdeu_voto_entre_turnos_2026": int((g.gf < 0).sum()),
        "bolsonaro_perdeu_voto_entre_turnos_2022": int((w.gb < 0).sum()),
        "lula_perdeu_voto_entre_turnos_2022": int((w.gl < 0).sum()),
        "flavio_perdeu_nos_grandes_do_rj_2026": int((rj.gf < 0).sum()),
        "grandes_do_rj": int(len(rj)),
        "campos_percentil_do_lula_no_pool_entre_grandes": round(100 * float((g.lula_do_pool < tweet["lula_ficou_com_pct_do_pool"] / 100).mean()), 1),
        "mediana_lula_do_pool_grandes_pct": round(100 * float(g.lula_do_pool.median()), 1),
        "mediana_lula_do_pool_grandes_rj_pct": round(100 * float(rj.lula_do_pool.median()), 1),
        "grandes_com_lula_de_75_a_100_do_pool": int(((g.lula_do_pool >= 0.75) & (g.lula_do_pool <= 1.0)).sum()),
        "flavio_perda_pct_campos": round(float(100 * r.gf / r.flavio_1t), 2),
        "flavio_perdeu_mais_que_campos_em_pct_grandes": int((100 * g.gf / g.flavio_1t < 100 * r.gf / r.flavio_1t).sum()),
        "lista_grandes_onde_o_flavio_perdeu": [
            {"municipio": f"{x.municipio.title()} ({x.uf.upper()})", "flavio_1t": int(x.flavio_1t), "flavio_2t": int(x.flavio_2t), "variacao_pct": round(float(x.gf_pct), 2)}
            for x in g[g.gf < 0].sort_values("gf_pct").itertuples()
        ][:12],
    }
    return out


# --------------------------------------------------------------------------- H26
def h26(mu, m22):
    pop = mu.pop_total
    ok = mu.dropna(subset=["pop_total"]).copy()
    n = len(ok)
    a2 = ok[ok.eleitores_2t > ok.pop_total]
    a1 = ok[ok.eleitores_1t > ok.pop_total]
    c2 = ok[ok.comparecimento_2t > ok.pop_total]
    w = m22.merge(ok[["cd_tse", "uf", "pop_total"]], on=["cd_tse", "uf"], how="inner")
    a22 = w[w.aptos_2t > w.pop_total]
    c22 = w[w.comp_2t > w.pop_total]
    ok["excesso_aptos"] = (ok.eleitores_2t - ok.pop_total).clip(lower=0)
    exc = ok.loc[ok.eleitores_2t > ok.pop_total]
    top = ok.assign(razao=ok.eleitores_2t / ok.pop_total).sort_values("razao", ascending=False).head(8)
    tibau = ok[(ok.uf == "rn") & (ok.municipio.str.upper().str.contains("TIBAU"))]
    pequenos = a2.pop_total.median()
    return {
        "municipios_com_censo": int(n),
        "eleitorado_maior_que_populacao_2026_2t": int(len(a2)),
        "eleitorado_maior_que_populacao_2026_1t": int(len(a1)),
        "eleitorado_maior_que_populacao_2022_2t": int(len(a22)),
        "comparecimento_maior_que_populacao_2026_2t": int(len(c2)),
        "comparecimento_maior_que_populacao_2022_2t": int(len(c22)),
        "pct_dos_municipios_eleitorado_maior_2026": pct(len(a2), n, 1),
        "eleitores_a_mais_que_habitantes_soma_2026": int(exc.eleitores_2t.sum() - exc.pop_total.sum()),
        "eleitorado_total_nesses_municipios": int(a2.eleitores_2t.sum()),
        "pct_do_eleitorado_do_pais_nesses_municipios": pct(a2.eleitores_2t.sum(), ok.eleitores_2t.sum(), 1),
        "mediana_da_populacao_desses_municipios": int(pequenos),
        "votos_acima_da_populacao_soma_2026": int((c2.comparecimento_2t - c2.pop_total).sum()),
        "votos_acima_da_populacao_pct_da_diferenca": pct((c2.comparecimento_2t - c2.pop_total).sum(), 4430191, 2),
        "lula_venceu_dos_120": int((c2.lula_2t > c2.flavio_2t).sum()),
        "flavio_venceu_dos_120": int((c2.flavio_2t > c2.lula_2t).sum()),
        "dos_835_lula_venceu": int((a2.lula_2t > a2.flavio_2t).sum()),
        "dos_835_flavio_venceu": int((a2.flavio_2t > a2.lula_2t).sum()),
        "maiores_razoes": [{"municipio": f"{x.municipio.title()} ({x.uf.upper()})", "eleitores": int(x.eleitores_2t), "habitantes": int(x.pop_total), "razao": round(float(x.razao), 2)} for x in top.itertuples()],
        "tibau_rn": None if tibau.empty else {"eleitores": int(tibau.iloc[0].eleitores_2t), "habitantes": int(tibau.iloc[0].pop_total)},
        "correlacao_razao_x_ganho_do_lula": round(float(np.corrcoef((ok.comparecimento_2t / ok.pop_total), ok.gl)[0, 1]), 3),
    }


# --------------------------------------------------------------------------- base por secao
def base_secoes():
    t1 = pd.read_parquet(C / "t1_secoes.parquet")
    t2 = pd.read_parquet(C / "t2_secoes.parquet")
    for d in (t1, t2):
        d["k"] = chave(d)
    t1 = t1[["k", "uf", "municipio", "zona", "aptos", "comparecimento", "branco", "nulo", "lula", "flavio", "situacao"]]
    t2 = t2[["k", "aptos", "comparecimento", "rdv_lula", "rdv_flavio", "rdv_branco", "rdv_nulo", "situacao"]].rename(
        columns={"aptos": "aptos2", "comparecimento": "comp2", "rdv_lula": "lula2", "rdv_flavio": "flavio2", "rdv_branco": "branco2", "rdv_nulo": "nulo2", "situacao": "sit2"})
    b = t1.merge(t2, on="k", how="inner")
    b = b.dropna(subset=["aptos", "comparecimento", "lula", "flavio", "aptos2", "comp2", "lula2", "flavio2"])
    b = b[(b.aptos > 0) & (b.aptos2 > 0) & (b.comparecimento > 0) & (b.comp2 > 0)]
    b["mun"] = b.uf + "|" + b.municipio
    b["abst1"] = 1 - b.comparecimento / b.aptos
    b["abst2"] = 1 - b.comp2 / b.aptos2
    b["ls1"] = b.lula / (b.lula + b.flavio)
    b["ls2"] = b.lula2 / (b.lula2 + b.flavio2)
    return b


def demean(df, col, by="mun"):
    return df[col] - df.groupby(by)[col].transform("mean")


def slope(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    xc = x - x.mean()
    return float((xc * (y - y.mean())).sum() / (xc ** 2).sum())


def boot_slope(x, y, grupos, B=300):
    """bootstrap por municipio (blocos)"""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    g = pd.factorize(grupos)[0]
    idx = {k: np.where(g == k)[0] for k in np.unique(g)}
    ks = np.array(list(idx))
    out = []
    for _ in range(B):
        pick = rng.choice(ks, size=len(ks), replace=True)
        ii = np.concatenate([idx[k] for k in pick])
        out.append(slope(x[ii], y[ii]))
    return [round(float(np.percentile(out, 2.5)), 3), round(float(np.percentile(out, 97.5)), 3)]


# --------------------------------------------------------------------------- H29
def h29(b):
    """queda da abstencao x ganho do Lula, secao a secao, dentro do municipio, 2026 e 2022"""
    b = b.copy()
    # novos votantes no 2o turno por 100 eleitores e a parte deles que foi para o Lula (acima do 1o turno)
    b["dabst"] = (b.abst1 - b.abst2)  # queda da abstencao (positivo = mais gente votou)
    b["dlula_pp"] = 100 * (b.lula2 / b.comp2 - b.lula / b.comparecimento)  # variacao do Lula em % dos comparecidos
    x = demean(b, "dabst") * 100
    y = demean(b, "dlula_pp")
    res26 = {"secoes": int(len(b)), "inclinacao_pontos_do_lula_por_ponto_de_queda_da_abstencao": round(slope(x, y), 3),
             "intervalo_95_bootstrap_por_municipio": boot_slope(x, y, b.mun)}
    # 2022
    s1 = pd.read_parquet(C / "s2022_t1.parquet")
    s2 = pd.read_parquet(C / "s2022_t2.parquet")
    for d in (s1, s2):
        d["k"] = d.uf.str.lower() + "|" + d.municipio.astype(str).str.zfill(5) + "|" + d.zona.astype(str).str.zfill(4) + "|" + d.secao.astype(str).str.zfill(4)
    m = s1[["k", "uf", "municipio", "aptos", "comparecimento", "lula", "bolsonaro"]].merge(
        s2[["k", "aptos", "comparecimento", "lula", "bolsonaro"]], on="k", suffixes=("", "2"))
    m = m[(m.aptos > 0) & (m.aptos2 > 0) & (m.comparecimento > 0) & (m.comparecimento2 > 0)].copy()
    m["mun"] = m.uf + "|" + m.municipio.astype(str)
    m["dabst"] = 100 * ((1 - m.comparecimento / m.aptos) - (1 - m.comparecimento2 / m.aptos2))
    m["dlula_pp"] = 100 * (m.lula2 / m.comparecimento2 - m.lula / m.comparecimento)
    x2 = demean(m, "dabst")
    y2 = demean(m, "dlula_pp")
    res22 = {"secoes": int(len(m)), "inclinacao_pontos_do_lula_por_ponto_de_queda_da_abstencao": round(slope(x2, y2), 3),
             "intervalo_95_bootstrap_por_municipio": boot_slope(x2, y2, m.mun)}
    # nacional: a abstencao do 2o turno nas duas eleicoes
    res = {"2026": res26, "2022": res22,
           "abstencao_1t_pct": pct(((b.aptos - b.comparecimento)).sum(), b.aptos.sum(), 2), "abstencao_2t_pct": pct(((b.aptos2 - b.comp2)).sum(), b.aptos2.sum(), 2),
           "abstencao_1t_2022_pct": pct((m.aptos - m.comparecimento).sum(), m.aptos.sum(), 2), "abstencao_2t_2022_pct": pct((m.aptos2 - m.comparecimento2).sum(), m.aptos2.sum(), 2)}
    # onde a abstencao caiu mais (top 5%), o Lula cresceu mais?
    q = b.dabst.quantile(0.95)
    alto = b[b.dabst >= q]
    res["secoes_onde_a_abstencao_mais_caiu_(5%)"] = {"n": int(len(alto)), "ganho_medio_do_lula_pontos": round(float(alto.dlula_pp.mean()), 2), "ganho_medio_geral_pontos": round(float(b.dlula_pp.mean()), 2)}
    q2 = m.dabst.quantile(0.95)
    alto2 = m[m.dabst >= q2]
    res["secoes_onde_a_abstencao_mais_caiu_(5%)_2022"] = {"n": int(len(alto2)), "ganho_medio_do_lula_pontos": round(float(alto2.dlula_pp.mean()), 2), "ganho_medio_geral_pontos": round(float(m.dlula_pp.mean()), 2)}
    return res


# --------------------------------------------------------------------------- H27
def h27(b):
    a = pd.read_parquet(D / "amostra_logs.parquet")
    a = a[a.grupo == "sorteio"].copy()
    a["k"] = a.uf.str.lower() + "|" + a.municipio.astype(str).str.zfill(5) + "|" + a.zona.astype(str).str.zfill(4) + "|" + a.secao.astype(str).str.zfill(4)
    a["sem_digital"] = (a.manual_mes + a.manual_sem + a.outra) / a.votos
    a["sem_digital_estrito"] = a.manual_sem / a.votos
    p = a.pivot(index="k", columns="turno", values=["sem_digital", "sem_digital_estrito", "votos"])
    p.columns = [f"{c}_{t}" for c, t in p.columns]
    p = p.dropna().reset_index()
    p = p.merge(b[["k", "mun", "ls1", "ls2"]], on="k", how="inner")
    p["dsd"] = 100 * (p.sem_digital_t2 - p.sem_digital_t1)
    p["dls"] = 100 * (p.ls2 - p.ls1)
    x = demean(p, "dsd")
    y = demean(p, "dls")
    por_turno = a.groupby("turno").apply(lambda g: pd.Series({"sem_digital_pct": 100 * (g.manual_mes + g.manual_sem + g.outra).sum() / g.votos.sum(),
                                                               "sem_digital_estrito_pct": 100 * g.manual_sem.sum() / g.votos.sum(), "secoes": len(g)}), include_groups=False)
    # estabilidade: a secao que tinha mais gente sem digital no 1o turno tem no 2o?
    estab = float(np.corrcoef(p.sem_digital_t1, p.sem_digital_t2)[0, 1])
    # mesma inclinacao no cruzamento de cada turno (o espelho e o proprio 1o turno)
    q = p.copy()
    q["sd1"] = 100 * q.sem_digital_t1
    q["sd2"] = 100 * q.sem_digital_t2
    q["l1"] = 100 * q.ls1
    q["l2"] = 100 * q.ls2
    s1 = slope(demean(q, "sd1"), demean(q, "l1"))
    s2 = slope(demean(q, "sd2"), demean(q, "l2"))
    # horario: parte sem digital por hora, 1o contra 2o turno
    hr = {}
    for t in ("t1", "t2"):
        g = a[a.turno == t]
        h = {}
        for hh in range(8, 18):
            tot = g[f"h{hh:02d}"].sum()
            man = g[f"m{hh:02d}"].sum()
            h[f"{hh:02d}h"] = pct(man, tot, 1)
        hr[t] = h
    return {
        "secoes_no_par": int(len(p)),
        "por_turno": {k: {kk: round(float(vv), 2) for kk, vv in v.items()} for k, v in por_turno.to_dict(orient="index").items()},
        "correlacao_do_sem_digital_entre_turnos": round(estab, 3),
        "inclinacao_variacao_sem_digital_x_variacao_do_lula": round(slope(x, y), 3),
        "intervalo_95_bootstrap_por_municipio": boot_slope(x, y, p.mun),
        "inclinacao_no_1t": round(s1, 3), "inclinacao_no_2t": round(s2, 3),
        "liberacao_manual_por_hora_pct": hr,
    }


# --------------------------------------------------------------------------- H28
def h28(b):
    L = pd.read_parquet(D / "local_votacao_2026.parquet")
    L = L[L.turno == "2"].copy()
    L["k"] = L.uf.str.lower() + "|" + L.municipio.astype(str).str.zfill(5) + "|" + L.zona.astype(str).str.zfill(4) + "|" + L.secao.astype(str).str.zfill(4)
    x = b.merge(L[["k", "local"]], on="k", how="inner")
    x["local_id"] = x.mun + "|" + x.zona.astype(str) + "|" + x["local"].astype(str)
    res = {}
    for turno, (l, f, tag) in {"t1": ("lula", "flavio", "1t"), "t2": ("lula2", "flavio2", "2t")}.items():
        d = x.copy()
        d["n"] = d[l] + d[f]
        d = d[d.n >= 30]
        g = d.groupby("local_id")
        d["nl"] = g.n.transform("sum")
        d["ll"] = g[l].transform("sum")
        d = d[g.n.transform("count") >= 2]
        # leave-one-out: a parte do Lula nas OUTRAS secoes do mesmo local
        d["p_out"] = (d["ll"] - d[l]) / (d["nl"] - d.n)
        d["p"] = d[l] / d.n
        d = d[(d.p_out > 0.03) & (d.p_out < 0.97)]
        d["z"] = (d.p - d.p_out) / np.sqrt(d.p_out * (1 - d.p_out) / d.n)
        res[tag] = {"secoes": int(len(d)), "locais": int(d.local_id.nunique()), "variancia_z": round(float(d.z.var()), 3),
                    "z_maior_que_4_pct": round(100 * float((d.z.abs() > 4).mean()), 3), "z_maior_que_6_pct": round(100 * float((d.z.abs() > 6).mean()), 3),
                    "z_maior_que_4_n": int((d.z.abs() > 4).sum()), "z_maior_que_6_n": int((d.z.abs() > 6).sum())}
        res[tag + "_z"] = d[["k", "z"]]
    z1 = res.pop("1t_z")
    z2 = res.pop("2t_z")
    mm = z1.merge(z2, on="k", suffixes=("_1", "_2"))
    res["correlacao_do_z_entre_turnos"] = round(float(np.corrcoef(mm.z_1, mm.z_2)[0, 1]), 3)
    res["secoes_nos_dois_turnos"] = int(len(mm))
    res["z_extremo_no_2t_e_normal_no_1t"] = int(((mm.z_2.abs() > 6) & (mm.z_1.abs() < 2)).sum())
    res["z_extremo_no_1t_e_normal_no_2t"] = int(((mm.z_1.abs() > 6) & (mm.z_2.abs() < 2)).sum())
    return res


# --------------------------------------------------------------------------- H30
def h30(b):
    """urnas substituidas (contingencia): dobraram do 1o para o 2o turno? as trocadas ja tinham voto para o Lula?"""
    a = pd.read_parquet(D / "amostra_logs.parquet")
    a = a[a.grupo == "sorteio"].copy()
    a["k"] = a.uf.str.lower() + "|" + a.municipio.astype(str).str.zfill(5) + "|" + a.zona.astype(str).str.zfill(4) + "|" + a.secao.astype(str).str.zfill(4)
    taxa = {t: {"secoes": int(len(g)), "com_urna_substituida": int(g.contingencia.sum()), "pct": round(100 * float(g.contingencia.mean()), 2)} for t, g in a.groupby("turno")}
    # nas secoes trocadas, o Lula (parte do Lula + Flavio) contra o resto do mesmo municipio; o 1o turno e o espelho
    bb = b.set_index("k")
    res = {}
    for t, col in (("t1", "ls1"), ("t2", "ls2")):
        trocadas = a[(a.turno == t) & a.contingencia].k
        trocadas = [k for k in trocadas if k in bb.index]
        difs = []
        for k in trocadas:
            m = bb.loc[k, "mun"]
            resto = b[(b.mun == m) & (b.k != k)][col]
            if len(resto):
                difs.append(100 * (float(bb.loc[k, col]) - float(resto.mean())))
        d = np.array(difs)
        res[t] = {"secoes": int(len(d)), "diferenca_media_do_lula_em_pontos": round(float(d.mean()), 2), "erro_padrao": round(float(d.std(ddof=1) / np.sqrt(len(d))), 2)}
    return {"taxa_na_amostra": taxa, "lula_nas_secoes_trocadas_contra_o_resto_do_municipio": res,
            "tse_observadores_2t": {"trocadas": 1551, "urnas": 499248, "pct": 0.31}}


def main():
    mu = municipios()
    m22 = m2022()
    out = {"H25": h25(mu, m22), "H26": h26(mu, m22)}
    b = base_secoes()
    out["secoes_pareadas_2026"] = int(len(b))
    out["H29"] = h29(b)
    out["H27"] = h27(b)
    out["H28"] = h28(b)
    out["H30"] = h30(b)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=lambda o: o.item() if hasattr(o, "item") else str(o)), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))


if __name__ == "__main__":
    main()
