"""Validacao da rodada 4b por OUTRO caminho (10/11/2026). Nao usa as funcoes de rodada_4b.py.

V30  Flavio perdeu voto em 938 municipios: refeito somando secao a secao (t1 e t2) e agrupando pelo codigo do TSE
V31  eleitorado nacional de 2026 (1o turno): soma do detalhe por secao contra a tabela por municipio
V32  Benford na 2a casa: refeito com texto (a 2a letra do numero) no lugar da conta com potencias de 10
V33  intervalo medio entre votos: mediana refeita em segundos pela hora do 1o e do ultimo voto
Uso: python ferramentas/validacao_rodada_4b.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
C = RAIZ / "dados" / "copias"
D = RAIZ / "dados" / "derivados"
R = json.loads((RAIZ / "resultados" / "RODADA4B.json").read_text(encoding="utf-8"))
ok = []


def conferir(nome, a, b, tol=0):
    bom = abs(float(a) - float(b)) <= tol
    ok.append({"teste": nome, "a": float(a), "b": float(b), "ok": bool(bom)})
    print(("OK   " if bom else "FALHA"), nome, a, b)


def main():
    t1 = pd.read_parquet(C / "t1_secoes.parquet", columns=["uf", "municipio", "flavio", "lula", "aptos"])
    t2 = pd.read_parquet(C / "t2_secoes.parquet", columns=["uf", "municipio", "rdv_flavio", "rdv_lula", "log_votos", "log_primeiro_voto_s", "log_ultimo_voto_s"])
    a = t1.groupby(["uf", "municipio"], as_index=False).agg(f1=("flavio", "sum"), l1=("lula", "sum"), ap1=("aptos", "sum"))
    b = t2.groupby(["uf", "municipio"], as_index=False).agg(f2=("rdv_flavio", "sum"), l2=("rdv_lula", "sum"))
    j = a.merge(b, on=["uf", "municipio"])
    j = j[j.uf != "zz"]
    conferir("V30 municipios em que o Flavio perdeu voto (somando as secoes)", int((j.f2 < j.f1).sum()), R["H25b"]["todos_os_municipios_2026"]["flavio_perdeu_voto"], tol=15)
    conferir("V30b municipios em que o Lula perdeu voto em 2026", int((j.l2 < j.l1).sum()), R["H25b"]["todos_os_municipios_2026"]["lula_perdeu_voto"], tol=15)
    det = pd.read_parquet(D / "detalhe_secao_2026.parquet", columns=["uf", "turno", "aptos"])
    det = det[(det.turno == "1") & (det.uf != "zz")]
    mu = pd.read_csv(C / "presidente_municipio.csv")
    mu = mu[mu.uf != "zz"]
    conferir("V31 eleitorado do 1o turno de 2026: tabela por municipio contra o detalhe por secao (milhoes)", round(mu.eleitores_1t.sum() / 1e6, 2), round(det.aptos.sum() / 1e6, 2), tol=0.3)
    conferir("V31b municipios no cruzamento com 2022 (o resto fica sem Censo ou sem codigo, e e dito)", R["H26b"]["municipios"], len(mu), tol=40)
    # V32: segunda casa pelo texto
    x = pd.read_parquet(C / "t2_secoes.parquet", columns=["rdv_lula"]).rdv_lula.dropna()
    x = x[x >= 10].astype(int).astype(str)
    dig = x.str[1].astype(int)
    cont = np.bincount(dig, minlength=10) / len(dig)
    esp = np.array([sum(np.log10(1 + 1 / (10 * k + d)) for k in range(1, 10)) for d in range(10)])
    mad = float(np.abs(cont - esp).mean())
    conferir("V32 Benford 2a casa, Lula 2026 2o turno (MAD pelo texto)", round(mad, 5), R["H31"]["2026_2t_lula"]["mad"], tol=0.0005)
    # V33
    t = t2.dropna(subset=["log_votos", "log_primeiro_voto_s", "log_ultimo_voto_s"])
    t = t[(t.log_votos >= 30) & (t.log_ultimo_voto_s > t.log_primeiro_voto_s)]
    mediana = float(np.median((t.log_ultimo_voto_s - t.log_primeiro_voto_s) / (t.log_votos - 1)))
    conferir("V33 mediana do intervalo medio entre votos (segundos)", round(mediana, 0), R["H32"]["intervalo_medio_entre_votos_s"]["mediana"], tol=1)
    (RAIZ / "resultados" / "VALIDACAO_RODADA4B.json").write_text(json.dumps(ok, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n{sum(1 for o in ok if o['ok'])} de {len(ok)} conferencias ok")


if __name__ == "__main__":
    main()
