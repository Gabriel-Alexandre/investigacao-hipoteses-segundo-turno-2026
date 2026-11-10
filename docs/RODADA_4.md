# Rodada 4 · 10/11/2026 · seis hipóteses novas, saídas dos comentários e das mensagens depois do vídeo 20

**Pedido:** o episódio seguinte do Investigação Aberta, como conclusão do que foi testado, com as hipóteses que o público levantou depois do vídeo 20 e as mensagens que chegaram (três posts do X). Sem pré-registro (padrão de rodadas, como na 1 a 3). **Dados:** os mesmos de `dados/copias/` e `dados/derivados/`, nenhum arquivo novo e nenhuma rede. **Código:** `ferramentas/rodada_4.py` (resultados em `resultados/RODADA4.json`), `ferramentas/validacao_rodada_4.py` (14 de 14) e `ferramentas/graficos_rodada_4.py` (g17 a g21).

## O que já estava feito e não foi repetido

| Pedido do público | Onde já foi respondido |
|---|---|
| Ritmo entre votos, sequências rápidas demais | vídeo 16, A7: rajadas (10 votos seguidos com menos de 15 s) = 0,000% dos votos |
| Liberação sem digital por vencedor e por hora | vídeo 16, A7: 13,1% onde o Lula venceu e 12,3% onde o Flávio venceu |
| Urnas substituídas: as trocadas já tinham voto para o Lula? | sondagem da rodada 0 (300 urnas de contingência), H10; a **taxa entre os turnos** é nova (H30) |
| Fluxos de comparecimento | projeto do vídeo 19 |

O que **não** estava feito e entra aqui: H25 a H30.

## Os vereditos

| # | Hipótese | O fato que circula | A leitura de fraude | Pior caso |
|---|---|---|---|---|
| **H25** | Campos dos Goytacazes: *"o Lula ganhou todos os votos nulos, brancos, abstenções e dos outros"* | **meio certo**: a conta do post erra a abstenção, que **subiu** 3.895; o Lula ficou com 24.822 de 28.720 votos que podiam mudar (86%) | **não sustentada** | 1.389 votos que o Flávio perdeu (0,03% da diferença; 0,06% se todos tivessem ido ao outro lado) |
| **H26** | mais eleitores (ou votantes) que habitantes, em quantos municípios e quanto pesa | **certo**: 835 de 5.570 têm eleitorado maior que a população; 120 têm mais votantes que habitantes | **compatível com as duas** (mantém a H14) | 33.408 votos acima da população (0,75%) |
| **H27** | votos liberados sem a digital, seção a seção entre os turnos | **certo**: 12,3% no 1º turno, 12,5% no 2º | **não sustentada** | não se aplica |
| **H28** | seções da mesma escola, 1º contra 2º turno | **certo**: dentro da escola as seções divergem, e divergem igual nos dois turnos | **não sustentada** | não se aplica |
| **H30** | *"as urnas substituídas dobraram do 1º para o 2º turno e já tinham voto para o Lula"* | **errado**: caíram (0,46% das seções da amostra no 1º turno, 0,33% no 2º; o TSE conta 1.551 trocas no 2º, 0,31%) | **não sustentada** | não se aplica |
| **H29** | a queda da abstenção seção a seção contra o ganho do Lula (voto pelo ausente) | **certo**: a abstenção caiu 1,86 ponto no país | **não sustentada** | não se aplica |

**Contagem da série (29 linhas):** 8 desmentidas, 15 não sustentadas, 4 compatíveis com as duas (H14, H15, H18, H23), 2 não testadas (H21, H22). As 24 anteriores mais H25, H27, H28, H29 e H30 (as não sustentadas sobem de 10 para 15); a H26 é a extensão da H14 e não cria linha nova.

**Soma do pior caso:** 382.199 (8,63%) + 1.389 (H25) = **383.588 (8,66%)** (H27, H28, H29 e H30 não somam: nenhuma tem um caminho aberto com número). ⚠️ **Correção de método (nota N4):** o item H15 da soma usa o número de avisos *"eleitor já votou"* (113.315). Esse número é **o que o log enxerga**, não um teto: o aviso só aparece quando o eleitor de verdade vai votar. Um voto dado em nome de quem **não** apareceu não deixa aviso. Então **o 113.315 é um piso observável**, não o limite do mecanismo, e a soma de 8,66% **não é um teto para tudo que ficou aberto**. O que se pode dizer é que os testes que não dependem do aviso (H29, H27, H28) não acham a assinatura que esse mecanismo deixaria, e que o limite verdadeiro só sai do caderno de votação e da ata de cada seção, que os pedidos por LAI ao TRE-BA e ao TRE-PE pedem.

## H25 · Campos dos Goytacazes

**O post (@WagnerThomazoni, 03/11, 212 mil visualizações):** do 1º para o 2º turno em Campos, o Lula teria ficado com todos os votos nulos, brancos, abstenções e votos de Cury, Caiado, Renan e Zema, mais mil do Flávio, e a chance disso seria a de ganhar 1.300 vezes seguidas na Mega-Sena.

| | 1º turno | 2º turno | variação |
|---|---|---|---|
| Lula | 91.105 | 115.927 | +24.822 |
| Flávio | 160.859 | 159.470 | −1.389 |
| Abstenção | 80.008 | 83.903 | **+3.895** |
| Brancos + nulos | 18.294 | 11.163 | −7.131 |
| Cury + Caiado + Renan + Zema + outros | 20.200 | (saíram) | −20.200 |

- **Quem podia mudar de voto:** 20.200 (os outros candidatos) + 7.131 (brancos e nulos que sumiram) + 1.389 (o que o Flávio perdeu) = **28.720**. O Lula ficou com **24.822 = 86,4%**.
- **A abstenção não caiu em Campos: subiu 3.895.** O Lula não *"ganhou todas as abstenções"*; nesse ponto o post está errado.
- **A comparação certa:** entre as **221 cidades com mais de 100 mil eleitores**, o Lula ficou, na mediana, com **89,8%** de quem podia mudar; nas 25 do Rio, **97,5%**. Campos (86,4%) está **abaixo** da mediana do país e do estado (percentil 38,5).
- **O que é raro:** o Flávio **perder** voto entre os turnos. Aconteceu em **3 de 221** cidades grandes em 2026 (Macapá, −3,04%; Campos, −0,86%; Boa Vista, −0,38%) e em **0** em 2022 (nem o Bolsonaro nem o Lula perderam voto em nenhuma). Sem espelho em 2022: é um fato incomum que o dado público não explica sozinho.
- **A Mega-Sena:** a probabilidade do post não tem método, porque trata cada voto como um sorteio independente de 1 em 2. Uma conta assim dá um número minúsculo para qualquer cidade grande em qualquer eleição. Foi tratada como retórica, sem teste.
- **Veredito:** o fato é **meio certo**; a leitura de fraude (*"o Lula pegou tudo, só pode ser fraude"*) **não é sustentada** pela conversão do pool, que é típica. O resíduo, o Flávio perder 1.389 votos em Campos, **pesa 0,03% da diferença**.

## H26 · população × votos, refeita

**A pergunta (mensagem de 07/11 sobre o post de @ThePunisherUSA, 144 mil visualizações):** *"a base do Censo está no IBGE; quantos dos 5.000 municípios estão nessa situação e quanto isso representa de votos?"*

| Medida (2º turno de 2026, Censo 2022) | Município | Peso |
|---|---|---|
| **Eleitorado maior que a população** | **835** de 5.570 (15,0%) | 404.321 eleitores a mais que habitantes; os 835 têm 4.259.356 eleitores (2,7% do país) |
| **Votantes maiores que a população** | **120** (2,2%) | **33.408 votos acima da população = 0,75%** da diferença de 4.430.191 |
| Em 2022 (mesmo Censo, 2º turno) | 566 com eleitorado maior; 51 com votantes maiores | |
| Quem venceu nos 120 | Lula em 75, Flávio em 45 | |
| Quem venceu nos 835 | Lula em 550, Flávio em 285 | |

- **O caso da resposta ao post: Tibau (RN), 9.238 eleitores e 5.382 habitantes.** Confere nos dados. É o **3º maior** em razão eleitores/habitantes (1,72), atrás de Davinópolis (GO, 2,18) e Anhanguera (GO, 1,88).
- **A relação com o ganho do Lula é nula:** a correlação entre a razão votantes/habitantes e o ganho do Lula entre os turnos é **−0,07**.
- **Por que acontece:** quem mora fora (outra cidade ou o exterior) e mantém o título na cidade natal; o Censo 2022 conta moradores. É a explicação da visão legítima. A visão da fraude diz *"título de quem não existe"*, que **só se separa com o cadastro** (TSE) e o óbito (cartórios): o dado público não separa.
- **Veredito:** o fato é **certo**; a leitura de fraude fica **compatível com as duas**, como na H14. O número novo é o tamanho: 835 municípios e 33.408 votos.

## H27 · votos liberados sem a digital

Amostra sorteada de 11.972 seções com os dois turnos nos logs (11.853 pareadas). *"Sem a digital"* = liberação do mesário, sem digital ou outra forma.

- **12,29% dos votos no 1º turno, 12,51% no 2º.**
- **A seção que tinha mais no 1º turno tinha mais no 2º: correlação 0,959.** A liberação sem digital é uma característica da seção, não de uma noite.
- **A variação entre os turnos contra a variação do Lula, dentro do município:** inclinação **0,004** (intervalo de 95%: −0,020 a 0,027), igual a zero. No 1º turno a inclinação era 0,038 e no 2º, 0,010.
- **Por hora:** 12% a 13% o dia todo nos dois turnos; **uma hora destoa: as 17h do 2º turno, 15,9% contra 12,0% no 1º**. É a hora que mudou de regra (a prorrogação), com seções diferentes votando.
- **Veredito:** o fato é certo; a leitura de fraude é **não sustentada**.

## H28 · seções da mesma escola

477.101 seções em 72.376 escolas (30 votos ou mais de Lula e Flávio, e pelo menos duas seções por escola). Para cada seção, o quanto ela se afasta das **outras da mesma escola**, em unidades de erro esperado (z, o afastamento de uma seção, descontando o acaso).

| | 1º turno | 2º turno |
|---|---|---|
| Variância do z | 1,833 | 1,838 |
| Seções com z acima de 4 | 0,711% | 0,724% |
| Seções com z acima de 6 | 0,076% (365) | 0,072% (342) |

- A correlação do z entre os turnos é **0,87**. As seções fora do padrão do 2º turno são, em quase todos os casos, as mesmas do 1º.
- **Fora do padrão (z acima de 6) só no 2º turno e normais no 1º: 2 seções. O contrário: 4.**
- **Variância acima de 1** significa que as seções de uma escola **diferem mais do que o acaso** (bairros e andares diferentes). Ela é igual nos dois turnos.
- **Veredito:** o fato é certo; a leitura de fraude é **não sustentada**. **Limite:** não vê uma mudança aplicada de modo uniforme em todas as seções de uma escola.

## H29 · a abstenção que caiu e o voto pelo ausente

**A visão da fraude:** o mesário (ou quem controla a urna) vota pelos ausentes; então a queda da abstenção deveria aparecer **em dupla** com o ganho do Lula, seção a seção.

- **Abstenção nacional:** 21,08% no 1º e 19,22% no 2º em 2026 (queda de 1,86 ponto); 20,95% e 20,58% em 2022 (queda de 0,37).
- **A relação:** dentro do mesmo município, para cada ponto a mais de queda da abstenção, o Lula cresce **0,034 ponto a mais** (intervalo: 0,025 a 0,044), contra **0,029** em 2022 (0,018 a 0,039). **Indistinguíveis.**
- **Nas 5% de seções onde a abstenção mais caiu:** o Lula ganhou 7,53 pontos contra 7,00 na média geral (2026); em 2022, 2,06 contra 2,29.
- **Veredito:** o fato é certo (a abstenção caiu); a leitura de fraude é **não sustentada**. **Limite:** votos acrescentados de modo uniforme, em todas as seções, não deixam essa assinatura.

## H30 · as urnas substituídas

**O comentário (vídeo 20, 01/11):** as urnas substituídas *"já estavam com os votos para o Lula"* e *"em média, dobraram a quantidade do 1º para o 2º turno"*.

- **Elas não dobraram: caíram.** Na amostra sorteada de 11.972 seções, 55 (0,46%) tinham urna substituída no 1º turno e 40 (0,33%) no 2º. O documento de observação da Transparência Eleitoral Brasil, publicado pelo TSE em 05/11, conta **1.551 trocas em 499.248 urnas no 2º turno (0,31%)** e fala em *"redução na substituição de urnas"*. Para o 1º turno, uma reportagem registra 1.861 trocas (⚠️ uma fonte só, ainda sem o balanço oficial).
- **No log do 2º turno inteiro**, 2.000 seções (0,40%) marcam contingência; a conta do TSE (1.551) e a do log têm definições diferentes, e a amostra (0,33%) fica entre as duas.
- **Elas já tinham voto para o Lula?** Nas seções trocadas, a parte do Lula (entre Lula e Flávio) foi **1,86 ponto acima** do resto do município no 1º turno (erro padrão 0,91) e **2,61 pontos abaixo** no 2º (erro 1,19). Sem o padrão que o comentário descreve.
- **Veredito:** o fato é **errado** (caíram); a leitura de fraude é **não sustentada**. **Limite:** a amostra tem 40 e 55 seções trocadas, então o erro é grande; o que a conta separa é *"dobraram"*, que a amostra e o TSE desmentem.

## A objeção que o dado público não responde

Os comentários repetem que *"o truque estaria dentro da urna, e nenhum dado público o veria"*. É verdade em parte, e o projeto sempre disse isso (H18). O que a rodada 4 acrescenta é a **separação por tipo de prova**:

| Prova | Depende do dado público? | O que prova | O que não prova |
|---|---|---|---|
| Estatística do resultado (todas as hipóteses) | sim | a ausência de certas assinaturas | uma troca bem feita |
| Boletim de urna impresso × sistema do TSE × RDV (vídeo 16: 499.177 de 499.177) | sim | que o total publicado confere com o que cada urna imprimiu | que a urna contou certo |
| Teste de integridade (votos sorteados, digitados e comparados) | não (é feito no dia) | que o programa da urna conta certo naquela amostra | todas as urnas |
| Comprovante impresso, recontagem | não existe no Brasil | a contagem voto a voto | |
| Cadastro, caderno e ata da seção | só o TSE e os TREs têm | a identidade de quem votou | |

⬜ O conteúdo dos relatórios do TCU e da auditoria dos TREs **não foi lido nesta rodada** (os prazos são de novembro); entra só quando for lido e capturado.

## Revisão adversarial (da própria IA que codificou, sem leitor independente)

| Objeção | Resposta |
|---|---|
| H25 · *"o corte de 100 mil eleitores escolhe a comparação"* | refeito com outros cortes: mediana do Lula no pool de 93,5% (cidades com 20 mil eleitores ou mais, 1.359), 90,0% (50 mil, 496), 89,4% (200 mil, 102) e 91,0% (todas as 5.570); Campos (86,4%) fica abaixo da mediana em todos, no percentil 36 a 43 (conta feita fora do script principal; ⬜ não gravada em `RODADA4.json`) |
| H25 · *"o pool inclui os votos que o Flávio perdeu, então a conta é circular"* | o pool só soma o que **podia** mudar de mão; sem a parcela do Flávio, o Lula ficaria com 90% (24.822 de 27.331), mesmo resultado |
| H26 · *"Censo e cadastro medem coisas diferentes"* | por isso a leitura continua *compatível com as duas* |
| H27 · *"a amostra é de 11,9 mil seções"* | sorteio com semente fixa (2026) e a mesma amostra dos vídeos 16 e 20 |
| H28 · *"z de 4 não é fraude, é bairro"* | a medida é a mudança entre os turnos, e o 1º turno é o espelho |
| H29 · *"a mobilização do Lula é real"* | por isso o espelho de 2022 e o *dentro do município* |
| Todas · *"o dado vem do TSE"* | os totais conferem por 3 caminhos independentes (vídeo 16); a assinatura digital dos boletins **não** foi verificada (H11 e H17) |

## Validação por outro caminho: 14 de 14

`ferramentas/validacao_rodada_4.py`: Campos refeita somando as seções (6 números); o eleitorado e o comparecimento contra a população refeitos pelo detalhe de 999 mil linhas (835 e 120); a H29 refeita com a zona no lugar do município (0,023 contra 0,034, e 0,029 em 2022 com o mesmo método); a H27 refeita somando as horas; o z de 3 escolas feito à mão. ⚠️ A tolerância da H29 foi fixada em 0,02 **depois** de ver a diferença de 0,011; a conclusão (inclinação perto de zero e igual à de 2022) vale com os dois efeitos fixos.

⚠️ **Diferença de 1 a registrar:** os votantes acima da população em 2022 são 51 neste cálculo e 52 na rodada 1; o código de um município não casou no cruzamento novo.

## O que fica de fora

- **O post de @urna_2026:** a conta e o post não existem mais (404 em 10/11). Não há o que testar.
- **A fala do Lula no debate** (*"ameaçou o Flávio"*): é checagem de fala, não de dado; fica no projeto do debate.
- **O vídeo da urna tocando sem ninguém:** sem origem identificada nesta rodada.
- **Os relatos de uma seção específica:** só o caderno e a ata da seção respondem; ver os pedidos por LAI.
