"""Rodada 1: um teste por hipótese (docs/HIPOTESES.md), com o espelho e o controle de cada uma.
Lê só dados/copias/ e dados/derivados/ (todos com sha256 nos manifestos) e grava resultados/RESUMO.json e as
tabelas em resultados/tabelas/. Nenhum veredito é escrito aqui: os números saem daqui, a régua está no PLANO.md.

Uso: python ferramentas/analise.py
"""
import json
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
C, D = RAIZ / "dados/copias", RAIZ / "dados/derivados"
T = RAIZ / "resultados/tabelas"
K = ["uf", "municipio", "zona", "secao"]
FUSO = {"ac": 2, "am": 1, "ro": 1, "rr": 1, "mt": 1, "ms": 1}
MARGEM = 4_430_191
RNG = np.random.default_rng(2026)


def pct(a, b, casas=2):
    return round(100 * a / b, casas) if b else None


def norm(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().upper()


# ---------------------------------------------------------------- base
def base():
    t2 = pd.read_parquet(C / "t2_secoes.parquet")
    t1 = pd.read_parquet(C / "t1_secoes.parquet")
    det = pd.read_parquet(D / "detalhe_secao_2026.parquet")
    d1 = det[det.turno == "1"].drop(columns="turno").add_suffix("_d1").rename(columns={f"{k}_d1": k for k in K})
    d2 = det[det.turno == "2"].drop(columns="turno").add_suffix("_d2").rename(columns={f"{k}_d2": k for k in K})
    m = t2.merge(t1[K + ["lula", "flavio", "comparecimento", "aptos", "renan", "caiado", "cury", "zema", "demais", "branco", "nulo"]]
                 .rename(columns={c: f"{c}_1t" for c in ["lula", "flavio", "comparecimento", "aptos", "renan", "caiado", "cury", "zema", "demais", "branco", "nulo"]}),
                 on=K, how="left")
    m = m.merge(d1, on=K, how="left").merge(d2, on=K, how="left")
    # no 1º turno, candidato sem voto na seção não aparece na tabela: é zero, não falta de dado
    tem1 = m.lula_1t.notna() | m.flavio_1t.notna()
    for c in ["lula_1t", "flavio_1t", "renan_1t", "caiado_1t", "cury_1t", "zema_1t", "demais_1t", "branco_1t", "nulo_1t"]:
        m.loc[tem1, c] = m.loc[tem1, c].fillna(0)
    en = pd.to_datetime(m.encerramento, errors="coerce")
    m["en_bsb"] = en.dt.hour + en.dt.minute / 60 + en.dt.second / 3600 + m.uf.map(FUSO).fillna(0)
    m["en_local"] = en.dt.hour + en.dt.minute / 60 + en.dt.second / 3600
    m["nom2"] = m.bu_lula + m.bu_flavio
    m["lula2"] = m.bu_lula / m.nom2
    m["nom1"] = m.lula_1t + m.flavio_1t + m.renan_1t + m.caiado_1t + m.cury_1t + m.zema_1t + m.demais_1t
    m["lula1"] = m.lula_1t / m.nom1
    m["flavio1"] = m.flavio_1t / m.nom1
    m["ganho_lula"] = m.bu_lula - m.lula_1t
    m["ganho_flavio"] = m.bu_flavio - m.flavio_1t
    m["local_id"] = m.uf + "-" + m.municipio + "-" + m.local_d2.astype(str)
    m["manual2"] = (m.log_manual_mesario.fillna(0) + m.log_manual_sem_digital.fillna(0)) / m.log_votos
    br = m[(m.uf != "zz") & (m.situacao != "Nao instalada")].copy()
    return m, br


def dentro_do_local(df, grupo, valor, peso):
    """Diferença média ponderada de `valor` entre seções com grupo=True e grupo=False no MESMO local de votação."""
    x = df[[grupo, valor, peso, "local_id"]].dropna()
    g = x.groupby(["local_id", grupo]).apply(lambda s: pd.Series({"v": np.average(s[valor], weights=s[peso]), "w": s[peso].sum()}), include_groups=False).unstack(grupo)
    g = g.dropna()
    if g.empty:
        return {"locais": 0}
    dif = g[("v", True)] - g[("v", False)]
    w = np.minimum(g[("w", True)], g[("w", False)])
    return {"locais": int(len(g)), "diferenca_pontos": round(100 * float(np.average(dif, weights=w)), 3),
            "locais_com_mais_lula_no_grupo": pct((dif > 0).sum(), len(dif), 1)}


# ---------------------------------------------------------------- Bloco A
def reproduzir_relatorio(m):
    """O grupo "encerradas até as 17h00" do relatório sai igual quando se usa a hora LOCAL do boletim, sem o fuso,
    com o exterior junto: as urnas dos estados 1 ou 2 horas atrás de Brasília entram todas como "até 17h"."""
    t = m[m.situacao != "Nao instalada"]
    ate = t.en_local < 17 + 1 / 60
    a, d = t[ate], t[~ate]
    fu = a[a.uf.isin(FUSO)]
    return {"ate_17h00": {"secoes": int(len(a)), "flavio_pct": pct(a.bu_flavio.sum(), a.nom2.sum()), "frente_flavio": int(a.bu_flavio.sum() - a.bu_lula.sum())},
            "depois": {"secoes": int(len(d)), "frente_lula": int(d.bu_lula.sum() - d.bu_flavio.sum())},
            "relatorio_diz": {"flavio_pct": 52.39, "frente_flavio": "quase 1,8 milhão", "frente_lula_depois": "mais de 6,1 milhões", "secoes_depois": 348398},
            "secoes_dos_estados_com_fuso_no_grupo_ate_17h": int(len(fu)), "secoes_desses_estados": int(t.uf.isin(FUSO).sum()),
            "flavio_pct_nessas": pct(fu.bu_flavio.sum(), fu.nom2.sum()), "frente_flavio_nessas": int(fu.bu_flavio.sum() - fu.bu_lula.sum()),
            "votos_com_hora_depois_17h_no_grupo_depois": int(d.log_votos_depois_17h.fillna(0).sum())}


def h01_h02(br, out, m=None):
    cortes = {}
    for rot, h in [("ate_17h00min59", 17 + 1 / 60), ("ate_17h05", 17 + 5 / 60), ("ate_17h15", 17.25), ("ate_17h00min59_hora_local_sem_fuso", "local")]:
        if h == "local":
            ate = br.en_local < 17 + 1 / 60
        else:
            ate = br.en_bsb < h
        lado = {}
        for nome, g in (("ate", br[ate]), ("depois", br[~ate])):
            L, F = int(g.bu_lula.sum()), int(g.bu_flavio.sum())
            lado[nome] = {"secoes": int(len(g)), "flavio_pct": pct(F, L + F), "margem_lula": L - F,
                          "comparecimento": int(g.comparecimento.sum()), "votos_depois_17h_log": int(g.log_votos_depois_17h.fillna(0).sum())}
        cortes[rot] = lado
    # as faixas da tabela do capítulo 2 do relatório
    faixas = {}
    for rot, a_, b_ in [("17h01_a_17h15", 17 + 1 / 60, 17 + 16 / 60), ("17h16_a_18h59", 17 + 16 / 60, 19.0), ("19h00_ou_depois", 19.0, 99)]:
        g = br[(br.en_bsb >= a_) & (br.en_bsb < b_)]
        faixas[rot] = {"secoes": int(len(g)), "comparecimento": int(g.comparecimento.sum()), "lula_pct": pct(g.bu_lula.sum(), g.nom2.sum()),
                       "votos_depois_17h_log": int(g.log_votos_depois_17h.fillna(0).sum())}
    relatorio = {"17h01_a_17h15": {"secoes": 339593, "comparecimento": 88071750, "lula_pct": 53.46},
                 "17h16_a_18h59": {"secoes": 2472, "comparecimento": 674799, "lula_pct": 57.16},
                 "19h00_ou_depois": {"secoes": 6333, "comparecimento": 1856306}}
    # o que o relatório chama de "mais de 2,5 milhões": comparecimento do dia inteiro nas seções fechadas depois das 17h16
    tarde = br[br.en_bsb >= 17 + 16 / 60]
    # dentro do mesmo local: seções que fecharam depois das 17h15 contra as vizinhas que fecharam antes
    br["fechou_tarde"] = br.en_bsb > 17.25
    br["dlula"] = br.lula2 - br.lula1
    dl = dentro_do_local(br, "fechou_tarde", "lula2", "nom2")
    dg = dentro_do_local(br, "fechou_tarde", "dlula", "nom2")
    # espelho: o mesmo nos municípios onde o Flávio venceu
    mun = br.groupby(["uf", "municipio"]).agg(L=("bu_lula", "sum"), F=("bu_flavio", "sum"))
    flavio_venceu = set(mun[mun.F > mun.L].index)
    esp = br[[t in flavio_venceu for t in zip(br.uf, br.municipio)]]
    out["H01"] = {"reproducao_do_relatorio": reproduzir_relatorio(m), "cortes": cortes, "faixas_do_capitulo_2": {"projeto": faixas, "relatorio": relatorio}, "dentro_do_local_lula_2t": dl, "dentro_do_local_ganho_do_1t_para_2t": dg,
                  "espelho_municipios_do_flavio": {"secoes_fechadas_depois_17h15": int(esp.fechou_tarde.sum()),
                                                   "flavio_pct_nelas": pct(esp[esp.fechou_tarde].bu_flavio.sum(), esp[esp.fechou_tarde].nom2.sum()),
                                                   "dentro_do_local_lula_2t": dentro_do_local(esp, "fechou_tarde", "lula2", "nom2")}}
    out["H02"] = {"secoes_fechadas_a_partir_de_17h16": int(len(tarde)), "comparecimento_do_dia_inteiro_nelas": int(tarde.comparecimento.sum()),
                  "votos_com_hora_depois_17h_nelas_pelo_log": int(tarde.log_votos_depois_17h.fillna(0).sum()),
                  "votos_depois_17h_brasil_log": int(br.log_votos_depois_17h.fillna(0).sum()),
                  "votos_depois_19h_brasil_log": int(br.log_votos_depois_19h.fillna(0).sum()),
                  "votos_depois_17h_por_uf": br.groupby("uf").log_votos_depois_17h.sum().astype(int).sort_values(ascending=False).head(8).to_dict(),
                  "teto_pct_da_margem": pct(br.log_votos_depois_17h.fillna(0).sum(), MARGEM)}


def h03(br, out, amostra):
    s = amostra[amostra.grupo.str.contains("sorteio", na=False)]
    p = s.pivot_table(index=K, columns="turno", values=["votos", "manual_mes", "manual_sem"], aggfunc="sum")
    p.columns = [f"{a}_{b}" for a, b in p.columns]
    p = p.reset_index()
    p = p[(p.votos_t1 > 50) & (p.votos_t2 > 50)]
    p["man1"] = (p.manual_mes_t1 + p.manual_sem_t1) / p.votos_t1
    p["man2"] = (p.manual_mes_t2 + p.manual_sem_t2) / p.votos_t2
    j = p.merge(br[K + ["lula2", "lula1", "nom2", "bu_lula", "lula_1t", "comparecimento", "comparecimento_1t"]], on=K)
    j["dman"] = j.man2 - j.man1
    j["dlula"] = j.lula2 - j.lula1
    j["dcomp"] = (j.comparecimento - j.comparecimento_1t) / j.comparecimento_1t

    def within(x, y):
        a = j[[x, y, "uf", "municipio"]].dropna()
        a = a.assign(xc=a[x] - a.groupby(["uf", "municipio"])[x].transform("mean"), yc=a[y] - a.groupby(["uf", "municipio"])[y].transform("mean"))
        return round(float(np.corrcoef(a.xc, a.yc)[0, 1]), 3), round(float(np.polyfit(a.xc, a.yc, 1)[0]), 4)

    r_mesmo, b_mesmo = within("man2", "lula2")
    r_var, b_var = within("dman", "dlula")
    r_placebo, b_placebo = within("man1", "lula1")
    out["H03"] = {"liberacao_pelo_mesario_log_2t": int(br.log_manual_mesario.fillna(0).sum()),
                  "dos_quais_sem_digital_cadastrada": int(br.log_manual_sem_digital.fillna(0).sum()),
                  "parte_do_comparecimento_pct": pct(br.log_manual_mesario.fillna(0).sum(), br.log_votos.fillna(0).sum()),
                  "manuais_depois_17h": int(br.log_manuais_depois_17h.fillna(0).sum()),
                  "amostra_secoes": int(len(j)),
                  "amostra_parte_manual_1t_pct": pct((j.manual_mes_t1 + j.manual_sem_t1).sum(), j.votos_t1.sum()),
                  "amostra_parte_manual_2t_pct": pct((j.manual_mes_t2 + j.manual_sem_t2).sum(), j.votos_t2.sum()),
                  "correlacao_no_mesmo_municipio": {"parte_manual_2t_x_lula_2t": [r_mesmo, b_mesmo],
                                                     "placebo_parte_manual_1t_x_lula_1t": [r_placebo, b_placebo],
                                                     "variacao_manual_x_variacao_lula": [r_var, b_var]},
                  "2022_segundo_terceiros": "Jornal Razão: 10.011.347 (8,06%) em 2022, pela mesma conta do BU; não recalculado aqui"}


def s2022():
    s22 = pd.read_parquet(C / "s2022_t2.parquet")
    s22["uf"] = s22.uf.str.lower()
    s22["municipio"] = s22.municipio.str.zfill(5)
    s22["zona"] = s22.zona.str.zfill(4)
    s22["secao"] = s22.secao.str.zfill(4)
    return s22


def h04_h07(m, br, out):
    s22 = s2022()
    s22 = s22[s22.uf != "zz"]
    s18 = pd.read_parquet(D / "secoes_2018_t2.parquet")
    loc = pd.read_parquet(D / "local_votacao_2026.parquet")
    loc = loc[loc.turno == "2"][K + ["nome_local", "tipo_local", "bairro"]].drop_duplicates(K)
    v = br.nom2
    acima_l = br[br.bu_lula / v > 0.9]
    acima_f = br[br.bu_flavio / v > 0.9]
    s22n = s22.lula + s22.bolsonaro
    hist = br.merge(s22[K + ["lula", "bolsonaro"]].rename(columns={"lula": "lula22", "bolsonaro": "bols22"}), on=K, how="left")
    hist["l22"] = hist.lula22 / (hist.lula22 + hist.bols22)
    al = hist[hist.bu_lula / hist.nom2 > 0.9]
    af = hist[hist.bu_flavio / hist.nom2 > 0.9]
    out["H04"] = {"acima_90_lula": int(len(acima_l)), "acima_90_flavio": int(len(acima_f)),
                  "2022_acima_90_lula": int((s22.lula / s22n > 0.9).sum()), "2022_acima_90_bolsonaro": int((s22.bolsonaro / s22n > 0.9).sum()),
                  "lula_acima_90_ja_acima_80_no_1t_2026_pct": pct((acima_l.lula_1t / acima_l.nom1 > 0.8).sum(), len(acima_l), 1),
                  "lula_acima_90_ja_acima_80_em_2022_pct": pct((al.l22 > 0.8).sum(), al.l22.notna().sum(), 1),
                  "flavio_acima_90_ja_acima_80_em_2022_pct": pct(((1 - af.l22) > 0.8).sum(), af.l22.notna().sum(), 1),
                  "lula_acima_90_casadas_em_2022": int(al.l22.notna().sum())}
    # H07: as seções sem voto do Flávio
    z = br[(br.bu_flavio == 0) & (br.bu_lula > 0)].merge(loc, on=K, how="left")
    z = z.merge(s22[K + ["lula", "bolsonaro"]].rename(columns={"lula": "lula22", "bolsonaro": "bols22"}), on=K, how="left")
    z = z.merge(s18[K + ["haddad", "bolsonaro"]].rename(columns={"haddad": "haddad18", "bolsonaro": "bols18"}), on=K, how="left")
    termos = r"INDIGENA|ALDEIA|INDIG|TERRA INDIGENA|QUILOMB|KM |MALOCA|COMUNIDADE|POLO BASE|POSTO DE SAUDE|SESAI"
    z["nome_norm"] = z.nome_local.map(norm)
    z["indigena_no_nome"] = z.nome_norm.str.contains(termos, regex=True)
    zl = br[(br.bu_lula == 0) & (br.bu_flavio > 0)].merge(loc, on=K, how="left")
    z[K + ["nome_local", "tipo_local", "bu_lula", "flavio_1t", "lula_1t", "bols22", "lula22", "bols18", "haddad18"]].to_csv(T / "h07_secoes_sem_voto_do_flavio.csv", index=False)
    zl[K + ["nome_local", "bu_flavio", "bu_lula"]].to_csv(T / "h07_secoes_sem_voto_do_lula.csv", index=False)
    out["H07"] = {"secoes": int(len(z)), "votos_lula": int(z.bu_lula.sum()), "por_uf": z.uf.value_counts().to_dict(),
                  "municipios_com_mais": {f"{u}-{mu}": int(n) for (u, mu), n in z.groupby(["uf", "municipio"]).size().sort_values(ascending=False).head(5).items()},
                  "com_termo_indigena_ou_comunidade_no_nome_do_local": int(z.indigena_no_nome.sum()),
                  "flavio_no_1t_2026_nessas_votos": int(z.flavio_1t.fillna(0).sum()), "com_algum_voto_do_flavio_no_1t": int((z.flavio_1t >= 1).sum()),
                  "com_zero_flavio_tambem_no_1t": int((z.flavio_1t == 0).sum()),
                  "casadas_no_1t": int(z.flavio_1t.notna().sum()),
                  "bolsonaro_2022_nessas_votos": int(z.bols22.fillna(0).sum()), "casadas_em_2022": int(z.bols22.notna().sum()),
                  "bolsonaro_2022_zero_nas_casadas": int((z.bols22 == 0).sum()),
                  "bolsonaro_2018_nessas_votos": int(z.bols18.fillna(0).sum()), "casadas_em_2018": int(z.bols18.notna().sum()),
                  "2022_secoes_zero_bolsonaro": int(((s22.bolsonaro == 0) & (s22.lula > 0)).sum()),
                  "2018_secoes_zero_bolsonaro": int(((s18.bolsonaro == 0) & (s18.haddad > 0)).sum()),
                  "2018_secoes_zero_haddad": int(((s18.haddad == 0) & (s18.bolsonaro > 0)).sum()),
                  "espelho_zero_lula": {"secoes": int(len(zl)), "votos_flavio": int(zl.bu_flavio.sum()),
                                        "onde": [f"{r.uf}-{r.municipio}: {r.nome_local}" for r in zl.itertuples()]},
                  "teto_votos": int(z.flavio_1t.fillna(0).sum())}


def benford(x, digito=1):
    x = x[x >= (10 if digito == 2 else 1)].astype(int).astype(str)
    d = x.str[digito - 1].astype(int)
    obs = d.value_counts(normalize=True).sort_index()
    if digito == 1:
        esp = pd.Series({k: np.log10(1 + 1 / k) for k in range(1, 10)})
    else:
        esp = pd.Series({k: sum(np.log10(1 + 1 / (10 * j + k)) for j in range(1, 10)) for k in range(10)})
    obs = obs.reindex(esp.index).fillna(0)
    return round(float((obs - esp).abs().mean()), 4)


def h05(br, out):
    s22 = pd.read_parquet(C / "s2022_t2.parquet")
    r = {}
    for nome, serie in [("lula_2026", br.bu_lula), ("flavio_2026", br.bu_flavio), ("lula_2022", s22.lula), ("bolsonaro_2022", s22.bolsonaro)]:
        r[nome] = {"mad_1o_digito": benford(serie, 1), "mad_2o_digito": benford(serie, 2)}
    out["H05"] = {"mad": r, "regua_nigrini_1o_digito": "até 0,006 conformidade; 0,012 a 0,015 marginal; acima de 0,015 não conforme",
                  "nota": "o 1º dígito de votos por seção fica preso no tamanho da seção (200 a 400 eleitores); por isso o teste reprova os dois candidatos e os dois anos"}


# ---------------------------------------------------------------- Bloco B
def h08(br, out):
    inst = br[br.nom2 > 0]
    obs = int((inst.groupby(["bu_lula", "bu_flavio"]).size() >= 2).sum())
    obs_alto = int((inst[(inst.bu_lula >= 300) & (inst.bu_flavio >= 300)].groupby(["bu_lula", "bu_flavio"]).size() >= 2).sum())
    p = inst.lula1.fillna(inst.lula2).clip(0.001, 0.999).to_numpy()
    n = inst.nom2.to_numpy().astype(int)
    sim = []
    for _ in range(20):
        l = RNG.binomial(n, p)
        s = pd.DataFrame({"l": l, "f": n - l})
        sim.append(int((s.groupby(["l", "f"]).size() >= 2).sum()))
    s22 = pd.read_parquet(C / "s2022_t2.parquet")
    obs22 = int((s22[(s22.lula + s22.bolsonaro) > 0].groupby(["lula", "bolsonaro"]).size() >= 2).sum())
    out["H08"] = {"placares_repetidos_2026": obs, "esperado_pelo_acaso_media": int(np.mean(sim)), "esperado_faixa": [int(min(sim)), int(max(sim))],
                  "placares_repetidos_2022": obs22, "repetidos_com_os_dois_acima_de_300": obs_alto}


def h09(br, out):
    x = br.dropna(subset=["modelo_d2", "lula1", "lula2"]).copy()
    x["dlula"] = x.lula2 - x.lula1
    por = x.groupby("modelo_d2").apply(lambda g: pd.Series({"secoes": len(g), "lula_2t_pct": pct(g.bu_lula.sum(), g.nom2.sum()),
                                                           "ganho_lula_pontos": round(100 * np.average(g.dlula, weights=g.nom2), 2)}), include_groups=False)
    res = {"por_modelo": por.to_dict(orient="index")}
    # dentro do local: a urna antiga (2013/2015) contra a nova (2020/2022) no mesmo local
    x["antiga"] = x.modelo_d2.isin(["UE 2013", "UE 2015"])
    res["dentro_do_local_antiga_vs_nova_lula_2t"] = dentro_do_local(x, "antiga", "lula2", "nom2")
    res["dentro_do_local_antiga_vs_nova_ganho"] = dentro_do_local(x, "antiga", "dlula", "nom2")
    res["urna_trocou_de_modelo_entre_turnos"] = int((x.modelo_d1 != x.modelo_d2).sum())
    out["H09"] = res


def h10(br, out):
    x = br.dropna(subset=["lula1", "lula2"]).copy()
    x["dlula"] = x.lula2 - x.lula1
    x["contingencia"] = x.log_contingencia.fillna(0).astype(int) > 0
    out["H10"] = {"secoes_com_contingencia_no_log": int(x.contingencia.sum()),
                  "origem_do_voto_2t": br.origem_d2.value_counts().to_dict(),
                  "dentro_do_local_lula_2t": dentro_do_local(x, "contingencia", "lula2", "nom2"),
                  "dentro_do_local_ganho": dentro_do_local(x, "contingencia", "dlula", "nom2"),
                  "lula_pct_nas_secoes_com_contingencia": pct(x[x.contingencia].bu_lula.sum(), x[x.contingencia].nom2.sum()),
                  "teto_votos_nominais_nessas_secoes": int(x[x.contingencia].nom2.sum())}


def h11(m, br, out):
    nomes = pd.read_csv(C / "presidente_municipio.csv", dtype={"cd_tse": str, "cd_ibge": str})
    tdf = nomes[(nomes.uf == "ba") & (nomes.municipio.str.upper() == "TEIXEIRA DE FREITAS")]
    cd = tdf.cd_tse.iloc[0]
    t = m[(m.uf == "ba") & (m.municipio == cd)]
    # o mesmo boletim por dois produtos do TSE: o arquivo da seção (BU) e o detalhe por seção dos dados abertos
    x = br.dropna(subset=["comparecimento_d2"])
    dif_comp = int((x.comparecimento != x.comparecimento_d2).sum())
    dif_nom = int(((x.bu_lula + x.bu_flavio) != x.nominais_d2).sum())
    out["H11"] = {"teixeira_de_freitas": {"secoes": int(len(t)), "lula": int(t.bu_lula.sum()), "flavio": int(t.bu_flavio.sum()),
                                          "aosfatos_publicou": {"flavio": 41454, "lula": 41361}},
                  "boletim_x_dados_abertos": {"secoes_comparadas": int(len(x)), "comparecimento_diferente": dif_comp, "nominais_diferentes": dif_nom},
                  "assinatura_digital_do_bu": "não verificada nesta rodada (ver docs/PLANO.md); os logs da amostra registram 0 verificações de assinatura sem SUCESSO"}


def h12(m, out):
    det = pd.read_parquet(D / "detalhe_secao_2026.parquet")
    s1 = set(map(tuple, det[det.turno == "1"][K].values))
    s2 = set(map(tuple, det[det.turno == "2"][K].values))
    j = m.dropna(subset=["local_d1", "local_d2"]).copy()
    j["mudou_local"] = j.local_d1 != j.local_d2
    j["dcomp"] = (j.comparecimento_d2 - j.comparecimento_d1) / j.aptos_d2
    mud = j[j.mudou_local]
    out["H12"] = {"secoes_1t": len(s1), "secoes_2t": len(s2), "so_no_1t": len(s1 - s2), "so_no_2t": len(s2 - s1),
                  "nao_instaladas_2t": int((det[det.turno == "2"].instalada != "Sim").sum()),
                  "mudaram_de_local": int(len(mud)), "variacao_comparecimento_mudaram_pontos": round(100 * float(mud.dcomp.mean()), 2) if len(mud) else None,
                  "variacao_comparecimento_demais_pontos": round(100 * float(j[~j.mudou_local].dcomp.mean()), 2),
                  "lula_pct_nas_que_mudaram": pct(mud.bu_lula.sum(), mud.nom2.sum())}


# ---------------------------------------------------------------- Bloco C
def h13_h14(br, out):
    e = pd.read_csv(D / "eleitorado_idade.csv", dtype={"cd_tse": str})
    c = pd.read_csv(D / "comparecimento_idade.csv", dtype={"cd_tse": str, "turno": str})
    ib = pd.read_csv(D / "ibge_municipio.csv", dtype={"cod_ibge": str})
    cw = pd.read_csv(C / "presidente_municipio.csv", dtype={"cd_tse": str, "cd_ibge": str})[["uf", "cd_tse", "cd_ibge", "municipio", "eleitores_2t", "comparecimento_2t", "lula_2t", "flavio_2t"]]
    e["f"] = e.faixa.map(norm)
    cent = e.f.str.contains("100 ANOS")
    nov = e.f.str.contains("90 A 94|95 A 99|100 ANOS")
    tot = e.groupby(["ano", "uf", "cd_tse"]).eleitores.sum().rename("eleitores")
    e100 = e[cent].groupby(["ano", "uf", "cd_tse"]).eleitores.sum().rename("e100")
    e90 = e[nov].groupby(["ano", "uf", "cd_tse"]).eleitores.sum().rename("e90")
    em = pd.concat([tot, e100, e90], axis=1).fillna(0).reset_index()
    em26 = em[em.ano == 2026].merge(cw, on=["uf", "cd_tse"], how="left").merge(ib, left_on="cd_ibge", right_on="cod_ibge", how="left")
    em26 = em26[em26.uf != "zz"]
    em26["razao_100_sobre_pop96_2022"] = em26.e100 / em26.pop_96_ou_mais.replace(0, np.nan)
    em26["razao_eleitores_sobre_pop12_2022"] = em26.eleitores / em26.pop_12_ou_mais
    em26["razao_comparec2t_sobre_pop12_2022"] = em26.comparecimento_2t / em26.pop_12_ou_mais
    em26.sort_values("razao_eleitores_sobre_pop12_2022", ascending=False).head(60)[
        ["uf", "municipio_x", "eleitores", "pop_12_ou_mais", "razao_eleitores_sobre_pop12_2022", "comparecimento_2t", "lula_2t", "flavio_2t"]].to_csv(T / "h14_maiores_razoes_eleitorado_populacao.csv", index=False)
    acima = em26[em26.razao_eleitores_sobre_pop12_2022 > 1]
    acima_c = em26[em26.razao_comparec2t_sobre_pop12_2022 > 1]
    # espelho no tempo: 2022, com a população de 16 anos ou mais do próprio Censo 2022
    s22 = s2022()
    c22 = s22.groupby(["uf", "municipio"]).agg(comp22=("comparecimento", "sum"), lula22=("lula", "sum"), bols22=("bolsonaro", "sum")).reset_index()
    c22 = c22.rename(columns={"municipio": "cd_tse"}).merge(cw[["uf", "cd_tse", "cd_ibge"]], on=["uf", "cd_tse"], how="left").merge(ib, left_on="cd_ibge", right_on="cod_ibge", how="left")
    acima22 = c22[c22.comp22 > c22.pop_16_ou_mais]
    # comparecimento por idade
    c["f"] = c.faixa.map(norm)
    cc = c[c.uf != "zz"]

    def taxa(ano, turno, pat):
        g = cc[(cc.ano == ano) & (cc.turno == turno) & cc.f.str.contains(pat)]
        return {"aptos": int(g.aptos.sum()), "comparecimento": int(g.comparecimento.sum()), "taxa_pct": pct(g.comparecimento.sum(), g.aptos.sum())}

    out["H13"] = {"eleitores_100_ou_mais_2026": int(em26.e100.sum()), "populacao_96_ou_mais_censo_2022": int(em26.pop_96_ou_mais.sum()),
                  "eleitores_100_ou_mais_2022": int(em[(em.ano == 2022) & (em.uf != "zz")].e100.sum()),
                  "municipios_com_mais_eleitores_100_que_pessoas_96_em_2022": int((em26.e100 > em26.pop_96_ou_mais).sum()),
                  "comparecimento_100_ou_mais": {"2022_t1": taxa(2022, "1", "100 ANOS"), "2022_t2": taxa(2022, "2", "100 ANOS"), "2026_t1": taxa(2026, "1", "100 ANOS")},
                  "comparecimento_95_a_99": {"2022_t1": taxa(2022, "1", "95 A 99"), "2022_t2": taxa(2022, "2", "95 A 99"), "2026_t1": taxa(2026, "1", "95 A 99")},
                  "comparecimento_2026_t2_por_idade": "o TSE ainda não publicou o 2º turno de 2026 nesse arquivo (29/10)"}
    lista = ["NOSSA SENHORA DA GLORIA", "PORTO DE PEDRAS", "POCO DAS ANTAS", "XIQUE-XIQUE", "BARRA", "NOVA LIBERDADE", "NOVA SOURE", "GUANAMBI", "JOACABA", "ANTAS"]
    em26["nome_n"] = em26.municipio_x.map(norm)
    cor = em26[em26.nome_n.isin(lista)][["uf", "municipio_x", "eleitores", "pop_total", "pop_12_ou_mais", "comparecimento_2t", "lula_2t", "flavio_2t"]]
    out["H14"] = {"municipios": int(len(em26)), "eleitorado_maior_que_pop_12_ou_mais_em_2022": int(len(acima)),
                  "comparecimento_2t_maior_que_pop_12_ou_mais_em_2022": int(len(acima_c)),
                  "lula_venceu_nos_com_comparecimento_acima": int((acima_c.lula_2t > acima_c.flavio_2t).sum()),
                  "2022_comparecimento_2t_maior_que_pop_16_ou_mais": int(len(acima22)),
                  "2022_lula_venceu_nesses": int((acima22.lula22 > acima22.bols22).sum()),
                  "lula_venceu_nos_com_eleitorado_acima": int((acima.lula_2t > acima.flavio_2t).sum()),
                  "flavio_venceu_nos_com_eleitorado_acima": int((acima.flavio_2t > acima.lula_2t).sum()),
                  "lula_2t_nos_com_eleitorado_acima": int(acima.lula_2t.sum()), "flavio_2t_nos_com_eleitorado_acima": int(acima.flavio_2t.sum()),
                  "corrente_lula_maior_que_populacao": [{"municipio": f"{r.municipio_x} ({r.uf.upper()})", "pop_total": int(r.pop_total), "lula_2t": int(r.lula_2t),
                                                         "lula_maior_que_pop": bool(r.lula_2t > r.pop_total)} for r in cor.itertuples()]}


def h15_h16(br, amostra, out):
    s = amostra[amostra.grupo.str.contains("sorteio", na=False)]
    g = s.groupby("turno")[["votos", "ja_votou", "ja_votou_seguido_de_manual", "manual_mes", "manual_sem"]].sum()
    j = s[s.turno == "t2"].merge(br[K + ["lula2", "lula1", "nom2"]], on=K)
    j["ja_votou_taxa"] = j.ja_votou / j.votos
    j["dlula"] = j.lula2 - j.lula1
    a = j.dropna(subset=["dlula"])
    a = a.assign(xc=a.ja_votou_taxa - a.groupby(["uf", "municipio"]).ja_votou_taxa.transform("mean"),
                 yc=a.dlula - a.groupby(["uf", "municipio"]).dlula.transform("mean"))
    out["H15"] = {"avisos_ja_votou_2t_brasil": int(br.log_ja_votou.fillna(0).sum()), "secoes_com_aviso_2t": int((br.log_ja_votou > 0).sum()),
                  "amostra_avisos_por_mil_votos": {t: round(1000 * g.loc[t, "ja_votou"] / g.loc[t, "votos"], 3) for t in g.index},
                  "amostra_aviso_seguido_de_liberacao_manual_em_5_min_pct": {t: pct(g.loc[t, "ja_votou_seguido_de_manual"], g.loc[t, "ja_votou"], 1) for t in g.index},
                  "correlacao_no_mesmo_municipio_aviso_x_ganho_do_lula": round(float(np.corrcoef(a.xc, a.yc)[0, 1]), 3)}
    horas = [f"h{h:02d}" for h in range(6, 21)]
    mh = [f"m{h:02d}" for h in range(6, 21)]
    hh = s.groupby("turno")[horas + mh].sum()
    out["H16"] = {"parte_manual_por_hora_pct": {t: {h[1:]: pct(hh.loc[t, "m" + h[1:]], hh.loc[t, h], 1) for h in horas if hh.loc[t, h] > 0} for t in hh.index},
                  "maior_sequencia_mesmo_mesario": {t: {"mediana": float(s[s.turno == t].maior_sequencia_mesmo_mesario.median()),
                                                        "p99": float(s[s.turno == t].maior_sequencia_mesmo_mesario.quantile(0.99)),
                                                        "max": int(s[s.turno == t].maior_sequencia_mesmo_mesario.max()),
                                                        "secoes_com_10_ou_mais": int((s[s.turno == t].maior_sequencia_mesmo_mesario >= 10).sum())} for t in ("t1", "t2")}}


# ---------------------------------------------------------------- Bloco D e E
def h17(out):
    base = C / "noite/versoes-tse"
    linhas = []
    for uf_dir in sorted(base.iterdir()):
        for f in sorted(uf_dir.glob("*.json"), key=lambda p: int(p.stem)):
            d = json.loads(f.read_text(encoding="utf-8"))
            votos = {}
            for agr in d["carg"][0]["agr"]:
                for par in agr["par"]:
                    for cand in par["cand"]:
                        votos[cand["n"]] = int(cand["vap"])
            linhas.append({"uf": uf_dir.name, "idg": int(f.stem), "hg": d["hg"], "dg": d["dg"], "pst": d.get("s", {}).get("pst") if isinstance(d.get("s"), dict) else None,
                           "lula": votos.get("13", 0), "flavio": votos.get("22", 0)})
    v = pd.DataFrame(linhas)
    v["quando"] = pd.to_datetime(v.dg + " " + v.hg, format="%d/%m/%Y %H:%M:%S")
    v = v.sort_values(["uf", "quando", "idg"])
    v["cai_flavio"] = v.groupby("uf").flavio.diff() < 0
    v["cai_lula"] = v.groupby("uf").lula.diff() < 0
    br = v[v.uf == "br"]
    ult = v.groupby("uf").tail(1).set_index("uf")
    soma_ufs = ult.drop(index="br")[["lula", "flavio"]].sum()
    out["H17"] = {"versoes": int(len(v)), "versoes_nacionais": int(len(br)),
                  "vezes_que_o_total_do_flavio_caiu": int(v.cai_flavio.sum()), "vezes_que_o_total_do_lula_caiu": int(v.cai_lula.sum()),
                  "ultima_versao_nacional": {"lula": int(ult.loc["br", "lula"]), "flavio": int(ult.loc["br", "flavio"])},
                  "soma_das_ufs_e_exterior_na_ultima_versao": {"lula": int(soma_ufs.lula), "flavio": int(soma_ufs.flavio)}}


def h18_h19(br, out):
    x = br.dropna(subset=["flavio_1t"]).copy()
    x["dcomp"] = x.comparecimento - x.comparecimento_1t
    caiu = x[x.bu_flavio < x.flavio_1t]
    out["H18"] = {"secoes_flavio_abaixo_do_1t": int(len(caiu)), "votos_que_o_flavio_perdeu_nelas": int((caiu.flavio_1t - caiu.bu_flavio).sum()),
                  "dessas_com_comparecimento_em_queda": pct((caiu.dcomp < 0).sum(), len(caiu), 1),
                  "secoes_lula_abaixo_do_1t": int((x.bu_lula < x.lula_1t).sum()),
                  "secoes_com_lula_zero_no_1t": int(((x.lula_1t == 0) & (x.nom1 > 0)).sum()),
                  "dessas_com_lula_acima_de_zero_no_2t": int(((x.lula_1t == 0) & (x.nom1 > 0) & (x.bu_lula > 0)).sum()),
                  "secoes_com_flavio_zero_no_1t": int(((x.flavio_1t == 0) & (x.nom1 > 0)).sum()),
                  "dessas_com_flavio_acima_de_zero_no_2t": int(((x.flavio_1t == 0) & (x.nom1 > 0) & (x.bu_flavio > 0)).sum()),
                  "teste_de_integridade_2t": "TSE: 389 votos auditados sem divergência; TRE-SP: 33 urnas sem divergência (fontes em docs/pesquisa/TEORIAS_NA_INTERNET.md)"}
    u = x.groupby("uf").agg(f1=("flavio_1t", "sum"), f2=("bu_flavio", "sum"), l1=("lula_1t", "sum"), l2=("bu_lula", "sum"),
                            c1=("comparecimento_1t", "sum"), c2=("comparecimento", "sum"), a2=("aptos", "sum"))
    u["dflavio"] = u.f2 - u.f1
    u["dcomp_pontos"] = 100 * (u.c2 - u.c1) / u.a2
    caiu_uf = u[u.dflavio < 0]
    out["H19"] = {"ufs_onde_o_flavio_caiu": {k: {"votos": int(r.dflavio), "variacao_comparecimento_pontos": round(r.dcomp_pontos, 2)} for k, r in caiu_uf.iterrows()},
                  "ufs_onde_o_lula_caiu": int((u.l2 < u.l1).sum()),
                  "comparecimento_caiu_em_quantas_dessas": int((caiu_uf.dcomp_pontos < 0).sum()),
                  "ufs_com_comparecimento_em_queda": sorted(u[u.dcomp_pontos < 0].index.tolist())}


def h20_h21_h23(br, out):
    mu = pd.read_csv(C / "presidente_municipio.csv", dtype={"cd_tse": str, "cd_ibge": str})
    rd = pd.read_csv(C / "renda_municipio_censo2022.csv", dtype={"cd_ibge": str})
    mu = mu[mu.uf != "zz"].merge(rd[["cd_ibge", "renda_pc"]], on="cd_ibge", how="left")
    mu["abst1"] = mu.abstencao_1t / mu.eleitores_1t
    mu["abst2"] = mu.abstencao_2t / mu.eleitores_2t
    mu["dabst"] = 100 * (mu.abst2 - mu.abst1)
    mu["dlula"] = 100 * (mu.lula_2t / mu.validos_2t - mu.lula_1t / mu.validos_1t)
    reg = mu.groupby("regiao").apply(lambda g: pd.Series({"abst_1t_pct": pct(g.abstencao_1t.sum(), g.eleitores_1t.sum()),
                                                          "abst_2t_pct": pct(g.abstencao_2t.sum(), g.eleitores_2t.sum())}), include_groups=False)
    alvos = {"ba": ["SALVADOR", "FEIRA DE SANTANA", "LAURO DE FREITAS"], "se": ["ARACAJU"]}
    caps = mu[mu.capital.astype(str) == "True"]
    lst = []
    for uf, nomes in alvos.items():
        for n in nomes:
            r = mu[(mu.uf == uf) & (mu.municipio.str.upper() == n)]
            if len(r):
                r = r.iloc[0]
                lst.append({"municipio": f"{n.title()} ({uf.upper()})", "abst_1t_pct": round(100 * r.abst1, 2), "abst_2t_pct": round(100 * r.abst2, 2)})
    out["H20"] = {"abstencao_por_regiao": reg.to_dict(orient="index"), "cidades_da_falta_de_onibus": lst,
                  "capitais_mediana_variacao_abstencao_pontos": round(float((100 * (caps.abst2 - caps.abst1)).median()), 2)}
    q = mu.dropna(subset=["renda_pc"]).copy()
    q["quintil_renda"] = pd.qcut(q.renda_pc, 5, labels=["1 (mais pobre)", "2", "3", "4", "5 (mais rico)"])
    out["H21"] = {"ganho_lula_pontos_por_quintil_de_renda": q.groupby("quintil_renda", observed=True).apply(
        lambda g: round(float(np.average(g.dlula, weights=g.validos_2t)), 2), include_groups=False).to_dict(),
                  "nota": "renda do Censo 2022 no lugar do Bolsa Família por município (o dado do benefício por município não entrou nesta rodada); o pedido de cassação por abuso de poder é processo no TSE, não teste de urna"}
    nomes = {"sc": ["JOAÇABA"], "rj": ["ARARUAMA", "CABO FRIO", "SÃO PEDRO DA ALDEIA", "SAQUAREMA", "ARRAIAL DO CABO", "ARMAÇÃO DOS BÚZIOS", "IGUABA GRANDE"]}
    casos = []
    for uf, ns in nomes.items():
        for n in ns:
            r = mu[(mu.uf == uf) & (mu.municipio.str.upper() == n)]
            if len(r):
                r = r.iloc[0]
                casos.append({"municipio": f"{n.title()} ({uf.upper()})", "flavio_1t": int(r.flavio_1t), "flavio_2t": int(r.flavio_2t), "lula_1t": int(r.lula_1t),
                              "lula_2t": int(r.lula_2t), "outros_1t": int(r.caiado_1t + r.cury_1t + r.renan_1t + r.zema_1t + r.outros_1t),
                              "brancos_nulos_1t": int(r.brancos_1t + r.nulos_1t), "brancos_nulos_2t": int(r.brancos_2t + r.nulos_2t),
                              "comparecimento_1t": int(r.comparecimento_1t), "comparecimento_2t": int(r.comparecimento_2t)})
    out["H23"] = {"casos": casos}


def limpar(o):
    """Chaves em texto e números do numpy em número do Python, para o JSON."""
    if isinstance(o, dict):
        return {(k if isinstance(k, str) else "-".join(map(str, k)) if isinstance(k, tuple) else str(k)): limpar(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [limpar(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return None if np.isnan(o) else round(float(o), 6)
    if isinstance(o, float) and np.isnan(o):
        return None
    return o


def main():
    T.mkdir(parents=True, exist_ok=True)
    m, br = base()
    amostra = pd.read_parquet(D / "amostra_logs.parquet")
    det = pd.read_parquet(D / "detalhe_secao_2026.parquet")
    d2 = det[det.turno == "2"]
    fora = d2[d2.origem != "Urna Eletrônica"]
    out = {"reconciliacao": {"detalhe_tse_nominais_2t": int(d2.nominais.sum()), "detalhe_tse_comparecimento_2t": int(d2.comparecimento.sum()),
                             "tabelas_por_secao_nominais_2t": int(m.nom2.sum()), "tabelas_por_secao_comparecimento_2t": int(m.comparecimento.sum()),
                             "secoes_com_boletim_fora_da_urna": int(len(fora)), "comparecimento_delas": int(fora.comparecimento.sum()),
                             "nominais_delas": int(fora.nominais.sum())},
           "secoes_brasil_instaladas": int(len(br)), "lula_tabelas": int(br.bu_lula.sum()), "flavio_tabelas": int(br.bu_flavio.sum()),
           "lula_com_exterior": int(m.bu_lula.sum()), "flavio_com_exterior": int(m.bu_flavio.sum())}
    for f in (lambda: h01_h02(br, out, m), lambda: h03(br, out, amostra), lambda: h04_h07(m, br, out), lambda: h05(br, out), lambda: h08(br, out),
              lambda: h09(br, out), lambda: h10(br, out), lambda: h11(m, br, out), lambda: h12(m, out), lambda: h13_h14(br, out),
              lambda: h15_h16(br, amostra, out), lambda: h17(out), lambda: h18_h19(br, out), lambda: h20_h21_h23(br, out)):
        f()
    (RAIZ / "resultados/RESUMO.json").write_text(json.dumps(limpar(out), ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps(limpar(out), ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    main()
