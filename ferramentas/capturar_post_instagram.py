"""Print do post do Instagram que espalhou o relatório pericial: só a imagem do post e a legenda do autor,
sem os comentários de outras pessoas embaixo (privacidade). Fecha o convite de cadastro, que tampa a página.

Uso: python ferramentas/capturar_post_instagram.py <url> <saida.png>
"""
import sys

from playwright.sync_api import sync_playwright

url, saida = sys.argv[1], sys.argv[2]
with sync_playwright() as p:
    nav = p.chromium.launch(headless=False, channel="chrome")
    pg = nav.new_context(viewport={"width": 1280, "height": 1100}, device_scale_factor=2, locale="pt-BR").new_page()
    pg.goto(url, wait_until="domcontentloaded", timeout=60000)
    pg.wait_for_timeout(6000)
    for sel in ("[aria-label='Fechar']", "svg[aria-label='Fechar']", "div[role='dialog'] button"):
        b = pg.locator(sel).first
        if b.count() and b.is_visible():
            b.click(timeout=3000)
            pg.wait_for_timeout(1500)
            break
    # a maior imagem da página é a do post; a legenda é o texto do autor; o recorte vai do topo do post ao fim da legenda
    img = pg.evaluate("""() => { let b=null, a=0; for (const i of document.images) { const r=i.getBoundingClientRect();
        if (r.width*r.height>a) { a=r.width*r.height; b={x:r.x,y:r.y,w:r.width,h:r.height}; } } return b; }""")
    leg = pg.get_by_text("This was sent in by a follower", exact=False).first.bounding_box()
    topo = min(img["y"], leg["y"]) - 70
    direita = leg["x"] + leg["width"] + 20
    clip = {"x": img["x"], "y": max(0, topo), "width": direita - img["x"], "height": max(img["y"] + img["h"], leg["y"] + leg["height"]) + 12 - max(0, topo)}
    pg.screenshot(path=saida, clip=clip)
    nav.close()
print("ok", saida)
