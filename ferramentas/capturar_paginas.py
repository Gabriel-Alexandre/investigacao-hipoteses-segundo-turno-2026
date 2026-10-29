"""Print de página (checagem, nota oficial, matéria) em 2x: a primeira tela e a página inteira.

Uso: python ferramentas/capturar_paginas.py <lista.json> <pasta_saida>
lista.json: [{"arquivo": "tse-relatorio-apocrifo", "url": "https://..."}]
Grava <arquivo>_tela.png, <arquivo>_inteira.png e <arquivo>.json (url, título, hora, sha256).
Somente leitura: abre, espera carregar, recusa o aviso de cookies se aparecer, e fotografa.
"""
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def main():
    lista = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    saida = Path(sys.argv[2])
    saida.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        nav = p.chromium.launch(headless="--visivel" not in sys.argv, channel="chrome" if "--visivel" in sys.argv else None)
        ctx = nav.new_context(viewport={"width": 1280, "height": 1500}, device_scale_factor=2, locale="pt-BR",
                              user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")
        pg = ctx.new_page()
        for it in lista:
            try:
                pg.goto(it["url"], wait_until="domcontentloaded", timeout=60000)
                pg.wait_for_timeout(5000)
                for rot in ("Rejeitar", "Recusar", "Somente necessários", "Apenas necessários"):
                    b = pg.locator(f"button:has-text('{rot}')").first
                    if b.count() and b.is_visible():
                        b.click(timeout=2000)
                        pg.wait_for_timeout(800)
                        break
                tela, inteira = saida / f"{it['arquivo']}_tela.png", saida / f"{it['arquivo']}_inteira.png"
                pg.screenshot(path=str(tela))
                pg.screenshot(path=str(inteira), full_page=True)
                meta = {"url": it["url"], "titulo": pg.title(), "capturado_em": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
                        "sha256_inteira": hashlib.sha256(inteira.read_bytes()).hexdigest()}
                (saida / f"{it['arquivo']}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
                print("ok", it["arquivo"], meta["titulo"][:70], flush=True)
            except Exception as e:  # noqa: BLE001
                print("FALHOU", it["arquivo"], repr(e)[:150], flush=True)
        nav.close()


if __name__ == "__main__":
    main()
