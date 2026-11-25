"""Transcreve as respostas da rodada 6, sem dado pessoal: o anexo do TSE (o .docx da área técnica, que não tem nenhum) e o
texto dos 2 e-mails (TSE de 19/11/2026 e TRE-BA de 24/11/2026), com o requerente trocado por [requerente].

Lê os originais (fora do git) só para o texto dos e-mails; o .docx vem da cópia do projeto (dados/lai/tse-2026-11-19/).
Saída: docs/lai/TSE_RESPOSTA_2026-11-19.md e docs/lai/TRE_BA_RESPOSTA_2026-11-24.md.
Uso: python ferramentas/transcrever_respostas_r6.py <pasta dos originais>
"""
import hashlib
import re
import sys
from pathlib import Path

import docx
import pypdf

RAIZ = Path(__file__).resolve().parents[1]


def limpar(t: str, nomes: list[str]) -> str:
    for n in nomes:
        t = t.replace(n, "[requerente]")
    t = re.sub(r"[\w.+-]+@gmail\.com", "[e-mail do requerente]", t)
    t = re.sub(r"https://mail\.google\.com\S*", "[endereço do Gmail]", t)
    return t


def main():
    orig = Path(sys.argv[1])
    nomes = [l.strip() for l in (orig / "nomes_para_tarja.txt").read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    nomes.sort(key=len, reverse=True)
    # TSE: o e-mail e o anexo
    em = orig / "2026-11-19_1714_tse_resposta-de-protocolo_82032521133805.pdf"
    texto_email = limpar("\n".join(p.extract_text() for p in pypdf.PdfReader(em).pages), nomes)
    dx = RAIZ / "dados" / "lai" / "tse-2026-11-19" / "resposta-institucional-do-tse_2026-11-19.docx"
    d = docx.Document(dx)
    partes = []
    for p in d.paragraphs:
        t = p.text.strip()
        if not t:
            continue
        if re.match(r"^\d+\. ", t) and len(t) < 90 or t.isupper():
            partes.append(f"\n### {t}\n")
        else:
            partes.append(t + "\n")
        if t.startswith("6. Cronologia"):
            linhas = [[c.text.strip() for c in r.cells] for r in d.tables[0].rows]
            partes.append("| " + " | ".join(linhas[0]) + " |\n|" + "---|" * len(linhas[0]) + "\n")
            partes += ["| " + " | ".join(l) + " |\n" for l in linhas[1:]]
    sha_em = hashlib.sha256(em.read_bytes()).hexdigest()
    sha_dx = hashlib.sha256(dx.read_bytes()).hexdigest()
    md = f"""# Resposta do TSE ao pedido por LAI · protocolo 82032521133805 · 19/11/2026

Transcrição sem dado pessoal (o requerente trocado por `[requerente]`). O e-mail foi impresso do Gmail (PDF, sha256
`{sha_em}`); o anexo é o arquivo `.docx` como chegou (`dados/lai/tse-2026-11-19/resposta-institucional-do-tse_2026-11-19.docx`,
sha256 `{sha_dx}`), sem nenhum dado pessoal e sem autor nos metadados (criado em 16/10/2026, pela propriedade do arquivo).
O e-mail com tarja está em `dados/lai/tse-2026-11-19/`. A leitura contra o dado público está em `docs/RODADA_6.md` (H39).

O pedido (21/10/2026) tinha 3 itens: (1) o relatório ou registro de incidente da interrupção de 4/10; (2) a documentação
dos campos de data e hora ("dr" e "hr") dos arquivos públicos por seção; (3) os registros do intervalo de 19:31:50 a
19:59:22 sem nenhum boletim nesses arquivos. O texto do pedido está em `docs/PEDIDOS_LAI.md` do projeto
`alegacoes-fraude-eleicoes-2026`.

## O e-mail

```text
{texto_email.strip()}
```

## O anexo (a resposta da área técnica)

{''.join(partes)}"""
    md = md.replace("—", "--").replace("–", "--") + "\nO travessão do original aparece como `--`.\n"
    (RAIZ / "docs" / "lai" / "TSE_RESPOSTA_2026-11-19.md").write_text(md, encoding="utf-8")
    # TRE-BA: o e-mail
    eb = orig / "2026-11-24_1311_tre-ba_resposta-de-protocolo_82034321135124.pdf"
    tb = limpar("\n".join(p.extract_text() for p in pypdf.PdfReader(eb).pages), nomes)
    md2 = f"""# Resposta do TRE-BA ao pedido por LAI · protocolo 82034321135124 · 24/11/2026

Transcrição do e-mail, sem dado pessoal (o requerente trocado por `[requerente]`). Impressão do Gmail (PDF, sha256
`{hashlib.sha256(eb.read_bytes()).hexdigest()}`); o e-mail com tarja está em `dados/lai/tre-ba-2026-11-24/`. O pedido
(21/10/2026) era sobre 26 seções do 1º turno: 19 marcadas pelo projeto `alegacoes-fraude-eleicoes-2026` e as seções 315 a
321 da zona 13 de Salvador. A leitura está em `docs/RODADA_6.md` (o andamento do TRE-BA).

```text
{tb.strip()}
```
"""
    md2 = md2.replace("—", "--").replace("–", "--")
    (RAIZ / "docs" / "lai" / "TRE_BA_RESPOSTA_2026-11-24.md").write_text(md2, encoding="utf-8")
    print("ok")


if __name__ == "__main__":
    main()
