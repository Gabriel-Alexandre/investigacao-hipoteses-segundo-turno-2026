"""Transcreve o e-mail de resposta do TRE-PE (13/11/2026) para docs/lai/, sem dado pessoal.

O PDF original (impressao do Gmail) fica fora do git: traz o nome e o e-mail do requerente e nomes de fiscais,
tecnicos e autoridades. Aqui o texto sai inteiro, com cada nome de pessoa trocado por [nome] e o requerente por
[requerente]. O sha256 do PDF lido fica no topo do arquivo gerado.
Uso: python ferramentas/transcrever_resposta_lai.py <caminho do PDF>
"""
import hashlib
import re
import sys
from pathlib import Path

import fitz

RAIZ = Path(__file__).resolve().parents[1]
OUT = RAIZ / "docs" / "lai" / "TRE_PE_RESPOSTA_2026-11-13.md"
NOMES = ["Ivoneide do Nascimento Cavalcante", "Valdilene do Nascimento Feitosa", "Edna Barbosa da Silva", "Paulo Gabriel de Almeida Siqueira",
         "Fabiana", "Poliana", "Andreza", "Louise", "Lucas do monte Silva", "Lucas do Monte", "Maria Clara", "João Victor de Almeida",
         "Ariano Tércio", "Rodrigo Fonseca Lins de Oliveira"]
REQ = ["GABRIEL ALEXANDRE CARVALHO", "Gabriel Alexandre"]


def main():
    pdf = Path(sys.argv[1])
    doc = fitz.open(pdf)
    linhas = []
    for p in doc:
        for ln in p.get_text().splitlines():
            if re.match(r"^\d\d/\d\d/2026, \d\d:\d\d Gmail - Resposta de Protocolo$", ln) or ln.startswith("https://mail.google.com"):
                continue
            linhas.append(ln)
    t = "\n".join(linhas)
    t = re.sub(r"<?[\w.+-]+@gmail\.com>?", "[e-mail do requerente]", t)
    for r in REQ:
        t = t.replace(r, "[requerente]")
    for n in NOMES:
        t = t.replace(n, "[nome]")
    t = t.replace("¿", "-").replace("—", "--")  # o travessao do original vira -- (regra do texto publico do projeto)
    cab = (f"# Resposta do TRE-PE ao pedido por LAI · protocolo 82034721135306 · 13/11/2026\n\n"
           f"Transcrição do e-mail, sem dado pessoal (nomes de pessoas trocados por `[nome]`; o requerente por `[requerente]`). "
           f"Gerada por `ferramentas/transcrever_resposta_lai.py` a partir da impressão do e-mail (PDF, sha256 `{hashlib.sha256(pdf.read_bytes()).hexdigest()}`). "
           f"A tabela seção a seção está em `dados/lai/tre_pe_resposta_2026-11-13.csv` e a leitura em `docs/RODADA_5.md`.\n\n"
           f"Os 4 anexos (atas das zonas 11, 78, 85 e 125) não estão neste repositório: a anonimização feita pelo cartório deixou primeiros nomes "
           f"e, em uma página, um número de título inteiro. O conteúdo de cada ata, sem nomes, está em `docs/RODADA_5.md` (§ As seções que as atas explicam). "
           f"Qualquer pessoa pode pedir as mesmas atas ao TRE-PE pela Ouvidoria. O travessão do original aparece como `--`.\n\n```text\n")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(cab + t.strip() + "\n```\n", encoding="utf-8")
    sobrou = [n for n in NOMES + REQ + ["biellalex"] if n in OUT.read_text(encoding="utf-8")]
    print("ok", OUT, "nomes que sobraram:", sobrou)


if __name__ == "__main__":
    main()
