"""Rodada 5 (17/11/2026): baixa de novo, do TSE, o log e o aux.json do 1o turno (04/10/2026) das secoes de
Pernambuco que o pedido por LAI ao TRE-PE (protocolo 82034721135306) citou.

Por que de novo: os logs do 1o turno foram lidos inteiros no projeto alegacoes-fraude-eleicoes-2026 e depois
apagados do disco (14/out). Para conferir, secao por secao, os numeros que os cartorios mandaram em 13/11
(assinaturas no caderno, Boletim de Eleitores com Habilitacao Biografica), basta baixar as 42 secoes envolvidas:
as 41 do pedido e a secao 24 da zona 121, porque a resposta da 121a zona fala da "secao 24" e o pedido era da 274.

Saida: dados/brutos/rodada5/<zona>-<secao>-log.jez e -aux.json (fora do git: o log traz o numero do titulo
digitado pelo mesario) e dados/MANIFESTO_RODADA5.json (no git), com o endereco, a hora e o sha256 de cada arquivo.
Um pedido por vez, com pausa; o TSE responde 429 acima do teto.
Uso: python ferramentas/rodada_5_coletar.py
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from hipoteses.coleta import BASE  # noqa: E402

PL = "3220"  # 1o turno
UA = "investigacao-hipoteses-segundo-turno-2026 (pesquisa aberta; github.com/Gabriel-Alexandre)"
OUT = RAIZ / "dados" / "brutos" / "rodada5"
MANIFESTO = RAIZ / "dados" / "MANIFESTO_RODADA5.json"

# (municipio TSE, zona, secao) do texto protocolado no TRE-PE em 21/10/2026 (docs/PEDIDOS_LAI.md)
SECOES = [
    (23418, 61, 124), (23574, 121, 274), (23574, 121, 24),
    (23817, 105, 247), (23817, 105, 318), (23817, 105, 356), (23817, 106, 321), (23817, 106, 325),
    (23914, 125, 22), (24350, 85, 314),
    (24570, 11, 55), (24570, 11, 56), (24570, 11, 103), (24570, 11, 283), (24570, 101, 724),
    (24570, 118, 77), (24570, 118, 86), (24570, 118, 95), (24570, 118, 151), (24570, 118, 165),
    (24570, 118, 259), (24570, 118, 270), (24570, 118, 281), (24570, 118, 320), (24570, 118, 342),
    (24570, 147, 2), (24570, 147, 256), (24570, 147, 392), (24570, 147, 436), (24570, 147, 438), (24570, 147, 459),
    (24597, 54, 185), (24619, 88, 26), (25070, 78, 23), (25178, 55, 50), (25178, 55, 209),
    (25313, 3, 808), (25313, 7, 460), (25313, 9, 530), (25518, 81, 15), (25771, 71, 244), (26271, 18, 87),
]


def baixar(url: str) -> bytes:
    for tentativa in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(10 * (tentativa + 1))
                continue
            raise
        except Exception:
            time.sleep(5 * (tentativa + 1))
    raise RuntimeError(f"falhou: {url}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    man = json.loads(MANIFESTO.read_text(encoding="utf-8")) if MANIFESTO.exists() else {"arquivos": []}
    feitos = {a["url"] for a in man["arquivos"]}
    for mun, zona, secao in SECOES:
        m, z, s = str(mun).zfill(5), str(zona).zfill(4), str(secao).zfill(4)
        base = f"{BASE}/arquivo-urna/{PL}/dados/pe/{m}/{z}/{s}"
        ua = f"{base}/p00{PL}-pe-m{m}-z{z}-s{s}-aux.json"
        aux = baixar(ua)
        nome_aux = f"{zona}-{secao}-aux.json"
        (OUT / nome_aux).write_bytes(aux)
        if ua not in feitos:
            man["arquivos"].append({"url": ua, "arquivo": nome_aux, "sha256": hashlib.sha256(aux).hexdigest(),
                                    "bytes": len(aux), "coletado_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")})
        dado = json.loads(aux)
        logs = [(h["hash"], a["nm"]) for h in dado.get("hashes", []) for a in h.get("arq", []) if a.get("tp") == "log"]
        for i, (h, nm) in enumerate(logs):
            url = f"{base}/{h}/{nm}"
            nome = f"{zona}-{secao}-log{'' if i == 0 else '-' + str(i)}.jez"
            if url in feitos and (OUT / nome).exists():
                continue
            corpo = baixar(url)
            (OUT / nome).write_bytes(corpo)
            man["arquivos"].append({"url": url, "arquivo": nome, "sha256": hashlib.sha256(corpo).hexdigest(),
                                    "bytes": len(corpo), "coletado_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")})
            time.sleep(0.6)
        print(zona, secao, len(logs), "log(s)", flush=True)
        time.sleep(0.6)
    man["arquivos"].sort(key=lambda a: a["arquivo"])
    MANIFESTO.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print("ok:", len(man["arquivos"]), "arquivos")


if __name__ == "__main__":
    main()
