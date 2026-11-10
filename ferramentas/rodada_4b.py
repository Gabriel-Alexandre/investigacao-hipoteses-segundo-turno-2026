"""Rodada 4b (10/11/2026): o aprofundamento das hipoteses H25 a H30 e duas novas, saidas dos comentarios.

H25b  Campos: a mesma conta com outros cortes de tamanho, e as 3 cidades grandes onde o Flavio perdeu voto
H26b  eleitorado de 2022 para 2026: onde cresceu, e se isso tem relacao com o ganho do Lula
H31   Benford na 2a casa decimal (a objecao de que o 1o digito nao vale para votos por urna)
H32   ritmo medio entre votos por secao (a objecao do intervalo entre votos)

Le so o que ja esta em dados/. Escreve resultados/RODADA4B.json. Sem rede.
Uso: python ferramentas/rodada_4b.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from rodada_4 import C, D, RAIZ, m2022, municipios, pct, demean, slope, boot_slope

OUT = RAIZ / "resultados" / "RODADA4B.json"


def h25b(mu):
    mu = mu.copy()
    mu["pool"] = mu.outros_1t_total + (mu.bn_1t - mu.bn_2t) - mu.gf.clip(upper=0)
    mu["p"] = mu.gl / mu.pool
    campos = mu[(mu.uf == "rj") & (mu.municipio.str.upper() == "CAMPOS DOS GOYTACAZES")].iloc[0]
    pc = float(campos.p)
    cortes = {}
    for corte in (20000, 50000, 100000, 200000, 0):
        g = mu[(mu.eleitores_1t >= corte) & (mu.pool > 0)]
        cortes[str(corte or "todas")] = {"municipios": int(len(g)), "mediana_pct": round(100 * float(g.p.median()), 1),
                                         "campos_abaixo_de_pct_dos_municipios": round(100 * float((g.p < pc).mean()), 1)}
    # as 3 grandes onde o Flavio perdeu voto: o que aconteceu com a abstencao e com o pool
    g = mu[mu.eleitores_1t >= 100000]
    perd = g[g.gf < 0]
    linhas = []
    for r in perd.itertuples():
        linhas.append({"municipio": f"{r.municipio.title()} ({r.uf.upper()})", "flavio_1t": int(r.flavio_1t), "flavio_2t": int(r.flavio_2t),
                       "perdeu_pct": round(float(100 * r.gf / r.flavio_1t), 2), "abstencao_variou": int(r.abstencao_2t - r.abstencao_1t),
                       "abstencao_1t_pct": pct(r.abstencao_1t, r.eleitores_1t, 1), "abstencao_2t_pct": pct(r.abstencao_2t, r.eleitores_2t, 1),
                       "lula_do_pool_pct": round(100 * float(r.p), 1)})
    # em todas as cidades (qualquer tamanho): quantas viram o Flavio perder voto e quantas o Lula
    todos = {"municipios": int(len(mu)), "flavio_perdeu_voto": int((mu.gf < 0).sum()), "lula_perdeu_voto": int((mu.gl < 0).sum()),
             "flavio_perdeu_voto_e_abstencao_subiu": int(((mu.gf < 0) & (mu.abstencao_2t > mu.abstencao_1t)).sum())}
    m22 = m2022()
    todos22 = {"bolsonaro_perdeu_voto": int((m22.gb < 0).sum()), "lula_perdeu_voto": int((m22.gl < 0).sum()), "municipios": int(len(m22))}
    # abstencao: quantos municipios tiveram a abstencao subindo entre os turnos, 2026 e 2022
    ab26 = int((mu.abstencao_2t / mu.eleitores_2t > mu.abstencao_1t / mu.eleitores_1t).sum())
    ab22 = int(((m22.aptos_2t - m22.comp_2t) / m22.aptos_2t > (m22.aptos_1t - m22.comp_1t) / m22.aptos_1t).sum())
    return {"campos_lula_do_pool_pct": round(100 * pc, 1), "cortes": cortes, "as_cidades_grandes_onde_o_flavio_perdeu": linhas,
            "todos_os_municipios_2026": todos, "todos_os_municipios_2022": todos22,
            "municipios_com_abstencao_subindo_2026": ab26, "municipios_com_abstencao_subindo_2022": ab22}


def h26b(mu, m22):
    m26 = mu[["cd_tse", "uf", "municipio", "eleitores_1t", "eleitores_2t", "pop_total", "gl", "lula_1t", "validos_1t", "lula_2t", "validos_2t"]].rename(
        columns={"lula_1t": "l26_1t", "lula_2t": "l26_2t"})
    w = m22.merge(m26, on=["cd_tse", "uf"], how="inner")
    w = w.dropna(subset=["pop_total"]).copy()
    w["cresc"] = w.eleitores_1t / w.aptos_1t - 1  # 2022 (1o turno) para 2026 (1o turno)
    w["razao26"] = w.eleitores_2t / w.pop_total
    w["acima"] = w.razao26 > 1
    total26, total22 = w.eleitores_1t.sum(), w.aptos_1t.sum()
    crescimento_pais = total26 / total22 - 1
    q = {
        "municipios": int(len(w)),
        "eleitorado_2022_1t": int(total22), "eleitorado_2026_1t": int(total26), "crescimento_nacional_pct": round(100 * float(crescimento_pais), 2),
        "mediana_do_crescimento_pct": round(100 * float(w.cresc.median()), 2),
        "nos_835_mediana_do_crescimento_pct": round(100 * float(w[w.acima].cresc.median()), 2),
        "nos_demais_mediana_do_crescimento_pct": round(100 * float(w[~w.acima].cresc.median()), 2),
        "municipios_que_cresceram_mais_de_20_pct": int((w.cresc > 0.20).sum()),
        "municipios_que_cresceram_mais_de_20_pct_entre_os_835": int(((w.cresc > 0.20) & w.acima).sum()),
        "municipios_cujo_eleitorado_caiu": int((w.cresc < 0).sum()),
    }
    # o eleitorado de 2022 ja era maior que a populacao nos que sao 835 hoje? (o fenomeno e antigo?)
    q["dos_835_ja_tinham_mais_eleitores_que_habitantes_em_2022"] = int((w[w.acima].aptos_1t > w[w.acima].pop_total).sum())
    q["dos_835_surgiram_depois_de_2022"] = int(((~(w.aptos_1t > w.pop_total)) & w.acima).sum())
    # ganho do Lula (pontos de % dos validos) contra o crescimento do eleitorado, e contra estar na lista
    w["dlula"] = 100 * (w.l26_2t / w.validos_2t - w.l26_1t / w.validos_1t)
    q["correlacao_crescimento_do_eleitorado_x_ganho_do_lula"] = round(float(np.corrcoef(w.cresc, w.dlula)[0, 1]), 3)
    q["ganho_medio_do_lula_nos_835_pontos"] = round(float(w[w.acima].dlula.mean()), 2)
    q["ganho_medio_do_lula_nos_demais_pontos"] = round(float(w[~w.acima].dlula.mean()), 2)
    # por UF: quantos e em que parte
    uf = w.groupby("uf").agg(n=("acima", "size"), acima=("acima", "sum"))
    uf["pct"] = 100 * uf.acima / uf.n
    q["ufs_com_mais_municipios_acima"] = [{"uf": i.upper(), "acima": int(r.acima), "de": int(r.n), "pct": round(float(r.pct), 1)} for i, r in uf.sort_values("acima", ascending=False).head(6).iterrows()]
    q["ufs_com_maior_parcela_acima"] = [{"uf": i.upper(), "acima": int(r.acima), "de": int(r.n), "pct": round(float(r.pct), 1)} for i, r in uf[uf.n >= 10].sort_values("pct", ascending=False).head(6).iterrows()]
    # tamanho: nos pequenos o fenomeno e mais comum?
    for lim, nome in ((5000, "ate_5_mil_habitantes"), (20000, "de_5_a_20_mil"), (100000, "de_20_a_100_mil"), (10 ** 9, "mais_de_100_mil")):
        pass
    faixas = pd.cut(w.pop_total, [0, 5000, 20000, 100000, 1e9], labels=["ate 5 mil", "5 a 20 mil", "20 a 100 mil", "mais de 100 mil"])
    t = w.groupby(faixas, observed=True).agg(n=("acima", "size"), acima=("acima", "sum"))
    q["parcela_acima_por_tamanho"] = {str(i): {"municipios": int(r.n), "acima": int(r.acima), "pct": round(100 * float(r.acima / r.n), 1)} for i, r in t.iterrows()}
    return q


def benford_2d(x):
    x = np.asarray(x, float)
    x = x[x >= 10].astype(int)
    d = (x // 10 ** (np.floor(np.log10(x)).astype(int) - 1)) % 10
    cont = np.bincount(d, minlength=10) / len(d)
    esp = np.array([sum(np.log10(1 + 1 / (10 * k + dd)) for k in range(1, 10)) for dd in range(10)])
    mad = float(np.abs(cont - esp).mean())
    return {"n": int(len(d)), "mad": round(mad, 5), "distribuicao": [round(float(v), 4) for v in cont]}, esp


def h31():
    t1 = pd.read_parquet(C / "t1_secoes.parquet", columns=["lula", "flavio"])
    t2 = pd.read_parquet(C / "t2_secoes.parquet", columns=["rdv_lula", "rdv_flavio"])
    s22 = pd.read_parquet(C / "s2022_t2.parquet", columns=["lula", "bolsonaro"])
    res = {}
    series = {"2026_2t_lula": t2.rdv_lula, "2026_2t_flavio": t2.rdv_flavio, "2026_1t_lula": t1.lula, "2026_1t_flavio": t1.flavio,
              "2022_2t_lula": s22.lula, "2022_2t_bolsonaro": s22.bolsonaro}
    for k, v in series.items():
        r, esp = benford_2d(v.dropna())
        res[k] = r
    res["esperado_benford_2a_casa"] = [round(float(v), 4) for v in esp]
    # a regra do Nigrini para 2a casa: MAD ate 0,008 = conforme (em 10 digitos); acima de 0,012 = nao conforme
    res["nota"] = "MAD (desvio medio absoluto) da 2a casa decimal; a regra de Nigrini para a 2a casa diz conforme ate 0,008 e nao conforme acima de 0,012"
    return res


def h32():
    t2 = pd.read_parquet(C / "t2_secoes.parquet", columns=["uf", "municipio", "zona", "secao", "rdv_lula", "rdv_flavio", "log_votos", "log_primeiro_voto_s", "log_ultimo_voto_s", "comparecimento"])
    t2 = t2.dropna(subset=["log_votos", "log_primeiro_voto_s", "log_ultimo_voto_s", "rdv_lula", "rdv_flavio"])
    t2 = t2[(t2.log_votos >= 30)].copy()
    t2["dur"] = t2.log_ultimo_voto_s - t2.log_primeiro_voto_s
    t2 = t2[t2.dur > 0]
    t2["intervalo"] = t2.dur / (t2.log_votos - 1)
    t2["mun"] = t2.uf + "|" + t2.municipio
    t2["ls"] = t2.rdv_lula / (t2.rdv_lula + t2.rdv_flavio)
    q = t2.intervalo.quantile([0.01, 0.05, 0.5, 0.95, 0.99])
    rapida = t2[t2.intervalo < 60]
    lenta = t2[t2.intervalo > 600]
    # a parte do Lula nas secoes mais rapidas e nas mais lentas, dentro do municipio
    x = demean(t2.assign(i=np.log(t2.intervalo)), "i")
    y = demean(t2, "ls") * 100
    res = {
        "secoes": int(len(t2)),
        "intervalo_medio_entre_votos_s": {"p1": round(float(q.loc[0.01]), 0), "p5": round(float(q.loc[0.05]), 0), "mediana": round(float(q.loc[0.5]), 0), "p95": round(float(q.loc[0.95]), 0), "p99": round(float(q.loc[0.99]), 0)},
        "secoes_com_intervalo_medio_abaixo_de_60s": int(len(rapida)),
        "secoes_com_intervalo_medio_acima_de_600s": int(len(lenta)),
        "inclinacao_pontos_do_lula_por_log_do_intervalo": round(slope(x, y), 3),
        "intervalo_95_bootstrap_por_municipio": boot_slope(x, y, t2.mun, B=200),
    }
    q1, q4 = t2.intervalo.quantile(0.1), t2.intervalo.quantile(0.9)
    res["parte_do_lula_nas_10pct_mais_rapidas_menos_o_resto_do_municipio_pontos"] = round(float(demean(t2, "ls")[t2.intervalo <= q1].mean() * 100), 2)
    res["parte_do_lula_nas_10pct_mais_lentas_menos_o_resto_do_municipio_pontos"] = round(float(demean(t2, "ls")[t2.intervalo >= q4].mean() * 100), 2)
    return res


def main():
    mu = municipios()
    m22 = m2022()
    out = {"H25b": h25b(mu), "H26b": h26b(mu, m22), "H31": h31(), "H32": h32()}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=lambda o: o.item() if hasattr(o, "item") else str(o)), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))


if __name__ == "__main__":
    main()
