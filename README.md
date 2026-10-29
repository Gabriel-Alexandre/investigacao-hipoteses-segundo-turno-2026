# Investigação Aberta, parte 3: as hipóteses do público sobre o 2º turno de 2026

Projeto aberto por trás do vídeo longo 20 do canal. Pega o que o público levantou nos comentários, o "Relatório Pericial Independente" que circulou em 28/10 e as teorias que circulam na internet, e testa **uma hipótese por vez**, cada uma pelas duas visões: a do resultado legítimo e a da fraude.

É a continuação de dois projetos públicos: [`pesquisas-e-resultado-segundo-turno-2026`](https://github.com/Gabriel-Alexandre/pesquisas-e-resultado-segundo-turno-2026) (as pesquisas e o resultado) e [`investigacao-segundo-turno-2026`](https://github.com/Gabriel-Alexandre/investigacao-segundo-turno-2026) (as urnas).

## O resultado, em uma frase

Das 21 hipóteses testadas, 17 não mostraram a marca que a fraude deixaria no dado público (7 desmentidas, 10 não sustentadas), 4 ficam compatíveis com as duas visões (H14, H15, H18 e H23), e 2 não foram testadas nesta rodada (H21 e H22). O "Relatório Pericial Independente" chega ao Flávio vencendo "até as 17h" por um erro de fuso. Somando o pior caso de todos os caminhos que ainda podem ter acrescentado voto, dá 8,63% da diferença de 4.430.191 votos.

| Comece por | O que tem |
|---|---|
| [`RESUMO_SIMPLES.md`](RESUMO_SIMPLES.md) | o resultado em uma página |
| [`RELATORIO.md`](RELATORIO.md) | cada hipótese com o fato, o veredito, as duas visões, o teto e o que fecharia |
| [`docs/REVISAO_ADVERSARIAL.md`](docs/REVISAO_ADVERSARIAL.md) | o que os três revisores apontaram e o que mudou |
| [`ESTADO.md`](ESTADO.md) | onde o trabalho parou |
| [`docs/HIPOTESES.md`](docs/HIPOTESES.md) | as 23 hipóteses, cada uma com o que cada visão espera ver e o teste que separa |
| [`docs/PLANO.md`](docs/PLANO.md) | o método, os dados, a ordem de execução e as travas |
| [`docs/COMENTARIOS.md`](docs/COMENTARIOS.md) | como os comentários foram lidos e quanto cada tema pesa |
| [`docs/PEDIDOS_LAI.md`](docs/PEDIDOS_LAI.md) | os pedidos que fechariam o que o dado público não fecha (redigidos, não protocolados) |
| [`docs/pesquisa/`](docs/pesquisa/) | a origem do relatório pericial e as teorias da internet, com fonte |
| [`resultados/RESUMO.json`](resultados/RESUMO.json) e [`resultados/figuras/`](resultados/figuras/) | todos os números e os 12 gráficos |
| [`docs/REPLICAR.md`](docs/REPLICAR.md) | como refazer tudo, comando por comando |

Todo número sai de script (`ferramentas/`), de arquivo com sha256. Análise feita pelo Claude, a pedido do autor do canal.
