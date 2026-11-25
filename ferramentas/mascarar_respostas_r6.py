"""Mascara as respostas da rodada 6 para publicar: o e-mail do TSE (19/11/2026, com a resposta institucional anexada) e o do
TRE-BA (24/11/2026).

O texto do nome e do e-mail do requerente e o endereço do Gmail no topo e no rodapé são REMOVIDOS do PDF (redação do
PyMuPDF), e a página vira imagem, para não sobrar texto por baixo da tarja. A resposta institucional do TSE (o .docx
anexado) não tem dado pessoal nem autor nos metadados: vira texto em docs/lai/TSE_RESPOSTA_2026-11-19.md
(transcrever_resposta_tse.py) e o .docx vai como está, com o sha256 conferido.

Os originais ficam fora do git. Saída: dados/lai/tse-2026-11-19/ e dados/lai/tre-ba-2026-11-24/, com --previa PNGs a 110
dpi para conferir.
Uso: python ferramentas/mascarar_respostas_r6.py <pasta dos originais> [--previa <pasta>]
"""
from __future__ import annotations

import hashlib
import io
import json
import shutil
import sys
from pathlib import Path

import fitz
from PIL import Image

RAIZ = Path(__file__).resolve().parents[1]
DPI = 150
ARQUIVOS = {
    "2026-11-19_1714_tse_resposta-de-protocolo_82032521133805.pdf": "tse-2026-11-19",
    "2026-11-24_1311_tre-ba_resposta-de-protocolo_82034321135124.pdf": "tre-ba-2026-11-24",
}
DOCX = "2026-11-19_tse_resposta-institucional_82032521133805.docx"


def ler_nomes(pasta: Path) -> list[str]:
    """Os nomes a esconder ficam fora do git, em nomes_para_tarja.txt na pasta dos originais."""
    return [l.strip() for l in (pasta / "nomes_para_tarja.txt").read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")]


def mascarar(orig: Path, nomes: list[str], previa: Path | None) -> dict:
    doc = fitz.open(orig)
    n = 0
    imagens = []
    for p in doc:
        alvos = []
        for t in nomes:
            alvos += p.search_for(t)
        for w in p.get_text("words"):
            if "@gmail.com" in w[4] or w[4].startswith("https://mail.google.com"):
                alvos.append(fitz.Rect(w[:4]))
        for r in alvos:
            p.add_redact_annot(r, fill=(0, 0, 0))
        n += len(alvos)
        p.apply_redactions()
        pix = p.get_pixmap(dpi=DPI)
        imagens.append(Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB"))
    saida = fitz.open()
    for im in imagens:
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=85, optimize=True)
        pg = saida.new_page(width=im.width * 72 / DPI, height=im.height * 72 / DPI)
        pg.insert_image(pg.rect, stream=buf.getvalue())
        if previa:
            previa.mkdir(parents=True, exist_ok=True)
            im.resize((im.width * 110 // DPI, im.height * 110 // DPI)).save(previa / (orig.stem + "_mascarado.png"))
    pasta = RAIZ / "dados" / "lai" / ARQUIVOS[orig.name]
    pasta.mkdir(parents=True, exist_ok=True)
    destino = pasta / (orig.stem.replace("resposta-de-protocolo", "email") + "_mascarado.pdf")
    saida.save(destino, garbage=4, deflate=True)
    # confere: nenhum nome nem e-mail sobrou no texto do PDF de saída (é imagem, então o texto tem de estar vazio)
    sobra = "".join(pg.get_text() for pg in fitz.open(destino))
    return {"arquivo": str(destino.relative_to(RAIZ)).replace("\\", "/"), "tarjas": n, "texto_no_pdf": len(sobra.strip()),
            "sha256": hashlib.sha256(destino.read_bytes()).hexdigest()}


def main():
    orig = Path(sys.argv[1])
    previa = Path(sys.argv[sys.argv.index("--previa") + 1]) if "--previa" in sys.argv else None
    nomes = ler_nomes(orig)
    out = [mascarar(orig / a, nomes, previa) for a in ARQUIVOS]
    d = RAIZ / "dados" / "lai" / "tse-2026-11-19"
    shutil.copy2(orig / DOCX, d / "resposta-institucional-do-tse_2026-11-19.docx")
    out.append({"arquivo": "dados/lai/tse-2026-11-19/resposta-institucional-do-tse_2026-11-19.docx",
                "sha256": hashlib.sha256((d / "resposta-institucional-do-tse_2026-11-19.docx").read_bytes()).hexdigest(),
                "observacao": "o anexo como chegou: sem dado pessoal e sem autor nos metadados"})
    (RAIZ / "dados" / "lai" / "MANIFESTO_RODADA6.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    for o in out:
        print(o)


if __name__ == "__main__":
    main()
