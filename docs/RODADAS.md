# Rodadas

## Rodada 0 · 29/10/2026 · o levantamento

- **Pedido:** o vídeo 20 como a parte 3 da investigação do 2º turno, analisando as hipóteses do público (comentários dos vídeos 8, 16 e 19, o relatório que circulou e a internet), com prints dos comentários e trechos para o trailer.
- **Feito:** leitura dos 1.484 comentários e respostas; rastro do relatório pericial; levantamento das teorias da internet com fonte; 23 hipóteses com teste e controle; sondagem com as tabelas copiadas do vídeo 16 (`ferramentas/sondagem.py`).
- **O que a sondagem já viu (declarado para o caso de pré-registro):** os números de `resultados/SONDAGEM.json` (encerramento por hora, votos depois das 17h pelo log, liberação manual, seções acima de 90%, as 106 seções sem voto do Flávio e o 1º turno delas, 2022, os avisos "eleitor já votou", placares repetidos, quem perdeu voto por UF, urnas de contingência).
- **Não feito:** nenhum teste com regra, nenhum veredito.

## Rodada 1 · 29/10/2026 · os testes

- **Pedido:** fazer tudo (pesquisa, relatório, organização, repositório público, assets, documentação, roteiro v1, commit e push) e validar no fim.
- **Decisão de forma:** sem pré-registro, pelo padrão de rodadas (o autor não pediu pré-registro); a rodada 0 já tinha visto parte dos números, declarados acima.
- **Coleta:** 8 arquivos abertos do TSE, o Censo 2022 por idade (IBGE), os logs de uma amostra sorteada de 12.000 seções mais as seções especiais (sem nenhuma falha e sem bloqueio do TSE).
- **Feito:** um teste por hipótese (`ferramentas/analise.py`), validação por outro caminho (15 de 15), relatório e 11 gráficos.

## Rodada 2 · 29/10/2026 · a revisão adversarial

- **Pedido:** a revisão por três leitores (fraude, resultado legítimo, método), como no vídeo 17.
- **O que mudou:** a tabela inteira está em `docs/REVISAO_ADVERSARIAL.md`. O principal: o fuso do oeste do Amazonas (556 seções relidas), a separação entre o fato e o veredito, H14, H15, H18 e H23 com espelho e régua novos, H21 como não testado, os tetos refeitos e a soma do pior caso de todos os caminhos ainda abertos.
- **Validação:** 16 de 16.
- **Contagem final:** 7 desmentidas, 10 não sustentadas, 4 compatíveis com as duas, 2 não testadas.
