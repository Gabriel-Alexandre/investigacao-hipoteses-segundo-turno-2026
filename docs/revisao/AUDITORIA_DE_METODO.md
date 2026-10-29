# Auditoria de método, conta e linguagem

**Rodada 1, 29/out/2026.** Papel: o terceiro revisor (confere as duas visões no método, na conta e na linguagem). Lido: `RELATORIO.md`, `RESUMO_SIMPLES.md`, `docs/LEITURA_DA_IA.md`, `resultados/RESUMO.json`, `resultados/VALIDACAO.json`, `ferramentas/analise.py`, `ferramentas/gerar_relatorio.py`, `ferramentas/validacao_independente.py`, `ferramentas/derivar_amostra.py`, `ferramentas/amostra_logs.py` e as 11 figuras. As contas foram refeitas em Python a partir de `dados/copias/` e `dados/derivados/`, sem editar nada do projeto.

## Resumo

| | Quantos |
|---|---|
| Erros de gravidade alta | 4 |
| Erros de gravidade média | 11 |
| Erros de gravidade baixa | 14 |
| Conferências que passaram | 33 |

Nenhum número do `RELATORIO.md` está errado contra o `RESUMO.json`: todos os que conferi batem. Os problemas estão em **número que ficou de fora** (e muda a leitura), em **veredito que não segue a régua** e em **título que diz o contrário do número** para quem lê rápido.

---

## 1. Erros de gravidade alta

### A1. H01: com o fuso certo, o Flávio continua na frente nas urnas que fecharam até as 17h, e o relatório não diz

- **Onde:** `RELATORIO.md` (H01, "O achado principal" e a conclusão "O relatório pericial nasce de um erro de fuso"), `RESUMO_SIMPLES.md` item 1, `resultados/figuras/g01_o_erro_de_fuso.png`.
- **O número que falta** (`RESUMO.json`, `H01.cortes.ate_17h00min59`): lendo a hora em Brasília, as **126.058 seções que fecharam até 17h00min59 deram 50,92% ao Flávio, com 564.877 votos de frente**. E, dentro do próprio grupo do relatório, as 118.745 seções fora dos 6 estados com fuso ainda dão ao Flávio **304.126 votos de frente** (1.747.639 menos 1.443.513).
- **Por que importa:** o erro de fuso explica o número de 52,39% e a maior parte da frente, mas o padrão "urna que fecha cedo dá mais Flávio" sobrevive ao fuso certo. Quem abrir o `RESUMO.json` acha esse número, e a frase "nasce de um erro de fuso" fica mais forte que o dado. O que derruba a conclusão do relatório (a de que a prorrogação virou o resultado) é outra coisa, que o próprio projeto já tem: só 34.393 votos depois das 17h e, no mesmo local, nenhuma vantagem do Lula na seção que fechou tarde (1.506 locais).
- **O que corrigir:** pôr o 50,92% e os 564.877 no texto de H01 e na figura g01, explicar que a seção que fecha na hora é a seção sem fila (perfil diferente), e trocar "nasce de um erro de fuso" por algo como *"o número de 52,39% vem de um erro de fuso; com o fuso certo, a frente do Flávio nas urnas que fecharam no horário cai para 564.877 votos, e a prorrogação só teve 34.393 votos"*. O veredito Desmentido serve para "a virada veio da prorrogação", não para "nas urnas fechadas até 17h o Flávio ganhou", que é verdade.

### A2. H14: em 120 municípios o comparecimento passou da população inteira, e em 3 o Lula sozinho teve mais votos que habitantes

- **Onde:** `RELATORIO.md` H14, `RESUMO_SIMPLES.md`, g11, `ferramentas/analise.py` `h13_h14`.
- **O que o relatório diz:** 579 municípios com comparecimento acima da população de 16 anos ou mais (596 em 2022), e *"na lista da corrente de WhatsApp, em nenhuma cidade o Lula teve mais votos que habitantes"*.
- **O que a conta mostra contra a população total do Censo 2022** (a palavra da alegação é "habitantes"):
  - **120 municípios** com comparecimento do 2º turno acima da população total (o Lula venceu em 75); em 2022, **52**. Mais que dobrou, então *"o número é parecido com o de 2022"* não vale para esta régua.
  - **3 municípios do Piauí em que os votos do Lula passam da população total:** Novo Santo Antônio (2.827 habitantes, 3.142 votos do Lula), Jatobá do Piauí (4.494 e 4.787) e Aroeiras do Itaim (2.690 e 3.104). Em 2022 isso aconteceu em 1 (Novo Santo Antônio, 3.005 votos do Lula). O Flávio não passou da população em nenhum.
  - **849 municípios** com eleitorado acima da população total, e **2.898** acima da população de 12 anos ou mais em 2022 (o número está no `RESUMO.json` e não aparece no texto).
  - A lista da corrente tem 10 nomes e só 9 foram achados ("Nova Liberdade" não casou com nenhum município); o texto não diz.
  - O `docs/HIPOTESES.md` previa usar também a estimativa de população de 2025 do IBGE; o teste usou só o Censo de 2022, que tem 4 anos.
- **O que corrigir:** dar os três números contra a população total, os 3 municípios com nome e o 2022 de cada um, e a causa provável com o que a fecha (título de quem mudou; estimativa 2025 e o recadastramento com o TSE). Pela régua, com o fato alegado existindo e crescendo desde 2022, o veredito "Não sustentado" não se sustenta: "Compatível com as duas" é o que cabe até a estimativa de 2025 e o cadastro responderem.

### A3. O título da hipótese diz um fato que o dado confirma, e o veredito ao lado parece negar o fato

- **Onde:** a tabela de vereditos do `RELATORIO.md`, a lista "O que deu" do `RESUMO_SIMPLES.md` e a figura g11.
- **Os casos:** "106 urnas com zero voto para o Flávio" (são exatamente 106) aparece como *não sustentado*; "O Flávio perdeu votos em 6 estados e o Lula em nenhum" (é exatamente isso) aparece como *não sustentado*; "8,6 milhões liberados sem biometria, quase o dobro da diferença" (8.615.564, 1,94 vez a diferença) aparece como *não sustentado*; "A lei de Benford reprova a votação" (reprova: desvio de 0,079 contra o limite de 0,015) aparece como *não sustentado*; "A abstenção caiu no Nordeste" (caiu, de 18,39% para 16,49%) aparece como *não sustentado*; "Mais de 2,5 milhões de eleitores votaram em urnas que passaram do horário" (2.537.055 votaram nessas urnas) aparece como *desmentido*.
- **Por que importa:** o leitor leigo, e quem recortar a tabela para a rede, lê "não sustentado" como "não aconteceu". O veredito é sobre a leitura de fraude, mas a frase não diz isso. É a frase do projeto mais fácil de usar contra ele.
- **O que corrigir:** separar em duas colunas, **o fato** (correto, correto em parte, errado) e **a leitura de fraude** (o veredito), ou reescrever o título como a alegação inteira: *"As 106 urnas sem voto do Flávio são sinal de fraude"*.

### A4. H21: pela outra métrica, o Lula cresceu relativamente mais nos municípios mais pobres

- **Onde:** `RELATORIO.md` H21, `docs/LEITURA_DA_IA.md`, `resultados/figuras/g10_ganho_por_renda.png`.
- **O problema:** o ganho em pontos tem efeito de teto. Nos 20% de municípios de menor renda o Lula já tinha 69,5% dos válidos no 1º turno; sobra pouco para crescer em pontos.
- **A conta pela outra métrica** (`dados/copias/presidente_municipio.csv`): nos 20% mais pobres, o Lula ficou com **102% do saldo de votos novos dos dois** (ganhou 733.943, o Flávio perdeu 14.976) e ganhou **1,52 vez** os votos que os outros candidatos tinham no 1º turno; nos 20% mais ricos, ficou com **68%** do saldo e ganhou **1,01 vez** os votos dos outros. Pela parte dos votos que mudaram de mão, o crescimento foi maior onde a renda é menor, que é o que a visão da fraude espera.
- **O que corrigir:** dizer as duas métricas e que a renda é um substituto do benefício, não o benefício. *"Foi o contrário"* é mais forte que o dado. Pela régua, o veredito que cabe é **Compatível com as duas** (a renda não separa), com o dado do Bolsa Família por município como o que fecharia. O título da g10 (*"O Lula cresceu mais onde a renda é maior"*) precisa dizer "em pontos".

---

## 2. Erros de gravidade média

### M1. H18: o próprio texto descreve "Compatível com as duas", e o veredito é "Não sustentado"

`RELATORIO.md` H18. A visão da fraude diz *"uma troca perfeita, que imitasse o eleitor, não se separa por estatística; é o limite deste teste"*: é a definição de "compatível com as duas" na régua. O que sustentaria o "não sustentado" é o teste de integridade, e o texto não dá o tamanho dele: pelo `docs/pesquisa/TEORIAS_NA_INTERNET.md`, são **389 votos auditados no TSE e 33 urnas no TRE-SP**. É uma amostra pequena perto de 499 mil seções. Corrigir: ou mudar o veredito, ou dizer o tamanho do teste de integridade e que é número de terceiro, não recalculado.

### M2. H06 deveria ser "Desmentido", e as datas foram digitadas

A alegação (`docs/HIPOTESES.md`) é que o TSE *"só soltou os boletins na quarta"*. O próprio texto mostra que os boletins foram afixados em 25/10 e os arquivos por seção estavam públicos desde 26/10, 7h30: o fato alegado é falso, e pela régua isso é **Desmentido**, não "Não sustentado". As datas (28/10 11h07, 26/10 15h e 18h31, 7h30) estão escritas à mão em `ferramentas/gerar_relatorio.py`, cuja primeira linha diz *"Nenhum número é digitado aqui"*. Corrigir: o veredito e mover as datas para o `RESUMO.json` (ou para o `SONDAGEM.json`, com a fonte).

### M3. H13: o salto da faixa de 95 a 99 anos compara turnos diferentes e não é exclusivo dessa faixa

- O texto compara o 2º turno de 2022 (2,14%) com o 1º turno de 2026 (4,35%). Do 1º turno para o 1º turno, vai de **1,60% para 4,35%**.
- O salto aparece em todas as faixas idosas, do 1º turno de 2022 para o de 2026: **85 a 89 anos, de 15,57% para 24,32%; 90 a 94, de 6,64% para 13,47%; 95 a 99, de 1,60% para 4,35%**. Ao mesmo tempo, os aptos de 90 a 94 caíram de 733.738 para 664.482 e os de 95 a 99 de 465.541 para 337.136, enquanto os de 100 ou mais subiram de 184.113 para 297.977. Isso aponta para mudança no cadastro (o denominador), não para algo só da faixa de 95 a 99.
- *"Há mortos no cadastro"* (título da g07, `RESUMO_SIMPLES.md` item 3, H13) afirma a causa. O número mostra 297.977 eleitores de 100 anos ou mais para 149.424 pessoas que poderiam ter essa idade: são registros que não podem ser de gente viva **com essa idade**, o que inclui mortos e data de nascimento errada.
- Corrigir: comparar 1º turno com 1º turno, mostrar as faixas vizinhas e trocar o título por *"O cadastro tem centenários demais, mas eles quase não votam"*.

### M4. H15: o teto do pior caso conta o voto errado

O voto que teria sido roubado é o que veio **antes** do aviso "já votou"; a liberação manual que vem **depois** do aviso é a do próximo eleitor ou de uma nova tentativa. O teto de 19.830 (113.315 avisos vezes os 17,5% da amostra) mede outra coisa e ainda mistura a taxa da amostra com a contagem do país. O pior caso honesto é **todo aviso ser um voto roubado: 113.315 votos, 2,56% da diferença**. Corrigir: dar os 113.315 como teto e os 19.830 como o subconjunto "a conferir".

### M5. H03: "sem sinal para medir" esconde a maior hipótese sem teto e um teto que dá para calcular

O máximo teórico é **15.858.427 votos sem a digital do eleitor, 3,6 vezes a diferença**, e isso deve estar escrito, porque é a hipótese em que o pior caso passa da diferença. Há também um teto informativo: a parte manual subiu **0,21 ponto** entre os turnos na amostra (12,29% para 12,50%); aplicada aos 127.697.270 votos com log, dá **cerca de 268 mil votos, 6,1% da diferença**, se toda a subida fosse voto falso. Corrigir: pôr os dois números na linha do teto.

### M6. H16: a hora que interessa ficou de fora do texto e do gráfico

- No 2º turno, das 17h às 18h de Brasília, a parte liberada sem a digital do eleitor foi **16,3%** (124 de 763 votos na amostra), contra 12,0% no 1º turno. O texto diz "entre 12% e 13% em quase todas as horas", e a figura `g08_liberacao_manual_por_hora.png` vai só das 8h às 16h. É justamente a hora da alegação ("quando a seção esvazia"). Mostrar, com o tamanho pequeno da amostra nessa hora.
- *"Nenhuma seção da amostra teve 10 ou mais seguidas"* vale para o 2º turno; no 1º turno uma seção teve 13. A mediana subiu de 1 para 2 entre os turnos. Dizer.

### M7. H20 e H23 usam o mesmo argumento e recebem vereditos diferentes

As duas se apoiam no "fora do padrão do vídeo 19". H23 é "Compatível com as duas"; H20 é "Não sustentado", embora a própria visão da fraude de H20 diga *"a queda sem precedente é real"* e se apoie em H03, H15 e H16, das quais H15 está "compatível". Alinhar. Em H23, a alegação específica (que os números de Joaçaba e Araruama não fechariam) é falsa: a conta fecha nos 8 municípios. Isso pede "Não sustentado" ou "Desmentido" para a alegação, com o "fora do padrão" do vídeo 19 dito à parte. Em Joaçaba, *"456 eleitores a mais"* são 456 **votantes** a mais (comparecimento).

### M8. O fuso do oeste do Amazonas está errado no código, e a validação herda o mesmo erro

`FUSO = {"am": 1, ...}` em `ferramentas/analise.py`, `ferramentas/derivar_amostra.py` e `ferramentas/validacao_independente.py` (e no `derivar-t2.py` do vídeo 16, de onde vem `log_votos_depois_17h`). Pelo próprio horário de encerramento, **556 seções do AM em 11 municípios** (Tabatinga, Benjamin Constant, Eirunepé, São Paulo de Olivença, Atalaia do Norte, Guajará, Ipixuna, Envira, Jutaí, Itamarati e Amaturá) fecharam às 15h no relógio local, que é 17h de Brasília: estão 2 horas atrás, não 1.

- Efeito em H02: os votos das 15h às 16h no relógio local dessas seções não entram nos 34.393; **29 dessas seções** têm último voto depois das 15h locais. O efeito é pequeno, mas é para cima.
- Efeito em H01: o corte de 17h00min59 vai de 126.058 seções e 50,92% do Flávio para 125.623 e 50,99%.
- A validação independente usa o mesmo mapa de fuso, então não tinha como pegar. Corrigir: fuso por município e refazer.

### M9. O exterior entra em 2018 e 2022 e não entra em 2026; e o partido de 2018 está errado na figura

- `secoes_2018_t2.parquet` tem 744 seções do exterior, que entram em H04 e H07: Bolsonaro acima de 90% em 2018 é **1.192 sem o exterior** (o texto e a g03 dizem 1.298); Haddad, 14.957 (dizem 14.958).
- Em H05 e H08, o 2022 é lido sem tirar as 1.018 seções do exterior: placares repetidos de 2022 são **43.030 sem o exterior** (dizem 43.111).
- `g03_unanimidade_no_tempo.png` chama o Bolsonaro de 2018 de "candidato do PL"; em 2018 ele era do PSL. E o título *"A unanimidade foi menor que em 2018 e 2022"* não vale para o lado do Flávio contra 2022 (368 contra 199).

### M10. Número de terceiro que não foi recalculado

*"Em 2022 foram cerca de 10 milhões, segundo a mesma conta feita pelo Jornal Razão"* (H03) contraria o `CLAUDE.md` do projeto (*"Número de terceiro só recalculado"*), e o próprio `RESUMO.json` diz *"não recalculado aqui"*. Além disso, os 10,0 milhões (8,06%) parecem ser só a digital do mesário, que em 2026 é 8,6 milhões (6,75%), e não os 12,42% somados. Recalcular ou tirar.

### M11. A conclusão é mais forte que a tabela

*"Nenhuma das 23 hipóteses mostrou a marca que a fraude deixaria no dado público"*: H22 não foi testada, e três ficaram "compatível com as duas", com itens "a conferir". Corrigir para *"nenhuma das 22 testadas"* e citar as três. Junto com A1, a frase *"O relatório pericial nasce de um erro de fuso"* precisa da ressalva.

---

## 3. Erros de gravidade baixa

1. **Reconciliação imprecisa** (`RELATORIO.md`, fim): *"os 798 que faltam cabem nas 86 seções [...] que têm 4.508"*. O exato: são **27 seções do exterior apuradas pelo "Sistema de apuração", sem boletim de urna, que somam exatamente 798 votos nominais** (445 do Lula e 353 do Flávio, a mesma diferença da UF exterior na curva da noite). Dizer isso, sem o "cabem".
2. **H17:** o título cita *"os 165 mil votos 'sem origem'"* e a "sala-cofre", e o texto não responde a nenhum dos dois com número. E o `RESUMO.json` traz `soma_das_ufs_e_exterior_na_ultima_versao` (Lula 64.249.830) diferente do nacional (64.256.232) sem explicar: é porque a última versão gravada de AM, BA, MA, MG e PA está entre 99,93% e 99,99% apurada. Pôr a nota.
3. **Teto sem porcentagem em H10:** 502.317 votos são **11,34%** da diferença. Em H07, dar também o teto largo: 14.860 votos do Lula nessas seções, 0,34%.
4. **Números digitados em `gerar_relatorio.py`** apesar da primeira linha: as datas de H06, *"entre 12% e 13%"* (H16), *"10 milhões"* (H03), *"de 200 a 400 eleitores"* (H05), a lista *"AC, AM, AP, MA, RR, TO"* (H19), *"499.248"*, *"12.691"* e *"12 mil"*, e as listas de hipóteses da tabela da conclusão. Todos batem com os dados hoje, mas mudam sozinhos se a análise mudar.
5. **"Os números centrais foram refeitos por outro caminho (15 de 15)":** as 15 checagens não cobrem a reprodução do relatório pericial (52,39% e 1.747.639), nem H03, H13, H14, H15 e H21. A checagem "Flávio nos 6 estados" compara as 32.037 seções com as 32.026 do grupo; bate pelo arredondamento. Dizer quais números foram validados.
6. **A limitação dos logs está escrita mais larga do que é:** H01, H02 e os totais de H03 e H15 vêm do log completo do vídeo 16; só as perguntas novas (1º turno contra 2º, sequências, aviso seguido de liberação, hora a hora) usam a amostra.
7. **H08, o sorteio usa a parte do Lula entre todos os candidatos do 1º turno** (`lula_1t/nom1`, média 0,457) em vez da parte entre os dois. A conclusão resiste: com a parte entre os dois o acaso dá de 42.533 a 42.651, e com o próprio 2º turno, de 41.632 a 41.795; todos acima de 41.133. Mas "menos que o acaso" depende do modelo; *"perto do acaso, um pouco abaixo"* é mais justo.
8. **H04:** os 6.899 e 384 da alegação não saem por nenhum caminho que testei (acima de 90%: 6.802 e 368; a partir de 90%: 6.885 e 374; com o exterior: 6.815 e 376). Dizer que não reproduz. *"99,6% já davam mais de 80% em 2022"* é sobre as 5.935 das 6.802 que existiam em 2022: dizer a base.
9. **H19:** a queda do comparecimento explica o Flávio perder votos, mas não por que o Lula não perdeu em nenhum estado. A outra metade é que ele ficou com os votos dos outros candidatos. Dizer.
10. **Critério das hipóteses:** H09 (voto por modelo de urna), H10 (voto da urna trocada contra a vizinha) e H18 (seções em que o Flávio caiu) são testes de comportamento dos votos, classificados como "arquivos", que pesa menos. Não muda a conclusão, mas muda o peso.
11. **"Liberado pelo mesário":** em H15 e H16 o código conta qualquer voto sem digital do eleitor (mesário, ano de nascimento e "outra"). Ajustar a palavra.
12. **Frases difíceis para o leigo:** *"correlação de 0,006"* sem dizer que zero é "nenhuma relação"; *"problema do aniversário"*; *"desvio médio do 1º dígito 0,079"* sem a régua (0,015 já reprova); *"ganho em pontos"* que mistura o 2º turno (só dois candidatos) com o 1º (todos); *"RED"*, *"recuperador de dados"*, *"BU"*; *"13 depois das 19h, igual ao número do TSE"* sem dizer qual número e onde.
13. **Figuras:** na g11, *"Compatível com as duas"* encosta na borda direita (termina em cerca de 1.910 de 1.920 pixels); na g05 o rodapé também encosta; na g08 o eixo usa ponto decimal ("20.0", "12.5"); na g04 o eixo não tem escala; na g06 *"6,6 pontos"* destoa dos outros com 2 casas; na g02 o rótulo "34.393" fica em cima da linha de base.
14. **`ESTADO.md` desatualizado:** diz *"Nenhum teste com regra rodou ainda"* e que a reconciliação está pendente, contra o relatório da rodada 1.

---

## 4. O que está certo e foi conferido

| # | Conferência | Número |
|---|---|---|
| 1 | Diferença | 64.256.232 menos 59.826.041 = 4.430.191 |
| 2 | Reprodução do relatório pericial (hora local, com o exterior) | 150.771 seções, 52,39% do Flávio, 1.747.639 de frente |
| 3 | Estados com fuso no grupo | 32.026 de 32.037 seções, 59,72%, 1.443.513 de frente |
| 4 | Mesmo local, seção que fechou depois das 17h15 | 1,25 ponto a menos de Lula e 0,14 a menos de ganho, 1.506 locais (`RESUMO.json`) |
| 5 | Votos depois das 17h no grupo "depois" | 31.357 |
| 6 | H02 | 8.848 seções a partir das 17h16, 2.537.055 de comparecimento, 5.663 votos depois das 17h nelas |
| 7 | Votos depois das 17h e das 19h no país, teto | 34.393 e 13; 0,78% da diferença |
| 8 | H03, liberações no país | 8.615.564 pela digital do mesário e 7.242.863 sem digital cadastrada; 12,42%; 1,94 vez a diferença |
| 9 | H03, amostra | 11.864 seções, 12,29% para 12,50%, correlações 0,006 e -0,009 |
| 10 | H04 | 6.802 e 368 (recalculado); 2022: 9.424 e 199 |
| 11 | H05 | desvios 0,079, 0,075, 0,081 e 0,071; o 2022 sem o exterior arredonda igual |
| 12 | H07 | 106 seções, 14.860 votos do Lula, 118 votos do Flávio no 1º turno, 50 e 56 (recalculado); 141 em 2022 e 328 em 2018 (328 também sem o exterior) |
| 13 | H08 | 41.133 placares repetidos (recalculado); o acaso fica acima com três escolhas de parâmetro |
| 14 | H09 | 53,94%, 51,96%, 51,53% e 51,83%; ganho de 6,46 a 6,60; 0,13 ponto em 933 locais |
| 15 | H10 | 1.996 seções com contingência no log (recalculado); -0,10 ponto em 1.727 locais; 502.317 votos |
| 16 | H11 | Teixeira de Freitas, 41.454 e 41.361 em 303 seções; 0 diferenças entre boletim e detalhe em 497.897 seções |
| 17 | H12 | 499.248 seções nos dois turnos, 0 só num deles, 41 não instaladas, 431 mudaram de local |
| 18 | H13 | 297.977 eleitores de 100 anos ou mais, 149.424 pessoas de 96 ou mais, 1.068 municípios, 2.141 (0,72%), 2.078 (1,13%), 14.661 (4,35%) (recalculado) |
| 19 | H13, teto | 2.141 mais 14.661 = 16.802 votos, 0,38% |
| 20 | H14 | 579 municípios (Lula em 393) e 596 em 2022 (recalculado) |
| 21 | H15 | 113.315 avisos em 73.044 seções (recalculado); 0,833 e 0,871 por mil; 12,7% e 17,5%; 19.830 é a conta declarada (0,45%) |
| 22 | H16 | mediana 2 e máximo 7 no 2º turno |
| 23 | H17 | 2.554 versões, 346 nacionais, 0 quedas do Lula e do Flávio (refeito por outro código, ordenado pela hora); a última nacional (23h27, 100%) é o resultado proclamado |
| 24 | H18 | 82.155 seções do Flávio abaixo do 1º turno, 9.575 do Lula, 53,5% com comparecimento em queda |
| 25 | H19 | AC, AM, AP, MA, RR e TO; AP -8,08, RR -6,02, AC -5,65; 9 estados com queda, os 7 do Norte mais MA e PI |
| 26 | H20 | Nordeste 18,39% para 16,49%; Salvador 20,14% para 15,77% |
| 27 | H21 | 4,45 a 7,27 pontos por quintil, como está no `RESUMO.json` (a leitura é que precisa mudar, ver A4) |
| 28 | H23 | a conta fecha nos 8 municípios (ganho dos dois igual a votos dos outros mais brancos e nulos a menos mais comparecimento a mais); Região dos Lagos 28.624, 1.476 e 27.127 |
| 29 | Contagem dos vereditos | 14 não sustentado, 5 desmentido, 3 compatível, 1 não testado = 23 |
| 30 | Reconciliação | os 798 votos que faltam são 445 do Lula e 353 do Flávio, todos no exterior |
| 31 | Amostra | 12.691 seções diferentes nos logs, 12.000 do sorteio |
| 32 | Travessão | nenhum em `RELATORIO.md`, `RESUMO_SIMPLES.md`, `docs/LEITURA_DA_IA.md`, `README.md`, `docs/HIPOTESES.md` e `docs/PLANO.md` |
| 33 | Travas de linguagem | "fraude" só como nome de uma das visões, nenhuma recomendação de voto, nenhum julgamento de intenção, os dois lados testados (espelho em H01, H07 e H18) |

## 5. Como refazer as contas desta auditoria

Os scripts usados estão fora do repositório (pasta temporária da sessão). Os números novos citados aqui saem de: o corte de H01 está no próprio `RESUMO.json`; H14, H21 e a reconciliação, de `dados/copias/presidente_municipio.csv`, `dados/derivados/ibge_municipio.csv`, `dados/derivados/detalhe_secao_2026.parquet` e `dados/copias/s2022_t2.parquet`; H13, de `dados/derivados/comparecimento_idade.csv`; H16, de `dados/derivados/amostra_logs.parquet`; o fuso do Amazonas, da coluna `encerramento` de `dados/copias/t2_secoes.parquet`; H17, de `dados/copias/noite/versoes-tse/`.
