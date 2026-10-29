"""Confere o texto que o público lê: sem travessão, sem conclusão geral de fraude, sem julgar intenção, sem recomendação
de voto. Lê README, ESTADO, RELATORIO, RESUMO_SIMPLES e docs/*.md (menos docs/pesquisa e docs/revisao, que citam
terceiros entre aspas). Sai com erro se achar algo.

Uso: python ferramentas/conferir_linguagem.py
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
PROIBIDO = [r"—", r"\bhouve fraude\b", r"\bnão houve fraude\b", r"\bfoi fraud", r"\bfraudulent", r"\bmentiu\b", r"\bvote em\b", r"\bvote no\b",
            r"\bde má-fé\b", r"\bquis enganar\b"]


def arquivos():
    yield from (RAIZ / n for n in ("README.md", "ESTADO.md", "RELATORIO.md", "RESUMO_SIMPLES.md"))
    for p in (RAIZ / "docs").glob("*.md"):
        yield p


def main():
    erros = []
    for p in arquivos():
        for i, ln in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            for rx in PROIBIDO:
                if re.search(rx, ln, re.I) and not re.search(r"\"[^\"]*" + rx.strip("\b") + r"[^\"]*\"", ln, re.I):
                    erros.append(f"{p.name}:{i}: {rx}")
    print("\n".join(erros) if erros else "linguagem ok")
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
