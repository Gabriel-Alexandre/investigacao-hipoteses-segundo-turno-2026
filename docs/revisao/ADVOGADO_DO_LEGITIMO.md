# Revisão adversarial: o advogado da visão do resultado legítimo

**Rodada 1, 29/out/2026.** Papel: defender a visão de que o resultado (Lula 51,79% × Flávio 48,21%) foi legítimo e procurar onde o projeto **exagerou contra o resultado**: veredito mais suspeito do que o dado mostra, número sem o contexto que o explica, frase que sugere mais do que o dado sustenta, e comparação que falta e que fecharia a explicação inocente.

Lido, nesta ordem: `docs/HIPOTESES.md`, `RELATORIO.md`, `resultados/RESUMO.json`, `ferramentas/analise.py`, `resultados/VALIDACAO.json` (e `RESUMO_SIMPLES.md`, `docs/PLANO.md`, `ferramentas/derivar_amostra.py`, `hipoteses/log.py`). Nenhum arquivo do projeto foi editado. Toda variante abaixo foi calculada com os dados de `dados/copias/`, `dados/derivados/` e `dados/brutos/` do próprio projeto; o código está no apêndice.

**Leitura geral.** O projeto é cuidadoso e, na maior parte, já pende para onde o dado aponta. O exagero não está nos 19 vereditos de "não sustentado" e "desmentido": está nos **3 vereditos de "compatível com as duas"** (H13, H15, H23), que são justamente os que a conclusão e o resumo simples deixam "de pé, a conferir". Os três têm explicação inocente que o dado do próprio projeto já mostra, e em dois deles a métrica usada não mede o que diz medir.

---

## As objeções, em uma tabela

| # | Hipótese | Objeção, em uma linha | Gravidade | Veredito proposto |
|---|---|---|---|---|
| 1 | H15 | A métrica "aviso seguido de liberação manual em 5 min" fica **abaixo do acaso** nos dois turnos; a subida de 12,7% para 17,5% é a subida do fundo (19,7% para 26,2%); o voto seguinte ao aviso é manual em 15,9% e 16,1% | alta | não sustentado |
| 2 | H13 | O "salto" de 95 a 99 anos some quando se divide pelos eleitores com biometria (16,3% em 2022, 15,6% em 2026); todas as faixas idosas subiram juntas; e a comparação mistura o 2º turno de 2022 com o 1º de 2026 | alta | não sustentado |
| 3 | H23 | A Região dos Lagos é prevista quase no voto pelo resto do RJ (Lula 28.734 previstos, 28.624 reais); Joaçaba está na mediana exata de SC; "a conta fecha" e "compatível com as duas" se contradizem | alta | não sustentado |
| 4 | conclusão e resumo | "Ficam de pé, a conferir" lista exatamente os três itens acima; "o Lula com quase todos os votos em disputa" é falso no Brasil (73,7%); "Há mortos no cadastro" abre o resumo sem dizer que em 2022 era pior | alta | reescrever |
| 5 | H18 | 82.155 seções com o Flávio abaixo do próprio 1º turno, sem o espelho: em 2022 o Lula (que venceu) ficou abaixo do próprio 1º turno em 88.885 seções | média | mantém, com o espelho |
| 6 | H19 | "O Flávio perdeu votos em 6 estados e o Lula em nenhum" já aconteceu em 2022 com os lados trocados: o Lula perdeu votos no AC, AM, AP e RR, e o Bolsonaro em nenhum | média | desmentido como sinal |
| 7 | H10 | O teto de 502.317 votos (11,3% da diferença) soma todos os votos das seções; pela diferença medida contra as vizinhas, o teto é de cerca de 492 votos, e contra o Lula | média | mantém, teto refeito |
| 8 | H03 | Somar os 7,24 milhões sem digital cadastrada dá um número maior que o da alegação, sem dizer que a cobertura de biometria subiu de 75,8% (2022) para 89,4% (2026) | média | mantém, com contexto |
| 9 | H09, H10 | Testes de comportamento (voto da seção contra a vizinha no mesmo local) foram classificados como "arquivos", o critério de menor peso | média | reclassificar |
| 10 | H04, H06, H11 | O dado contradiz a alegação, e o veredito ficou um degrau abaixo (não sustentado no lugar de desmentido) | baixa | desmentido |
| 11 | H20 | "A queda sem precedente é real" na voz da fraude sugere um sinal que o próprio texto diz não existir | baixa | reescrever |
| 12 | H16 | Os 16,3% de liberação manual às 17h do 2º turno (no `RESUMO.json`) são 124 de 763 votos da amostra; no Brasil, as 5.472 liberações manuais depois das 17h são 0,12% da diferença | baixa | acrescentar |
| 13 | H17 | A soma das UFs na última versão gravada não fecha o total nacional (faltam 6.402 do Lula e 3.185 do Flávio) porque 5 UFs tiveram a última captura antes de 100% das seções; o relatório não diz isso | baixa | acrescentar |
| 14 | H14 | "É o eleitor que mora fora" vem afirmado sem teste; o espelho mais forte não aparece: em 2022, 3.805 municípios tinham eleitorado maior que a população de 16 anos ou mais, contra 2.898 em 2026 | baixa | acrescentar |

---

## 1. H15: a subida dos avisos "já votou" seguidos de liberação manual é a subida do acaso

**O que o projeto diz.** *"O aviso seguido de um voto liberado pelo mesário em até 5 minutos foi de 12,7% para 17,5%"*, e isso vira *"a parte a conferir"* na visão da fraude, o motivo do "compatível com as duas" e um dos itens que a conclusão deixa de pé.

**A objeção.** A métrica (`ferramentas/derivar_amostra.py`, linha 75) conta se **qualquer** voto não biométrico da seção, de **qualquer** eleitor, caiu nos 5 minutos depois do aviso. Ela não liga o aviso ao eleitor que foi liberado. Sem um placebo, ela mede sobretudo quantos votos manuais costumam cair em 5 minutos naquela seção. O placebo natural é a mesma conta a partir de **cada voto**, não do aviso. Refeito nos mesmos 12 mil logs sorteados (as mesmas seções do projeto, que reproduzem os 12,7% e os 17,5%):

| | 1º turno | 2º turno |
|---|---|---|
| Aviso seguido de voto não biométrico em 5 min (o número do projeto) | 315 de 2.479 = **12,7%** | 469 de 2.679 = **17,5%** |
| **Placebo**: qualquer voto seguido de voto não biométrico em 5 min | 586.098 de 2.980.171 = **19,7%** | 808.614 de 3.082.789 = **26,2%** |
| O voto seguinte ao aviso foi manual (mesário ou sem digital cadastrada) | 274 de 1.724 = **15,9%** | 325 de 2.023 = **16,1%** |
| O mesmo, só quando o voto seguinte veio em até 5 min | 221 de 1.468 = 15,1% | 259 de 1.665 = 15,6% |

Três leituras: (a) depois de um aviso, a chance de um voto manual em 5 minutos é **menor** que depois de um voto qualquer, nos dois turnos; (b) o fundo subiu de 19,7% para 26,2% entre os turnos, e o número do aviso subiu na mesma proporção (0,65 e 0,67 do placebo); (c) a medida que liga o aviso ao voto que vem logo depois (o eleitor que digitou o título errado e tentou de novo) **não mudou**: 15,9% e 16,1%. Por que o fundo subiu não foi medido aqui; uma hipótese é que o voto do 1º turno, com mais cargos, demora mais (na amostra, 89.400 votos depois das 17h no 1º turno contra 804 no 2º, sinal de fila mais longa).

**O teto também exagera.** Os "cerca de 19.830 votos" tratam como roubado todo aviso seguido de liberação manual. Pela conta acima, o excesso sobre o acaso é negativo; o teto honesto, se quiser manter um número, é "nenhum excesso medido".

**Veredito proposto:** não sustentado. Fica o caso individual (Campinas e Valinhos), que é do TRE-SP e não muda com estatística.

## 2. H13: o "salto" dos eleitores de 95 a 99 anos é mudança na composição do cadastro

**O que o projeto diz.** *"Fora do padrão, a conferir: na faixa de 95 a 99 anos o comparecimento foi de 2,14% no 2º turno de 2022 para 4,35% no 1º turno de 2026."* E abre o resumo simples com *"Há mortos no cadastro"*.

**Objeção (a): a comparação mistura turnos.** O 1º turno de 2026 deve ser comparado com o 1º turno de 2022, não com o 2º. O próprio `RESUMO.json` tem os dois: de 95 a 99 anos, 1,60% no 1º turno de 2022 (e não 2,14%); de 100 anos ou mais, 0,90% (e não 1,13%). Registro por honestidade: com a comparação certa o salto de 95 a 99 fica **maior** (1,60% para 4,35%) e a queda dos centenários fica menor (0,90% para 0,72%). A correção sozinha não ajuda a visão do resultado legítimo; o que desfaz o salto é a objeção (b).

**Objeção (b): todas as faixas idosas subiram juntas, e a subida some quando se olha só para quem tem biometria.** Comparecimento do 1º turno sobre os aptos, por faixa (`comparecimento_idade.csv`):

| Faixa | 2022 | 2026 | Comparecimento sobre eleitores **com biometria**, 2022 | 2026 |
|---|---|---|---|---|
| 75 a 79 | 41,7% | 52,3% | | |
| 80 a 84 | 26,8% | 37,2% | 48,8% | 49,2% |
| 85 a 89 | 15,6% | 24,3% | 36,3% | 36,9% |
| 90 a 94 | 6,6% | 13,5% | 24,8% | 25,3% |
| 95 a 99 | 1,6% | 4,3% | **16,3%** | **15,6%** |
| 100 ou mais | 0,9% | 0,7% | 14,6% | 9,0% |

A faixa de 90 a 94 dobrou também, e ninguém a apontou. Dividindo pelos eleitores com biometria (que fizeram o cadastro em vida, depois de 2008), o comparecimento de 95 a 99 anos **caiu** de 16,3% para 15,6%. O que mudou foi o denominador: em 2022 só 9,8% dos eleitores de 95 a 99 tinham biometria; em 2026, 27,8%. Menos registro parado no cadastro, mais gente viva no denominador, taxa maior. A conta é a de uma razão, não prova que cada voto foi biométrico.

**Objeção (c): o excesso de centenários era maior em 2022, e o de 95 a 99 já cabe na população.** Pelo Censo de 2022 (os arquivos de `dados/brutos/ibge/`, idade por idade):

| | Cadastro | Censo (no mesmo ano ou o teto possível) | Razão |
|---|---|---|---|
| 100 anos ou mais, 2022 | 184.330 | 37.814 (Censo 2022) | 4,9 |
| 100 anos ou mais, 2026 | 297.977 | no máximo 149.424 (quem tinha 96 ou mais em 2022, sem contar quem morreu) | 2,0 ou mais |
| 95 a 99 anos, 2022 | 466.703 | 165.178 | 2,8 |
| 95 a 99 anos, 2026 | 337.136 | no máximo 461.087 (quem tinha 91 a 95 em 2022) | abaixo do teto |

Em 2022, com a mesma conta no mesmo ano, **2.865 municípios** tinham mais eleitores de 100 anos ou mais que centenários no Censo; o relatório cita 1.068 em 2026 com um teto mais folgado. O registro de quem morreu e não saiu do cadastro é problema conhecido e antigo, e o dado mostra que ele **diminuiu** de 2022 para 2026, não que cresceu.

**Veredito proposto:** não sustentado (critério de comportamento: o comparecimento de quem tem biometria ficou igual, e o dos centenários caiu de 0,90% para 0,72% no 1º turno). O "que fecharia" continua certo: o cruzamento com os óbitos (SIRC) e o comparecimento por idade do 2º turno. A frase do resumo deveria ser *"o cadastro tem registros de pessoas que provavelmente já morreram, menos que em 2022, e eles quase não votam"*.

## 3. H23: Joaçaba e a Região dos Lagos se comportam como o resto do próprio estado

**O que o projeto diz.** *"A conta fecha"* e, ainda assim, *"Compatível com as duas"*, com a visão da fraude dizendo que é *"o Lula com quase todos os votos que estavam em disputa"*.

**A objeção.** O teste que falta é perguntar se essas cidades fogem do padrão **do próprio estado**. Não fogem:

- Ajustando o ganho do Lula e do Flávio entre os turnos, município a município do RJ, pelos votos do 1º turno de cada outro candidato, pela queda de branco e nulo e pela variação do comparecimento (regressão simples sem os 7 municípios, usada só para prever), a Região dos Lagos teria: **Lula +28.734 (real: +28.624)** e **Flávio +1.365 (real: +1.476)**. Os coeficientes são instáveis (os candidatos andam juntos entre municípios), então o que vale é a previsão, não cada coeficiente. Com o Brasil inteiro no ajuste, a previsão erra mais (Lula +23.349, Flávio +6.750), o que só mostra que o RJ inteiro se moveu, não a região.
- Parte do ganho que foi para o Lula: Araruama 99,8%, no percentil 86 dos 92 municípios do RJ com ganho, e a mediana do RJ é 88,1%. **Joaçaba: 55,4%, exatamente a mediana de SC** (295 municípios).
- No Brasil, 423 de 3.203 municípios com ganho acima de 500 votos deram 95% ou mais do ganho ao Lula.

**A frase "quase todos" é exagero.** No Brasil, o Lula ficou com 73,7% do que os dois ganharam entre os turnos (+10.333.927 contra +3.693.941), o mesmo "74%" do vídeo 19. "Quase todos" vale para Araruama, que é um município típico do RJ.

**Veredito proposto:** não sustentado. A pergunta de fundo (por que os votos dos outros foram tanto para o Lula) é do vídeo 19 e não ganha nada com esses casos.

## 4. A conclusão e o resumo simples deixam de pé exatamente o que se explica

**O que o projeto diz.** Na conclusão: *"ficam de pé, a conferir, o cadastro com mortos (sem voto em escala), o salto do comparecimento de 95 a 99 anos, a subida dos avisos 'já votou' seguidos de liberação manual e o Lula com quase todos os votos em disputa (vídeo 19)"*. No `RESUMO_SIMPLES.md`, a terceira das "três coisas mais importantes" é *"Há mortos no cadastro"*, e o fecho repete *"o salto do comparecimento de quem tem 95 a 99 anos, os avisos 'já votou' seguidos de liberação manual"*.

**A objeção.** Os quatro itens são os das objeções 1 a 3, e todos têm a explicação inocente no dado do próprio projeto. Mantê-los como "a conferir" é o tipo de frase que o público lê como "acharam alguma coisa". A frase sobre os mortos aparece entre as três mais importantes sem a comparação que a desarma (era pior em 2022). **Gravidade alta**, porque é o que vai para o vídeo e para o título dos cortes.

**Proposta:** "a conferir" fica só com o que depende do TSE (a lista de quem votou, o cruzamento com os óbitos, a assinatura de cada boletim) e com o caso individual de Campinas e Valinhos.

## 5. H18: o número de seções em que o Flávio caiu precisa do espelho de 2022

**O que o projeto diz.** *"O Flávio ficou abaixo do próprio 1º turno em 82.155 seções (e o Lula em 9.575); em 53,5% delas o comparecimento também caiu."* Lido sozinho, "82.155" e "só metade com queda de comparecimento" soam como sinal.

**O espelho que falta** (`s2022_t1.parquet` e `s2022_t2.parquet`, 471.010 seções casadas):

| | Seções abaixo do próprio 1º turno | Votos perdidos nelas | Com queda de comparecimento | Seções com queda de comparecimento, todas |
|---|---|---|---|---|
| Lula, 2022 (venceu) | **88.885** | 458.329 | 69,4% | 38,4% |
| Bolsonaro, 2022 | 14.670 | 52.729 | 81,3% | 38,4% |
| Flávio, 2026 | 82.155 | 382.939 | 53,5% | **19,8%** |
| Lula, 2026 | 9.575 | n/d | 93,8% | 19,8% |

Em 2022 o vencedor ficou abaixo do próprio 1º turno em mais seções do que o Flávio em 2026, e ninguém tratou isso como troca de voto. E os 53,5% têm de ser lidos contra a base: só 19,8% de todas as seções tiveram queda de comparecimento em 2026, então a queda do Flávio se concentra 2,7 vezes mais onde menos gente foi votar. As outras 38.226 seções (126.384 votos) são compatíveis com eleitor que mudou de lado, que é comportamento comum entre turnos.

**Proposta:** manter o veredito e pôr o espelho de 2022 no texto.

## 6. H19: "perdeu votos em 6 estados e o outro em nenhum" já aconteceu em 2022, com os lados trocados

**O que falta.** O relatório explica com o comparecimento (certo), mas não mostra que o padrão é recorrente. Em 2022, entre os turnos, o **Lula perdeu votos no AM (-14.693), no AP (-7.464), no AC (-7.456) e em RR (-1.632)**, e o Bolsonaro não perdeu em nenhum estado; o comparecimento caiu em 12 UFs (AC, AL, AM, AP, MA, MS, PA, PI, RO, RR, SE, TO). O Norte perde comparecimento no 2º turno, e quem perde voto lá é quem tem mais voto a perder naquele dia. Em 2022 foi o vencedor.

**Proposta:** desmentido como sinal de fraude (a alegação é que a assimetria seria prova; o histórico mostra a mesma assimetria numa eleição que a mesma visão não contesta do mesmo jeito do outro lado).

## 7. H10: o teto de 502.317 votos é a soma das seções, não o que elas poderiam ter mudado

**O que o projeto diz.** *"Teto do pior caso: todos os votos nominais dessas seções somam 502.317."* É 11,3% da diferença, o maior "teto" de toda a tabela, e aparece na tabela-resumo ao lado de tetos de 0,01% a 0,78%. Quem lê a tabela entende que a troca de urna "poderia ter movido" 11% da diferença.

**A objeção.** O teto das outras hipóteses é o que a fraude poderia ter mexido, não o total dos votos envolvidos. Aqui o projeto mediu a diferença contra as vizinhas do mesmo local: -0,098 ponto no ganho do Lula (1.727 locais). Aplicada aos 502.317 votos, dá **cerca de 492 votos, no sentido contrário ao Lula** (0,01% da diferença). Mesmo com o teto conservador de "toda a seção", a coluna deveria dizer que são votos dados, contados e iguais aos das vizinhas.

**Proposta:** teto = "a diferença contra as vizinhas, cerca de 492 votos e contra o Lula"; o total de 502.317 fica no texto, não na coluna do teto.

## 8. H03: o número que o projeto soma é maior que o da alegação, e falta o contexto da cobertura de biometria

**O que o projeto diz.** *"O número existe: 8.615.564 [...] e mais 7.242.863 sem digital cadastrada [...] (12,42% dos votos, somando os dois)."* O leitor sai com "15,9 milhões sem biometria", um número quase o dobro do da alegação, produzido pelo projeto.

**A objeção.** Os 7,24 milhões não são liberação no lugar da biometria: são eleitores que **não têm digital no cadastro** e se identificam pelo ano de nascimento, como sempre. O contexto que fecha (`eleitorado_idade.csv`): em 2026, 16.747.631 eleitores (10,6%) não têm biometria cadastrada, e os votos desse tipo foram 5,67% do total, coerente com um grupo mais idoso, que vota menos. Em 2022 eram 37.734.619 eleitores sem biometria (24,2%). A cobertura subiu de 75,8% para 89,4%; o voto sem a digital do eleitor tende a ter caído, não subido. O número de 2022 do Jornal Razão (10.011.347) segue sem recálculo, e o projeto deveria dizer isso no texto, não só no JSON.

**Proposta:** manter "não sustentado", separar os dois números (o da alegação é o primeiro) e pôr a cobertura de 2022 e 2026 ao lado.

## 9. H09 e H10: teste de comportamento classificado como "arquivos"

Pelos pesos do vídeo 16, "arquivos" pesa menos porque *"bater é o esperado nas duas visões"*. Mas os testes que decidem H09 (o voto por modelo de urna, e a urna antiga contra a nova no mesmo local) e H10 (a seção com urna trocada contra a vizinha no mesmo local) são comparações de **comportamento do voto**, as mesmas que decidem H01 e H03 com peso maior. Com a etiqueta errada, duas refutações diretas contam menos na conclusão. O mesmo vale em parte para H18 (o Flávio contra o próprio 1º turno é comportamento; o teste de integridade é arquivo). **Proposta:** H09 e H10 em "comportamento"; H18 com os dois critérios separados.

## 10. H04, H06 e H11: o dado contradiz a alegação e o veredito ficou um degrau abaixo

- **H04** (*"a assimetria prova manipulação"*): em 2022 a assimetria era maior (9.424 contra 199), em 2018 também (14.958 contra 1.298), e 99,6% das seções do Lula acima de 90% já davam mais de 80% para ele em 2022. A conclusão da alegação é contrariada pelo dado: desmentido.
- **H06** (*"só soltou os boletins na quarta"*): o boletim foi afixado na seção em 25/10 e os arquivos por seção estavam públicos pelo menos desde 26/10, 7h30. A única parte verdadeira (a data no catálogo) não é a alegação: desmentido.
- **H11**, no caso que circulou (Teixeira de Freitas): as 303 seções dão o resultado publicado. Para o caso, desmentido; "não sustentado" vale para a hipótese geral enquanto a assinatura não for verificada.

## 11. H20: a frase da visão da fraude sugere o que o texto nega

*"A queda sem precedente é real; o que ela não tem é marca de voto acrescentado."* A primeira metade, sozinha, vira corte. A abstenção caiu em 4 das 5 regiões e subiu no Norte, o que é o desenho de mobilização, não de acréscimo uniforme. **Proposta:** *"a abstenção caiu mais que em qualquer 2º turno anterior (vídeo 19), em quase todo o país e dos dois lados, e não deixou marca de voto acrescentado (H03, H15, H16)"*.

## 12. H16: o número das 17h que está no JSON e não está no texto

O `RESUMO.json` mostra a parte manual do 2º turno às 17h em 16,3% (contra 12% a 13% nas outras horas). Ele não aparece no relatório, e quem defende a fraude vai achá-lo. São **124 de 763 votos** da amostra naquela hora. No Brasil, pelo log, as liberações manuais depois das 17h foram 5.472 de 34.393 votos (15,9%), ou **0,12% da diferença** mesmo que todas fossem falsas. **Proposta:** pôr o número e o teto no texto da H16, em vez de deixá-lo para ser descoberto.

## 13. H17: a soma das UFs na última versão gravada não fecha, e há uma razão simples

No `RESUMO.json`, a soma das UFs e do exterior na última versão gravada dá Lula 64.249.830 e Flávio 59.822.856, contra o nacional de 64.256.232 e 59.826.041 (faltam 6.402 e 3.185). O `HIPOTESES.md` prometia conferir se *"a soma por estado com o exterior fecha o total nacional em cada arquivo"*, e o relatório não fala disso. A razão está nos próprios arquivos: a última captura de 5 UFs foi antes de 100% das seções (AM 99,99%, BA 99,99%, MA 99,98%, MG 99,93%, PA 99,99%), enquanto a nacional das 23h27 está em 100%. **Proposta:** dizer isso no texto e, se possível, refazer a soma só com versões de UF em 100%.

## 14. H14: a explicação inocente vem afirmada, e o espelho mais forte não aparece

*"É o eleitor que mora fora e mantém o título na cidade de origem"* vem sem teste. O que sustenta o veredito é a comparação com 2022 (596 municípios contra 579). Há um espelho mais forte no próprio dado: o **eleitorado** maior que a população de 16 anos ou mais aparecia em **3.805 municípios em 2022** (população do mesmo ano) e em **2.898 em 2026** (população que teria 16 anos ou mais, sem migração nem mortes). **Proposta:** pôr o espelho e tratar "mora fora" como a explicação provável, não como fato medido.

---

## O que este advogado não contesta

Para registro, e para a terceira IA conferir: H01 e H02 (o erro de fuso do relatório pericial e os 34.393 votos depois das 17h), H05, H07, H08, H12 e H21 estão bem medidos e bem escritos, e os tetos de H01, H02 e H07 são honestos. O limite de H18 (uma troca que imitasse o eleitor não se separa por estatística) é verdadeiro e deve ficar.

## Vereditos propostos, se as objeções forem aceitas

| # | Hoje | Proposto |
|---|---|---|
| H13 | compatível com as duas | não sustentado |
| H15 | compatível com as duas | não sustentado |
| H23 | compatível com as duas | não sustentado |
| H04, H06 | não sustentado | desmentido |
| H19 | não sustentado | desmentido como sinal (com o espelho de 2022) |
| H09, H10 | critério "arquivos" | critério "comportamento" |

Com isso a contagem iria de 14 / 5 / 3 / 1 para 14 / 8 / 0 / 1 (não sustentado / desmentido / compatível / não testado). A terceira IA decide.

---

## Apêndice: como refazer as variantes

Rodado em 29/out/2026 a partir da raiz do projeto, com os arquivos de `dados/` sem alteração.

**Objeção 1 (H15), placebo nos logs da amostra.** Lê `dados/brutos/t2/amostra.sqlite` com o mesmo leitor do projeto (`hipoteses/log.py`), só as seções do grupo "sorteio" com mais de 50 votos no turno (as mesmas do `RESUMO.json`):

```python
import sys, sqlite3, re, bisect, collections, json
import pandas as pd
RAIZ = "."  # raiz do projeto
sys.path.insert(0, RAIZ)
from hipoteses.log import ler_jez, ler_log
RE_URL = re.compile(r"/dados/(\w\w)/(\d+)/(\d+)/(\d+)/")
DIAS = {"t1": "04/10/2026", "t2": "25/10/2026"}
am = pd.read_csv(RAIZ + "/dados/derivados/amostra_secoes.csv", dtype=str)
grupo = {tuple(x[:4]): x[4] for x in am.itertuples(index=False)}
con = sqlite3.connect(RAIZ + "/dados/brutos/t2/amostra.sqlite")
R = collections.defaultdict(collections.Counter)
for url, corpo in con.execute("SELECT url, body FROM raw WHERE status=200 AND url LIKE '%-log.jez'"):
    if "sorteio" not in (grupo.get(RE_URL.search(url).groups()) or ""):
        continue
    linhas = ler_jez(corpo)
    for turno, dia in DIAS.items():
        lt = ler_log(linhas, b"x", dia=dia)
        if len(lt.eleitores) <= 50:
            continue
        c = R[turno]
        ts = [e[0] for e in lt.eleitores]
        nb = sorted(e[0] for e in lt.eleitores if e[1] != "biometrica")
        c["votos"] += len(ts)
        for s in ts:  # placebo: depois de cada voto
            i = bisect.bisect_right(nb, s)
            c["placebo"] += i < len(nb) and nb[i] - s <= 300
        for s in lt.ja_votou:  # depois de cada aviso
            c["avisos"] += 1
            i = bisect.bisect_left(nb, s)
            c["aviso_nb_5min"] += i < len(nb) and nb[i] - s <= 300
            j = bisect.bisect_left(ts, s)
            if j < len(ts):
                c["prox_" + lt.eleitores[j][1]] += 1
print(json.dumps({t: dict(v) for t, v in R.items()}, indent=1))
```

**Objeção 2 (H13).** `comparecimento_idade.csv` (1º turno, sem `zz`) dividido por `aptos` e por `com_biometria` de `eleitorado_idade.csv`, por faixa e ano; Censo 2022 idade por idade somado das séries municipais de `dados/brutos/ibge/censo2022_9514_86_a_95.json` e `..._96_ou_mais.json`; o número de municípios de 2022 compara os eleitores de 100 anos ou mais de 2022 com os centenários do Censo 2022 por município (`cd_ibge` de `presidente_municipio.csv`).

**Objeção 3 (H23).** `presidente_municipio.csv`: ganho = votos do 2º turno menos os do 1º; regressão de mínimos quadrados sem constante, nos municípios do RJ fora os 7 da região, do ganho de cada candidato sobre `caiado_1t`, `zema_1t`, `cury_1t`, `renan_1t`, `outros_1t`, a queda de branco e nulo e a variação do comparecimento; previsão somada nos 7 municípios. Percentis: parte do ganho que foi para o Lula entre os municípios do estado com ganho positivo.

**Objeções 5 e 6 (H18, H19).** `s2022_t1.parquet` e `s2022_t2.parquet` casados pela chave (uf, município, zona, seção), sem `zz`; a base de 2026 sai de `ferramentas/analise.py:base()`.

**Objeção 7 (H10).** 502.317 × 0,00098 (a diferença de -0,098 ponto no ganho, do `RESUMO.json`).

**Objeção 8 (H03).** `eleitorado_idade.csv`, soma de `eleitores` e `com_biometria` por ano, sem `zz`; votos por tipo de `analise.py:base()`.

**Objeção 13 (H17).** A última versão de cada UF em `dados/copias/noite/versoes-tse/`, com o campo `s.pst` (percentual de seções totalizadas).

**Objeção 14 (H14).** `eleitorado_idade.csv` somado por município e ano contra `pop_16_ou_mais` (2022) e `pop_12_ou_mais` (2026) de `ibge_municipio.csv`.
