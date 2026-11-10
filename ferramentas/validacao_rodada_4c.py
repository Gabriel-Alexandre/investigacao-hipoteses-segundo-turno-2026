"""Validacao da rodada 4c por OUTRO caminho (10/11/2026). Nao usa as funcoes de rodada_4c.py.

V40  secoes que fecharam depois das 17h15 (hora de Brasilia): refeito com os segundos do log (log_encerrar_s) no lugar do texto do encerramento
V41  secoes que mudaram de local: refeito com a tabela de locais de votacao (outro arquivo)
V42  Santa Catarina: somado pela tabela por municipio no lugar das secoes
V43  exterior: refeito com o boletim (bu_) no lugar do registro de voto (rdv_)
Uso: python ferramentas/validacao_rodada_4c.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
C = RAIZ / "dados" / "copias"
D = RAIZ / "dados" / "derivados"
R = json.loads((RAIZ / "resultados" / "RODADA4C.json").read_text(encoding="utf-8"))
ok = []
OFFSET = {"ac": 2, "am": 1, "mt": 1, "ms": 1, "ro": 1, "rr": 1}


def conferir(nome, a, b, tol=0):
    bom = abs(float(a) - float(b)) <= tol
    ok.append({"teste": nome, "a": float(a), "b": float(b), "ok": bool(bom)})
    print(("OK   " if bom else "FALHA"), nome, a, b)


def main():
    t2 = pd.read_parquet(C / "t2_secoes.parquet", columns=["uf", "log_encerrar_s", "bu_lula", "bu_flavio", "rdv_lula", "rdv_flavio"])
    t = t2.dropna(subset=["log_encerrar_s"]).copy()
    t["brt_h"] = t.log_encerrar_s / 3600 + t.uf.str.lower().map(OFFSET).fillna(0)
    t = t[(t.brt_h >= 15) & (t.brt_h <= 21)]
    conferir("V40 secoes fechadas depois das 17h15 BRT (pelos segundos do log)", int((t.brt_h > 17.25).sum()), R["H33"]["fecharam_depois_das_17h15_brt"], tol=400)
    L = pd.read_parquet(D / "local_votacao_2026.parquet", columns=["uf", "municipio", "zona", "secao", "turno", "local"])
    L = L[L.uf != "zz"]
    L["k"] = L.uf.str.lower() + "|" + L.municipio.astype(str) + "|" + L.zona.astype(str) + "|" + L.secao.astype(str)
    p = L.pivot_table(index="k", columns="turno", values="local", aggfunc="first").dropna()
    p.columns = ["a", "b"]
    conferir("V41 secoes que mudaram de local (tabela de locais de votacao)", int((p.a != p.b).sum()), R["H34"]["mudaram_de_local"], tol=60)
    mu = pd.read_csv(C / "presidente_municipio.csv")
    sc = mu[mu.uf == "sc"]
    conferir("V42 Santa Catarina, votos do Lula no 1o turno (por municipio)", int(sc.lula_1t.sum()), R["H36"]["santa_catarina"]["lula_1t"], tol=500)
    conferir("V42b Santa Catarina, votos do Lula no 2o turno (por municipio)", int(sc.lula_2t.sum()), R["H36"]["santa_catarina"]["lula_2t"], tol=500)
    z = t2[t2.uf == "zz"]
    # 70 das 1.351 secoes do exterior nao tem boletim no arquivo (bu vazio): compara so onde os dois existem
    com_bu = z.dropna(subset=["bu_lula"])
    conferir("V43 exterior: boletim = registro de voto onde os dois existem (diferenca de votos do Lula)", int(abs(com_bu.bu_lula.sum() - com_bu.rdv_lula.sum())), 0, tol=0)
    conferir("V43b exterior: secoes sem boletim no arquivo", int(z.bu_lula.isna().sum()), 70, tol=0)
    conferir("V43c exterior: Lula no 2o turno pelo registro de voto (rodada 4c)", int(z.rdv_lula.sum()), R["H36"]["exterior"]["votos_lula_2t"], tol=0)
    (RAIZ / "resultados" / "VALIDACAO_RODADA4C.json").write_text(json.dumps(ok, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n{sum(1 for o in ok if o['ok'])} de {len(ok)} conferencias ok")


if __name__ == "__main__":
    main()
