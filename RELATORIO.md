# Relatório: as hipóteses do público sobre o 2º turno de 2026

**Rodada 1, 29/out/2026.** Investigação Aberta, parte 3. Cada hipótese que o público levantou (comentários dos vídeos 8, 16 e 19, o "Relatório Pericial Independente" e as teorias da internet) foi testada pelas duas visões: o resultado foi legítimo, ou houve fraude. Todo número sai de `ferramentas/analise.py` (`resultados/RESUMO.json`); os números centrais foram refeitos por outro caminho em `ferramentas/validacao_independente.py` (15 de 15 passaram).

## O que este projeto não consegue dizer

- Quem votou em cada seção: a lista é do TSE. Sem ela, nenhuma hipótese de voto no lugar de outra pessoa fecha caso a caso.
- Se um programa adulterado trocou votos imitando o eleitor: estatística não separa isso; o que fecha é o teste de integridade e o voto impresso.
- A assinatura digital de cada boletim não foi verificada nesta rodada.
- O comparecimento por idade do 2º turno de 2026 ainda não foi publicado pelo TSE.
- Os testes dos logs usam uma amostra sorteada de 12 mil seções (mais as seções especiais), porque os brutos completos do vídeo 16 foram apagados.

## Os vereditos, em uma tabela

| # | Hipótese | Critério | Veredito | Teto contra a diferença de 4.430.191 votos |
|---|---|---|---|---|
| H01 | Nas urnas encerradas até as 17h, o Flávio ganhou | comportamento | **Desmentido** | 34.393 votos depois das 17h (0,78% da diferença) |
| H02 | Mais de 2,5 milhões de eleitores votaram em urnas que passaram do horário | comportamento | **Desmentido** | 0,78% da diferença |
| H03 | 8,6 milhões liberados sem biometria, quase o dobro da diferença | comportamento | **Não sustentado** | sem sinal para medir: a liberação manual não anda junto com o voto de nenhum lado |
| H04 | 6.899 seções com mais de 90% para o Lula contra 384 do Flávio | raridade | **Não sustentado** | não se aplica: a assimetria é menor que a de 2022 |
| H05 | A lei de Benford reprova a votação | raridade | **Não sustentado** | não se aplica |
| H06 | Os boletins ficaram 72 horas escondidos | arquivos | **Não sustentado** | não se aplica |
| H07 | 106 urnas com zero voto para o Flávio | raridade | **Não sustentado** | 118 votos (o que o Flávio teve nelas no 1º turno), menos de 0,01% da diferença |
| H08 | Seções com placar repetido seriam impossíveis | raridade | **Desmentido** | não se aplica |
| H09 | As urnas antigas votam diferente das novas | arquivos | **Não sustentado** | não se aplica |
| H10 | Urnas trocadas e levadas em carro de partido | arquivos | **Não sustentado** | todos os votos nominais dessas seções somam 502.317 |
| H11 | O boletim de papel não bate com o site do TSE | arquivos | **Não sustentado** | não medido |
| H12 | Seções criadas, cortadas ou "virtuais" | arquivos | **Desmentido** | não se aplica |
| H13 | Mortos votaram | comportamento | **Compatível com as duas** | se todo voto de 95 anos ou mais do 1º turno de 2026 fosse falso: 16.802 votos, 0,38% da diferença |
| H14 | Cidades com mais eleitores ou votos que habitantes | comportamento | **Não sustentado** | não se aplica |
| H15 | Cheguei e já tinham votado por mim | comportamento | **Compatível com as duas** | se todo aviso seguido de liberação manual fosse um voto roubado, cerca de 19.830 votos, 0,45% da diferença |
| H16 | O mesário vota o dia todo, quando a seção esvazia | comportamento | **Não sustentado** | não se aplica |
| H17 | A contagem na sala-cofre, os 165 mil votos "sem origem" e o Flávio "perdendo votos" no painel | arquivos | **Desmentido** | não se aplica |
| H18 | O programa da urna troca o voto | arquivos | **Não sustentado** | não medido |
| H19 | O Flávio perdeu votos em 6 estados e o Lula em nenhum | comportamento | **Não sustentado** | não se aplica |
| H20 | A abstenção caiu no Nordeste, mesmo com a falta de ônibus | comportamento | **Não sustentado** | não se aplica |
| H21 | Compra de voto com benefício social | comportamento | **Não sustentado** | não se aplica |
| H22 | Onde tem mais celular e 5G, mais voto novo no Lula | comportamento | **Não testado nesta rodada** | não medido |
| H23 | Joaçaba (SC), Araruama e a Região dos Lagos (RJ) | comportamento | **Compatível com as duas** | não se aplica |

Contagem: Não sustentado: 14; Desmentido: 5; Compatível com as duas: 3; Não testado nesta rodada: 1.

## O achado principal do relatório pericial

O "Relatório Pericial Independente" diz que o Flávio venceu nas urnas encerradas até as 17h. O número dele (52,39%) sai igual neste projeto só de um jeito: lendo a hora de encerramento no relógio local de cada estado, sem o fuso. Com isso, as 32.026 seções de AC, AM, MT, MS, RO e RR, que encerraram às 17h de Brasília (15h ou 16h no relógio delas), viram "urnas fechadas até 17h". Esses estados deram 59,72% ao Flávio e respondem por 1.443.513 dos 1.747.639 votos de frente do grupo. Os votos dados de fato depois das 17h foram 34.393, 0,78% da diferença.

## Hipótese por hipótese

### Bloco A · o relatório pericial

#### H01. Nas urnas encerradas até as 17h, o Flávio ganhou

**Veredito: Desmentido** (critério: comportamento, que pesa mais).

O número do relatório sai igual (52,39% para o Flávio e 1.747.639 votos de frente) só quando se lê a hora de encerramento de cada urna no relógio local, sem acertar o fuso. Assim, as urnas de AC, AM, MT, MS, RO e RR, que fecharam às 15h ou às 16h no horário local (17h em Brasília), entram todas no grupo "até 17h": são 32.026 das 32.037 seções desses estados, com 59,72% para o Flávio e 1.443.513 votos de frente. No mesmo local de votação, a seção que fechou depois das 17h15 não deu mais voto ao Lula que a vizinha que fechou antes: teve 1,25 ponto a menos de Lula no 2º turno (1.506 locais com os dois tipos de seção) e 0,14 ponto a menos de ganho desde o 1º turno (1.506 locais). E o grupo "depois das 17h" é o voto do dia inteiro: só 31.357 votos dele têm hora depois das 17h no log.

- Visão do resultado legítimo: urna que fecha mais tarde é a de fila, e a diferença entre os grupos é de lugar e de fuso, não de hora do voto.
- Visão da fraude: a separação por horário mostraria voto acrescentado na prorrogação; o dado mostra que o grupo nasceu de um erro de fuso.
- Teto do pior caso: 34.393 votos depois das 17h (0,78% da diferença).
- O que fecharia: já fechado: o log de cada urna é público e tem a hora de cada voto.

#### H02. Mais de 2,5 milhões de eleitores votaram em urnas que passaram do horário

**Veredito: Desmentido** (critério: comportamento, que pesa mais).

Os 2,5 milhões são o comparecimento do dia inteiro das 8.848 seções que fecharam a partir das 17h16 (2.537.055 pelas tabelas do projeto). Votos com hora depois das 17h nessas seções: 5.663. No Brasil inteiro, 34.393 depois das 17h e 13 depois das 19h, igual ao número do TSE.

- Visão do resultado legítimo: estar numa urna aberta depois das 17h não é votar depois das 17h.
- Visão da fraude: a conta mistura eleitor do dia inteiro com voto da prorrogação.
- Teto do pior caso: 0,78% da diferença.
- O que fecharia: já fechado pelo log.

#### H03. 8,6 milhões liberados sem biometria, quase o dobro da diferença

**Veredito: Não sustentado** (critério: comportamento, que pesa mais).

O número existe: 8.615.564 eleitores liberados pela digital do mesário no 2º turno, e mais 7.242.863 sem digital cadastrada, liberados pelo ano de nascimento (12,42% dos votos, somando os dois). Na amostra de 11.864 seções, essa parte foi de 12,29% no 1º turno para 12,50% no 2º. Dentro do mesmo município, a seção com mais liberação manual não deu mais voto ao Lula (correlação de 0,006), e a seção em que a liberação manual subiu do 1º para o 2º turno não deu mais ganho a ele (-0,009). Em 2022 foram cerca de 10 milhões, segundo a mesma conta feita pelo Jornal Razão.

- Visão do resultado legítimo: a liberação sem a digital do eleitor é rotina (dedo gasto, idoso, digital não cadastrada), acontece o dia todo e cai dos dois lados.
- Visão da fraude: a fraude por liberação manual deixaria a parte manual subir onde o Lula cresceu; ela não sobe.
- Teto do pior caso: sem sinal para medir: a liberação manual não anda junto com o voto de nenhum lado.
- O que fecharia: a lista de quem votou em cada seção, com o tipo de liberação (pedido ao TSE).

#### H04. 6.899 seções com mais de 90% para o Lula contra 384 do Flávio

**Veredito: Não sustentado** (critério: raridade, que pesa no meio).

Pelo arquivo do TSE: 6.802 acima de 90% para o Lula e 368 para o Flávio (no Brasil, sem o exterior). Em 2022 foram 9.424 para o Lula e 199 para o Bolsonaro; em 2018, 14.958 para o Haddad e 1.298 para o Bolsonaro. Das seções do Lula acima de 90% em 2026, 99,6% já davam mais de 80% para ele em 2022.

- Visão do resultado legítimo: as seções de quase unanimidade são as mesmas de antes, nos mesmos lugares, e eram mais numerosas em 2018 e 2022.
- Visão da fraude: seriam seções novas na lista; não são.
- Teto do pior caso: não se aplica: a assimetria é menor que a de 2022.
- O que fecharia: já fechado pelo histórico de cada seção.

#### H05. A lei de Benford reprova a votação

**Veredito: Não sustentado** (critério: raridade, que pesa no meio).

Desvio médio do 1º dígito: 0,079 no Lula e 0,075 no Flávio em 2026, 0,081 no Lula e 0,071 no Bolsonaro em 2022. Todos "reprovam" do mesmo jeito, porque o voto por seção fica preso no tamanho da seção (de 200 a 400 eleitores) e o 1º dígito não pode seguir Benford. O relatório não deu número nenhum para o teste.

- Visão do resultado legítimo: o teste não serve para voto por seção, e a prova é que ele reprova os dois candidatos e os dois anos.
- Visão da fraude: um desvio só de um lado, ou só em 2026, seria sinal; não há.
- Teto do pior caso: não se aplica.
- O que fecharia: já fechado.

#### H06. Os boletins ficaram 72 horas escondidos

**Veredito: Não sustentado** (critério: arquivos, que pesa menos (bater é o esperado nas duas visões)).

O pacote do 2º turno entrou no catálogo de Dados Abertos em 28/10, 11h07, mas o servidor do TSE mostra os mesmos arquivos desde 26/10, entre 15h e 18h31; os arquivos de cada seção estavam no site de resultados pelo menos desde 26/10, 7h30, quando o projeto do vídeo 16 começou a baixá-los; e o boletim de cada seção foi impresso e afixado na própria seção em 25/10.

- Visão do resultado legítimo: o catálogo demorou, o dado não.
- Visão da fraude: a única parte verdadeira é a data de entrada no catálogo.
- Teto do pior caso: não se aplica.
- O que fecharia: já fechado pelas datas dos arquivos.

### Bloco B · as seções e as urnas

#### H07. 106 urnas com zero voto para o Flávio

**Veredito: Não sustentado** (critério: raridade, que pesa no meio).

São 106 seções e 14.860 votos, como circulou (30 no AM, 20 no MA, 16 no PA, 8 em RR); 46 têm nome de aldeia, escola indígena ou comunidade no local de votação. No 1º turno de 2026, 50 delas já não tinham voto do Flávio, e as outras 56 somavam 118 votos dele. O mesmo fenômeno foi maior antes: 141 seções sem voto do Bolsonaro em 2022 e 328 em 2018. O espelho existe: 4 seções sem voto do Lula, no RS e no PA.

- Visão do resultado legítimo: voto concentrado em aldeia e comunidade, que se repete eleição após eleição e foi mais frequente em 2018 e 2022.
- Visão da fraude: a lista teria seções sem histórico de unanimidade; quase todas já votavam assim.
- Teto do pior caso: 118 votos (o que o Flávio teve nelas no 1º turno), menos de 0,01% da diferença.
- O que fecharia: já fechado pelo histórico; o TSE checou o mesmo caso no 1º turno.

#### H08. Seções com placar repetido seriam impossíveis

**Veredito: Desmentido** (critério: raridade, que pesa no meio).

41.133 placares (Lula, Flávio) aparecem em mais de uma seção. Sorteando os votos de cada seção 20 vezes pelo próprio voto dela no 1º turno, o acaso dá entre 41.840 e 42.002: há menos repetição do que o acaso daria. Em 2022 foram 43.111. Nenhum placar se repete com os dois candidatos acima de 300 votos.

- Visão do resultado legítimo: com meio milhão de seções, placar repetido é o esperado (é o problema do aniversário).
- Visão da fraude: a fraude por cópia deixaria repetição acima do acaso; há abaixo.
- Teto do pior caso: não se aplica.
- O que fecharia: já fechado.

#### H09. As urnas antigas votam diferente das novas

**Veredito: Não sustentado** (critério: arquivos, que pesa menos (bater é o esperado nas duas visões)).

O modelo de cada urna está no arquivo do TSE. O Lula ficou com 53,94% nas UE2013, 51,96% nas UE2015, 51,53% nas UE2020 e 51,83% nas UE2022, e o ganho desde o 1º turno ficou entre 6,46 e 6,60 pontos nos quatro modelos. No mesmo local, a urna antiga (2013 e 2015) contra a nova: 0,13 ponto no ganho, em 933 locais.

- Visão do resultado legítimo: o modelo não muda o voto.
- Visão da fraude: um programa adulterado num modelo deixaria marca nele; não deixa.
- Teto do pior caso: não se aplica.
- O que fecharia: já fechado para a pergunta do modelo.

#### H10. Urnas trocadas e levadas em carro de partido

**Veredito: Não sustentado** (critério: arquivos, que pesa menos (bater é o esperado nas duas visões)).

1.996 seções registraram troca de urna no log. No mesmo local, elas votaram como as vizinhas (-0,10 ponto no ganho do Lula, em 1.727 locais). O caso da caminhonete com adesivo no Riacho Fundo II (DF) é irregularidade real de transporte, apurada pelo TRE-DF, mas o boletim já tinha sido impresso e transmitido.

- Visão do resultado legítimo: a urna de contingência segue o procedimento e vota como as vizinhas.
- Visão da fraude: uma urna trocada com voto pronto votaria diferente das vizinhas; não vota.
- Teto do pior caso: todos os votos nominais dessas seções somam 502.317.
- O que fecharia: a lista oficial de urnas substituídas, com o motivo (pedido ao TSE).

#### H11. O boletim de papel não bate com o site do TSE

**Veredito: Não sustentado** (critério: arquivos, que pesa menos (bater é o esperado nas duas visões)).

Teixeira de Freitas inteira, 303 seções: Flávio 41.454, Lula 41.361, igual ao Aos Fatos (a soma de 3 boletins não é a cidade). O boletim de cada seção e o detalhe por seção dos dados abertos batem em 497.897 seções, sem uma diferença. A assinatura digital dos boletins não foi verificada nesta rodada.

- Visão do resultado legítimo: o boletim afixado na seção é o mesmo arquivo publicado.
- Visão da fraude: um boletim trocado na totalização apareceria como diferença entre a foto do papel e o arquivo; nenhum fiscal mostrou uma.
- Teto do pior caso: não medido.
- O que fecharia: fotos de boletins de papel comparadas com o arquivo (convite público) e a verificação da assinatura de cada boletim.

#### H12. Seções criadas, cortadas ou "virtuais"

**Veredito: Desmentido** (critério: arquivos, que pesa menos (bater é o esperado nas duas visões)).

As mesmas 499.248 seções nos dois turnos, nenhuma só num deles; 41 não instaladas. 431 mudaram de local entre os turnos, e nelas o comparecimento subiu menos (0,85 ponto, contra 1,71 nas demais).

- Visão do resultado legítimo: a lista de seções é a mesma nos dois turnos.
- Visão da fraude: seção fantasma apareceria só num turno; não há.
- Teto do pior caso: não se aplica.
- O que fecharia: já fechado.

### Bloco C · os eleitores

#### H13. Mortos votaram

**Veredito: Compatível com as duas** (critério: comportamento, que pesa mais).

Há mortos no cadastro: o eleitorado de 2026 tem 297.977 eleitores com 100 anos ou mais, e o Censo de 2022 contou 149.424 pessoas com 96 anos ou mais (as únicas que podem ter 100 em 2026); em 1.068 municípios há mais eleitores centenários que pessoas que poderiam ser centenárias. Mas eles quase não votam: no 1º turno de 2026 compareceram 2.141 eleitores de 100 anos ou mais (0,72%), contra 2.078 no 2º turno de 2022 (1,13%). Fora do padrão, a conferir: na faixa de 95 a 99 anos o comparecimento foi de 2,14% no 2º turno de 2022 para 4,35% no 1º turno de 2026 (14.661 votos). O TSE ainda não publicou o comparecimento por idade do 2º turno de 2026.

- Visão do resultado legítimo: o cadastro demora a tirar quem morreu, e esses registros não votam.
- Visão da fraude: a fraude usaria esses registros com a liberação do mesário; o comparecimento de quem tem 100 anos ou mais é de menos de 1 em 100, e o salto da faixa de 95 a 99 é a parte a conferir.
- Teto do pior caso: se todo voto de 95 anos ou mais do 1º turno de 2026 fosse falso: 16.802 votos, 0,38% da diferença.
- O que fecharia: o cruzamento do cadastro com os óbitos dos cartórios (SIRC) e o comparecimento por idade do 2º turno, os dois com o TSE.

#### H14. Cidades com mais eleitores ou votos que habitantes

**Veredito: Não sustentado** (critério: comportamento, que pesa mais).

Em 579 municípios o comparecimento do 2º turno passou da população que teria 16 anos ou mais em 2026 (o Lula venceu em 393). Em 2022 o mesmo aconteceu em 596 municípios. É o eleitor que mora fora e mantém o título na cidade de origem. Na lista da corrente de WhatsApp, em nenhuma cidade o Lula teve mais votos que habitantes.

- Visão do resultado legítimo: título mantido na cidade natal, o mesmo de 2022.
- Visão da fraude: seria um salto em 2026; o número é parecido com o de 2022.
- Teto do pior caso: não se aplica.
- O que fecharia: o recadastramento por município, com o TSE.

#### H15. Cheguei e já tinham votado por mim

**Veredito: Compatível com as duas** (critério: comportamento, que pesa mais).

O aviso "o eleitor identificado já votou" aparece 113.315 vezes no 2º turno, em 73.044 seções. Na amostra, foi 0,833 por mil votos no 1º turno e 0,871 no 2º; o aviso seguido de um voto liberado pelo mesário em até 5 minutos foi de 12,7% para 17,5%. Dentro do município, a seção com mais aviso não deu mais ganho ao Lula (correlação de -0,019). Casos com nome existem (Campinas e Valinhos) e estão com o TRE-SP.

- Visão do resultado legítimo: o aviso nasce de título digitado errado e de eleitor que tenta de novo; é raro e igual nos dois turnos.
- Visão da fraude: o caso individual é real, e a subida dos avisos seguidos de liberação manual é a parte a conferir.
- Teto do pior caso: se todo aviso seguido de liberação manual fosse um voto roubado, cerca de 19.830 votos, 0,45% da diferença.
- O que fecharia: a ata e o caderno de cada caso, com o TRE.

#### H16. O mesário vota o dia todo, quando a seção esvazia

**Veredito: Não sustentado** (critério: comportamento, que pesa mais).

A parte dos votos liberados sem a digital do eleitor fica entre 12% e 13% em quase todas as horas, nos dois turnos. A maior sequência de votos seguidos liberados pelo mesmo mesário tem mediana de 2 e máximo de 7 no 2º turno; nenhuma seção da amostra teve 10 ou mais seguidas.

- Visão do resultado legítimo: a liberação manual acompanha o movimento da seção.
- Visão da fraude: o mesário que vota por quem faltou deixaria rajadas de liberações seguidas na hora vazia; não há.
- Teto do pior caso: não se aplica.
- O que fecharia: a lista de quem votou em cada seção (pedido ao TSE).

### Bloco D · a totalização

#### H17. A contagem na sala-cofre, os 165 mil votos "sem origem" e o Flávio "perdendo votos" no painel

**Veredito: Desmentido** (critério: arquivos, que pesa menos (bater é o esperado nas duas visões)).

Nas 346 versões nacionais do resultado gravadas ao vivo na noite, o total do Flávio nunca caiu (0 quedas), nem o do Lula (0). A última versão dá Lula 64.256.232 e Flávio 59.826.041, o resultado proclamado. O boletim de cada seção é impresso na seção antes de chegar ao TSE (H11).

- Visão do resultado legítimo: a soma é aberta seção por seção.
- Visão da fraude: uma totalização mexida apareceria entre o boletim da seção e o total; os dois batem.
- Teto do pior caso: não se aplica.
- O que fecharia: já fechado pelo boletim de cada seção.

#### H18. O programa da urna troca o voto

**Veredito: Não sustentado** (critério: arquivos, que pesa menos (bater é o esperado nas duas visões)).

O Flávio ficou abaixo do próprio 1º turno em 82.155 seções (e o Lula em 9.575); em 53,5% delas o comparecimento também caiu. O teste de integridade do 2º turno, com urnas sorteadas votando em papel e na urna, não achou divergência. Os logs da amostra não registram nenhuma verificação de assinatura do programa sem sucesso.

- Visão do resultado legítimo: o voto segue o 1º turno de cada seção, e a auditoria por amostra bateu.
- Visão da fraude: uma troca perfeita, que imitasse o eleitor, não se separa por estatística; é o limite deste teste.
- Teto do pior caso: não medido.
- O que fecharia: o teste de integridade em mais urnas e o voto impresso, que o Brasil não tem.

### Bloco E · o comportamento dos votos

#### H19. O Flávio perdeu votos em 6 estados e o Lula em nenhum

**Veredito: Não sustentado** (critério: comportamento, que pesa mais).

Os 6 estados (AC, AM, AP, MA, RR, TO) tiveram queda do comparecimento entre os turnos: no AP, -8,08 pontos; em RR, -6,02; no AC, -5,65. O comparecimento caiu em 9 estados, todos no Norte e no meio-norte.

- Visão do resultado legítimo: menos gente foi votar onde o Flávio perdeu votos.
- Visão da fraude: a queda seria do Flávio sem queda de comparecimento; não é.
- Teto do pior caso: não se aplica.
- O que fecharia: já fechado.

#### H20. A abstenção caiu no Nordeste, mesmo com a falta de ônibus

**Veredito: Não sustentado** (critério: comportamento, que pesa mais).

A abstenção caiu no Nordeste (18,39% para 16,49%), no Sudeste (22,70% para 20,27%) e no Sul (20,46% para 18,19%), e subiu no Norte. Em Salvador, onde faltou ônibus, foi de 20,14% para 15,77%. O vídeo 19 mostrou que a queda da abstenção entre os turnos não tem precedente.

- Visão do resultado legítimo: a mobilização dos dois lados levou mais gente a votar em quase todo o país.
- Visão da fraude: a queda sem precedente é real; o que ela não tem é marca de voto acrescentado (H03, H15, H16).
- Teto do pior caso: não se aplica.
- O que fecharia: a lista de quem votou, com o TSE.

#### H21. Compra de voto com benefício social

**Veredito: Não sustentado** (critério: comportamento, que pesa mais).

O Lula cresceu mais nas cidades mais ricas: 7,27 pontos entre o 1º e o 2º turno nos 20% de municípios de maior renda, contra 4,45 nos 20% de menor renda. O pedido de cassação por abuso de poder é processo no TSE, fora do alcance do dado de urna.

- Visão do resultado legítimo: o crescimento veio mais de onde o benefício pesa menos.
- Visão da fraude: a compra de voto com benefício faria o Lula crescer mais nas cidades pobres; foi o contrário.
- Teto do pior caso: não se aplica.
- O que fecharia: o processo de abuso de poder no TSE.

#### H22. Onde tem mais celular e 5G, mais voto novo no Lula

**Veredito: Não testado nesta rodada** (critério: comportamento, que pesa mais).

O dado de cobertura por município da Anatel não entrou nesta rodada. A renda (H21) já mostra que o Lula cresceu mais nas cidades mais ricas, que também são as mais conectadas, então uma correlação com 5G sozinha não separaria as duas coisas.

- Visão do resultado legítimo: seria a renda e o tamanho da cidade.
- Visão da fraude: precisaria aparecer com a renda controlada.
- Teto do pior caso: não medido.
- O que fecharia: a cobertura da Anatel por município, com controle por renda e tamanho.

#### H23. Joaçaba (SC), Araruama e a Região dos Lagos (RJ)

**Veredito: Compatível com as duas** (critério: comportamento, que pesa mais).

A conta fecha. Em Joaçaba, o Flávio cresceu 843 e o Lula 1.046, com 1.366 votos dos outros candidatos e 456 eleitores a mais. Em Araruama, o Flávio cresceu 11 e o Lula 5.581, com 5.331 votos dos outros e 1.085 brancos e nulos a menos. Nos 7 municípios da Região dos Lagos, o Lula ganhou 28.624 votos e o Flávio 1.476, com 27.127 votos dos outros no 1º turno.

- Visão do resultado legítimo: o eleitor dos outros candidatos votou no Lula naquela região.
- Visão da fraude: é o mesmo fora do padrão do vídeo 19: o Lula com quase todos os votos que estavam em disputa.
- Teto do pior caso: não se aplica.
- O que fecharia: pesquisa com o eleitor daquela região.

## O que já foi respondido antes

| Hipótese | Onde |
|---|---|
| A conta dos 10 milhões e "a conta não fecha" | vídeos 16 e 19 |
| A curva da noite "programada" | vídeo 16 |
| As pesquisas e as regras quebradas (líder do 1º turno, Minas) | vídeo 19 |
| Mesários votando por quem faltou no 1º turno | vídeo 8 |

## A conclusão pelas duas visões

Com os pesos do vídeo 16 (o comportamento dos votos pesa mais, a raridade no meio e os arquivos das urnas menos):

| Critério | Hipóteses | O que o dado sustenta mais |
|---|---|---|
| Comportamento dos votos | H01, H02, H03, H13 a H16, H19 a H23 | o resultado legítimo; ficam de pé, a conferir, o cadastro com mortos (sem voto em escala), o salto do comparecimento de 95 a 99 anos, a subida dos avisos "já votou" seguidos de liberação manual e o Lula com quase todos os votos em disputa (vídeo 19) |
| Raridade | H04, H05, H07, H08 | o resultado legítimo: unanimidade, dígitos e placares repetidos aparecem do mesmo jeito em 2018 e 2022 |
| Arquivos das urnas | H06, H09 a H12, H17, H18 | o resultado legítimo, com peso pequeno (os arquivos bateriam nas duas visões) |

Nenhuma das 23 hipóteses mostrou a marca que a fraude deixaria no dado público. O relatório pericial nasce de um erro de fuso. O que continua sem resposta está dentro do TSE: a lista de quem votou em cada seção, o cruzamento do cadastro com os óbitos e a assinatura de cada boletim.

## Validação independente

| Checagem | Obtido | Esperado | Fonte | Passou |
|---|---|---|---|---|
| Lula no 2º turno (votação por seção dos dados abertos) | 64256232 | 64256232 | resultado proclamado pelo TSE | sim |
| Flávio no 2º turno (votação por seção dos dados abertos) | 59826041 | 59826041 | resultado proclamado pelo TSE | sim |
| seções sem voto do Flávio | 106 | 106 | RESUMO.json H07 | sim |
| votos do Lula nessas seções | 14860 | 14860 | RESUMO.json H07 | sim |
| seções sem voto do Lula | 4 | 4 | RESUMO.json H07 | sim |
| votos do Flávio no 1º turno nessas seções | 118 | 118 | RESUMO.json H07 | sim |
| seções com mais de 90% para o Lula | 6802 | 6802 | RESUMO.json H04 | sim |
| seções com mais de 90% para o Flávio | 368 | 368 | RESUMO.json H04 | sim |
| placares repetidos (Lula, Flávio) | 41133 | 41133 | RESUMO.json H08 | sim |
| Teixeira de Freitas, Flávio | 41454 | 41454 | Aos Fatos, 28/10 | sim |
| Teixeira de Freitas, Lula | 41361 | 41361 | Aos Fatos, 28/10 | sim |
| Flávio nos 6 estados com fuso (%) | 59.72 | 59.72 | RESUMO.json H01 (só as seções do grupo até 17h, que são quase todas) | sim |
| votos depois das 17h nas 12 mil seções sorteadas (log lido de novo × tabela do vídeo 16) | 804 | 804 | tabela do vídeo 16 | sim |
| eleitorado 2026 | 158745463 | 158745463 | TSE, eleitorado apto em 2026 | sim |
| população do Censo 2022 | 203080756 | 203080756 | IBGE, Censo 2022 | sim |

## Reconciliação com o total proclamado

O detalhe por seção do TSE soma 124.082.273 votos nominais e 128.236.074 de comparecimento, o total proclamado. As tabelas por seção copiadas do vídeo 16 somam 124.081.475 nominais: os 798 que faltam cabem nas 86 seções cujo boletim não saiu da urna (recuperador de dados, totalização ou sistema de apuração), que têm 4.508 votos nominais. Nenhum teste muda por isso.

Fontes, método e como refazer: `docs/PLANO.md`, `docs/HIPOTESES.md`, `docs/FONTES_DE_DADOS.md` e `docs/REPLICAR.md`. Análise feita pelo Claude, a pedido do autor do canal.
