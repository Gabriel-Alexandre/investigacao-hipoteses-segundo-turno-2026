# Os comentários: como foram lidos e o que pediram

**Rodada 0, 29/out/2026.**

## De onde

| Vídeo | ID | Comentários e respostas lidos |
|---|---|---|
| 8 · os mesários do 1º turno | `GMi7q2QetgQ` | 1.019 |
| 16 · as urnas do 2º turno | `l0WeS4f09Fw` | 372 |
| 19 · as pesquisas e o resultado | `30FYWMAOb3Y` | 93 |
| **Total** (sem as respostas do próprio canal) | | **1.484**, dos quais 78 só vistos pelo Zernio nas triagens de 26 a 29/10 (retidos ou apagados depois) |

Os comentários públicos e **todas** as respostas foram lidos pela página pública do YouTube (o script `ler_comentarios.py` do repositório de triagem do canal), e os que só o Zernio mostra vieram dos dados das triagens. Os brutos ficam fora do git (têm o @ de cada pessoa).

## Como

1. **Primeira passada por palavra-chave** (`ferramentas/temas_comentarios.py`): marca os temas de cada comentário, só para ordenar a pilha. Contagem em `resultados/COMENTARIOS_TEMAS.json`.
2. **Leitura à mão** dos 803 que tocam algum tema concreto ou passam de 160 caracteres; os outros 681 são apoio, ofensa, opinião sem hipótese ou "foi fraude" sem dizer como.
3. Cada hipótese concreta virou uma entrada de `docs/HIPOTESES.md`, na versão mais forte que ela admite.

## Quanto cada tema pesa (primeira passada)

| Tema | Comentários | Vira |
|---|---|---|
| "foi fraude", sem dizer como | 320 | não é hipótese testável sozinha |
| pede uma análise específica | 195 | as hipóteses abaixo |
| mesário votando por quem faltou | 177 | H03, H16 (o vídeo 8 cobriu o 1º turno) |
| código, software, sistema | 140 | H18 |
| horário, 17h, prorrogação | 127 | H01, H02 |
| biometria, liberação sem digital | 112 | H03, H16 |
| voto impresso, auditoria | 87 | fora do dado (é proposta de mudança); entra no "o que fecharia" |
| cadastro, título, eleitores a mais | 50 | H13, H14 |
| boletim de urna | 44 | H11 |
| compra de voto, benefício, transporte | 43 | H20, H21 |
| curva da apuração, virada | 42 | H17 (a curva já foi respondida no vídeo 16) |
| seções com 100% ou zero voto | 41 | H04, H07 |
| abstenção, comparecimento | 38 | H20 |
| "votei e já tinham votado por mim" | 20 | H15 |
| mortos votaram | 12 | H13 |

A contagem por palavra-chave subestima temas escritos de muitos jeitos (os mortos aparecem também como "tumbas", "defunto", "voto espírita"). O peso no vídeo é decisão do autor; a tabela só diz o que fica sem resposta se um tema sair.

## Os pedidos mais diretos, em paráfrase

- Comparar as 106 urnas sem voto do Flávio com o 1º turno das mesmas seções (o pedido mais repetido no vídeo 16).
- "Você considerou se mortos votaram?" e "faz um vídeo se teve voto de pessoa falecida".
- Comparar as urnas que fecharam no horário com as que fecharam depois, "na mesma localização".
- Para onde foram os votos liberados sem biometria, comparando os dois turnos.
- Seções com placar repetido entre si.
- As urnas de modelo antigo contra as novas (a tese da live argentina de 2022).
- Os fiscais mandarem foto do boletim de papel para comparar com o arquivo do TSE.
- Cruzar a cobertura de celular e 5G (Anatel) com o aumento de votos.
- Seções com fiscal dos dois partidos, de um só, ou de nenhum.
- Por que o Flávio perdeu votos em 6 estados e o Lula em nenhum.

## Os prints

Os prints dos comentários usados no vídeo (79, separados por hipótese, com a foto de perfil borrada quando é foto) moram no repositório de documentação do canal, na pasta do vídeo 20, gerados por `ferramentas/capturar_comentarios.py`. Aqui não entra nome nem imagem de ninguém.

## Depois da coleta (29/out, noite)

Na validação final, os 3 vídeos foram lidos de novo: chegaram 56 comentários e respostas novos (23 no vídeo dos mesários, 30 no das urnas, 3 no das pesquisas). Nenhum traz hipótese que não esteja nas 23. Eles caem na sala-cofre e na apuração (H17), no programa que troca o voto (H18), nos mesários (H15 e H16), no boletim de papel (H11) e nas 106 seções (H07). Uma objeção de método aparece: comparar eleições que usam o mesmo sistema não ajudaria. A comparação com 2018 e 2022 diz se o padrão é novo, e não se o sistema é íntegro; isso fica no critério dos arquivos, que pesa menos justamente por isso, e o que fecha é o teste de integridade maior e a lista de quem votou (`docs/PEDIDOS_LAI.md`).
