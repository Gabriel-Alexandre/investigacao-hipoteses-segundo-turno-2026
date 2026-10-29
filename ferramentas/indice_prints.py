"""Escreve o índice dos prints de comentários (arquivo, hipótese, quem, curtidas, texto) na pasta dos prints.
O índice tem o @ de cada pessoa, por isso fica junto dos prints, no repositório de documentação, e não aqui.

Uso: python ferramentas/indice_prints.py <pasta_dos_prints>   ->  <pasta>/INDICE.md
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
HIP = {"horario-17h": "H01 e H02 (urnas encerradas depois das 17h)", "zero-voto-flavio": "H07 (106 urnas sem voto do Flávio)",
       "mortos-votaram": "H13 (mortos votaram)", "sem-biometria": "H03 e H16 (liberação sem biometria)",
       "ja-votaram-por-mim": "H15 (já tinham votado por mim)", "resultados-repetidos": "H08 (placares repetidos)",
       "voto-trocado-no-codigo": "H18 (o código troca o voto)", "sala-cofre-e-boletim": "H11 e H17 (boletim de papel e sala-cofre)",
       "abstencao": "H20 (abstenção)", "cidades-que-viraram": "H23 (cidades)", "beneficios-e-idosos": "H21 (benefícios e idosos)",
       "celular-e-5g": "H22 (celular e 5G)", "urnas-antigas": "H09 (urna antiga e nova)", "fiscais": "H16 (seções com fiscal)",
       "urnas-trocadas": "H10 (urnas trocadas)", "totalizacao-e-queda": "H17 (totalização)", "assinatura-no-caderno": "H15 (assinatura)",
       "eleitores-e-populacao": "H14 (eleitores e população)", "urna-que-bipou": "H18 (a urna que bipou sozinha)",
       "votos-dos-outros": "já respondido nos vídeos 16 e 19 (os votos dos outros candidatos)", "pesquisas": "já respondido no vídeo 19 (pesquisas)"}
VIDEO = {"08": "vídeo 8 (mesários)", "16": "vídeo 16 (urnas)", "19": "vídeo 19 (pesquisas)"}


def main():
    pasta = Path(sys.argv[1])
    idx = json.loads((RAIZ / "dados/derivados/prints_indice.json").read_text(encoding="utf-8"))
    linhas, falta, n_borr = [], [], 0
    for x in idx:
        meta_p = pasta / f"{x['arquivo']}.json"
        if not meta_p.exists():
            falta.append(x)
            continue
        m = json.loads(meta_p.read_text(encoding="utf-8"))
        n_borr += m["avatar_borrado"]
        txt = re.sub(r"\s+", " ", m["texto_na_pagina"]).replace("|", "/")
        txt = txt if len(txt) <= 180 else txt[:177] + "..."
        linhas.append(f"| `{x['arquivo']}.png` | {HIP.get(x['tema'], x['tema'])} | {m['autor']} | {VIDEO[x['video']]} | {m['quando']} | {m['curtidas'] or '0'} | {'sim' if m['avatar_borrado'] else 'não (avatar de letra)'} | {txt} |")
    out = ["# Prints dos comentários (vídeo longo 20)", "",
           f"Gerado por `investigacao-hipoteses-segundo-turno-2026/ferramentas/indice_prints.py`. {len(linhas)} prints, {n_borr} com a foto de perfil borrada "
           "(borrado tudo que não é avatar de letra, por segurança). Cada `.png` tem um `.json` ao lado com o endereço, o texto lido na página e a hora da captura. "
           "Tema claro, escala 2x, só o comentário (sem as respostas). O texto abaixo é o lido na página no momento do print.", "",
           "⚠️ Comentário de pessoa comum **não vai para a biblioteca de assets** do executor (privacidade); fica aqui, e na edição entra com o @ visível e a foto borrada, como ele pediu.", "",
           "| Arquivo | Hipótese | Quem | Vídeo | Quando | Curtidas | Foto borrada | Texto |", "|---|---|---|---|---|---|---|---|", *linhas]
    if falta:
        out += ["", "## Não capturados (o comentário não apareceu mais na página: apagado, retido ou oculto)", "",
                "| Arquivo previsto | Hipótese | Quem | Texto (dos dados da triagem) |", "|---|---|---|---|"]
        for x in falta:
            t = re.sub(r"\s+", " ", x["texto"]).replace("|", "/")[:160]
            out.append(f"| `{x['arquivo']}` | {HIP.get(x['tema'], x['tema'])} | {x['autor']} | {t} |")
    (pasta / "INDICE.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(len(linhas), "prints,", len(falta), "faltando")


if __name__ == "__main__":
    main()
