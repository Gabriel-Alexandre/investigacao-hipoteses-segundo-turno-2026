"""Baixa o log da urna (log.jez) de uma amostra de seções do 2º turno, que traz também o 1º turno quando a urna
é a mesma, e guarda num SQLite (dados/brutos/t2/amostra.sqlite) com URL, hora, tamanho e sha256 de cada resposta.

Por que amostra: os 85 GB do vídeo 16 foram apagados; as perguntas novas (modelo da urna, aviso "eleitor já votou",
hora das liberações, mesário que libera muitos seguidos) se respondem com uma amostra grande sorteada.

A amostra (semente 2026, gravada em dados/derivados/amostra_secoes.csv):
  sorteio   12.000 seções do Brasil sorteadas entre as instaladas
  zero      as 106 seções sem voto do Flávio (H07)
  conting   300 seções sorteadas entre as que tiveram urna de contingência no log (H10)
  javotou   as 300 seções com mais avisos "eleitor já votou" (H15)
O coletor (hipoteses/coleta.py) é o do vídeo 16, copiado com a origem anotada; um coletor só, teto adaptativo.

Uso: python ferramentas/amostra_logs.py [--teto 60]
"""
import argparse
import asyncio
import json
import sys
from pathlib import Path

import aiohttp
import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from hipoteses.coleta import Limitador, abrir, baixar, guardar, salvo, url_arq, url_aux  # noqa: E402

PL = "3221"
UA = "investigacao-hipoteses-segundo-turno-2026/0.1 (analise aberta, amostra com teto; github.com/Gabriel-Alexandre)"


def montar_amostra():
    t2 = pd.read_parquet(RAIZ / "dados/copias/t2_secoes.parquet")
    br = t2[(t2.uf != "zz") & (t2.situacao != "Nao instalada")].copy()
    k = ["uf", "municipio", "zona", "secao"]
    partes = [br.sample(12000, random_state=2026)[k].assign(grupo="sorteio"),
              br[(br.bu_flavio == 0) & (br.bu_lula > 0)][k].assign(grupo="zero"),
              br[br.log_contingencia.fillna(0).astype(int) > 0].sample(300, random_state=2026)[k].assign(grupo="conting"),
              br.sort_values("log_ja_votou", ascending=False).head(300)[k].assign(grupo="javotou")]
    a = pd.concat(partes).groupby(k, as_index=False).agg(grupo=("grupo", lambda s: "+".join(sorted(set(s)))))
    a.to_csv(RAIZ / "dados/derivados/amostra_secoes.csv", index=False)
    return a


async def coletar(a, teto):
    lim = Limitador(teto)
    timeout = aiohttp.ClientTimeout(total=120, connect=20)
    cons = {}
    async with aiohttp.ClientSession(headers={"User-Agent": UA}, timeout=timeout,
                                     connector=aiohttp.TCPConnector(limit=48, ttl_dns_cache=300)) as s:
        con = abrir("t2", "amostra")
        sem = asyncio.Semaphore(48)
        trava = asyncio.Lock()
        feitas = 0

        async def uma(uf, mun, zona, secao):
            nonlocal feitas
            async with sem:
                ua = url_aux(PL, uf, mun, zona, secao)
                if salvo(con, ua):
                    st, corpo = con.execute("SELECT status, body FROM raw WHERE url=?", (ua,)).fetchone()
                else:
                    st, corpo = await baixar(s, lim, ua)
                    async with trava:
                        guardar(con, ua, st, corpo)
                if st == 200:
                    for h in json.loads(corpo).get("hashes", []):
                        for arq in h.get("arq", []):
                            if arq.get("tp") == "log":
                                ub = url_arq(PL, uf, mun, zona, secao, h["hash"], arq["nm"])
                                if not salvo(con, ub):
                                    stb, cb = await baixar(s, lim, ub)
                                    async with trava:
                                        guardar(con, ub, stb, cb)
                feitas += 1
                if feitas % 500 == 0:
                    async with trava:
                        con.commit()
                    print(f"{feitas}/{len(a)} taxa={lim.taxa:.0f} 429={lim.penalizacoes}", flush=True)

        await asyncio.gather(*[uma(*r) for r in a[["uf", "municipio", "zona", "secao"]].itertuples(index=False)])
        con.commit()
        falhas = con.execute("SELECT COUNT(*) FROM raw WHERE status NOT IN (200,404)").fetchone()[0]
        print(json.dumps({"secoes": len(a), "itens": con.execute("SELECT COUNT(*) FROM raw").fetchone()[0], "falhas": falhas}))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--teto", type=float, default=60.0)
    a = montar_amostra()
    print(a.grupo.value_counts().to_dict(), flush=True)
    asyncio.run(coletar(a, ap.parse_args().teto))


if __name__ == "__main__":
    main()
