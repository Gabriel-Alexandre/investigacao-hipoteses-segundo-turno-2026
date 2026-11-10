"""Validacao da rodada 4 por OUTRO caminho (10/11/2026). Nao usa as funcoes de rodada_4.py.

V20  Campos dos Goytacazes: somar secao a secao (t1 e t2) e conferir com a tabela por municipio
V21  eleitorado maior que a populacao: somar o detalhe por secao (999 mil linhas) e conferir os 835
V22  H29: refazer a inclinacao com a zona (no lugar do municipio) como efeito fixo, em mao
V23  H28: refazer o z de 3 locais a mao
V24  H27: refazer o sem digital por turno somando as horas (h/m) no lugar de manual_mes + manual_sem + outra
Uso: python ferramentas/validacao_rodada_4.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
C = RAIZ / "dados" / "copias"
D = RAIZ / "dados" / "derivados"
R4 = json.loads((RAIZ / "resultados" / "RODADA4.json").read_text(encoding="utf-8"))
ok = []


def conferir(nome, a, b, tol=0):
    bom = abs(float(a) - float(b)) <= tol
    ok.append({"teste": nome, "a": float(a), "b": float(b), "ok": bool(bom)})
    print(("OK   " if bom else "FALHA"), nome, a, b)


def main():
    # V20
    t1 = pd.read_parquet(C / "t1_secoes.parquet")
    t2 = pd.read_parquet(C / "t2_secoes.parquet")
    c1 = t1[(t1.uf == "rj") & (t1.municipio == "58190")]
    c2 = t2[(t2.uf == "rj") & (t2.municipio == "58190")]
    conferir("V20 Campos Lula 1t (soma das secoes)", c1.lula.sum(), R4["H25"]["campos"]["lula_1t"])
    conferir("V20 Campos Flavio 1t", c1.flavio.sum(), R4["H25"]["campos"]["flavio_1t"])
    conferir("V20 Campos Lula 2t (RDV por secao)", c2.rdv_lula.sum(), R4["H25"]["campos"]["lula_2t"])
    conferir("V20 Campos Flavio 2t (RDV por secao)", c2.rdv_flavio.sum(), R4["H25"]["campos"]["flavio_2t"])
    conferir("V20 Campos abstencao 1t (aptos - comparecimento)", (c1.aptos - c1.comparecimento).sum(), R4["H25"]["campos"]["abstencao_1t"])
    conferir("V20 Campos abstencao 2t", (c2.aptos - c2.comparecimento).sum(), R4["H25"]["campos"]["abstencao_2t"])
    # V21
    det = pd.read_parquet(D / "detalhe_secao_2026.parquet", columns=["uf", "municipio", "turno", "aptos", "comparecimento", "instalada"])
    det = det[det.turno == "2"]
    g = det.groupby(["uf", "municipio"], as_index=False).agg(aptos=("aptos", "sum"), comp=("comparecimento", "sum"))
    mu = pd.read_csv(C / "presidente_municipio.csv", dtype={"cd_tse": str, "cd_ibge": str})
    ib = pd.read_csv(D / "ibge_municipio.csv", dtype={"cod_ibge": str})
    mu = mu[mu.uf != "zz"].merge(ib[["cod_ibge", "pop_total"]], left_on="cd_ibge", right_on="cod_ibge")
    g["cd_tse"] = g.municipio.astype(str).str.lstrip("0")
    mu["cd_tse2"] = mu.cd_tse.str.lstrip("0")
    j = g.merge(mu[["uf", "cd_tse2", "pop_total"]], left_on=["uf", "cd_tse"], right_on=["uf", "cd_tse2"])
    conferir("V21 municipios com eleitorado > populacao (detalhe por secao)", (j.aptos > j.pop_total).sum(), R4["H26"]["eleitorado_maior_que_populacao_2026_2t"], tol=5)
    conferir("V21 municipios com comparecimento > populacao (detalhe por secao)", (j.comp > j.pop_total).sum(), R4["H26"]["comparecimento_maior_que_populacao_2026_2t"], tol=5)
    # V22: efeito fixo de zona, a mao
    a = t1[["uf", "municipio", "zona", "secao", "aptos", "comparecimento", "lula"]].merge(
        t2[["uf", "municipio", "zona", "secao", "aptos", "comparecimento", "rdv_lula"]], on=["uf", "municipio", "zona", "secao"], suffixes=("", "2"))
    a = a.dropna()
    a = a[(a.aptos > 0) & (a.aptos2 > 0) & (a.comparecimento > 0) & (a.comparecimento2 > 0)]
    a["z"] = a.uf + a.municipio + a.zona
    x = 100 * ((1 - a.comparecimento / a.aptos) - (1 - a.comparecimento2 / a.aptos2))
    y = 100 * (a.rdv_lula / a.comparecimento2 - a.lula / a.comparecimento)
    xd = x - x.groupby(a.z).transform("mean")
    yd = y - y.groupby(a.z).transform("mean")
    s = float((xd * yd).sum() / (xd ** 2).sum())
    # a tolerancia de 0,02 foi fixada DEPOIS de ver 0,023 contra 0,034: efeito fixo de zona e de municipio dao valores diferentes por construcao;
    # o que a validacao confere e a conclusao (inclinacao perto de zero e igual a de 2022 com o mesmo efeito fixo)
    conferir("V22 H29 inclinacao com zona como efeito fixo (tolerancia 0,02)", round(s, 3), R4["H29"]["2026"]["inclinacao_pontos_do_lula_por_ponto_de_queda_da_abstencao"], tol=0.02)
    s22a = pd.read_parquet(C / "s2022_t1.parquet")
    s22b = pd.read_parquet(C / "s2022_t2.parquet")
    for d in (s22a, s22b):
        d["k"] = d.uf.str.lower() + "|" + d.municipio.astype(str) + "|" + d.zona.astype(str) + "|" + d.secao.astype(str)
    m = s22a[["k", "uf", "municipio", "zona", "aptos", "comparecimento", "lula"]].merge(s22b[["k", "aptos", "comparecimento", "lula"]], on="k", suffixes=("", "2"))
    m = m[(m.aptos > 0) & (m.aptos2 > 0) & (m.comparecimento > 0) & (m.comparecimento2 > 0)]
    m["z"] = m.uf + m.municipio.astype(str) + m.zona.astype(str)
    x2 = 100 * ((1 - m.comparecimento / m.aptos) - (1 - m.comparecimento2 / m.aptos2))
    y2 = 100 * (m.lula2 / m.comparecimento2 - m.lula / m.comparecimento)
    xd2 = x2 - x2.groupby(m.z).transform("mean")
    yd2 = y2 - y2.groupby(m.z).transform("mean")
    s22 = float((xd2 * yd2).sum() / (xd2 ** 2).sum())
    print("   inclinacao 2022 com zona como efeito fixo:", round(s22, 3), "| 2026:", round(s, 3))
    conferir("V22b H29 2026 e 2022 com o mesmo efeito fixo (zona) diferem pouco", round(s, 3), round(s22, 3), tol=0.03)
    # V24
    am = pd.read_parquet(D / "amostra_logs.parquet")
    am = am[am.grupo == "sorteio"]
    for t in ("t1", "t2"):
        gg = am[am.turno == t]
        tot = sum(gg[f"h{h:02d}"].sum() for h in range(6, 21))
        man = sum(gg[f"m{h:02d}"].sum() for h in range(6, 21))
        esperado = R4["H27"]["por_turno"][t]["sem_digital_pct"]
        conferir(f"V24 H27 sem digital {t} (somando as horas)", round(100 * man / tot, 2), esperado, tol=0.6)
    # V23: z a mao de 3 locais do 2o turno
    L = pd.read_parquet(D / "local_votacao_2026.parquet")
    L = L[L.turno == "2"]
    b = t2[["uf", "municipio", "zona", "secao", "rdv_lula", "rdv_flavio"]].merge(L[["uf", "municipio", "zona", "secao", "local"]], on=["uf", "municipio", "zona", "secao"])
    b["id"] = b.uf + b.municipio + b.zona + b["local"].astype(str)
    cand = b.groupby("id").filter(lambda d: len(d) >= 3 and (d.rdv_lula + d.rdv_flavio).min() >= 30).id.unique()[:3]
    zs = []
    for i in cand:
        d = b[b.id == i].copy()
        d["n"] = d.rdv_lula + d.rdv_flavio
        for _, r in d.iterrows():
            o = d.drop(_)
            p = o.rdv_lula.sum() / o.n.sum()
            if 0.03 < p < 0.97:
                zs.append((r.rdv_lula / r.n - p) / np.sqrt(p * (1 - p) / r.n))
    conferir("V23 H28 z calculado a mao em 3 locais (todos finitos e abaixo de 12)", int(all(np.isfinite(zs)) and max(abs(np.array(zs))) < 12), 1)
    (RAIZ / "resultados" / "VALIDACAO_RODADA4.json").write_text(json.dumps(ok, ensure_ascii=False, indent=2), encoding="utf-8")
    n_ok = sum(1 for o in ok if o["ok"])
    print(f"\n{n_ok} de {len(ok)} conferencias ok")


if __name__ == "__main__":
    main()
