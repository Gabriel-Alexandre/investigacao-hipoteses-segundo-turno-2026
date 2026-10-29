"""Baixa os arquivos abertos usados pelas hipóteses, um por vez, e grava endereço, hora, tamanho e sha256
em dados/MANIFESTO.json. Arquivo que já está no disco com o mesmo tamanho do servidor não baixa de novo.

Uso: python ferramentas/coletar.py [nome ...]    (sem nome: todos da lista FONTES)
"""
import datetime as dt
import hashlib
import json
import shutil
import sys
import time
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DEST = RAIZ / "dados" / "brutos" / "tse"
MAN = RAIZ / "dados" / "MANIFESTO.json"
UA = {"User-Agent": "investigacao-hipoteses-segundo-turno-2026 (github.com/Gabriel-Alexandre)"}
CDN = "https://cdn.tse.jus.br/estatistica/sead/odsele/"
FONTES = {
    "local_votacao_2026": CDN + "eleitorado_locais_votacao/eleitorado_local_votacao_2026.zip",
    "perfil_eleitorado_2026": CDN + "perfil_eleitorado/perfil_eleitorado_2026.zip",
    "perfil_eleitorado_2022": CDN + "perfil_eleitorado/perfil_eleitorado_2022.zip",
    "comparecimento_abstencao_2026": CDN + "perfil_comparecimento_abstencao/perfil_comparecimento_abstencao_2026.zip",
    "comparecimento_abstencao_2022": CDN + "perfil_comparecimento_abstencao/perfil_comparecimento_abstencao_2022.zip",
    "detalhe_votacao_secao_2026": CDN + "detalhe_votacao_secao/detalhe_votacao_secao_2026.zip",
    "votacao_secao_2018_BR": CDN + "votacao_secao/votacao_secao_2018_BR.zip",
    "votacao_secao_2026_BR": CDN + "votacao_secao/votacao_secao_2026_BR.zip",
}


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def baixar(nome, url, man):
    DEST.mkdir(parents=True, exist_ok=True)
    alvo = DEST / url.rsplit("/", 1)[1]
    req = urllib.request.Request(url, headers=UA, method="HEAD")
    with urllib.request.urlopen(req, timeout=60) as r:
        tam = int(r.headers.get("Content-Length") or 0)
        mod = r.headers.get("Last-Modified")
    if not (alvo.exists() and alvo.stat().st_size == tam):
        for tentativa in range(4):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=900) as r, open(alvo, "wb") as f:
                    shutil.copyfileobj(r, f, 1 << 20)
                break
            except Exception as e:  # noqa: BLE001
                print("tentativa", tentativa + 1, nome, e, flush=True)
                time.sleep(10 * (tentativa + 1))
    man[nome] = {"url": url, "arquivo": str(alvo.relative_to(RAIZ)).replace("\\", "/"), "bytes": alvo.stat().st_size,
                 "last_modified_servidor": mod, "baixado_em": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
                 "sha256": sha256(alvo)}
    print("ok", nome, man[nome]["bytes"], flush=True)


def main():
    man = json.loads(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    for nome in (sys.argv[1:] or FONTES):
        try:
            baixar(nome, FONTES[nome], man)
        except Exception as e:  # noqa: BLE001
            print("FALHOU", nome, e, flush=True)
        MAN.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
