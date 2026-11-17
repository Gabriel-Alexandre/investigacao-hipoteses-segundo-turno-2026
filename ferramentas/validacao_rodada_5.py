"""Validacao da rodada 5 por outro caminho (17/11/2026).

1. O numero de votos lido no log de cada secao bate com o comparecimento do boletim oficial (t1_secoes.parquet)?
2. A liberacao com a digital do mesario (a digital do eleitor falhou) bate com o campo do boletim de urna
   QT_ELEITORES_BIOMETRIA_NH, guardado no projeto publico alegacoes-fraude-eleicoes-2026 (secoes_2026.parquet)?
3. Contando direto os eventos do log, sem o classificador, o total de votos e o de liberacoes batem?
4. A transcricao da resposta tem as 41 secoes do pedido e as 20 zonas que responderam?
5. H38 refeito com chaves numericas em vez de texto: as mesmas contagens?
Saida: resultados/VALIDACAO_RODADA5.json
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
R5 = json.loads((RAIZ / "resultados" / "RODADA5.json").read_text(encoding="utf-8"))
ALEG = RAIZ.parent / "alegacoes-fraude-eleicoes-2026" / "resultados" / "dados" / "secoes_2026.parquet"


def main():
    sec = pd.DataFrame(R5["H37"]["por_secao"])
    checks = []

    t1 = pd.read_parquet(RAIZ / "dados" / "copias" / "t1_secoes.parquet")
    t1 = t1[t1.uf == "pe"].copy()
    t1["z"] = t1.zona.astype(int)
    t1["s"] = t1.secao.astype(int)
    x = sec.merge(t1, left_on=["zona", "secao"], right_on=["z", "s"])
    ok1 = int((x.votos == x.comparecimento).sum())
    checks.append({"teste": "votos do log = comparecimento do boletim", "ok": ok1, "de": len(sec)})

    if ALEG.exists():
        a = pd.read_parquet(ALEG, columns=["uf", "zona", "secao", "biom_nh"])
        a = a[a.uf.str.lower() == "pe"].copy()
        a["zona"] = a.zona.astype(int)
        a["secao"] = a.secao.astype(int)
        y = sec.merge(a, on=["zona", "secao"])
        ok2 = int((y.digital_falhou_mesario == y.biom_nh).sum())
        checks.append({"teste": "digital do mesario no log = QT_ELEITORES_BIOMETRIA_NH do boletim", "ok": ok2, "de": len(y)})

    sc = R5["H37"]["segundo_caminho"]
    ok3 = sum(1 for r in sec.itertuples() if sc[f"{r.zona}-{r.secao}"]["ev_voto"] == r.votos)
    ok3b = sum(1 for r in sec.itertuples() if sc[f"{r.zona}-{r.secao}"]["ev_biometrica"] >= r.biometrica)
    checks.append({"teste": "eventos 'voto computado' contados direto = votos do classificador", "ok": ok3, "de": len(sec)})
    checks.append({"teste": "eventos de habilitacao biometrica >= votos biometricos do classificador", "ok": ok3b, "de": len(sec)})

    tre = pd.read_csv(RAIZ / "dados" / "lai" / "tre_pe_resposta_2026-11-13.csv", dtype=str)
    checks.append({"teste": "a transcricao tem as 41 secoes do pedido", "ok": int(len(tre)), "de": 41})
    checks.append({"teste": "zonas que responderam", "ok": int(tre.zona.nunique()), "de": 20})

    b = pd.read_parquet(RAIZ / "dados" / "copias" / "s2022_t2.parquet")
    c = pd.read_parquet(RAIZ / "dados" / "copias" / "t2_secoes.parquet", columns=["uf", "municipio", "zona", "secao", "bu_lula", "bu_flavio"]).dropna()
    for d in (b, c):
        d["k"] = d.uf.str.lower() + "|" + d.municipio.astype(int).astype(str) + "|" + d.zona.astype(int).astype(str) + "|" + d.secao.astype(int).astype(str)
    m = c.merge(b, on="k")
    h = R5["H38"]
    checks.append({"teste": "H38 secoes casadas (chave numerica)", "ok": int(len(m)), "de": h["secoes_casadas_2022_2026"]})
    checks.append({"teste": "H38 Lula 2026 = Lula 2022", "ok": int((m.bu_lula == m.lula).sum()), "de": h["lula_2026_igual_lula_2022"]})
    checks.append({"teste": "H38 Flavio 2026 = Bolsonaro 2022", "ok": int((m.bu_flavio == m.bolsonaro).sum()), "de": h["flavio_2026_igual_bolsonaro_2022"]})

    passou = sum(1 for k in checks if k["ok"] == k["de"])
    out = {"passou": passou, "de": len(checks), "checagens": checks}
    (RAIZ / "resultados" / "VALIDACAO_RODADA5.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    for k in checks:
        print(("OK " if k["ok"] == k["de"] else "XX ") + k["teste"], k["ok"], "de", k["de"])
    print(f"{passou} de {len(checks)}")


if __name__ == "__main__":
    main()
