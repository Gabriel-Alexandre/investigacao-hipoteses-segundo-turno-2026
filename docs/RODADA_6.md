# Rodada 6 · 24/11/2026 · a resposta do TSE, a negativa do TRE-BA e o "mesmo mesário em 2 cidades"

**Pedido:** o episódio seguinte do Investigação Aberta, com a resposta do TSE ao pedido por Lei de Acesso à Informação (protocolo 82032521133805, resposta de 19/11/2026), a do TRE-BA (protocolo 82034321135124, 24/11/2026) e as hipóteses novas que chegaram de 17 a 24/11 pelos comentários do YouTube, pelo Instagram, pelo LinkedIn e pelo X. Sem pré-registro (padrão de rodadas).

**Dados novos:**

| O quê | Onde | Observação |
|---|---|---|
| a resposta do TSE (o e-mail e o anexo *"Resposta Institucional"*), transcrita sem dado pessoal | `docs/lai/TSE_RESPOSTA_2026-11-19.md`; e-mail com tarja e o `.docx` em `dados/lai/tse-2026-11-19/` | o `.docx` foi criado em 16/10/2026 (propriedade do arquivo) |
| a resposta do TRE-BA, transcrita sem dado pessoal | `docs/lai/TRE_BA_RESPOSTA_2026-11-24.md`; e-mail com tarja em `dados/lai/tre-ba-2026-11-24/` | |
| o diário (log) e o `aux.json` das urnas das cidades citadas nos reels do *"mesário em 2 cidades"*, nos 2 turnos | `dados/brutos/rodada6/logs.sqlite` (**fora do git**: o diário traz o número do título digitado) | baixados do TSE em 24/11; endereço e sha256 de cada arquivo em `dados/MANIFESTO_RODADA6.json`. As capitais ficaram de fora (grandes demais para baixar inteiras) |

**Código:** `ferramentas/mascarar_respostas_r6.py` e `transcrever_respostas_r6.py` (as respostas), `rodada_6.py` (H39, H40, H42 e o TRE-BA, em `resultados/RODADA6.json`), `rodada_6_coletar.py` e `rodada_6_mesarios.py` (H41, em `resultados/RODADA6_MESARIOS.json`), `validacao_rodada_6.py` (`resultados/VALIDACAO_RODADA6.json`) e `graficos_rodada_6.py` (g34 a g38).

🔒 **O número de mesário nunca é publicado.** Todo número de 12 dígitos lido no diário vira um código (`HMAC-SHA256` com uma chave local, os 12 primeiros caracteres); os resultados e as tabelas só têm o código.

## H39 · A pausa da noite do 1º turno, contra a resposta do TSE

### O que o TSE respondeu

| O TSE diz | Palavras do texto |
|---|---|
| a falha atingiu só o arquivo nacional de Presidente, por volta das 19h14, com 64,81% das seções | os arquivos de cada estado continuaram saindo |
| a equipe *"suspendeu, de forma deliberada e controlada, o processamento da totalização entre 19h32 e 19h59"* para achar a falha | |
| o arquivo nacional voltou às 20h04, com 84,96% | |
| *"Não houve, portanto, 'salto na totalização'"*: a tela alcançou o que já estava totalizado | |
| a relação entre a falha e o volume de boletins *"está em análise"* | |

O texto responde os itens 1 (a causa) e 3 (o intervalo sem boletim) do pedido, com um texto e não com o registro do incidente. ⚠️ O **item 2** (o que os campos de hora `dr` e `hr` do arquivo público registram) **ficou sem resposta**, e o texto fala do 2º turno no futuro (*"vêm realizando testes [...] para o 2º turno, em 25 de outubro"*), embora tenha chegado em 19/11. O anexo `.docx` foi criado e salvo pela última vez em 16/10/2026, com o título interno *"Esclarecimentos - Interrupção na divulgação - 1º turno 2026 (minuta v1.0)"*.

### O que o arquivo público mostra

| Conta | Resultado |
|---|---|
| boletins com hora entre 19:31:50 e 19:59:22 | **0**, no campo do detalhe por seção e no `recebido` do `aux.json` (389.857 seções com esse campo) |
| boletins nos 4 minutos depois do buraco | **19.235** (a fila que ficou parada) |
| ritmo antes (19h25 a 19h31) e depois (20h04 a 20h10) | 1.658 e 504 boletins por minuto |
| os 64,81% da tela | = a soma dos boletins até **19:03:56**: Flávio 49,56% (tela 49,58%), Lula 42,27% (tela 42,25%) |
| os 84,96% da tela | = a soma até **19:31:11**: Flávio 48,46% (48,47%), Lula 43,49% (43,49%) |
| os 90,56% da tela | = a soma até 20:18:56, igual nas 2 casas |
| o "salto" de 64,81% para 84,96% | 100.598 seções; Lula 47,22% e Flávio 45,10% nelas; **81% das seções da janela são do Sudeste e do Nordeste**, contra 61% antes |

Ou seja, a tela mostrava a soma dos boletins com alguns minutos de atraso, e o número com que ela voltou é o que já estava somado antes do buraco. O pulo para o Lula vem da composição da janela.

### O que a resposta não explica

| O quê | O dado |
|---|---|
| 2 paradas menores, antes das 19h | 18:01:00 a 18:08:47 (7,8 min, com 15,6% das seções somadas) e 18:49:47 a 18:53:59 (4,2 min, com 54,7%) |
| o item 2 do pedido | o dado mostra que o campo de hora para quando a soma para; o TSE não disse o que ele registra |

**Veredito:** **desmentida** (a pausa existiu, mas a leitura de que votos entraram nela não para em pé: a tela é a soma dos boletins, e cada boletim é público). As 2 paradas menores e o item 2 ficam como pergunta, sem mudar o resultado.

## O TRE-BA · o andamento do pedido (sem linha própria na série)

| O quê | O que chegou em 24/11 |
|---|---|
| o pedido (21/10) | caderno contra o log, ocorrências e fiscais de 26 seções do 1º turno (19 marcadas pelo projeto `alegacoes-fraude-eleicoes-2026` e as seções 315 a 321 da zona 13 de Salvador); ou, como alternativa, a cópia das atas |
| a resposta | **indeferiu** a conferência: *"trabalhos adicionais de análise, interpretação ou consolidação"* (Lei 12.527/2011; Res. CNJ 215/2015, art. 12, III) |
| o pedido alternativo | *"será avaliada a viabilidade de atendimento"*, sem prazo |
| o recurso | 10 dias a contar de 24/11 (até 04/12/2026), pelo link do e-mail |
| a comparação | o TRE-PE respondeu 27 de 41 seções e mandou 4 PDFs de ata (rodada 5) |

## H40 · O 2º turno para governador mudou o voto para presidente?

Pedido por mensagem no LinkedIn: *"onde teve 2º turno para governador o comportamento dos votos foi diferente de onde não houve?"*

| | Com 2º turno para governador | Sem |
|---|---|---|
| 2026 · estados | AC, AM, DF, ES, RN, TO (6) | os outros 21 |
| mudança do Lula entre os turnos (mediana dos estados) | **+5,83 pontos** | **+5,75** |
| mudança do comparecimento | +0,54 | +1,96 |
| 2022 · estados | AL, AM, BA, ES, MS, PB, PE, RO, RS, SC, SE, SP (12) | os outros 15 |
| mudança do Lula (mediana) | +1,61 | +2,12 |

Dentro de cada região a diferença é pequena e muda de lado (2026: Centro-Oeste +7,62 com contra +5,72 sem, Sudeste +5,87 contra +7,49; 2022: Nordeste +2,40 contra +2,45, Sudeste +2,71 contra +2,35). Tabelas: `resultados/tabelas/r6_h40_uf_2026.csv` e `r6_h40_uf_2022.csv`.

**Veredito:** **não sustentada** (o voto para presidente mudou o mesmo tanto com e sem 2º turno para governador, em 2026 e em 2022).

## H41 · "O mesmo título de mesário em 2 cidades longe uma da outra, com segundos de diferença"

Os 2 reels de 23/11 (Felipe Gimenez e Rafael Carvalho, 56 mil curtidas somadas), o vídeo do deputado estadual Paulo Mansur e a pergunta no YouTube (vídeo 16). A Justiça Eleitoral publicou em 23/11 que é erro de digitação no registro de presença, sem mostrar os diários.

### O que foi lido

O diário de **5.310 urnas** das cidades citadas nos reels (as capitais ficaram de fora), 546.418 eventos com número de 12 dígitos, e 21.602 números de mesário diferentes (já como código).

| Evento do diário | Códigos | Em 2 ou mais cidades |
|---|---|---|
| registrado | 21.384 | 8 |
| habilitou o eleitor | 8.279 | 2 |
| biometria do mesário encontrada | 8.279 | 2 |
| é ou não é eleitor da seção | 21.384 | 8 |
| pedido de leitura da biometria | 21.437 | 8 |
| título digitado para encerramento | 5.588 | 1 |
| mídia gerada pelo usuário | 38 | 0 |

### Os pares dos reels

| Par | Turno | O reel diz | Urnas baixadas | Números em comum | Menor intervalo |
|---|---|---|---|---|---|
| Bragança e Rio Maria | 1º | 2 s | 341 e 50 | 1 | 2 s |
| Diadema e Guaraci | 1º | 6 min | 937 e 27 | 1 | 47 s |
| Ataléia e Goianésia | 1º | 7 min | 38 e 172 | 1 | 3 s |
| Mogi Mirim e Petrópolis | 1º | 16 min | 215 e 804 | 1 | 5 s |
| José Bonifácio e São Vicente | 1º | 17 min | 83 e 766 | 1 | 17 min |
| Porto Seguro e Casa Nova | 2º | 22 s | 323 e 185 | 1 | 14 s |
| Camacan e Juazeiro | 2º | 32 s | 66 e 495 | 1 | 26 s |
| Alagoinhas e Porto Seguro | 2º | 37 s | 366 e 323 | 1 | 37 s |

O reel não diz de que evento é o intervalo dele; o do diário é o menor entre quaisquer 2 eventos do número nas 2 cidades. Em Ataléia e Goianésia (3 s) e em Mogi Mirim e Petrópolis (5 s), os 2 eventos mais próximos são conferências de digital no meio da manhã ou do dia (*"Biometria coletada não é do mesário [nº]"*, que a urna anota quando a digital posta para liberar um eleitor não é a desse mesário), e não registros de presença. Em Juazeiro e em São Vicente o número só aparece num pedido de leitura de digital que não virou registro; em Porto Seguro (com Alagoinhas), só no título digitado para encerrar a urna.

### O que cada número fez em cada lugar

| Turno | Código | Cidade | Liberou eleitores | Digital do mesário conferida | Registros de presença | Só no registro do fechamento | 1º e último evento |
|---|---|---|---|---|---|---|---|
| 1º | `183947de7f7c` | Diadema | 0 | 0 | 1 | não | 07:23:23 a 15:08:17 |
| 1º | `183947de7f7c` | Guaraci | 0 | 0 | 2 | não | 07:30:10 a 17:04:07 |
| 1º | `3bd5f2994950` | Mogi Mirim | 7 | 7 | 1 | não | 07:25:32 a 14:11:51 |
| 1º | `3bd5f2994950` | Petrópolis | 0 | 0 | 1 | não | 07:42:52 a 09:43:07 |
| 1º | `5a782e972ad2` | Bragança | 2 | 2 | 2 | não | 08:02:24 a 17:07:57 |
| 1º | `5a782e972ad2` | Rio Maria | 0 | 0 | 1 | sim | 17:07:53 a 17:08:00 |
| 1º | `6dcfa945b5cf` | José Bonifácio | 0 | 0 | 1 | não | 07:15:09 a 16:52:10 |
| 1º | `6dcfa945b5cf` | São Vicente | 0 | 0 | 0 | não | 07:32:37 a 07:32:37 |
| 1º | `9cf70dc9436f` | Ataléia | 0 | 0 | 2 | não | 07:22:09 a 17:03:30 |
| 1º | `9cf70dc9436f` | Goianésia | 0 | 0 | 2 | não | 07:51:21 a 17:11:13 |
| 2º | `37c85cf097e5` | Camacan | 0 | 0 | 4 | não | 07:09:06 a 17:17:36 |
| 2º | `37c85cf097e5` | Juazeiro | 0 | 0 | 0 | não | 17:03:39 a 17:03:39 |
| 2º | `73e0bd945c90` | Alagoinhas | 0 | 0 | 4 | não | 07:31:04 a 17:02:17 |
| 2º | `73e0bd945c90` | Porto Seguro | 0 | 0 | 0 | não | 17:00:58 a 17:00:58 |
| 2º | `f459ee5b6c27` | Casa Nova | 0 | 0 | 1 | sim | 17:03:08 a 17:03:15 |
| 2º | `f459ee5b6c27` | Porto Seguro | 0 | 0 | 4 | não | 07:13:01 a 17:19:31 |

**Somando:** 8 números de mesário aparecem em 2 ou mais cidades; **0** liberaram eleitor ou tiveram a digital conferida nas 2; 2 atuaram numa cidade e na outra só foram digitados (no registro de presença ou no encerramento); 6 não liberaram ninguém em nenhuma. Para comparar, 140 números aparecem em 2 ou mais seções da **mesma** cidade (o mesário que muda de seção, ou o número digitado errado que bate com outro mesário da cidade).

Ou seja, o número repetido existe nos 8 pares, como os reels dizem. O que não aparece é o mesmo mesário liberando voto em 2 lugares: em 2 pares ele liberou eleitores numa cidade só (Bragança e Mogi Mirim), e nos outros 6 ninguém liberou eleitor com ele em nenhuma das 2. Ele se repete no registro de presença (de manhã ou no fechamento) ou no título digitado para encerrar a urna, e em pelo menos uma das pontas de cada par o diário anota *"Mesário [nº] não é eleitor da seção"*: a urna não tem a digital do cadastro para conferir e guarda o número que foi digitado. Em 3 casos o diário mostra *"Digitado título inválido para o registro de mesário"* logo antes do registro, o que mostra que o erro de digitação acontece. Os segundos de diferença vêm de milhares de urnas anotarem os mesmos eventos nos mesmos minutos (o registro de manhã e às 17h, e a conferência de digital ao longo do dia).

**Limite:** só as cidades dos reels, sem as capitais (os pares com Rio de Janeiro, São Paulo e Goiânia ficam para uma rodada que baixe as capitais). Quem estava de fato em cada seção, só o cartório diz (a lista de convocados e a digital guardada).

**Veredito:** o fato que circula é **certo** (o número repete); a leitura de fraude (um mesário que não existe, liberando voto) é **desmentida nos casos conferidos**. Tabela: `resultados/tabelas/r6_h41_codigos_em_2_municipios.csv` (só códigos).

## H42 · O "DE-PARA": os votos trocados ao chegar no TSE

Comentário no vídeo 26: *"o número de votos que chegava no TSE era invertido, na programação isso chama-se DE-PARA"*.

| Conta | Resultado |
|---|---|
| válidos somados seção a seção (2º turno) | **124.082.273** = o total oficial |
| os boletins eletrônicos | Lula 64.255.787 e Flávio 59.825.688, contra 64.256.232 e 59.826.041 no oficial |
| a diferença (798 votos) | é das **70 seções sem boletim eletrônico** (41 por totalização e 29 pelo sistema de apuração), que somam exatamente 798 válidos |
| o registro de cada voto (RDV) contra o boletim | igual em 499.177 de 499.177 seções (projeto `investigacao-segundo-turno-2026`) |

Cada boletim é o mesmo que fica colado na porta da seção e que qualquer pessoa baixa no site do TSE. Uma troca no caminho apareceria na diferença entre a soma dos boletins e o total.

**Veredito:** **desmentida**.

## O que chegou e já estava respondido

| Pedido | Onde já está |
|---|---|
| Campos dos Goytacazes (X, @WagnerThomazoni) | H25 (rodada 4) |
| o cálculo urna a urna entre o 1º e o 2º turno (LinkedIn) | o projeto `investigacao-segundo-turno-2026` (A1: os votos do Lula que exigem troca de eleitor somam 3,34% da margem) |
| população × votos (X, @ThePunisherUSA) | H14 e H26 |
| mortos, fiscais, depois das 17h, urnas trocadas, 2018 | H13, H37, H33, H10 e H18, H07 |
| o post do @urna_2026 | fora do ar (o X responde 404 em 24/11) |

## Contagem da série

39 linhas: **12 desmentidas**, **20 não sustentadas**, **5 compatíveis com as duas** (H14, H15, H18, H23 e H37), **2 não testadas**. A soma do pior caso do 2º turno não muda: 383.588 votos (8,66%), com a ressalva da nota N4 da rodada 4 (o item do *"já votou"* é piso). A H39 é do 1º turno; a H41 não tem nenhum número que liberou eleitor em 2 lugares, então não soma nada.

## Validação (`resultados/VALIDACAO_RODADA6.json`)

7 de 7:

- ✅ buraco também no campo recebido do aux.json: 0 boletins entre 19:31:50 e 19:59:22 em 389857 seções com esse campo
- ✅ 2º turno: válidos somados seção a seção = oficial: seções 124082273; oficial 124082273
- ✅ 2º turno: o que falta nos boletins eletrônicos é o voto das seções sem boletim eletrônico: faltam 798 votos; as 70 seções sem boletim eletrônico somam 798
- ✅ 1º turno: Lula na soma das seções = oficial, com 2 casas: seções 45.16%; oficial 45.16%
- ✅ H40 pelo oficial: a diferença entre os grupos fica abaixo de 0,5 ponto: mediana com 2º turno para governador 5.83, sem 5.75 (análise: 5.83 e 5.75)
- ✅ H41: números em 2+ municípios, contados direto no texto: texto 8; análise 8
- ✅ H41: liberou eleitor nas 2 pontas: texto 0; análise 0

## Os pedidos

| Protocolo | Situação em 24/11 |
|---|---|
| TSE · 82032521133805 | **respondido em 19/11** (itens 1 e 3; o item 2 sem resposta) |
| TRE-BA · 82034321135124 | **indeferido em 24/11** (a conferência); as atas em avaliação; recurso até 04/12 |
| TRE-PE · 82034721135306 | respondido em 13/11 (rodada 5) |
