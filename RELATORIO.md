# Relatório: as hipóteses do público sobre o 2º turno de 2026

**Rodada 3, 30/out/2026.** Investigação Aberta, parte 3. Cada hipótese que o público levantou (comentários dos vídeos 8, 16 e 19, o "Relatório Pericial Independente" e as teorias da internet) foi testada pelas duas visões: a do resultado legítimo e a da fraude. A rodada 2 aplicou a revisão de três leitores (`docs/REVISAO_ADVERSARIAL.md`). Todo número sai de `ferramentas/analise.py` (`resultados/RESUMO.json`); os números centrais foram refeitos por outro caminho em `ferramentas/validacao_independente.py` (19 de 19 passaram).

## O que este projeto não consegue dizer

- Quem votou em cada seção: a lista é do TSE. Sem ela, nenhuma hipótese de voto no lugar de outra pessoa fecha caso a caso.
- Se um programa adulterado trocou votos imitando o eleitor: estatística não separa isso; o que fecha é o teste de integridade e o voto impresso.
- A assinatura digital de cada boletim não foi verificada nesta rodada.
- O comparecimento por idade do 2º turno de 2026 ainda não foi publicado pelo TSE.
- Os testes dos logs usam uma amostra sorteada de 12 mil seções (mais as seções especiais), porque os brutos completos do vídeo 16 foram apagados.
- A comparação dentro do mesmo local de votação e contra o 1º turno não pega uma fraude que atinja o lugar inteiro, ou os dois turnos do mesmo jeito.

## Os vereditos, em uma tabela

Duas respostas separadas: se o fato que circula está certo, e o que o dado diz sobre a leitura de fraude.

| # | Hipótese | O fato que circula | Veredito sobre a fraude | Critério | Teto contra a diferença de 4.430.191 votos |
|---|---|---|---|---|---|
| H01 | Nas urnas encerradas até as 17h, o Flávio ganhou | errado: o 52,39% só sai com o fuso trocado | **Desmentido** | comportamento | 34.424 votos depois das 17h (0,78% da diferença) |
| H02 | Mais de 2,5 milhões de eleitores votaram em urnas que passaram do horário | o número confere, mas é o comparecimento do dia inteiro | **Desmentido** | comportamento | 34.424 votos (0,78% da diferença) |
| H03 | 8,6 milhões liberados sem biometria, quase o dobro da diferença | certo: 8,6 milhões liberados pela digital do mesário | **Não sustentado** | comportamento | sem sinal para medir: a liberação manual não anda junto com o voto de nenhum lado |
| H04 | 6.899 seções com mais de 90% para o Lula contra 384 do Flávio | quase: 6.802 e 368 no Brasil | **Desmentido** | raridade | não se aplica: a assimetria é menor que a de 2022 |
| H05 | A lei de Benford reprova a votação | o relatório não mostrou número nenhum | **Não sustentado** | raridade | não se aplica |
| H06 | Os boletins ficaram 72 horas escondidos | meio certo: só a entrada no catálogo foi em 28/10 | **Desmentido** | arquivos | não se aplica |
| H07 | 106 urnas com zero voto para o Flávio | certo: 106 seções e 14.860 votos | **Não sustentado** | raridade | 118 votos (o que o Flávio teve nelas no 1º turno), menos de 0,01% da diferença |
| H08 | Seções com placar repetido seriam impossíveis | existem, e o boletim inteiro igual também (mensagem de um seguidor) | **Desmentido** | raridade | não se aplica |
| H09 | As urnas antigas votam diferente das novas | os quatro modelos (2013 a 2022) votaram em 2026 | **Não sustentado** | comportamento | não se aplica |
| H10 | Urnas trocadas e levadas em carro de partido | houve 1.996 trocas registradas e um caso real de transporte irregular | **Não sustentado** | comportamento | 246 votos pela diferença contra as vizinhas (menos de 0,01%); se todos os votos dessas seções fossem falsos, 502.317 |
| H11 | O boletim de papel não bate com o site do TSE | o caso que circulou (Teixeira de Freitas) está errado | **Não sustentado** | arquivos | não medido |
| H12 | Seções criadas, cortadas ou "virtuais" | errado: a lista de seções é a mesma nos dois turnos | **Desmentido** | arquivos | não se aplica |
| H13 | Mortos votaram | certo que há registros de mortos no cadastro: pelo menos 148.553 de centenários | **Não sustentado** | comportamento | se todo registro de centenário sem pessoa possível votasse: 148.553 votos, 3,35% da diferença (o comparecimento real de todos os centenários foi de 2.141 no 1º turno) |
| H14 | Cidades com mais eleitores ou votos que habitantes | certo: 120 municípios com mais votos que habitantes | **Compatível com as duas** | comportamento | 33.408 votos acima da população, somados nesses municípios (0,75%) |
| H15 | Cheguei e já tinham votado por mim | certo: o aviso apareceu 113.315 vezes | **Compatível com as duas** | comportamento | se cada aviso fosse um voto roubado: 113.315 votos (2,56%) |
| H16 | O mesário vota o dia todo, quando a seção esvazia | não: a liberação manual acompanha o movimento da seção | **Não sustentado** | comportamento | não se aplica |
| H17 | O Flávio "perdendo votos" no painel, os 165 mil "sem origem" e a sala-cofre | errado: o total do Flávio nunca caiu | **Desmentido** | arquivos | não se aplica |
| H24 | A linha do Flávio desce como se fosse programada (o zoom na curva) | certo que, com zoom, a porcentagem desce em degraus; o total de votos nunca desce | **Desmentido** | comportamento | não se aplica |
| H18 | O programa da urna troca o voto | certo que o Flávio caiu em 82.155 seções | **Compatível com as duas** | arquivos | se as quedas grandes do Flávio fossem votos trocados para o Lula: 49.110 votos de diferença (1,11%) |
| H19 | O Flávio perdeu votos em 6 estados e o Lula em nenhum | certo | **Não sustentado** | comportamento | não se aplica |
| H20 | A abstenção caiu no Nordeste, mesmo com a falta de ônibus | certo | **Não sustentado** | comportamento | não se aplica |
| H21 | Compra de voto com benefício social | não medido: o dado do benefício por município não entrou | **Não testado nesta rodada** | comportamento | não medido |
| H22 | Onde tem mais celular e 5G, mais voto novo no Lula | não medido | **Não testado nesta rodada** | comportamento | não medido |
| H23 | Joaçaba (SC), Araruama e a Região dos Lagos (RJ) | certo: a conta fecha | **Compatível com as duas** | comportamento | 3.025 votos (0,07%) |

Contagem: Não sustentado: 10; Desmentido: 8; Compatível com as duas: 4; Não testado nesta rodada: 2.

## O achado principal do relatório pericial

O "Relatório Pericial Independente" diz que o Flávio venceu nas urnas encerradas até as 17h. O número dele (52,39%) sai igual neste projeto só de um jeito: lendo a hora de encerramento no relógio local de cada estado, sem o fuso. Com isso, as 32.022 seções dos estados atrás de Brasília, que encerraram às 17h de Brasília, viram "urnas fechadas até 17h". Elas deram 59,72% ao Flávio e respondem por 1.443.643 dos 1.747.639 votos de frente do grupo. Com o fuso certo, as seções que fecham na hora ainda dão um pouco mais ao Flávio (50,99%), porque são as pequenas, sem fila; no mesmo local de votação, a seção que fechou tarde dá menos ao Lula, não mais. Os votos dados de fato depois das 17h foram 34.424, 0,78% da diferença.

## Hipótese por hipótese

### Bloco A · o relatório pericial

#### H01. Nas urnas encerradas até as 17h, o Flávio ganhou

**O fato que circula:** errado: o 52,39% só sai com o fuso trocado. **Veredito sobre a fraude: Desmentido** (critério: comportamento, que pesa mais).

O número do relatório sai igual (52,39% para o Flávio e 1.747.639 votos de frente) só quando se lê a hora de encerramento de cada urna no relógio local, sem acertar o fuso. Assim, as urnas dos estados atrás de Brasília (AC, AM, MT, MS, RO e RR), que fecharam às 15h ou às 16h no relógio delas, às 17h de Brasília, entram todas no grupo "até 17h": são 32.022 das 32.033 seções desses estados, com 59,72% para o Flávio e 1.443.643 votos de frente. Com o fuso certo, as 125.626 seções que fecharam até 17h00min59 de Brasília ainda deram 50,99% ao Flávio: são as seções pequenas, sem fila, que fecham na hora. O teste que separa é o do mesmo local de votação: a seção que fechou depois das 17h15 teve 1,25 ponto a menos de Lula que a vizinha que fechou antes (1.506 locais) e 0,14 ponto a menos de ganho desde o 1º turno (1.506 locais). E o grupo "depois das 17h" é o voto do dia inteiro: só 31.357 votos dele têm hora depois das 17h no log.

- Visão do resultado legítimo: urna que fecha mais tarde é a de fila; a diferença entre os grupos é de tamanho de seção, lugar e fuso, não da hora do voto.
- Visão da fraude: se a prorrogação tivesse acrescentado voto, as seções que fecharam tarde dariam mais ao Lula que as vizinhas do mesmo local; dão menos.
- Teto do pior caso: 34.424 votos depois das 17h (0,78% da diferença).
- O que fecharia: já fechado: o log de cada urna é público e tem a hora de cada voto.

#### H02. Mais de 2,5 milhões de eleitores votaram em urnas que passaram do horário

**O fato que circula:** o número confere, mas é o comparecimento do dia inteiro. **Veredito sobre a fraude: Desmentido** (critério: comportamento, que pesa mais).

Os 2,5 milhões são o comparecimento do dia inteiro das 8.848 seções que fecharam a partir das 17h16 (2.537.055 pelas tabelas do projeto). Votos com hora depois das 17h nessas seções: 5.663. No Brasil inteiro, o log dá 34.393 depois das 17h, o mesmo número do TSE, mais 31 no oeste do Amazonas, que fica 2 horas atrás de Brasília e a conta anterior tratou com 1 hora (556 seções relidas nesta rodada). Total: 34.424. Depois das 19h: 13.

- Visão do resultado legítimo: estar numa urna aberta depois das 17h não é votar depois das 17h.
- Visão da fraude: a conta mistura o eleitor do dia inteiro com o voto da prorrogação.
- Teto do pior caso: 34.424 votos (0,78% da diferença).
- O que fecharia: já fechado pelo log.

#### H03. 8,6 milhões liberados sem biometria, quase o dobro da diferença

**O fato que circula:** certo: 8,6 milhões liberados pela digital do mesário. **Veredito sobre a fraude: Não sustentado** (critério: comportamento, que pesa mais).

O número existe: 8.615.564 eleitores liberados pela digital do mesário no 2º turno, e mais 7.242.863 sem digital cadastrada, liberados pelo ano de nascimento (12,42% dos votos, somando os dois; o máximo teórico seria 15.858.427 votos, 3,58 vezes a diferença). Na amostra de 11.864 seções, essa parte foi de 12,29% no 1º turno para 12,50% no 2º. Dentro do mesmo município, a seção com mais liberação manual não deu mais voto ao Lula (correlação de 0,006), e a seção em que a liberação manual subiu do 1º para o 2º turno não deu mais ganho a ele (-0,009). O eleitorado com biometria foi de 75,8% em 2022 para 89,4% em 2026; o Jornal Razão somou cerca de 10 milhões de liberações em 2022 pela mesma conta (não recalculado aqui).

- Visão do resultado legítimo: a liberação sem a digital do eleitor é rotina (dedo gasto, idoso, digital não cadastrada), acontece o dia todo e cai dos dois lados.
- Visão da fraude: a fraude por liberação manual deixaria a parte manual subir onde o Lula cresceu; ela não sobe, nem no mesmo município.
- Teto do pior caso: sem sinal para medir: a liberação manual não anda junto com o voto de nenhum lado.
- O que fecharia: a lista de quem votou em cada seção, com o tipo de liberação (pedido ao TSE).

#### H04. 6.899 seções com mais de 90% para o Lula contra 384 do Flávio

**O fato que circula:** quase: 6.802 e 368 no Brasil. **Veredito sobre a fraude: Desmentido** (critério: raridade, que pesa no meio).

Pelo arquivo do TSE: 6.802 acima de 90% para o Lula e 368 para o Flávio, no Brasil (os 6.899 e 384 do relatório não saíram por nenhum recorte testado). Em 2022 foram 9.424 para o Lula e 199 para o Bolsonaro; em 2018, 14.957 para o Haddad e 1.192 para o Bolsonaro. Das seções do Lula acima de 90% em 2026, 99,6% já davam mais de 80% para ele em 2022.

- Visão do resultado legítimo: as seções de quase unanimidade são as mesmas de antes, nos mesmos lugares, e eram mais numerosas em 2018 e 2022.
- Visão da fraude: seriam seções novas na lista; não são.
- Teto do pior caso: não se aplica: a assimetria é menor que a de 2022.
- O que fecharia: já fechado pelo histórico de cada seção.

#### H05. A lei de Benford reprova a votação

**O fato que circula:** o relatório não mostrou número nenhum. **Veredito sobre a fraude: Não sustentado** (critério: raridade, que pesa no meio).

Desvio médio do 1º dígito: 0,079 no Lula e 0,075 no Flávio em 2026, 0,081 no Lula e 0,071 no Bolsonaro em 2022. Todos "reprovam" do mesmo jeito, porque o voto por seção fica preso no tamanho da seção (de 200 a 400 eleitores) e o 1º dígito não pode seguir Benford.

- Visão do resultado legítimo: o teste não serve para voto por seção; a prova é que ele reprova os dois candidatos e os dois anos.
- Visão da fraude: um desvio só de um lado, ou só em 2026, seria sinal; não há.
- Teto do pior caso: não se aplica.
- O que fecharia: já fechado.

#### H06. Os boletins ficaram 72 horas escondidos

**O fato que circula:** meio certo: só a entrada no catálogo foi em 28/10. **Veredito sobre a fraude: Desmentido** (critério: arquivos, que pesa menos (bater é o esperado nas duas visões)).

Os 28 pacotes do 2º turno entraram no catálogo de Dados Abertos em 28/10 11h07, mas o servidor do TSE dá a eles a data de 26/10 15h03 a 26/10 18h31; os arquivos de cada seção já estavam no site de resultados (o projeto do vídeo 16 começou a baixá-los em 26/10 às 7h30), e o boletim de cada seção foi impresso e afixado na própria seção em 25/10.

- Visão do resultado legítimo: o catálogo demorou, o dado não.
- Visão da fraude: a única parte verdadeira é a data de entrada no catálogo.
- Teto do pior caso: não se aplica.
- O que fecharia: já fechado pelas datas dos arquivos.

### Bloco B · as seções e as urnas

#### H07. 106 urnas com zero voto para o Flávio

**O fato que circula:** certo: 106 seções e 14.860 votos. **Veredito sobre a fraude: Não sustentado** (critério: raridade, que pesa no meio).

São 106 seções e 14.860 votos (30 no AM, 20 no MA, 16 no PA, 8 em RR); 46 têm nome de aldeia, escola indígena ou comunidade no local de votação. No 1º turno de 2026, 50 delas já não tinham voto do Flávio, e as outras 56 somavam 118 votos dele; pelo acaso, com a divisão do 1º turno, seriam esperadas 79 seções zeradas entre as que tinham voto do Flávio. O fenômeno foi maior antes: 141 seções sem voto do Bolsonaro em 2022 e 328 em 2018. O espelho existe: 4 seções sem voto do Lula, no RS e no PA. As que têm 100% para um candidato, sem branco nem nulo: 29 do Lula e 1 do Flávio em 2026; em 2022, 27 do Lula; em 2018, 42 do Haddad. Sorteando pelo próprio 1º turno de cada seção, seriam esperadas 151 a 189 seções sem voto do Flávio, mais do que as 106 que apareceram.

- Visão do resultado legítimo: voto concentrado em aldeia e comunidade, que se repete eleição após eleição e foi mais frequente em 2018 e 2022.
- Visão da fraude: a lista teria seções sem histórico de unanimidade; quase todas já votavam assim.
- Teto do pior caso: 118 votos (o que o Flávio teve nelas no 1º turno), menos de 0,01% da diferença.
- O que fecharia: já fechado pelo histórico; o TSE checou o mesmo caso no 1º turno.

#### H08. Seções com placar repetido seriam impossíveis

**O fato que circula:** existem, e o boletim inteiro igual também (mensagem de um seguidor). **Veredito sobre a fraude: Desmentido** (critério: raridade, que pesa no meio).

41.133 placares (Lula, Flávio) aparecem em mais de uma seção. Sorteando os votos de cada seção 20 vezes pela divisão Lula e Flávio dela no 1º turno, o acaso dá entre 42.494 e 42.693. Em 2022 foram 43.111. Nenhum placar se repete com os dois candidatos acima de 300 votos. Boletim inteiro (Lula, Flávio, branco e nulo iguais): 54.304 em 2026, 31.016 em 2022 e 12.565 em 2018. A subida acompanha a queda dos brancos e nulos (24,4 por seção em 2018, 12,1 em 2022, 8,3 em 2026), porque com menos branco e nulo há menos combinações possíveis: o sorteio dá 43.808 a 44.541 em 2026, 22.423 a 22.955 em 2022 e 7.597 a 7.989 em 2018. O real passa do sorteio nos 3 anos, e 2026 é o ano em que passa menos (23% acima, contra 37% em 2022 e 61% em 2018). O maior boletim repetido tem 393 votos.

- Visão do resultado legítimo: com meio milhão de seções, placar repetido é o esperado (é o problema do aniversário).
- Visão da fraude: a fraude por cópia deixaria repetição acima do acaso; não há.
- Teto do pior caso: não se aplica.
- O que fecharia: já fechado.

#### H09. As urnas antigas votam diferente das novas

**O fato que circula:** os quatro modelos (2013 a 2022) votaram em 2026. **Veredito sobre a fraude: Não sustentado** (critério: comportamento, que pesa mais).

O modelo de cada urna está no arquivo do TSE. O Lula ficou com 53,94% nas UE2013, 51,96% nas UE2015, 51,53% nas UE2020 e 51,83% nas UE2022, e o ganho desde o 1º turno ficou entre 6,46 e 6,60 pontos nos quatro. No mesmo local, a urna antiga (2013 e 2015) contra a nova: 0,13 ponto no ganho, em 933 locais.

- Visão do resultado legítimo: o modelo não muda o voto.
- Visão da fraude: um programa adulterado num modelo deixaria marca nele; não deixa.
- Teto do pior caso: não se aplica.
- O que fecharia: já fechado para a pergunta do modelo.

#### H10. Urnas trocadas e levadas em carro de partido

**O fato que circula:** houve 1.996 trocas registradas e um caso real de transporte irregular. **Veredito sobre a fraude: Não sustentado** (critério: comportamento, que pesa mais).

1.996 seções registraram troca de urna no log. No mesmo local, elas votaram como as vizinhas (-0,10 ponto no ganho do Lula, em 1.727 locais). O caso da caminhonete com adesivo no Riacho Fundo II (DF) é irregularidade real de transporte, apurada pelo TRE-DF, mas o boletim já tinha sido impresso e transmitido.

- Visão do resultado legítimo: a urna de contingência segue o procedimento e vota como as vizinhas.
- Visão da fraude: uma urna trocada com voto pronto votaria diferente das vizinhas; não vota.
- Teto do pior caso: 246 votos pela diferença contra as vizinhas (menos de 0,01%); se todos os votos dessas seções fossem falsos, 502.317.
- O que fecharia: a lista oficial de urnas substituídas, com o motivo (pedido ao TSE).

#### H11. O boletim de papel não bate com o site do TSE

**O fato que circula:** o caso que circulou (Teixeira de Freitas) está errado. **Veredito sobre a fraude: Não sustentado** (critério: arquivos, que pesa menos (bater é o esperado nas duas visões)).

Teixeira de Freitas inteira, 303 seções: Flávio 41.454, Lula 41.361, igual ao Aos Fatos (a soma de 3 boletins não é a cidade). O boletim de cada seção e o detalhe por seção dos dados abertos batem em 497.897 seções, sem uma diferença, mas isso é arquivo do TSE contra arquivo do TSE: bate nas duas visões. O que separa é a foto do boletim de papel e a assinatura digital de cada boletim, que esta rodada não verificou.

- Visão do resultado legítimo: o boletim afixado na seção é o mesmo arquivo publicado.
- Visão da fraude: um boletim trocado na totalização apareceria entre a foto do papel e o arquivo; nenhuma foto mostrou isso até agora.
- Teto do pior caso: não medido.
- O que fecharia: fotos de boletins de papel comparadas com o arquivo (convite público) e a verificação da assinatura de cada boletim.

#### H12. Seções criadas, cortadas ou "virtuais"

**O fato que circula:** errado: a lista de seções é a mesma nos dois turnos. **Veredito sobre a fraude: Desmentido** (critério: arquivos, que pesa menos (bater é o esperado nas duas visões)).

As mesmas 499.248 seções nos dois turnos, nenhuma só num deles; 41 não instaladas. 431 mudaram de local entre os turnos, e nelas o comparecimento subiu menos (0,85 ponto, contra 1,71 nas demais).

- Visão do resultado legítimo: a lista de seções é a mesma nos dois turnos.
- Visão da fraude: seção fantasma apareceria só num turno; não há.
- Teto do pior caso: não se aplica.
- O que fecharia: já fechado.

### Bloco C · os eleitores

#### H13. Mortos votaram

**O fato que circula:** certo que há registros de mortos no cadastro: pelo menos 148.553 de centenários. **Veredito sobre a fraude: Não sustentado** (critério: comportamento, que pesa mais).

O cadastro tem registros de pessoas que provavelmente já morreram: 297.977 eleitores com 100 anos ou mais em 2026, quando o Censo de 2022 contou 149.424 pessoas com 96 anos ou mais (as únicas que podem ter 100 em 2026); a diferença, 148.553, é o mínimo de registros sem pessoa viva possível. Em 2022 era parecido: 184.330 eleitores centenários para 37.814 centenários no Censo (4,9 vezes). Esses registros quase não votam: no 1º turno de 2026 compareceram 2.141 eleitores de 100 anos ou mais (0,72%; no 1º turno de 2022, 0,90%). Na faixa de 95 a 99 anos, o comparecimento foi de 1,60% no 1º turno de 2022 para 4,35% no 1º de 2026, mas, contado sobre quem tem biometria, ficou parado (16,3% e 15,6%): o que mudou foi o cadastro, que tirou registros, e não o voto. O TSE ainda não publicou o comparecimento por idade do 2º turno de 2026.

- Visão do resultado legítimo: o cadastro demora a tirar quem morreu, e esses registros não votam.
- Visão da fraude: a fraude usaria esses registros com a liberação do mesário; o comparecimento deles é de menos de 1 em 100, e a subida da faixa de 95 a 99 some quando se olha quem tem biometria.
- Teto do pior caso: se todo registro de centenário sem pessoa possível votasse: 148.553 votos, 3,35% da diferença (o comparecimento real de todos os centenários foi de 2.141 no 1º turno).
- O que fecharia: o cruzamento do cadastro com os óbitos dos cartórios (SIRC) e o comparecimento por idade do 2º turno, os dois com o TSE.

#### H14. Cidades com mais eleitores ou votos que habitantes

**O fato que circula:** certo: 120 municípios com mais votos que habitantes. **Veredito sobre a fraude: Compatível com as duas** (critério: comportamento, que pesa mais).

Em 120 municípios o comparecimento do 2º turno passou da população total do Censo 2022 (em 2022 tinham sido 52); o Lula venceu em 75 deles. Contra a população de 16 anos ou mais, foram 579 municípios em 2026 e 596 em 2022. Em 3 municípios do Piauí o Lula sozinho teve mais votos que habitantes: Novo Santo Antônio (Pi), 3.142 votos do Lula para 2.827 habitantes; Jatobá do Piauí (Pi), 4.787 votos do Lula para 4.494 habitantes; Aroeiras do Itaim (Pi), 3.104 votos do Lula para 2.690 habitantes; nos três, ele já tinha votação parecida no 1º turno. É o eleitor que mora fora e mantém o título na cidade de origem, mais comum em cidade pequena do Nordeste, e o próprio Censo pode ter contado menos gente nelas; quanto maior a razão entre votos e população, menor o ganho do Lula (correlação de -0,04). Na lista da corrente de WhatsApp, em nenhuma cidade o Lula teve mais votos que habitantes.

- Visão do resultado legítimo: título mantido na cidade natal e Censo que conta menos gente em cidade pequena; não é o lugar onde o Lula mais cresceu.
- Visão da fraude: o número de municípios acima da população mais que dobrou desde 2022, e três deles deram ao Lula mais votos que habitantes; é a parte a conferir com o cadastro.
- Teto do pior caso: 33.408 votos acima da população, somados nesses municípios (0,75%).
- O que fecharia: o recadastramento e a lista de quem votou nesses municípios, com o TSE.

#### H15. Cheguei e já tinham votado por mim

**O fato que circula:** certo: o aviso apareceu 113.315 vezes. **Veredito sobre a fraude: Compatível com as duas** (critério: comportamento, que pesa mais).

O aviso "o eleitor identificado já votou" aparece 113.315 vezes no 2º turno, em 73.044 seções. Na amostra, foi 0,833 por mil votos no 1º turno e 0,871 no 2º. Tirando as repetições (o mesmo eleitor tentando de novo em até 2 minutos), os avisos isolados foram de 1.861 para 2.174. Depois do aviso, o voto seguinte foi liberado sem a digital em 15,9% das vezes no 1º turno e 16,0% no 2º, contra 12,3% e 12,5% de todos os votos; e um voto liberado sem a digital em até 5 minutos veio depois de 17,5% dos avisos, contra 26,3% depois de um voto qualquer. Dentro do município, a seção com mais aviso não deu mais ganho ao Lula (correlação de -0,019). Casos com nome existem (Campinas e Valinhos) e estão com o TRE-SP.

- Visão do resultado legítimo: o aviso nasce de título digitado errado e de eleitor que tenta de novo; o que vem depois dele é igual ao que vem depois de um voto qualquer.
- Visão da fraude: o caso individual é real, os avisos isolados subiram do 1º para o 2º turno, e o voto que veio antes do aviso não aparece no arquivo público.
- Teto do pior caso: se cada aviso fosse um voto roubado: 113.315 votos (2,56%).
- O que fecharia: a ata e o caderno de cada caso, com o TRE, e a lista de quem votou.

#### H16. O mesário vota o dia todo, quando a seção esvazia

**O fato que circula:** não: a liberação manual acompanha o movimento da seção. **Veredito sobre a fraude: Não sustentado** (critério: comportamento, que pesa mais).

A parte dos votos liberados sem a digital do eleitor fica entre 12% e 13% de 8h a 16h, nos dois turnos. Às 17h do 2º turno ela sobe para 16,3%, mas são 765 votos na amostra inteira, os últimos da fila. A maior sequência de votos seguidos liberados pelo mesmo mesário tem mediana de 2 e máximo de 7 no 2º turno (no 1º, uma seção teve 13); nenhuma seção da amostra teve 10 ou mais seguidas no 2º turno.

- Visão do resultado legítimo: a liberação manual acompanha o movimento da seção.
- Visão da fraude: o mesário que vota por quem faltou deixaria rajadas de liberações seguidas na hora vazia; não há.
- Teto do pior caso: não se aplica.
- O que fecharia: a lista de quem votou em cada seção (pedido ao TSE).

### Bloco D · a totalização

#### H17. O Flávio "perdendo votos" no painel, os 165 mil "sem origem" e a sala-cofre

**O fato que circula:** errado: o total do Flávio nunca caiu. **Veredito sobre a fraude: Desmentido** (critério: arquivos, que pesa menos (bater é o esperado nas duas visões)).

Nas 346 versões nacionais do resultado gravadas ao vivo na noite, o total do Flávio nunca caiu (0 quedas), nem o do Lula (0), e a última dá Lula 64.256.232 e Flávio 59.826.041, o resultado proclamado. A maior distância entre duas versões nacionais foi de 01h54, a suspensão da divulgação depois da prorrogação. Os 165 mil "sem origem" foram uma comparação de painéis feita às 17h57, durante essa suspensão: o TSE e o Aos Fatos mostram que o painel nacional já tinha os votos do exterior e os dos estados não estavam atualizados do mesmo jeito (as versões gravadas aqui não têm os painéis de cada estado daquele minuto). A sala-cofre não conta voto: o boletim de cada seção é impresso na seção antes de chegar ao TSE (H11).

- Visão do resultado legítimo: a soma é aberta seção por seção, e o painel só cresceu.
- Visão da fraude: uma totalização mexida apareceria entre o boletim da seção e o total; os dois batem, mas isso também bateria numa fraude feita antes do boletim.
- Teto do pior caso: não se aplica.
- O que fecharia: já fechado para o painel; para a totalização, a assinatura dos boletins.

#### H24. A linha do Flávio desce como se fosse programada (o zoom na curva)

**O fato que circula:** certo que, com zoom, a porcentagem desce em degraus; o total de votos nunca desce. **Veredito sobre a fraude: Desmentido** (critério: comportamento, que pesa mais).

Com muito zoom, a porcentagem do Flávio desce em degraus: caiu em 230 e subiu em 101 das versões gravadas ao vivo, e o total de votos dele caiu 0 vezes. A curva foi refeita com cada seção repetindo o próprio 1º turno, na mesma ordem de chegada: a própria composição das seções explica 99,5% dos passos em 2026 e 99,5% em 2022 (em 2018, sem hora de chegada no arquivo público, pela hora de encerramento, 97,9%). O Bolsonaro desceu em 74,8% dos passos em 2022, mais que o Flávio (59,8%). Os vales não têm ritmo: o intervalo entre eles varia quase tanto quanto ao acaso (0,97 em 2026, 0,90 em 2022; um relógio daria 0), igual à curva prevista (1,01 e 0,99). Dentro da mesma zona, chegar mais tarde não muda o resultado da seção (correlação 0,002 em 2026, 0,025 em 2022).

- Visão do resultado legítimo: a porcentagem desce quando entra seção de lugar que já votava mais no Lula, sem nenhum voto sair.
- Visão da fraude: um programa deixaria passos que a composição não explica, ritmo fixo e desconto crescente com a ordem; nada disso aparece.
- Teto do pior caso: não se aplica.
- O que fecharia: já fechado para a curva; um programa agindo dentro da urna é a H18.

#### H18. O programa da urna troca o voto

**O fato que circula:** certo que o Flávio caiu em 82.155 seções. **Veredito sobre a fraude: Compatível com as duas** (critério: arquivos, que pesa menos (bater é o esperado nas duas visões)).

O Flávio ficou abaixo do próprio 1º turno em 82.155 seções; em 53,5% delas o comparecimento também caiu (em todas as seções, a queda do comparecimento aconteceu em 19,8%). Em 2022, o Lula, que liderou o 1º turno, ficou abaixo do próprio 1º turno em 88.885 seções. Fora do padrão, a conferir: as quedas grandes do Flávio com comparecimento estável (perdeu 10% ou mais de pelo menos 30 votos) foram 3.250 seções e 24.555 votos, contra 1.148 seções e 10.358 votos do Lula em 2022. O teste de integridade do 2º turno, com urnas sorteadas votando em papel e na urna, não achou divergência, mas é pequeno: 389 votos no TSE e 33 urnas em São Paulo. Os logs da amostra não registram nenhuma verificação de assinatura do programa sem sucesso.

- Visão do resultado legítimo: o voto segue o 1º turno de cada seção, o padrão geral é o de 2022 com os lados trocados, e a auditoria por amostra bateu.
- Visão da fraude: uma troca que imitasse o eleitor não se separa por estatística, e as quedas grandes do Flávio são mais que as do Lula em 2022.
- Teto do pior caso: se as quedas grandes do Flávio fossem votos trocados para o Lula: 49.110 votos de diferença (1,11%).
- O que fecharia: o teste de integridade em mais urnas e o voto impresso, que o Brasil não tem.

### Bloco E · o comportamento dos votos

#### H19. O Flávio perdeu votos em 6 estados e o Lula em nenhum

**O fato que circula:** certo. **Veredito sobre a fraude: Não sustentado** (critério: comportamento, que pesa mais).

Os 6 estados (AC, AM, AP, MA, RR, TO) tiveram queda do comparecimento entre os turnos: no AP, -8,08 pontos; em RR, -6,02; no AC, -5,65. Em 2022 aconteceu o mesmo com os lados trocados: o Lula perdeu votos em 4 estados (AC, AM, AP, RR) e o Bolsonaro em 0.

- Visão do resultado legítimo: menos gente foi votar onde o Flávio perdeu votos, e em 2022 o mesmo aconteceu com o Lula.
- Visão da fraude: a queda seria do Flávio sem queda de comparecimento; não é.
- Teto do pior caso: não se aplica.
- O que fecharia: já fechado.

#### H20. A abstenção caiu no Nordeste, mesmo com a falta de ônibus

**O fato que circula:** certo. **Veredito sobre a fraude: Não sustentado** (critério: comportamento, que pesa mais).

A abstenção caiu no Nordeste (18,39% para 16,49%), no Sudeste (22,70% para 20,27%) e no Sul (20,46% para 18,19%), e subiu no Norte. Em Salvador, onde faltou ônibus, foi de 20,14% para 15,77%. O vídeo 19 mostrou que a queda da abstenção entre os turnos não tem precedente; aqui ela não vem acompanhada de nenhuma marca de voto acrescentado (H03, H15, H16).

- Visão do resultado legítimo: a mobilização dos dois lados levou mais gente a votar em quase todo o país.
- Visão da fraude: a queda sem precedente é real; o que falta a ela é a marca de voto acrescentado.
- Teto do pior caso: não se aplica.
- O que fecharia: a lista de quem votou, com o TSE.

#### H21. Compra de voto com benefício social

**O fato que circula:** não medido: o dado do benefício por município não entrou. **Veredito sobre a fraude: Não testado nesta rodada** (critério: comportamento, que pesa mais).

Sem o dado do benefício, a renda do município (Censo 2022) serve só de aproximação, e as duas medidas apontam para lados diferentes: em pontos, o Lula cresceu mais nas cidades mais ricas (7,27 pontos nos 20% de maior renda, contra 4,45 nos 20% de menor renda); na parte do saldo, ficou com 102,1% dos votos novos nas mais pobres (o Flávio perdeu votos nelas) e 67,6% nas mais ricas. O pedido de cassação por abuso de poder é processo no TSE, fora do alcance do dado de urna.

- Visão do resultado legítimo: a renda não separa voto convencido de voto comprado.
- Visão da fraude: a parte do saldo que o Lula levou nas cidades pobres é a que a acusação espera; falta o dado do benefício.
- Teto do pior caso: não medido.
- O que fecharia: o pagamento do benefício por município (Portal da Transparência) e o processo de abuso de poder no TSE.

#### H22. Onde tem mais celular e 5G, mais voto novo no Lula

**O fato que circula:** não medido. **Veredito sobre a fraude: Não testado nesta rodada** (critério: comportamento, que pesa mais).

O dado de cobertura por município da Anatel não entrou nesta rodada. A renda (H21) já mostra que o Lula cresceu mais, em pontos, nas cidades mais ricas, que também são as mais conectadas; uma correlação com 5G sozinha não separaria as duas coisas.

- Visão do resultado legítimo: seria a renda e o tamanho da cidade.
- Visão da fraude: precisaria aparecer com a renda controlada.
- Teto do pior caso: não medido.
- O que fecharia: a cobertura da Anatel por município, com controle por renda e tamanho.

#### H23. Joaçaba (SC), Araruama e a Região dos Lagos (RJ)

**O fato que circula:** certo: a conta fecha. **Veredito sobre a fraude: Compatível com as duas** (critério: comportamento, que pesa mais).

Em Joaçaba, o Flávio cresceu 843 e o Lula 1.046, com 1.366 votos dos outros candidatos no 1º turno e 456 votantes a mais; o Lula ficou com 55,4% do saldo, exatamente a mediana dos municípios de SC (55,4%). Em Araruama, o Flávio cresceu 11 e o Lula 5.581, com 5.331 votos dos outros e 1.085 brancos e nulos a menos. Na Região dos Lagos inteira, o Lula ficou com 95,1% do saldo; nos 25 municípios do RJ em que o Flávio teve votação parecida no 1º turno (cerca de 64%), foi 85,0%. A diferença dá 3.025 votos do Lula acima do esperado.

- Visão do resultado legítimo: Joaçaba votou como o resto de SC, e onde o Flávio já tinha quase tudo no 1º turno ele tinha pouco para crescer.
- Visão da fraude: a Região dos Lagos deu ao Lula mais do saldo que as cidades parecidas do RJ, 3.025 votos acima.
- Teto do pior caso: 3.025 votos (0,07%).
- O que fecharia: pesquisa com o eleitor daquela região.

## O que já foi respondido antes

| Hipótese | Onde |
|---|---|
| A conta dos 10 milhões e "a conta não fecha" | vídeos 16 e 19 |
| As pesquisas e as regras quebradas (líder do 1º turno, Minas) | vídeo 19 |
| Mesários votando por quem faltou no 1º turno | vídeo 8 |

## A conclusão pelas duas visões

Com os pesos do vídeo 16 (o comportamento dos votos pesa mais, a raridade no meio e os arquivos das urnas menos):

| Critério | Hipóteses | O que o dado sustenta mais |
|---|---|---|
| Comportamento dos votos | H01, H02, H03, H09, H10, H13, H14, H15, H16, H24, H19, H20, H21, H22, H23 | o resultado legítimo; ficam de pé, a conferir, H14, H15, H23 |
| Raridade | H04, H05, H07, H08 | o resultado legítimo: unanimidade, dígitos e placares repetidos aparecem do mesmo jeito em 2018 e 2022 |
| Arquivos das urnas | H06, H11, H12, H17, H18 | o resultado legítimo, com peso pequeno: arquivo do TSE contra arquivo do TSE bateria nas duas visões; fica a conferir H18 |

Das 22 hipóteses testadas, 18 não mostraram a marca que a fraude deixaria no dado público (8 desmentidas e 10 não sustentadas), e 4 ficam compatíveis com as duas visões (H14, H15, H18, H23). O número do relatório pericial sai de um erro de fuso. Mesmo somando o pior caso de todos os caminhos que ainda podem ter acrescentado voto, um por cima do outro, dá 382.199 votos, 8,63% da diferença. O que continua sem resposta está dentro do TSE: a lista de quem votou em cada seção, o cadastro cruzado com os óbitos, a assinatura de cada boletim e um teste de integridade maior.

## O pior caso de cada caminho ainda aberto

| Caminho | Votos |
|---|---|
| votos depois das 17h, todos para um lado (H02) | 34.424 |
| registros de centenário sem pessoa possível, todos votando (H13) | 148.553 |
| votos acima da população nos municípios em que isso acontece (H14) | 33.408 |
| cada aviso "já votou" como um voto roubado (H15) | 113.315 |
| as quedas grandes do Flávio trocadas para o Lula (H18, cada voto trocado conta 2) | 49.110 |
| os votos do Lula acima do esperado na Região dos Lagos (H23) | 3.025 |
| urnas trocadas, pela diferença contra as vizinhas (H10) | 246 |
| o que o Flávio tinha nas 106 seções (H07) | 118 |
| **soma, um por cima do outro** | **382.199 (8,63% da diferença)** |

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
| votos depois das 17h nas seções sorteadas fora do oeste do AM (log lido de novo × tabela do vídeo 16) | 804 | 804 | tabela do vídeo 16 | sim |
| votos depois das 17h no oeste do AM (fuso tirado do próprio log) | 31 | 31 | RESUMO.json (fuso pela abertura no boletim) | sim |
| eleitorado 2026 | 158745463 | 158745463 | TSE, eleitorado apto em 2026 | sim |
| população do Censo 2022 | 203080756 | 203080756 | IBGE, Censo 2022 | sim |
| boletins inteiros repetidos em 2026 (votação por seção × boletim) | 54304 | 54304 | resultados/RODADA3.json | sim |
| seções sem voto do Flávio (votação por seção × boletim) | 106 | 106 | resultados/RODADA3.json | sim |
| a composição explica mais de 99% dos passos da curva de 2026 (blocos de 250 seções, sem rodada_3.py) | True | True | obtido 99.54% | sim |

## Reconciliação com o total proclamado

O detalhe por seção do TSE soma 124.082.273 votos nominais e 128.236.074 de comparecimento, o total proclamado. As tabelas por seção copiadas do vídeo 16 somam 124.081.475 nominais: os 798 que faltam são as 27 seções com voto no detalhe e sem boletim de urna nas tabelas (798 votos; 27 delas no exterior, apuradas pelo sistema de apuração). Nenhum teste muda por isso.

Fontes, método e como refazer: `docs/PLANO.md`, `docs/HIPOTESES.md`, `docs/FONTES_DE_DADOS.md` e `docs/REPLICAR.md`. Análise feita pelo Claude, a pedido do autor do canal.
