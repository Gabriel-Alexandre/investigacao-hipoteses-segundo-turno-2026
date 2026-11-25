"""Rodada 6: acrescenta ao dados/MANIFESTO_RODADA6.json o endereço, o status, o tamanho e o sha256 de cada arquivo
baixado pelo rodada_6_coletar.py (o corpo fica em dados/brutos/rodada6/logs.sqlite, fora do git).

Uso: python ferramentas/manifesto_rodada_6.py   (depois do rodada_6_coletar.py)
"""
import json
import sqlite3
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
BANCO = RAIZ / "dados/brutos/rodada6/logs.sqlite"
MAN = RAIZ / "dados/MANIFESTO_RODADA6.json"


def main():
    con = sqlite3.connect(f"file:{BANCO.as_posix()}?mode=ro", uri=True, timeout=60)
    linhas = con.execute("SELECT url, status, nbytes, sha256, fetched_utc FROM raw ORDER BY url").fetchall()
    man = json.loads(MAN.read_text(encoding="utf-8")) if MAN.exists() else {"rodada": 6}
    man["arquivos"] = [{"url": u, "status": st, "bytes": nb, "sha256": sh, "coletado_utc": t} for u, st, nb, sh, t in linhas]
    MAN.write_text(json.dumps(man, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(len(linhas), "arquivos no manifesto;", round(MAN.stat().st_size / 1e6, 1), "MB")


if __name__ == "__main__":
    main()
