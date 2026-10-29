"""Conta, por tema e por video, os comentarios marcados por temas_comentarios.py (sem nome de ninguem).
Uso: python ferramentas/contar_temas.py  ->  resultados/COMENTARIOS_TEMAS.json
"""
import collections
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
linhas = [json.loads(l) for l in (RAIZ / "dados/derivados/comentarios_temas.jsonl").read_text(encoding="utf-8").splitlines()]
por_tema = collections.defaultdict(collections.Counter)
for x in linhas:
    for t in x["temas"]:
        por_tema[t][x["video"]] += 1
out = {"comentarios_e_respostas": len(linhas),
       "por_video": dict(collections.Counter(x["video"] for x in linhas)),
       "so_vistos_pelo_zernio": sum(1 for x in linhas if x.get("so_zernio")),
       "sem_tema": sum(1 for x in linhas if not x["temas"]),
       "por_tema": {t: {"total": sum(c.values()), **dict(sorted(c.items()))} for t, c in sorted(por_tema.items(), key=lambda kv: -sum(kv[1].values()))}}
(RAIZ / "resultados/COMENTARIOS_TEMAS.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=1))
