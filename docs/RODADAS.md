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

## Validação final · 29/10/2026, noite

- **Pedido:** uma última validação de tudo, antes de ele ajustar o roteiro.
- **Pipeline do zero:** da derivação ao relatório, com o mesmo `RESUMO.json`, as mesmas tabelas e os mesmos 11 gráficos, byte a byte; validação 16 de 16; testes e linguagem ok.
- **Acrescentado:** `resultados/tabelas/h17_curva_nacional.csv` e o gráfico `g12_a_noite.png` (as 346 versões nacionais da noite; nenhum total caiu), sem mudar nenhum número do `RESUMO.json`.
- **Comentários depois da coleta:** 56 novos nos 3 vídeos, nenhuma hipótese nova (`docs/COMENTARIOS.md`, último bloco).
- **Correções de texto:** a amostra de logs tem 13.221 seções (`REPLICAR`, `DADOS_LOCAIS`, `FONTES_DE_DADOS`); 79 prints de comentário, não 80.

## Rodada 3 · 30/10/2026 · a curva com zoom e as urnas idênticas

- **Pedido:** testar a curva da apuração com muito zoom em 2026, 2022 e 2018 (a linha do Flávio pareceria programada) e a mensagem de um seguidor sobre urnas idênticas, e deixar o roteiro mais direto (o relatório não muda de método).
- **Dados:** o boletim de urna de 2022, com a hora de chegada de cada seção (`dados/brutos/bweb2022`, hashes em `dados/MANIFESTO_RODADA3.json`); o histórico de 2018 copiado do projeto `apuracao-eleicoes-2026` (`dados/copias/historico2018`). ⚠️ O boletim público de 2018 não traz a hora de chegada: em 2018 a ordem é o encerramento da urna em horário de Brasília, e 2022 e 2026 também foram medidos assim para comparar igual (`resultados/RODADA3.json`).
- **H24, nova:** desmentida. A composição das seções (cada uma repetindo o próprio 1º turno, na mesma ordem) explica 99,5% dos passos da linha em 2026 e em 2022; os vales não têm ritmo; a ordem de chegada dentro da zona não muda o resultado; o total de votos nunca caiu. O limite: um desvio igual nos 2 turnos não apareceria neste teste.
- **H07 e H08, ampliadas:** boletins inteiros iguais são 54.304 em 2026, 31.016 em 2022 e 12.565 em 2018; o sorteio dá 44 mil, 23 mil e 8 mil. O real passa do sorteio nos 3 anos, menos em 2026, e a subida acompanha a queda dos brancos e nulos. Vereditos mantidos.
- **Validação:** 19 de 19. **Contagem:** 8 desmentidas, 10 não sustentadas, 4 compatíveis com as duas, 2 não testadas; o teto somado não muda (382.199, 8,63%).
