# As hipóteses do público sobre o 2º turno de 2026

> **Documento da rodada 0 (o plano antes dos testes).** Os vereditos, os números finais e o que mudou com a revisão estão no `RELATORIO.md` e no `docs/REVISAO_ADVERSARIAL.md`; onde este arquivo divergir deles, eles ganham.

**Rodada 0, 29/out/2026.** De onde vieram: (1) os 1.484 comentários e respostas dos vídeos 8 (mesários), 16 (as urnas do 2º turno) e 19 (as pesquisas e o resultado), lidos um a um depois de uma primeira passada por palavra-chave (`ferramentas/temas_comentarios.py`, contagem em `resultados/COMENTARIOS_TEMAS.json`); (2) o "Relatório Pericial Independente" divulgado em 28/10 (`docs/pesquisa/RELATORIO_PERICIAL_ORIGEM_E_ALEGACOES.md`); (3) o que circula na internet e na imprensa (`docs/pesquisa/TEORIAS_NA_INTERNET.md`). A sondagem (o que o dado por seção já mostra, sem regra e sem veredito) está em `resultados/SONDAGEM.json`, gerado por `ferramentas/sondagem.py`.

**Como ler cada hipótese.** A alegação vem na versão mais forte que ela admite. Para cada uma: o que a visão do **resultado legítimo** espera ver no dado, o que a visão da **fraude** espera ver, o teste que separa as duas, o controle e o espelho (o mesmo teste para o outro lado), o **teto do pior caso** (o máximo que ela poderia ter movido contra a diferença de 4.430.191 votos) e o que fecharia de vez. Nenhum número da sondagem é veredito; o veredito sai na rodada de execução, com as regras do `docs/PLANO.md`.

**O que já foi respondido em vídeo anterior** entra no fim do bloco com uma frase e a remissão (regra de continuidade): a conta dos 10 milhões e "a conta não fecha" (vídeos 16 e 19), a curva da noite "programada" (16), as pesquisas e as regras quebradas (19), os mesários do 1º turno (8).

---

## Bloco A · O "Relatório Pericial Independente"

### H01. Nas urnas encerradas até as 17h, o Flávio ganhou

| | |
|---|---|
| Alegação | Pelo carimbo de encerramento (`DT_ENCERRAMENTO`), nas urnas fechadas até as 17h o Flávio teve 52,39% dos válidos e quase 1,8 milhão de frente; nas fechadas depois, o Lula abriu 6,1 milhões. "A vitória foi fabricada exclusivamente nas urnas que encerraram depois do horário" |
| Quem levanta | o relatório (Joey Mannarino no X e no Instagram; o @carlosphyll no TikTok); nos comentários, o pedido de comparar as urnas que fecharam no horário com as que fecharam depois, *"na mesma localização"* |
| Legítimo espera | urna que fecha mais tarde é a de fila: seção grande, de cidade grande, de capital do Nordeste e de periferia. A diferença entre os grupos é do **lugar**, não da hora; quase todos os votos dessas urnas foram dados antes das 17h |
| Fraude espera | dentro do **mesmo local de votação**, as seções que fecharam depois votam mais no Lula do que as vizinhas que fecharam no horário, e o ganho do Lula do 1º para o 2º turno é maior nelas |
| Teste | (a) refazer a conta do relatório com o mesmo arquivo e achar o corte que dá 52,39%; (b) a mesma comparação **dentro do mesmo local de votação** e do mesmo município; (c) a variação de cada seção contra o próprio 1º turno; (d) os votos com hora depois das 17h no log de cada uma |
| Espelho | as seções que fecharam tarde em cidade onde o Flávio ganhou (Sul, interior de SP) |
| Sondagem | quase todas as urnas fecham depois das 17h00 (a urna só encerra depois do último eleitor da fila): pelo corte de 17h00, só 556 seções ficam no grupo "até"; pelo corte de 17h01, 129.491 seções com 49,11% para o Lula; o grupo "depois de 17h01" teve **34.035 votos com hora depois das 17h no log**. Nenhum corte reproduz ainda os 52,39%. Pela tabela do próprio relatório (cap. 2), o grupo "depois das 17h" tem 348.398 seções e **70,7% do comparecimento do dia inteiro**; o TSE registra 497.333 seções encerradas depois das 17h, então o grupo "até 17h00" do relatório não bate com o dado oficial (`docs/pesquisa/RELATORIO_PERICIAL_ORIGEM_E_ALEGACOES.md`, alegações 3 a 6). O arquivo usado por ele é o BWeb (`DT_ENCERRAMENTO`), que a coleta tem de baixar para refazer a conta igual |
| Teto | os votos dados depois das 17h: 34.393 (0,78% da diferença) |
| Fecharia | o log de cada urna (público) já fecha a pergunta de "quando o voto foi dado" |

### H02. "Mais de 2,5 milhões de eleitores estavam em urnas que passaram do horário"

| | |
|---|---|
| Alegação | o TSE diz 34 mil votos depois das 17h, mas 2,5 milhões de eleitores estavam em urnas abertas depois do horário |
| Legítimo espera | "estar numa urna aberta depois das 17h" não é "votar depois das 17h": o eleitor pode ter votado às 9h numa urna que fechou às 17h20 |
| Fraude espera | o número de votos com hora depois das 17h no log é muito maior que 34 mil, ou o log foi alterado e o comparecimento dessas seções sobe fora do padrão |
| Teste | votos por minuto no log, por seção; comparecimento dessas seções contra o 1º turno e contra 2022; os dois números lado a lado |
| Sondagem | votos com hora depois das 17h no log: **34.393** no Brasil (34.810 com o exterior), igual ao número do TSE; 13 depois das 19h |

### H03. 8,6 milhões liberados sem biometria, quase o dobro da diferença

| | |
|---|---|
| Alegação | 8.632.488 eleitores votaram sem biometria; o "colapso da biometria" basta para virar a eleição |
| Legítimo espera | a liberação sem digital é rotina (dedo gasto, idoso, digital não cadastrada) e cai dos dois lados, parecida com o 1º turno e com 2022 |
| Fraude espera | a parte sem digital sobe do 1º para o 2º turno onde o Lula ganhou; nas seções com mais liberação manual, o Lula ganha mais votos novos; liberação manual concentrada em horário sem fila |
| Teste | por seção: parte liberada sem digital no 2º turno contra o 1º turno, e a correlação com o ganho do Lula, com controle por idade do eleitorado e pelo mesmo local; espelho no Flávio |
| Sondagem | pelo log: 111,8 milhões pela digital, **8,62 milhões** liberados pelo mesário (7,24 milhões sem digital cadastrada); 5.472 liberações manuais depois das 17h. O campo do BWeb (`QT_ELEI_BIOM_SEM_HABILITACAO`) soma 8.632.488 (6,73%), igual ao relatório; **em 2022 foram 10.011.347 (8,06%)**, segundo o Jornal Razão, então "escala inédita" não se sustenta à primeira vista (a conferir no arquivo de 2022) |
| Teto | todas as liberações manuais com diferença de comportamento dos dois lados; o vídeo 16 já mediu que a liberação sem digital é igual dos dois lados |

### H04. 6.899 seções com mais de 90% para o Lula contra 384 do Flávio

| | |
|---|---|
| Alegação | "aberrações de unanimidade": a assimetria prova manipulação |
| Legítimo espera | as seções de quase unanimidade ficam nos mesmos lugares do 1º turno e de 2022 (aldeias, quilombos, interior do Nordeste), e a assimetria tem o tamanho que já tinha |
| Fraude espera | seções novas na lista, que no 1º turno ou em 2022 eram divididas |
| Teste | a lista de 2026 contra o 1º turno e contra 2022, seção a seção, e o local de votação de cada uma |
| Sondagem | 6.802 acima de 90% para o Lula e 368 para o Flávio (no Brasil, sem o exterior); o vídeo 16 já mostrou que 2022 teve 2.369 seções acima de 95% contra 1.686 em 2026 |

### H05. A lei de Benford reprova a votação

| | |
|---|---|
| Alegação | os dígitos dos votos por seção não seguem a lei de Benford |
| Legítimo espera | Benford não se aplica a votos por seção (as seções têm tamanho parecido, entre 200 e 400 eleitores, e o primeiro dígito fica preso nessa faixa); a mesma "reprovação" aparece no Flávio, em 2022 e em eleições sem contestação |
| Fraude espera | o desvio aparece só no Lula, ou só no 2º turno |
| Teste | o teste do relatório refeito, com o espelho (Flávio), o 1º turno, 2022, e o teste do segundo dígito |

### H06. Os boletins só foram liberados 72 horas depois

| | |
|---|---|
| Alegação | o TSE proclamou no domingo e só soltou os boletins na quarta |
| Teste | a linha do tempo dos arquivos públicos (o BU de cada seção na página de resultados desde a noite; o pacote em lote depois), com hora e hash; o vídeo 16 baixou os boletins de 26/10 em diante |
| Sondagem | meio certo: o pacote do 2º turno entrou no catálogo de Dados Abertos em 28/10, 11h07, mas o servidor do TSE mostra os mesmos arquivos desde 26/10, entre 15h e 18h31, e os arquivos por seção estavam públicos pelo menos desde 26/10, 7h30 (quando o projeto do vídeo 16 começou a baixar); o BU também foi afixado em cada seção e publicado no site de resultados em 25/10 |

### Os capítulos que não são dado eleitoral

O cap. 6 do relatório (o passaporte do Flávio "sete minutos depois", a PF, o Banco Master, Trump, a China) não é teste de urna: entra numa frase, com o que já foi conferido no projeto do vídeo 17 (o pedido da PF foi assinado às 21h16, sete minutos depois da confirmação matemática do TSE; a hora da decisão do Moraes não foi divulgada).

### Quem fez o relatório

Sem autor, sem código e sem arquivo publicado. Circula como imagens de 7 páginas (não há PDF); o post mais antigo que se prova é de 28/10 às 13h28 no X, de autor desconhecido (o post sumiu); o Joey Mannarino (comentarista americano pró-Trump, 732 mil seguidores no X) postou às 17h00 do mesmo dia com *"This was sent in by a follower, I don't take credit for the work"*. Única checagem direta: a Justiça Eleitoral, 28/10, 21h49. Detalhe e fontes no arquivo de pesquisa.

---

## Bloco B · As seções e as urnas

### H07. 106 urnas com zero voto para o Flávio

| | |
|---|---|
| Alegação | em 106 urnas o Lula levou os 14.860 votos e o Flávio teve zero; em parte delas o Flávio tinha voto no 1º turno |
| Quem levanta | levantamento divulgado no Painel da Folha, repercutido por vários sites e pelo Grok no X; o pedido mais repetido nos comentários do vídeo 16 (*"compare elas com o primeiro turno"*) |
| Legítimo espera | aldeias e comunidades com voto concentrado, as mesmas de 2018 e 2022; o espelho existe (seções com zero Lula no Sul) |
| Fraude espera | seções sem histórico de unanimidade, em lugar sem perfil para isso |
| Teste | as 106 com o local de votação (nome e endereço: escola indígena, aldeia, quilombo), o 1º turno de 2026, 2022 e 2018; o espelho |
| Sondagem | **106 seções, 14.860 votos** (confere); 30 no AM, 20 no MA, 16 no PA, 8 em RR; zero Lula: 4 seções. No 1º turno, das 60 que casaram pela chave, 56 tinham algum voto do Flávio (118 votos ao todo). Em **2022, 141 seções** deram zero para o Bolsonaro no 2º turno, e 2 deram zero para o Lula. ⚠️ 46 das 106 não casaram com o 1º turno pela chave: conferir antes de qualquer conta |
| Teto | 118 votos (o que o Flávio tinha nelas no 1º turno) |

### H08. Seções com resultado repetido

| | |
|---|---|
| Alegação | seções diferentes com o mesmo placar (ex.: Lula 543 e Flávio 567 nas duas) seriam "matematicamente impossíveis" |
| Legítimo espera | repetição de placar é comum com meio milhão de seções (o problema do aniversário) e fica no tamanho que o acaso dá |
| Fraude espera | mais repetições que o acaso, ou repetição em placares altos e raros, ou em blocos (mesmo município, mesma hora) |
| Teste | contar os placares repetidos e comparar com o esperado por sorteio (simulação com o tamanho e a divisão de cada seção); o mesmo para o Flávio e para 2022 |
| Sondagem | 41.133 placares aparecem em mais de uma seção; nenhum com os dois candidatos acima de 300 votos |

### H09. As urnas antigas votam diferente das novas

| | |
|---|---|
| Alegação | em 2022 a "live do argentino" (Fernando Cerimedo) disse que os modelos mais antigos da urna deram mais votos ao Lula; nos comentários, o pedido de comparar os modelos |
| Legítimo espera | o modelo da urna segue a região (as antigas ficam onde há mais seções antigas); dentro do mesmo local, o modelo não muda o voto |
| Fraude espera | dentro do mesmo local de votação (ou do mesmo município), as urnas de um modelo dão mais voto a um lado |
| Teste | o modelo de cada urna (está no log), comparação dentro do mesmo local, espelho, e 2022 se o dado existir |
| Dado | precisa do log de cada urna de novo (os brutos do vídeo 16 foram apagados); o leitor do log tem de ganhar o campo do modelo |

### H10. Urnas trocadas, levadas em carro de partido, "chegaram depois do resultado"

| | |
|---|---|
| Alegação | vídeos de urna em caminhonete adesivada, de urna substituída por "urna já com votos", de motorista que filma o painel adiantado |
| Legítimo espera | a troca de urna segue o procedimento de contingência (o log da urna nova registra), é rara (1.551, 0,28%, segundo a OEA) e o resultado da seção trocada fica como o das vizinhas |
| Fraude espera | seções com urna trocada votam diferente das vizinhas do mesmo local |
| Teste | as 1.996 seções com sinal de contingência no log contra as vizinhas; a hora de envio do BU contra o horário dos vídeos |
| Casos | Riacho Fundo II (DF): irregularidade real de transporte, apurada pelo TRE-DF, com os votos já transmitidos (TSE, 28/10) |

### H11. O boletim de papel não bate com o site do TSE

| | |
|---|---|
| Alegação | fiscais somaram boletins e o resultado era outro (Teixeira de Freitas, BA; "vídeo de uma cidade da Bahia"); boletim com hora 19h25; boletins "falsos" inseridos na totalização |
| Legítimo espera | o boletim de papel é o mesmo arquivo publicado, com a mesma assinatura digital; o município inteiro bate |
| Fraude espera | boletim publicado sem assinatura válida, ou diferente da foto do papel |
| Teste | (a) **verificar a assinatura digital de todos os boletins publicados** com a chave pública do TSE (o vídeo 16 não fez); (b) o caso de Teixeira de Freitas com todas as seções; (c) **convite público**: quem tem foto de boletim de papel manda, e o projeto compara com o arquivo da seção |

### H12. Seções criadas, cortadas ou "virtuais"

| | |
|---|---|
| Alegação | seções e urnas criadas fora do sistema, sem boletim; escolas "fantasmas"; 4.384 seções cortadas no 2º turno |
| Teste | a lista de seções do 1º e do 2º turno, uma a uma: as que só existem num turno, as sem boletim, as agregadas; local de votação de cada uma |

---

## Bloco C · Os eleitores

### H13. Mortos votaram

| | |
|---|---|
| Alegação | eleitores mortos continuam no cadastro e "votam" pela liberação do mesário (o "voto espírita") |
| Quem levanta | pedido direto nos comentários (*"você considerou se mortos votaram?"*, *"faz um vídeo se teve voto de pessoa falecida"*), relatos de parente falecido que "votou" em 2022, corrente de WhatsApp com cidades "onde até os mortos votaram" |
| Legítimo espera | o eleitorado muito idoso e o comparecimento dele ficam no tamanho da população viva daquela idade |
| Fraude espera | mais eleitores de 90 e de 100 anos que a população dessa idade, e esses eleitores "comparecendo" mais que o normal, com liberação pelo mesário |
| Teste | (a) eleitores por idade em cada município (`perfil_eleitorado`) contra a população por idade do Censo 2022 e da estimativa do IBGE; (b) **comparecimento por faixa de idade** (dado aberto do TSE) dos muito idosos, 1º e 2º turno e 2022; (c) espelho: os municípios onde o Flávio ganhou |
| O que não é público | o cruzamento nome a nome do cadastro com os óbitos dos cartórios (SIRC): pedido por LAI pronto |
| Casos | nenhum caso com nome e prova achado para o 2º turno de 2026 até 29/10 |

### H14. Cidades com mais eleitores ou votos que habitantes

| Teste | eleitorado e votos de cada município contra a população do Censo 2022 (16 anos ou mais) e a estimativa de 2025; a lista da corrente conferida nome a nome |
|---|---|

### H15. "Cheguei e já tinham votado por mim"

| | |
|---|---|
| Alegação | eleitores chegaram e a urna dizia que já tinham votado (casos de Campinas e Valinhos, e relatos nos comentários com zona e seção) |
| Legítimo espera | o aviso "eleitor já votou" é raro, cai em erro de digitação do título e repetição de tentativa, e aparece parecido no 1º turno e nos dois lados |
| Fraude espera | aviso concentrado em seções com muita liberação manual, e seguido de voto liberado pelo mesário |
| Teste | o aviso "O eleitor identificado já votou" no log de cada seção (hora, o que veio antes e depois), contra o 1º turno e por lado; as seções citadas nos comentários |
| Sondagem | **113.315 avisos em 73.044 seções** no 2º turno, ainda sem leitura do contexto |

### H16. O mesário vota o dia todo, não só depois das 17h

| | |
|---|---|
| Alegação | o "mesário pianista" age à tarde, quando a seção esvazia, com a própria digital |
| Teste | liberação manual por hora do dia e por seção, nos horários sem fila; a mesma digital de mesário liberando muitos eleitores seguidos; para onde foram os votos das seções com mais liberação manual (o pedido mais repetido no vídeo 19); 1º × 2º turno; o vídeo 8 é o molde |

---

## Bloco D · A totalização

### H17. A contagem secreta na sala-cofre, os 165.699 votos "sem origem" e o Flávio "perdendo votos" no painel

| Teste | os 2.554 arquivos da noite (curva oficial minuto a minuto): o total do Flávio nunca cai entre dois arquivos?; a soma por estado com o exterior fecha o total nacional em cada arquivo?; o boletim de cada seção é impresso antes de chegar ao TSE (H11) |
|---|---|

### H18. O código da urna troca o voto ("vote flip")

| | |
|---|---|
| Alegação | um gatilho no programa troca uma parte dos votos do Flávio para o Lula, depois de uma hora ou num percentual fixo, e o boletim já sai trocado |
| Legítimo espera | o teste de integridade (urnas sorteadas votando em cédula e na urna, filmado) não acha divergência; o resultado de cada seção segue o 1º turno de cada uma |
| Fraude espera | a troca deixa marca: o Flávio cai abaixo do 1º turno em seções onde nada mudou no comparecimento, o efeito aparece igual em todo tipo de seção, ou muda com o modelo da urna |
| Teste | o Flávio abaixo do próprio 1º turno, seção a seção, com o comparecimento; seções em que o Lula tinha zero no 1º turno; o modelo da urna (H09); os hashes do programa no log contra os da lacração; o relatório do teste de integridade |
| Limite | uma troca que imitasse o comportamento do eleitor não se separa por estatística; o que fecha é o teste de integridade e o voto impresso, que o Brasil não tem |

---

## Bloco E · O comportamento dos votos

| # | Hipótese | Teste | Sondagem |
|---|---|---|---|
| H19 | O Flávio perdeu votos em 6 estados e o Lula em nenhum | por UF e por seção, com o comparecimento | o Flávio caiu no AC, AM, AP, MA, RR e TO; o Lula não caiu em nenhum UF; o vídeo 19 mostrou que a abstenção subiu no Norte |
| H20 | Abstenção caindo no Nordeste, mesmo com a falta de ônibus | por seção e por zona, com o espelho do outro lado (a falta de ônibus em Salvador e Aracaju, que é fato confirmado) | já medido em parte no vídeo 19 |
| H21 | Compra de voto com benefício (Bolsa Família, Pé-de-Meia) | beneficiários por município contra o ganho do Lula, com 2022 como controle; é acusação de abuso de poder (o pedido de cassação), não de urna | o Poder360 publicou 2 milhões de votos a mais em locais com mais benefício |
| H22 | Onde tem mais celular e 5G, mais voto novo no Lula | cobertura da Anatel por município contra o ganho, com controle por tamanho de cidade e renda | um comentário diz ter achado correlação forte |
| H23 | Casos de cidade: Joaçaba (SC), Araruama e a Região dos Lagos (RJ) | os números de cada cidade, seção a seção, contra o 1º turno e 2022 | ainda não medido |

---

## Rodada 3 · H24. A linha do Flávio desce como se fosse programada

| | |
|---|---|
| Alegação | com muito zoom, a linha do Flávio sobe um pouco e cai, num ritmo de programa, como se um algoritmo o penalizasse |
| Legítimo espera | a porcentagem desce quando entra seção de lugar que vota mais no Lula; a mesma linha aparece se cada seção repetir o próprio 1º turno; 2022 e 2018 fazem igual |
| Fraude espera | passos que a composição não explica, ritmo fixo, e um desconto que cresce com a ordem de chegada dentro da mesma zona |
| Teste | a curva na ordem de chegada contra a curva prevista, nos passos a cada 100 seções; regularidade dos vales; a ordem de chegada contra o resultado dentro da zona; os totais nas versões gravadas ao vivo |

---

## O que é dado de pessoa e nunca vai para este repositório

Nome, foto e @ de quem comentou ficam fora (os prints moram no repositório de documentação do canal); aqui só a contagem e a paráfrase. Identificador de mesário e de eleitor que aparecer em log é codificado (HMAC) e nunca publicado.
