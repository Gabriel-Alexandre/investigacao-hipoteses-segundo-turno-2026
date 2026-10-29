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
    # horas atrás de Brasília pela hora de abertura de cada urna (todas abrem às 8h de Brasília); rodada 2: o oeste do AM
    # está 2 horas atrás, não 1 como o mapa por UF dizia
    h_ab = pd.to_datetime(m.abertura, errors="coerce").dt.hour
    m["fuso"] = np.where(h_ab.isin([6, 7, 8]), 8 - h_ab, m.uf.map(FUSO).fillna(0))
    m["en_bsb"] = en.dt.hour + en.dt.minute / 60 + en.dt.second / 3600 + m.fuso
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
    fu = a[a.fuso > 0]
    return {"ate_17h00": {"secoes": int(len(a)), "flavio_pct": pct(a.bu_flavio.sum(), a.nom2.sum()), "frente_flavio": int(a.bu_flavio.sum() - a.bu_lula.sum())},
            "depois": {"secoes": int(len(d)), "frente_lula": int(d.bu_lula.sum() - d.bu_flavio.sum())},
            "relatorio_diz": {"flavio_pct": 52.39, "frente_flavio": "quase 1,8 milhão", "frente_lula_depois": "mais de 6,1 milhões", "secoes_depois": 348398},
            "secoes_dos_estados_com_fuso_no_grupo_ate_17h": int(len(fu)), "secoes_desses_estados": int((t.fuso > 0).sum()),
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
                  "votos_entre_17h_e_19h_brasil_log": int(br.log_votos_depois_17h.fillna(0).sum() - br.log_votos_depois_19h.fillna(0).sum()),
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

    def within(x, y):
        a = j[[x, y, "uf", "municipio"]].dropna()
        a = a.assign(xc=a[x] - a.groupby(["uf", "municipio"])[x].transform("mean"), yc=a[y] - a.groupby(["uf", "municipio"])[y].transform("mean"))
        return round(float(np.corrcoef(a.xc, a.yc)[0, 1]), 3), round(float(np.polyfit(a.xc, a.yc, 1)[0]), 4)

    e = pd.read_csv(D / "eleitorado_idade.csv", dtype={"cd_tse": str})
    e = e[e.uf != "zz"]
    bio = e.groupby("ano")[["eleitores", "com_biometria"]].sum()
    mes = br.log_manual_mesario.fillna(0).sum()
    sem = br.log_manual_sem_digital.fillna(0).sum()
    out["H03"] = {"liberados_pela_digital_do_mesario_2t": int(mes), "liberados_sem_digital_cadastrada_pelo_ano_de_nascimento_2t": int(sem),
                  "digital_do_mesario_pct_dos_votos": pct(mes, br.log_votos.fillna(0).sum()),
                  "sem_a_digital_do_eleitor_pct_dos_votos": pct(mes + sem, br.log_votos.fillna(0).sum()),
                  "maximo_teorico_votos": int(mes + sem), "maximo_teorico_vezes_a_diferenca": round((mes + sem) / MARGEM, 2),
                  "manuais_depois_17h": int(br.log_manuais_depois_17h.fillna(0).sum()),
                  "eleitores_com_biometria_pct": {str(a): pct(r.com_biometria, r.eleitores, 1) for a, r in bio.iterrows()},
                  "amostra_secoes": int(len(j)),
                  "amostra_parte_manual_1t_pct": pct((j.manual_mes_t1 + j.manual_sem_t1).sum(), j.votos_t1.sum()),
                  "amostra_parte_manual_2t_pct": pct((j.manual_mes_t2 + j.manual_sem_t2).sum(), j.votos_t2.sum()),
                  "correlacao_no_mesmo_municipio": {"parte_manual_2t_x_lula_2t": list(within("man2", "lula2")),
                                                     "placebo_parte_manual_1t_x_lula_1t": list(within("man1", "lula1")),
                                                     "variacao_manual_x_variacao_lula": list(within("dman", "dlula"))},
                  "2022_segundo_terceiros": "Jornal Razão: 10.011.347 (8,06%) em 2022, pela mesma conta do BU; não recalculado aqui (o arquivo de 2022 por seção com esse campo não foi baixado)"}



def s2022():
    s22 = pd.read_parquet(C / "s2022_t2.parquet")
    s22["uf"] = s22.uf.str.lower()
    s22["municipio"] = s22.municipio.str.zfill(5)
    s22["zona"] = s22.zona.str.zfill(4)
    s22["secao"] = s22.secao.str.zfill(4)
    return s22


def s2022_turno(turno):
    s = pd.read_parquet(C / ("s2022_t1.parquet" if turno == 1 else "s2022_t2.parquet"))
    s["uf"] = s.uf.str.lower()
    for c_, z in (("municipio", 5), ("zona", 4), ("secao", 4)):
        s[c_] = s[c_].str.zfill(z)
    return s[s.uf != "zz"]


def h04_h07(m, br, out):
    s22 = s2022()
    s22 = s22[s22.uf != "zz"]
    s18 = pd.read_parquet(D / "secoes_2018_t2.parquet")
    s18 = s18[s18.uf != "zz"]
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
                  "lula_acima_90_casadas_em_2022": int(al.l22.notna().sum()),
                  "2018_acima_90_haddad": int((s18.haddad / (s18.haddad + s18.bolsonaro) > 0.9).sum()),
                  "2018_acima_90_bolsonaro": int((s18.bolsonaro / (s18.haddad + s18.bolsonaro) > 0.9).sum())}
    # H07: as seções sem voto do Flávio
    z = br[(br.bu_flavio == 0) & (br.bu_lula > 0)].merge(loc, on=K, how="left")
    z = z.merge(s22[K + ["lula", "bolsonaro"]].rename(columns={"lula": "lula22", "bolsonaro": "bols22"}), on=K, how="left")
    z = z.merge(s18[K + ["haddad", "bolsonaro"]].rename(columns={"haddad": "haddad18", "bolsonaro": "bols18"}), on=K, how="left")
    termos = r"INDIGENA|ALDEIA|INDIG|TERRA INDIGENA|QUILOMB|KM |MALOCA|COMUNIDADE|POLO BASE|POSTO DE SAUDE|SESAI"
    z["nome_norm"] = z.nome_local.map(norm)
    z["indigena_no_nome"] = z.nome_norm.str.contains(termos, regex=True)
    zl = br[(br.bu_lula == 0) & (br.bu_flavio > 0)].merge(loc, on=K, how="left")
    # o acaso: entre as seções em que o Flávio teve voto no 1º turno, quantas dariam zero no 2º com a mesma divisão?
    cf = br[(br.flavio_1t >= 1) & (br.nom2 > 0)]
    pf = (cf.flavio_1t / (cf.lula_1t + cf.flavio_1t)).clip(0, 1)
    esperado_zero = float(((1 - pf) ** cf.nom2).sum())
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
                  "acaso_esperado_zero_entre_as_que_tinham_voto_no_1t": round(esperado_zero, 1),
                  "espelho_zero_lula": {"secoes": int(len(zl)), "votos_flavio": int(zl.bu_flavio.sum()),
                                        "onde": [f"{r.uf}-{r.municipio}: {r.nome_local}" for r in zl.itertuples()]},
                  "teto_votos": int(z.flavio_1t.fillna(0).sum())}


def distribuicao_1o_digito(x):
    x = x[x >= 1].astype(int).astype(str).str[0].astype(int)
    return {str(k): round(float(v), 4) for k, v in x.value_counts(normalize=True).sort_index().items()}


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
    out["H05"] = {"mad": r, "distribuicao_1o_digito": {"lula_2026": distribuicao_1o_digito(br.bu_lula), "flavio_2026": distribuicao_1o_digito(br.bu_flavio),
                                                       "benford": {str(k): round(float(np.log10(1 + 1 / k)), 4) for k in range(1, 10)}}, "regua_nigrini_1o_digito": "até 0,006 conformidade; 0,012 a 0,015 marginal; acima de 0,015 não conforme",
                  "nota": "o 1º dígito de votos por seção fica preso no tamanho da seção (200 a 400 eleitores); por isso o teste reprova os dois candidatos e os dois anos"}


def h06(out):
    out["H06"] = json.loads((RAIZ / "dados/brutos/relatorio-pericial/capturas/linha_do_tempo.json").read_text(encoding="utf-8"))


# ---------------------------------------------------------------- Bloco B
def h08(br, out):
    inst = br[br.nom2 > 0]
    obs = int((inst.groupby(["bu_lula", "bu_flavio"]).size() >= 2).sum())
    obs_alto = int((inst[(inst.bu_lula >= 300) & (inst.bu_flavio >= 300)].groupby(["bu_lula", "bu_flavio"]).size() >= 2).sum())
    # o sorteio usa a divisão Lula contra Flávio de cada seção no 1º turno (rodada 2: antes usava a parte do Lula em todos os nominais)
    p1 = (inst.lula_1t / (inst.lula_1t + inst.flavio_1t)).fillna(inst.lula2).clip(0.001, 0.999).to_numpy()
    n = inst.nom2.to_numpy().astype(int)
    sim = []
    for _ in range(20):
        l = RNG.binomial(n, p1)
        s = pd.DataFrame({"l": l, "f": n - l})
        sim.append(int((s.groupby(["l", "f"]).size() >= 2).sum()))
    s22 = s2022()
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
    dg = dentro_do_local(x, "contingencia", "dlula", "nom2")
    nom = int(x[x.contingencia].nom2.sum())
    out["H10"] = {"secoes_com_contingencia_no_log": int(x.contingencia.sum()),
                  "origem_do_voto_2t": br.origem_d2.value_counts().to_dict(),
                  "dentro_do_local_lula_2t": dentro_do_local(x, "contingencia", "lula2", "nom2"),
                  "dentro_do_local_ganho": dg,
                  "lula_pct_nas_secoes_com_contingencia": pct(x[x.contingencia].bu_lula.sum(), x[x.contingencia].nom2.sum()),
                  "votos_nominais_nessas_secoes": nom,
                  "teto_pela_diferenca_no_mesmo_local_votos": int(round(abs(dg["diferenca_pontos"]) / 100 * nom / 2)),
                  "nota_teto": "diferença de ganho contra as vizinhas do mesmo local, aplicada aos votos dessas seções; metade, porque cada voto que troca de lado mexe a diferença por dois"}



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
    cw = pd.read_csv(C / "presidente_municipio.csv", dtype={"cd_tse": str, "cd_ibge": str})[["uf", "cd_tse", "cd_ibge", "municipio", "eleitores_2t", "comparecimento_2t", "comparecimento_1t", "lula_2t", "flavio_2t", "lula_1t", "flavio_1t"]]
    e["f"] = e.faixa.map(norm)
    e = e[e.uf != "zz"]
    cent = e.f.str.contains("100 ANOS")
    tot = e.groupby(["ano", "uf", "cd_tse"]).eleitores.sum().rename("eleitores")
    e100 = e[cent].groupby(["ano", "uf", "cd_tse"]).eleitores.sum().rename("e100")
    em = pd.concat([tot, e100], axis=1).fillna(0).reset_index()
    em = em.merge(cw[["uf", "cd_tse", "cd_ibge"]], on=["uf", "cd_tse"], how="left").merge(ib, left_on="cd_ibge", right_on="cod_ibge", how="left")
    em26, em22 = em[em.ano == 2026].copy(), em[em.ano == 2022].copy()
    # piso de registros de centenário sem pessoa viva possível, por município (não pode ser negativo)
    em26["excesso"] = (em26.e100 - em26.pop_96_ou_mais).clip(lower=0)
    em22["excesso"] = (em22.e100 - em22.pop_100_ou_mais).clip(lower=0)
    c["f"] = c.faixa.map(norm)
    cc = c[c.uf != "zz"]
    eb = e.groupby(["ano", "f"])[["eleitores", "com_biometria"]].sum()

    def taxa(ano, turno, pat):
        g = cc[(cc.ano == ano) & (cc.turno == turno) & cc.f.str.contains(pat)]
        bio = eb[eb.index.get_level_values(0) == ano]
        bio = bio[bio.index.get_level_values(1).str.contains(pat)].com_biometria.sum()
        return {"aptos": int(g.aptos.sum()), "comparecimento": int(g.comparecimento.sum()), "taxa_pct": pct(g.comparecimento.sum(), g.aptos.sum()),
                "eleitores_com_biometria": int(bio), "taxa_sobre_quem_tem_biometria_pct": pct(g.comparecimento.sum(), bio)}

    faixas = {"85 a 89": "85 A 89", "90 a 94": "90 A 94", "95 a 99": "95 A 99", "100 ou mais": "100 ANOS"}
    comp = {k: {"2022_t1": taxa(2022, "1", v), "2022_t2": taxa(2022, "2", v), "2026_t1": taxa(2026, "1", v)} for k, v in faixas.items()}
    # o piso é nacional: idoso muda de cidade e leva ou não o título, então o excesso por município exagera
    exc26 = int(max(0, em26.e100.sum() - em26.pop_96_ou_mais.sum()))
    exc22 = int(max(0, em22.e100.sum() - em22.pop_100_ou_mais.sum()))
    out["H13"] = {"eleitores_100_ou_mais_2026": int(em26.e100.sum()), "populacao_96_ou_mais_censo_2022": int(em26.pop_96_ou_mais.sum()),
                  "eleitores_100_ou_mais_2022": int(em22.e100.sum()), "populacao_100_ou_mais_censo_2022": int(em22.pop_100_ou_mais.sum()),
                  "registros_de_100_ou_mais_sem_pessoa_possivel_2026_piso": exc26, "registros_de_100_ou_mais_sem_pessoa_possivel_2022": exc22,
                  "razao_eleitores_100_sobre_censo": {"2022": round(em22.e100.sum() / em22.pop_100_ou_mais.sum(), 2), "2026_sobre_96_ou_mais": round(em26.e100.sum() / em26.pop_96_ou_mais.sum(), 2)},
                  "municipios_com_excesso_2026": int((em26.excesso > 0).sum()), "municipios_com_excesso_2022": int((em22.excesso > 0).sum()),
                  "comparecimento_por_idade": comp,
                  "teto_se_todo_registro_impossivel_votasse": exc26, "teto_se_todo_registro_impossivel_votasse_pct": pct(exc26, MARGEM),
                  "comparecimento_2026_t2_por_idade": "o TSE ainda não publicou o 2º turno de 2026 nesse arquivo (29/10)"}
    m = cw[cw.uf != "zz"].merge(ib, left_on="cd_ibge", right_on="cod_ibge", how="left")
    s22 = s2022()
    c22 = s22.groupby(["uf", "municipio"]).agg(comp22=("comparecimento", "sum"), lula22=("lula", "sum"), bols22=("bolsonaro", "sum")).reset_index()
    c22 = c22.rename(columns={"municipio": "cd_tse"}).merge(cw[["uf", "cd_tse", "cd_ibge"]], on=["uf", "cd_tse"], how="left").merge(ib, left_on="cd_ibge", right_on="cod_ibge", how="left")
    a16 = m[m.comparecimento_2t > m.pop_12_ou_mais]
    at = m[m.comparecimento_2t > m.pop_total]
    at22 = c22[c22.comp22 > c22.pop_total]
    lula_pop = m[m.lula_2t > m.pop_total]
    m["razao"] = m.comparecimento_2t / m.pop_total
    m["dlula"] = (m.lula_2t - m.lula_1t) / m.comparecimento_2t
    r = float(m[["razao", "dlula"]].dropna().corr().iloc[0, 1])
    lista = ["NOSSA SENHORA DA GLORIA", "PORTO DE PEDRAS", "POCO DAS ANTAS", "XIQUE-XIQUE", "BARRA", "NOVA LIBERDADE", "NOVA SOURE", "GUANAMBI", "JOACABA", "ANTAS"]
    m["nome_n"] = m.municipio_x.map(norm)
    cor = m[m.nome_n.isin(lista)]
    out["H14"] = {"municipios": int(len(m)),
                  "comparecimento_2t_maior_que_pop_16_ou_mais": int(len(a16)), "2022_comparecimento_2t_maior_que_pop_16_ou_mais": int((c22.comp22 > c22.pop_16_ou_mais).sum()),
                  "comparecimento_2t_maior_que_pop_total": int(len(at)), "2022_comparecimento_2t_maior_que_pop_total": int(len(at22)),
                  "lula_venceu_nos_acima_da_pop_total": int((at.lula_2t > at.flavio_2t).sum()),
                  "votos_acima_da_pop_total_soma": int((at.comparecimento_2t - at.pop_total).sum()),
                  "votos_acima_da_pop_total_pct_da_diferenca": pct((at.comparecimento_2t - at.pop_total).sum(), MARGEM),
                  "municipios_com_mais_votos_do_lula_que_habitantes": [{"municipio": f"{x.municipio_x} ({x.uf.upper()})", "pop_total": int(x.pop_total), "lula_2t": int(x.lula_2t),
                                                                        "flavio_2t": int(x.flavio_2t), "lula_1t": int(x.lula_1t)} for x in lula_pop.itertuples()],
                  "correlacao_razao_comparecimento_populacao_x_ganho_do_lula": round(r, 3),
                  "corrente_lula_maior_que_populacao": [{"municipio": f"{x.municipio_x} ({x.uf.upper()})", "pop_total": int(x.pop_total), "lula_2t": int(x.lula_2t),
                                                         "lula_maior_que_pop": bool(x.lula_2t > x.pop_total)} for x in cor.itertuples()]}



def h15_h16(br, amostra, out):
    s = amostra[amostra.grupo.str.contains("sorteio", na=False)]
    cols = ["votos", "ja_votou", "ja_votou_seguido_de_manual", "manual_mes", "manual_sem", "votos_seguidos_de_manual", "votos_com_seguinte",
            "ja_votou_proximo_voto_manual", "ja_votou_com_proximo_voto", "ja_votou_isolado"]
    g = s.groupby("turno")[cols].sum()
    j = s[s.turno == "t2"].merge(br[K + ["lula2", "lula1", "nom2"]], on=K)
    j["ja_votou_taxa"] = j.ja_votou / j.votos
    j["dlula"] = j.lula2 - j.lula1
    a = j.dropna(subset=["dlula"])
    a = a.assign(xc=a.ja_votou_taxa - a.groupby(["uf", "municipio"]).ja_votou_taxa.transform("mean"),
                 yc=a.dlula - a.groupby(["uf", "municipio"]).dlula.transform("mean"))
    tot = int(br.log_ja_votou.fillna(0).sum())
    out["H15"] = {"avisos_ja_votou_2t_brasil": tot, "secoes_com_aviso_2t": int((br.log_ja_votou > 0).sum()),
                  "amostra_avisos_por_mil_votos": {t: round(1000 * g.loc[t, "ja_votou"] / g.loc[t, "votos"], 3) for t in g.index},
                  "amostra_avisos_isolados": {t: int(g.loc[t, "ja_votou_isolado"]) for t in g.index},
                  "amostra_avisos_isolados_por_mil_votos": {t: round(1000 * g.loc[t, "ja_votou_isolado"] / g.loc[t, "votos"], 3) for t in g.index},
                  "amostra_aviso_seguido_de_liberacao_manual_em_5_min_pct": {t: pct(g.loc[t, "ja_votou_seguido_de_manual"], g.loc[t, "ja_votou"], 1) for t in g.index},
                  "regua_qualquer_voto_seguido_de_liberacao_manual_em_5_min_pct": {t: pct(g.loc[t, "votos_seguidos_de_manual"], g.loc[t, "votos_com_seguinte"], 1) for t in g.index},
                  "proximo_voto_depois_do_aviso_foi_manual_pct": {t: pct(g.loc[t, "ja_votou_proximo_voto_manual"], g.loc[t, "ja_votou_com_proximo_voto"], 1) for t in g.index},
                  "parte_manual_de_todos_os_votos_pct": {t: pct(g.loc[t, "manual_mes"] + g.loc[t, "manual_sem"], g.loc[t, "votos"], 1) for t in g.index},
                  "correlacao_no_mesmo_municipio_aviso_x_ganho_do_lula": round(float(np.corrcoef(a.xc, a.yc)[0, 1]), 3),
                  "teto_se_cada_aviso_fosse_um_voto_roubado": tot, "teto_pct": pct(tot, MARGEM)}
    horas = [f"h{h:02d}" for h in range(6, 21)]
    mh = [f"m{h:02d}" for h in range(6, 21)]
    hh = s.groupby("turno")[horas + mh].sum()
    out["H16"] = {"parte_manual_por_hora_pct": {t: {h[1:]: pct(hh.loc[t, "m" + h[1:]], hh.loc[t, h], 1) for h in horas if hh.loc[t, h] > 0} for t in hh.index},
                  "votos_por_hora": {t: {h[1:]: int(hh.loc[t, h]) for h in horas if hh.loc[t, h] > 0} for t in hh.index},
                  "maior_sequencia_mesmo_mesario": {t: {"mediana": float(s[s.turno == t].maior_sequencia_mesmo_mesario.median()),
                                                        "p99": float(s[s.turno == t].maior_sequencia_mesmo_mesario.quantile(0.99)),
                                                        "max": int(s[s.turno == t].maior_sequencia_mesmo_mesario.max()),
                                                        "secoes_com_10_ou_mais": int((s[s.turno == t].maior_sequencia_mesmo_mesario >= 10).sum())} for t in ("t1", "t2")}}
    # o oeste do Amazonas (2 horas atrás de Brasília): os votos depois das 17h que a contagem do vídeo 16 não pegou
    w = amostra[amostra.grupo.str.contains("am_oeste", na=False) & (amostra.turno == "t2")]
    out["H02_oeste_do_amazonas"] = {"secoes": int(len(w)), "votos_depois_17h_brasilia": int(w.votos_depois_17h.sum()),
                                    "votos_depois_19h_brasilia": int(w.votos_depois_19h.sum())}



# ---------------------------------------------------------------- Bloco D e E
def h17(out):
    base = C / "noite/versoes-tse"
    linhas = []
    for uf_dir in sorted(base.iterdir()):
        for f in sorted(uf_dir.glob("*.json"), key=lambda p: int(p.stem)):
            d = json.loads(f.read_text(encoding="utf-8"))
            votos = {cand["n"]: int(cand["vap"]) for agr in d["carg"][0]["agr"] for par in agr["par"] for cand in par["cand"]}
            linhas.append({"uf": uf_dir.name, "idg": int(f.stem), "hg": d["hg"], "dg": d["dg"],
                           "pst": float(d["s"]["pst"].replace(",", ".")), "lula": votos.get("13", 0), "flavio": votos.get("22", 0)})
    v = pd.DataFrame(linhas)
    v["quando"] = pd.to_datetime(v.dg + " " + v.hg, format="%d/%m/%Y %H:%M:%S")
    v = v.sort_values(["uf", "quando", "idg"])
    v["cai_flavio"] = v.groupby("uf").flavio.diff() < 0
    v["cai_lula"] = v.groupby("uf").lula.diff() < 0
    nac = v[v.uf == "br"].reset_index(drop=True)
    ult = v.groupby("uf").tail(1).set_index("uf")
    soma_ufs = ult.drop(index="br")[["lula", "flavio"]].sum()
    incompletas = sorted(ult[(ult.index != "br") & (ult.pst < 100)].index.tolist())

    def soma_em(t, com_exterior=True):
        u = v[(v.uf != "br") & (v.quando <= t)]
        if not com_exterior:
            u = u[u.uf != "zz"]
        return u.groupby("uf").tail(1)[["lula", "flavio"]].sum()

    # o painel das 17h57: a divulgação estava suspensa desde 17h07; o nacional já trazia o exterior
    n1757 = nac[nac.quando <= pd.Timestamp("2026-10-25 17:57:00")].tail(1).iloc[0]
    s_com = soma_em(pd.Timestamp("2026-10-25 17:57:00"))
    s_sem = soma_em(pd.Timestamp("2026-10-25 17:57:00"), com_exterior=False)
    pausa = nac.quando.diff().max()
    out["H17"] = {"versoes": int(len(v)), "versoes_nacionais": int(len(nac)),
                  "vezes_que_o_total_do_flavio_caiu": int(v.cai_flavio.sum()), "vezes_que_o_total_do_lula_caiu": int(v.cai_lula.sum()),
                  "ultima_versao_nacional": {"lula": int(ult.loc["br", "lula"]), "flavio": int(ult.loc["br", "flavio"])},
                  "soma_das_ufs_e_exterior_na_ultima_versao": {"lula": int(soma_ufs.lula), "flavio": int(soma_ufs.flavio)},
                  "ufs_cuja_ultima_versao_gravada_nao_tinha_100_pct": incompletas,
                  "painel_17h57": {"nacional_hora": str(n1757.quando.time()), "nacional_lula": int(n1757.lula),
                                   "soma_ufs_com_exterior_lula": int(s_com.lula), "soma_ufs_sem_exterior_lula": int(s_sem.lula),
                                   "exterior_lula": int(s_com.lula - s_sem.lula)},
                  "maior_intervalo_sem_versao_nacional": str(pausa)}



def h18_h19(br, out):
    x = br.dropna(subset=["flavio_1t"]).copy()
    x["dcomp"] = x.comparecimento - x.comparecimento_1t
    caiu = x[x.bu_flavio < x.flavio_1t]
    grande = x[(x.flavio_1t >= 30) & ((x.flavio_1t - x.bu_flavio) >= 0.1 * x.flavio_1t) & (x.dcomp >= 0)]
    # o espelho de 2022: o líder do 1º turno (Lula) contra o próprio 1º turno, seção a seção
    s1 = s2022_turno(1)
    s2 = s2022()
    j22 = s2.merge(s1[K + ["lula", "bolsonaro", "comparecimento"]].rename(columns={"lula": "lula_1t", "bolsonaro": "bols_1t", "comparecimento": "comp_1t"}), on=K)
    j22["dcomp"] = j22.comparecimento - j22.comp_1t
    caiu22 = j22[j22.lula < j22.lula_1t]
    grande22 = j22[(j22.lula_1t >= 30) & ((j22.lula_1t - j22.lula) >= 0.1 * j22.lula_1t) & (j22.dcomp >= 0)]
    out["H18"] = {"secoes_flavio_abaixo_do_1t": int(len(caiu)), "votos_que_o_flavio_perdeu_nelas": int((caiu.flavio_1t - caiu.bu_flavio).sum()),
                  "dessas_com_comparecimento_em_queda_pct": pct((caiu.dcomp < 0).sum(), len(caiu), 1),
                  "todas_as_secoes_com_comparecimento_em_queda_pct": pct((x.dcomp < 0).sum(), len(x), 1),
                  "secoes_lula_abaixo_do_1t": int((x.bu_lula < x.lula_1t).sum()),
                  "queda_grande_do_flavio_com_comparecimento_estavel": {"secoes": int(len(grande)), "votos": int((grande.flavio_1t - grande.bu_flavio).sum())},
                  "espelho_2022_lider_do_1t_lula": {"secoes_abaixo_do_1t": int(len(caiu22)), "dessas_com_comparecimento_em_queda_pct": pct((caiu22.dcomp < 0).sum(), len(caiu22), 1),
                                                     "queda_grande_com_comparecimento_estavel": {"secoes": int(len(grande22)), "votos": int((grande22.lula_1t - grande22.lula).sum())}},
                  "teste_de_integridade_2t": {"tse_votos_auditados": 389, "tre_sp_urnas": 33, "divergencias": 0,
                                              "fonte": "TSE, 25/10, 20h11; TRE-SP, 25 e 26/10 (docs/pesquisa/TEORIAS_NA_INTERNET.md)"}}
    u = x.groupby("uf").agg(f1=("flavio_1t", "sum"), f2=("bu_flavio", "sum"), l1=("lula_1t", "sum"), l2=("bu_lula", "sum"),
                            c1=("comparecimento_1t", "sum"), c2=("comparecimento", "sum"), a2=("aptos", "sum"))
    u["dflavio"] = u.f2 - u.f1
    u["dcomp_pontos"] = 100 * (u.c2 - u.c1) / u.a2
    caiu_uf = u[u.dflavio < 0]
    u22 = j22.groupby("uf").agg(l1=("lula_1t", "sum"), l2=("lula", "sum"), b1=("bols_1t", "sum"), b2=("bolsonaro", "sum"), c1=("comp_1t", "sum"), c2=("comparecimento", "sum"))
    out["H19"] = {"ufs_onde_o_flavio_caiu": {k: {"votos": int(r.dflavio), "variacao_comparecimento_pontos": round(r.dcomp_pontos, 2)} for k, r in caiu_uf.iterrows()},
                  "ufs_onde_o_lula_caiu": int((u.l2 < u.l1).sum()),
                  "comparecimento_caiu_em_quantas_dessas": int((caiu_uf.dcomp_pontos < 0).sum()),
                  "ufs_com_comparecimento_em_queda": sorted(u[u.dcomp_pontos < 0].index.tolist()),
                  "espelho_2022": {"ufs_onde_o_lula_caiu": sorted(u22[u22.l2 < u22.l1].index.tolist()), "ufs_onde_o_bolsonaro_caiu": sorted(u22[u22.b2 < u22.b1].index.tolist()),
                                   "ufs_com_comparecimento_em_queda": int((u22.c2 < u22.c1).sum())}}



def h20_h21_h23(br, out):
    mu = pd.read_csv(C / "presidente_municipio.csv", dtype={"cd_tse": str, "cd_ibge": str})
    rd = pd.read_csv(C / "renda_municipio_censo2022.csv", dtype={"cd_ibge": str})
    mu = mu[mu.uf != "zz"].merge(rd[["cd_ibge", "renda_pc"]], on="cd_ibge", how="left")
    mu["abst1"] = mu.abstencao_1t / mu.eleitores_1t
    mu["abst2"] = mu.abstencao_2t / mu.eleitores_2t
    mu["dlula"] = 100 * (mu.lula_2t / mu.validos_2t - mu.lula_1t / mu.validos_1t)
    mu["gl"] = mu.lula_2t - mu.lula_1t
    mu["gf"] = mu.flavio_2t - mu.flavio_1t
    reg = mu.groupby("regiao").apply(lambda g: pd.Series({"abst_1t_pct": pct(g.abstencao_1t.sum(), g.eleitores_1t.sum()),
                                                          "abst_2t_pct": pct(g.abstencao_2t.sum(), g.eleitores_2t.sum())}), include_groups=False)
    alvos = {"ba": ["SALVADOR", "FEIRA DE SANTANA", "LAURO DE FREITAS"], "se": ["ARACAJU"]}
    caps = mu[mu.capital.astype(str) == "True"]
    lst = []
    for uf, nomes in alvos.items():
        for nm in nomes:
            r = mu[(mu.uf == uf) & (mu.municipio.str.upper() == nm)]
            if len(r):
                r = r.iloc[0]
                lst.append({"municipio": f"{nm.title()} ({uf.upper()})", "abst_1t_pct": round(100 * r.abst1, 2), "abst_2t_pct": round(100 * r.abst2, 2)})
    out["H20"] = {"abstencao_por_regiao": reg.to_dict(orient="index"), "cidades_da_falta_de_onibus": lst,
                  "capitais_mediana_variacao_abstencao_pontos": round(float((100 * (caps.abst2 - caps.abst1)).median()), 2)}
    q = mu.dropna(subset=["renda_pc"]).copy()
    q["quintil_renda"] = pd.qcut(q.renda_pc, 5, labels=["1 (mais pobre)", "2", "3", "4", "5 (mais rico)"])
    out["H21"] = {"ganho_lula_pontos_por_quintil_de_renda": q.groupby("quintil_renda", observed=True).apply(
        lambda g: round(float(np.average(g.dlula, weights=g.validos_2t)), 2), include_groups=False).to_dict(),
                  "parte_do_saldo_que_foi_para_o_lula_pct_por_quintil": q.groupby("quintil_renda", observed=True).apply(
        lambda g: pct(g.gl.sum(), g.gl.sum() + g.gf.sum(), 1), include_groups=False).to_dict(),
                  "nota": "renda do Censo 2022 no lugar do Bolsa Família por município (o dado do benefício por município não entrou nesta rodada); o pedido de cassação por abuso de poder é processo no TSE, não teste de urna"}
    nomes = {"sc": ["JOAÇABA"], "rj": ["ARARUAMA", "CABO FRIO", "SÃO PEDRO DA ALDEIA", "SAQUAREMA", "ARRAIAL DO CABO", "ARMAÇÃO DOS BÚZIOS", "IGUABA GRANDE"]}
    casos = []
    for uf, ns in nomes.items():
        for nm in ns:
            r = mu[(mu.uf == uf) & (mu.municipio.str.upper() == nm)]
            if len(r):
                r = r.iloc[0]
                casos.append({"municipio": f"{nm.title()} ({uf.upper()})", "flavio_1t": int(r.flavio_1t), "flavio_2t": int(r.flavio_2t), "lula_1t": int(r.lula_1t),
                              "lula_2t": int(r.lula_2t), "outros_1t": int(r.caiado_1t + r.cury_1t + r.renan_1t + r.zema_1t + r.outros_1t),
                              "brancos_nulos_1t": int(r.brancos_1t + r.nulos_1t), "brancos_nulos_2t": int(r.brancos_2t + r.nulos_2t),
                              "comparecimento_1t": int(r.comparecimento_1t), "comparecimento_2t": int(r.comparecimento_2t)})
    # régua: a parte do saldo que foi para o Lula na Região dos Lagos contra o resto do RJ, e Joaçaba contra os municípios de SC
    lagos = [n_.upper() for n_ in nomes["rj"]]
    rj = mu[mu.uf == "rj"]
    rl = rj[rj.municipio.str.upper().isin(lagos)]
    rr = rj[~rj.municipio.str.upper().isin(lagos)]
    sc = mu[mu.uf == "sc"].copy()
    sc["parte"] = sc.gl / (sc.gl + sc.gf)
    jo = sc[sc.municipio.str.upper() == "JOAÇABA"].parte.iloc[0]
    # comparação justa: municípios do RJ com voto parecido no Flávio no 1º turno (até 5 pontos de diferença)
    f1l = rl.flavio_1t.sum() / rl.validos_1t.sum()
    rr = rr.assign(f1=rr.flavio_1t / rr.validos_1t)
    par = rr[(rr.f1 >= f1l - 0.05) & (rr.f1 <= f1l + 0.05)]
    parte_par = par.gl.sum() / (par.gl.sum() + par.gf.sum())
    saldo_l = rl.gl.sum() + rl.gf.sum()
    out["H23"] = {"casos": casos, "parte_do_saldo_para_o_lula_regiao_dos_lagos_pct": pct(rl.gl.sum(), rl.gl.sum() + rl.gf.sum(), 1),
                  "parte_do_saldo_para_o_lula_resto_do_rj_pct": pct(rr.gl.sum(), rr.gl.sum() + rr.gf.sum(), 1),
                  "flavio_1t_regiao_dos_lagos_pct": round(100 * float(f1l), 1),
                  "municipios_parecidos_no_rj": int(len(par)), "parte_do_saldo_para_o_lula_parecidos_rj_pct": round(100 * float(parte_par), 1),
                  "votos_do_lula_acima_do_esperado_pelos_parecidos": int(round(rl.gl.sum() - parte_par * saldo_l)),
                  "parte_do_saldo_para_o_lula_joacaba_pct": round(100 * float(jo), 1),
                  "parte_do_saldo_para_o_lula_mediana_sc_pct": round(100 * float(sc.parte.median()), 1),
                  "joacaba_percentil_em_sc": round(100 * float((sc.parte < jo).mean()), 1),
                  "parte_do_saldo_para_o_lula_brasil_pct": pct(mu.gl.sum(), mu.gl.sum() + mu.gf.sum(), 1)}



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
    tab = set(map(tuple, m[m.nom2.notna() & (m.nom2 > 0)][K].values))
    falta = d2[[tuple(x) not in tab for x in d2[K].itertuples(index=False)] & (d2.nominais > 0)]
    out = {"reconciliacao": {"detalhe_tse_nominais_2t": int(d2.nominais.sum()), "detalhe_tse_comparecimento_2t": int(d2.comparecimento.sum()),
                             "tabelas_por_secao_nominais_2t": int(m.nom2.sum()), "tabelas_por_secao_comparecimento_2t": int(m.comparecimento.sum()),
                             "secoes_com_boletim_fora_da_urna": int(len(fora)), "comparecimento_delas": int(fora.comparecimento.sum()),
                             "nominais_delas": int(fora.nominais.sum()),
                             "secoes_com_voto_no_detalhe_e_fora_das_tabelas": int(len(falta)), "nominais_delas_fora_das_tabelas": int(falta.nominais.sum()),
                             "dessas_no_exterior": int((falta.uf == "zz").sum()), "origem_delas": falta.origem.value_counts().to_dict()},
           "secoes_brasil_instaladas": int(len(br)), "lula_tabelas": int(br.bu_lula.sum()), "flavio_tabelas": int(br.bu_flavio.sum()),
           "lula_com_exterior": int(m.bu_lula.sum()), "flavio_com_exterior": int(m.bu_flavio.sum())}
    for f in (lambda: h01_h02(br, out, m), lambda: h03(br, out, amostra), lambda: h04_h07(m, br, out), lambda: h05(br, out), lambda: h06(out), lambda: h08(br, out),
              lambda: h09(br, out), lambda: h10(br, out), lambda: h11(m, br, out), lambda: h12(m, out), lambda: h13_h14(br, out),
              lambda: h15_h16(br, amostra, out), lambda: h17(out), lambda: h18_h19(br, out), lambda: h20_h21_h23(br, out)):
        f()
    (RAIZ / "resultados/RESUMO.json").write_text(json.dumps(limpar(out), ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps(limpar(out), ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    main()
