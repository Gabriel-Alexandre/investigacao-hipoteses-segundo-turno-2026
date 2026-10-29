"""Tira o print de comentarios do YouTube, um por arquivo, no tema claro e em 2x,
e borra a foto de perfil quando ela e uma foto (o avatar de letra fica como esta).

Uso:  python -I ferramentas/capturar_comentarios.py <lista.json> <pasta_saida>
lista.json: [{"arquivo": "H01_01_fulano", "video": "<videoId>", "comentario": "<commentId>"}, ...]

Como funciona: abre watch?v=<video>&lc=<comentario>, que poe o comentario em destaque no topo
da lista; recorta o bloco do comentario; mede o avatar (cor unica = letra; muitas cores = foto)
e, se for foto, aplica desfoque forte so no circulo do avatar. Grava tambem <arquivo>.json com
o que foi feito (avatar borrado ou nao, texto lido na pagina, hora da captura).
Somente leitura: sem login, sem clicar em nada alem de rolar a pagina.
"""
import datetime as dt
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter
from playwright.sync_api import sync_playwright

ESCALA = 2


def avatar_e_foto(img):
    """Avatar de letra do YouTube: um fundo de cor chapada com a letra branca por cima. E letra so
    quando quase todo o miolo do circulo esta perto da cor dominante ou perto do branco; qualquer
    outra coisa (inclusive foto escura ou quase de uma cor so) conta como foto e e borrada."""
    w, h = img.size
    p = img.convert("RGB").crop((int(w * .22), int(h * .22), int(w * .78), int(h * .78))).resize((36, 36))
    px = list(p.get_flattened_data()) if hasattr(p, "get_flattened_data") else list(p.getdata())
    q = [(r // 24, g // 24, b // 24) for r, g, b in px]
    dom = max(set(q), key=q.count)
    dr, dg, db = [(v * 24 + 12) for v in dom]
    perto = sum(1 for r, g, b in px if abs(r - dr) + abs(g - dg) + abs(b - db) < 60)
    branco = sum(1 for r, g, b in px if min(r, g, b) > 215)
    chapado = (perto + branco) / len(px)
    saturado = max(dr, dg, db) - min(dr, dg, db) > 40  # o fundo da letra e colorido, nao cinza nem preto
    return not (chapado > 0.92 and saturado and branco > 0.04 * len(px))


def borrar_circulo(img, caixa):
    x0, y0, x1, y1 = [int(v) for v in caixa]
    pad = 4 * ESCALA
    x0, y0, x1, y1 = max(0, x0 - pad), max(0, y0 - pad), min(img.width, x1 + pad), min(img.height, y1 + pad)
    regiao = img.crop((x0, y0, x1, y1))
    borrada = regiao.resize((max(1, regiao.width // 12), max(1, regiao.height // 12))).resize(regiao.size)
    borrada = borrada.filter(ImageFilter.GaussianBlur(6 * ESCALA))
    mascara = Image.new("L", regiao.size, 0)
    ImageDraw.Draw(mascara).ellipse((0, 0, regiao.width - 1, regiao.height - 1), fill=255)
    img.paste(borrada, (x0, y0), mascara)
    return img


def capturar(pagina, item, saida):
    url = f"https://www.youtube.com/watch?v={item['video']}&lc={item['comentario']}"
    pagina.goto(url, wait_until="domcontentloaded", timeout=60000)
    pagina.wait_for_timeout(3000)
    for _ in range(12):
        if pagina.locator("ytd-comment-thread-renderer").count():
            break
        pagina.mouse.wheel(0, 900)
        pagina.wait_for_timeout(1200)
    cid = item["comentario"]
    # o comentario (ou a resposta) pelo proprio ID, no link da data; nunca "o primeiro da lista".
    # Resposta aparece duas vezes (a previa escondida e o fio aberto): vale a copia visivel.
    todos = pagina.locator(f'ytd-comment-view-model:has(#published-time-text a[href*="{cid}"])')
    alvo = None
    for _ in range(10):
        for i in range(todos.count()):
            if todos.nth(i).is_visible():
                alvo = todos.nth(i)
                break
        if alvo is not None:
            break
        pagina.mouse.wheel(0, 700)
        pagina.wait_for_timeout(1500)
    if alvo is None:
        raise RuntimeError("comentario nao apareceu na pagina")
    alvo.scroll_into_view_if_needed()
    pagina.wait_for_timeout(1200)
    try:  # abre o "Ler mais" para o texto sair inteiro
        mais = alvo.locator("#more, tp-yt-paper-button#more, button:has-text('Ler mais')").first
        if mais.is_visible(timeout=1500):
            mais.click(timeout=3000)
            pagina.wait_for_timeout(600)
    except Exception:  # noqa: BLE001
        pass
    texto = alvo.locator("#content-text").first.inner_text(timeout=10000)
    autor = alvo.locator("#author-text").first.inner_text(timeout=10000).strip()
    try:
        curtidas = alvo.locator("#vote-count-middle").first.inner_text(timeout=3000).strip()
    except Exception:  # noqa: BLE001
        curtidas = ""
    try:
        quando = alvo.locator("#published-time-text").first.inner_text(timeout=3000).strip()
    except Exception:  # noqa: BLE001
        quando = ""
    png = saida / f"{item['arquivo']}.png"
    alvo.screenshot(path=str(png))
    caixa_alvo = alvo.bounding_box()
    caixa_av = alvo.locator("#author-thumbnail img, #author-thumbnail yt-img-shadow img").first.bounding_box()
    img = Image.open(png)
    borrado = False
    if caixa_av:
        rel = [(caixa_av["x"] - caixa_alvo["x"]) * ESCALA, (caixa_av["y"] - caixa_alvo["y"]) * ESCALA,
               (caixa_av["x"] - caixa_alvo["x"] + caixa_av["width"]) * ESCALA,
               (caixa_av["y"] - caixa_alvo["y"] + caixa_av["height"]) * ESCALA]
        av = img.crop([int(v) for v in rel])
        if "--guardar-avatar" in sys.argv:
            av.save(saida / f"_avatar_{item['arquivo']}.png")
        if avatar_e_foto(av):
            img = borrar_circulo(img.convert("RGB"), rel)
            borrado = True
    img.save(png)
    esperado = (item.get("autor") or "").strip()
    meta = {"url": url, "autor_esperado": esperado, "autor_confere": (not esperado) or esperado == autor, "autor": autor, "curtidas": curtidas, "quando": quando, "texto_na_pagina": texto, "avatar_borrado": borrado,
            "capturado_em": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            "tamanho": list(Image.open(png).size)}
    (saida / f"{item['arquivo']}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    return meta


def main():
    lista = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    saida = Path(sys.argv[2])
    saida.mkdir(parents=True, exist_ok=True)
    so_faltando = "--so-faltando" in sys.argv
    with sync_playwright() as p:
        nav = p.chromium.launch(headless=True)
        ctx = nav.new_context(viewport={"width": 1100, "height": 1400}, device_scale_factor=ESCALA,
                              locale="pt-BR", color_scheme="light",
                              user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")
        ctx.add_cookies([{"name": "SOCS", "value": "CAI", "domain": ".youtube.com", "path": "/"},
                         {"name": "CONSENT", "value": "YES+1", "domain": ".youtube.com", "path": "/"}])
        pagina = ctx.new_page()
        for item in lista:
            if so_faltando and (saida / f"{item['arquivo']}.png").exists():
                continue
            try:
                m = capturar(pagina, item, saida)
                print("ok", item["arquivo"], "borrado" if m["avatar_borrado"] else "letra", flush=True)
            except Exception as e:  # noqa: BLE001
                print("FALHOU", item["arquivo"], repr(e)[:160], flush=True)
        nav.close()


if __name__ == "__main__":
    main()
