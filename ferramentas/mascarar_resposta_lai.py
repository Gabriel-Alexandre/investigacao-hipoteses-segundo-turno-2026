"""Mascara a resposta do TRE-PE (13/11/2026) para publicar: o e-mail e as 4 atas anexadas.

E-mail: o texto de cada nome de pessoa, do nome e do e-mail do requerente e do endereco do Gmail no rodape e
REMOVIDO do PDF (redacao do PyMuPDF), e a pagina vira imagem, para nao sobrar texto por baixo da tarja.
Atas (fotos e escaneamentos): cada pagina e redesenhada como imagem a 200 dpi com as caixas pretas de
dados/lai/mascaras_atas.json (nome, assinatura, rubrica, titulo, CPF, RG e as iniciais que o cartorio deixou).

Os originais ficam fora do git. Saida: dados/lai/tre-pe-2026-11-13/*.pdf e, com --previa, PNGs a 110 dpi
para conferir pagina por pagina.
Uso: python ferramentas/mascarar_resposta_lai.py <pasta dos originais> [--previa <pasta>]
"""
from __future__ import annotations

import hashlib
import io
import json
import re
import sys
from pathlib import Path

import fitz
from PIL import Image, ImageDraw

RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "dados" / "lai" / "tre-pe-2026-11-13"
MASCARAS = json.loads((RAIZ / "dados" / "lai" / "mascaras_atas.json").read_text(encoding="utf-8"))
EMAIL = "2026-11-13_1339_tre-pe_resposta-de-protocolo_82034721135306.pdf"
DPI_ATA, DPI_EMAIL, DPI_BOX = 200, 150, 110
NOMES: list[str] = []


def ler_nomes(pasta: Path) -> tuple[list[str], list[str]]:
    """Os nomes a esconder ficam fora do git, em nomes_para_tarja.txt na pasta dos originais (REQ: marca o requerente)."""
    linhas = [l.strip() for l in (pasta / "nomes_para_tarja.txt").read_text(encoding="utf-8").splitlines()
              if l.strip() and not l.startswith("#")]
    return [l[4:] for l in linhas if l.startswith("REQ:")], [l for l in linhas if not l.startswith("REQ:")]


def para_pdf(paginas: list[Image.Image], destino: Path) -> None:
    doc = fitz.open()
    for im in paginas:
        buf = io.BytesIO()
        im.convert("RGB").save(buf, "JPEG", quality=82, optimize=True)
        pg = doc.new_page(width=im.width * 72 / DPI_ATA if im.info.get("dpi_ata") else im.width * 72 / DPI_EMAIL,
                          height=im.height * 72 / DPI_ATA if im.info.get("dpi_ata") else im.height * 72 / DPI_EMAIL)
        pg.insert_image(pg.rect, stream=buf.getvalue())
    doc.save(destino, garbage=4, deflate=True)


def email(orig: Path, previa: Path | None) -> dict:
    doc = fitz.open(orig / EMAIL)
    n = 0
    for p in doc:
        alvos = []
        for t in NOMES:
            alvos += p.search_for(t)
        for w in p.get_text("words"):
            if "@gmail.com" in w[4] or w[4].startswith("https://mail.google.com"):
                alvos.append(fitz.Rect(w[:4]))
        alvos += [r for r in p.search_for("https://mail.google.com")]
        # o rodape do Gmail inteiro (endereco da conversa) e o cabecalho com a data da impressao
        for b in p.get_text("blocks"):
            if "mail.google.com" in b[4]:
                alvos.append(fitz.Rect(b[:4]))
        for r in alvos:
            p.add_redact_annot(r + (-2, -1, 2, 1), fill=(0, 0, 0))
            n += 1
        p.apply_redactions()
    paginas = []
    for i, p in enumerate(doc):
        pix = p.get_pixmap(dpi=DPI_EMAIL)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        paginas.append(im)
        if previa:
            im.reduce(2).save(previa / f"email_p{i + 1:02d}.png")
    sobra = [t for t in NOMES + ["@gmail.com"] for p in doc if t in p.get_text()]
    out = SAIDA / "resposta-do-tre-pe_2026-11-13_mascarada.pdf"
    para_pdf(paginas, out)
    return {"arquivo": out.name, "paginas": len(paginas), "tarjas": n, "texto_que_sobrou": sobra}


def atas(orig: Path, previa: Path | None) -> list[dict]:
    res = []
    for nome, caixas in MASCARAS.items():
        if nome.startswith("_"):
            continue
        doc = fitz.open(orig / nome)
        paginas = []
        for i, p in enumerate(doc):
            pix = p.get_pixmap(dpi=DPI_ATA)
            im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            k = DPI_ATA / DPI_BOX
            d = ImageDraw.Draw(im)
            for x0, y0, x1, y1 in caixas.get(str(i + 1), []):
                d.rectangle((x0 * k, y0 * k, x1 * k, y1 * k), fill=(15, 15, 15))
            im.info["dpi_ata"] = True
            paginas.append(im)
            if previa:
                im.resize((round(im.width / k), round(im.height / k))).save(previa / f"{nome[:-4]}_p{i + 1:02d}.png")
        out = SAIDA / f"{nome[:-4]}_mascarado.pdf"
        para_pdf(paginas, out)
        res.append({"arquivo": out.name, "paginas": len(paginas), "caixas": sum(len(v) for v in caixas.values())})
    return res


def main():
    orig = Path(sys.argv[1])
    req, outros = ler_nomes(orig)
    NOMES.extend(req + outros)
    previa = Path(sys.argv[sys.argv.index("--previa") + 1]) if "--previa" in sys.argv else None
    if previa:
        previa.mkdir(parents=True, exist_ok=True)
    SAIDA.mkdir(parents=True, exist_ok=True)
    r = {"email": email(orig, previa), "atas": atas(orig, previa)}
    for f in sorted(SAIDA.glob("*.pdf")):
        r.setdefault("sha256", {})[f.name] = hashlib.sha256(f.read_bytes()).hexdigest()
    (SAIDA / "MANIFESTO.json").write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(r, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
