"""Rodada 6 (24/11/2026): baixa do TSE o aux.json e o log da urna de todas as seções dos municípios que os 2 reels do
Instagram citam como "o mesmo mesário em 2 cidades longe, com segundos ou minutos de diferença" (H43).

Ficam de fora as capitais e as cidades com mais de 3 mil seções (Rio de Janeiro, São Paulo e Goiânia): sem elas, os pares
testáveis são 8 (Bragança e Rio Maria; Diadema e Guaraci; Ataléia e Goianésia; Mogi Mirim e Petrópolis; José Bonifácio e
São Vicente, no 1º turno; Porto Seguro e Casa Nova; Camacan e Juazeiro; Alagoinhas e Porto Seguro, no 2º turno), e mais
Ribeira do Pombal, Santa Cruz Cabrália e Limeira, que só têm um lado.

Saída: dados/brutos/rodada6/logs.sqlite (fora do git: o log traz o número do título digitado e o número do mesário),
tabela raw(url, status, fetched_utc, nbytes, sha256, body), e dados/MANIFESTO_RODADA6.json (no git) com as contagens.
Taxa: até 4 pedidos por segundo, com recuo no 429 (o TSE limita; um coletor só).
Uso: python ferramentas/rodada_6_coletar.py
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
import threading
import time
import unicodedata
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from hipoteses.coleta import BASE, PLEITOS  # noqa: E402

UA = "investigacao-hipoteses-segundo-turno-2026 (pesquisa aberta; github.com/Gabriel-Alexandre)"
OUT = RAIZ / "dados" / "brutos" / "rodada6"
NOMES = RAIZ.parent / "investigacao-segundo-turno-2026" / "dados" / "derivados" / "municipios_nomes.csv"
ALVOS = [  # (uf, município, turno), na ordem de prioridade: os pares dos reels primeiro (Ribeira do Pombal e Bragança/Rio
    # Maria já baixados na 1ª passada; Limeira e Santa Cruz Cabrália saíram porque o par delas é uma capital)
    ("pa", "BRAGANCA", "1"), ("pa", "RIO MARIA", "1"), ("ba", "RIBEIRA DO POMBAL", "1"),
    ("ba", "PORTO SEGURO", "2"), ("ba", "CASA NOVA", "2"), ("ba", "CAMACAN", "2"), ("ba", "JUAZEIRO", "2"),
    ("ba", "ALAGOINHAS", "2"),
    ("mg", "ATALEIA", "1"), ("go", "GOIANESIA", "1"), ("sp", "JOSE BONIFACIO", "1"), ("sp", "SAO VICENTE", "1"),
    ("sp", "GUARACI", "1"), ("sp", "DIADEMA", "1"), ("sp", "MOGI MIRIM", "1"), ("rj", "PETROPOLIS", "1"),
]


def sem_acento(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().upper().strip()


class Taxa:
    def __init__(self, por_segundo: float):
        self.intervalo = 1 / por_segundo
        self.prox = 0.0
        self.lock = threading.Lock()

    def esperar(self):
        with self.lock:
            agora = time.monotonic()
            if self.prox > agora:
                time.sleep(self.prox - agora)
            self.prox = max(agora, self.prox) + self.intervalo

    def recuar(self):
        with self.lock:
            self.intervalo = min(self.intervalo * 1.5, 5.0)
            self.prox = time.monotonic() + 15


TAXA = Taxa(4)


def baixar(url: str) -> tuple[int, bytes]:
    for tentativa in range(8):
        TAXA.esperar()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as r:
                return 200, r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                TAXA.recuar()
                continue
            if e.code == 404:
                return 404, b""
            time.sleep(3 * (tentativa + 1))
        except Exception:
            time.sleep(3 * (tentativa + 1))
    return -1, b""


def secoes() -> list[tuple[str, str, str, str, str]]:
    n = pd.read_csv(NOMES, dtype=str)
    n["nf"] = n.nome.map(sem_acento)
    d = pd.read_parquet(RAIZ / "dados" / "derivados" / "detalhe_secao_2026.parquet", columns=["uf", "municipio", "zona", "secao", "turno"])
    out = []
    for uf, nome, t in ALVOS:
        cod = n[(n.uf == uf) & (n.nf == nome)].municipio.iloc[0]
        s = d[(d.uf == uf) & (d.municipio == cod) & (d.turno == t)]
        out += [(uf, cod, r.zona, r.secao, t) for r in s.itertuples()]
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(OUT / "logs.sqlite", check_same_thread=False, timeout=60)
    con.execute("PRAGMA journal_mode=WAL")  # deixa a análise ler enquanto a coleta grava
    con.execute("CREATE TABLE IF NOT EXISTS raw (url TEXT PRIMARY KEY, status INTEGER, fetched_utc TEXT, nbytes INTEGER, sha256 TEXT, body BLOB)")
    feitos = {u for (u,) in con.execute("SELECT url FROM raw WHERE status IN (200, 404)")}
    lock = threading.Lock()

    def guardar(url, st, corpo):
        with lock:
            con.execute("INSERT OR REPLACE INTO raw VALUES (?,?,?,?,?,?)", (url, st, datetime.now(timezone.utc).isoformat(timespec="seconds"),
                        len(corpo), hashlib.sha256(corpo).hexdigest() if corpo else None, corpo))
            con.commit()

    def uma(sec):
        uf, mun, z, s, t = sec
        pl = PLEITOS["t" + t]
        base = f"{BASE}/arquivo-urna/{pl}/dados/{uf}/{mun}/{z}/{s}"
        ua = f"{base}/p00{pl}-{uf}-m{mun}-z{z}-s{s}-aux.json"
        if ua in feitos:
            aux = con.execute("SELECT body FROM raw WHERE url=?", (ua,)).fetchone()[0]
            st = 200 if aux else 404
        else:
            st, aux = baixar(ua)
            guardar(ua, st, aux)
        if st != 200:
            return 0
        n = 0
        for h in json.loads(aux).get("hashes", []):
            for a in h.get("arq", []):
                if a.get("tp") == "log":
                    url = f"{base}/{h['hash']}/{a['nm']}"
                    if url not in feitos:
                        st2, corpo = baixar(url)
                        guardar(url, st2, corpo)
                    n += 1
        return n

    lista = secoes()
    print(len(lista), "seções", flush=True)
    feitas = 0
    with ThreadPoolExecutor(6) as ex:
        for _ in ex.map(uma, lista):
            feitas += 1
            if feitas % 250 == 0:
                print(feitas, "de", len(lista), flush=True)
    resumo = {r[0]: r[1] for r in con.execute("SELECT status, COUNT(*) FROM raw GROUP BY status")}
    man = {"rodada": 6, "coletado_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "alvos": ALVOS,
           "secoes": len(lista), "arquivos_por_status": resumo,
           "observacao": "os corpos ficam em dados/brutos/rodada6/logs.sqlite (fora do git); cada linha tem o sha256"}
    (RAIZ / "dados" / "MANIFESTO_RODADA6.json").write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print(resumo)


if __name__ == "__main__":
    main()
