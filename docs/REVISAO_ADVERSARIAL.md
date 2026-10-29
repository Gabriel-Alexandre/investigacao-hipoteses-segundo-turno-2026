# Revisão adversarial

**29/out/2026.** Três leitores revisaram a rodada 1, cada um com um papel, sem editar o projeto: o **advogado da visão da fraude** (`docs/revisao/ADVOGADO_DA_FRAUDE.md`), o **advogado da visão do resultado legítimo** (`docs/revisao/ADVOGADO_DO_LEGITIMO.md`) e o **auditor de método, conta e linguagem** (`docs/revisao/AUDITORIA_DE_METODO.md`). Os três foram feitos pela mesma IA em papéis separados; as contas que eles fizeram estão nos próprios arquivos. A rodada 2 aplicou o que está abaixo; o número de cada hipótese, depois da revisão, está no `RELATORIO.md`.

| Objeção | De quem | O que mudou na rodada 2 |
|---|---|---|
| O oeste do Amazonas fica 2 horas atrás de Brasília, não 1; votos depois das 17h dessas seções ficaram de fora | auditor | fuso pela hora de abertura de cada urna; os logs das 556 seções foram baixados e relidos (31 votos a mais depois das 17h); a validação tira o fuso do próprio log |
| Com o fuso certo, as seções que fecham até 17h00 ainda dão mais ao Flávio; "nasce de erro de fuso" diz demais | auditor | o texto de H01 dá esse número e explica (seções pequenas, sem fila); o veredito fica no teste do mesmo local e nos votos com hora depois das 17h |
| Os títulos parecem dizer que o fato é falso quando ele é certo | auditor e fraude | a tabela separa "o fato que circula" do "veredito sobre a fraude" |
| H14 sem a população total e sem o espelho de 2022 | auditor e legítimo | contra a população total: 120 municípios em 2026, 52 em 2022; 3 municípios do Piauí com mais votos do Lula que habitantes; veredito vira "compatível com as duas" |
| H15: o teto media a coisa errada, faltava a régua do voto qualquer e os avisos isolados | fraude e legítimo | teto de 113.315 avisos (2,56%); o que vem depois do aviso é comparado com o que vem depois de um voto qualquer; os avisos isolados (sem repetição em 2 minutos) entram, e subiram |
| H13: o teto estava no turno errado e o piso por município exagerava; o "salto" de 95 a 99 anos some pela biometria | fraude e legítimo | piso nacional (148.553 registros); 2022 comparado no mesmo turno; a taxa sobre quem tem biometria entra; veredito "não sustentado" para voto de morto em escala |
| H18 sem o espelho de 2022 e com teste de integridade sem tamanho; arquivo contra arquivo não pode desmentir | fraude e auditor | espelho de 2022 (Lula abaixo do próprio 1º turno em 88.885 seções); as quedas grandes do Flávio (3.250 seções) contra as do Lula em 2022 (1.148) ficam a conferir; o tamanho do teste de integridade no texto; veredito vira "compatível com as duas" |
| H21: a medida decide o veredito, e o dado do benefício não entrou | fraude e auditor | as duas medidas no texto e no gráfico; veredito "não testado nesta rodada" |
| H23: "a conta fecha" e "compatível" se contradiziam | legítimo | comparação com os municípios do RJ de votação parecida no Flávio (85,0% do saldo contra 95,1% na Região dos Lagos, 3.025 votos acima) e com SC (Joaçaba na mediana); veredito "compatível com as duas", com teto |
| H10: o teto era a soma de todos os votos | legítimo | teto pela diferença contra as vizinhas (246 votos) |
| H04 e H06 deveriam ser "desmentido"; H06 tinha datas escritas à mão | legítimo e auditor | os dois viram "desmentido"; as datas de H06 saem de `ferramentas/linha_do_tempo.py` |
| H09 e H10 testam comportamento, não arquivo | legítimo | critério trocado |
| H08: o sorteio usava a parte do Lula em todos os nominais | auditor | o sorteio usa a divisão Lula e Flávio de cada seção no 1º turno; o resultado (abaixo do acaso) não muda |
| 2018 entrava com o exterior e 2026 não | auditor | o exterior sai dos três anos |
| A reconciliação não tinha a causa exata | auditor | os 798 votos são as 27 seções do exterior apuradas pelo sistema de apuração |
| A conclusão dizia "nenhuma das 23" | fraude e auditor | a conclusão conta as testadas, nomeia as compatíveis e soma o pior caso de todos os caminhos ainda abertos (8,63% da diferença) |
| O controle "dentro do mesmo local" e "contra o 1º turno" não pega fraude que atinja o lugar inteiro | fraude | entra como limite no topo do relatório; o advogado da fraude mediu, por município, que o ganho do Lula sobe com a parte de votos depois das 17h quase só por tamanho de cidade (sobra +0,41 ponto com UF e tamanho controlados, e nada com 2022 como controle) |

**O que ficou como estava, e por quê:** H01, H02, H08, H12 e H17 continuam "desmentido", porque o fato alegado (o grupo das 17h, os 2,5 milhões como votos da prorrogação, os placares impossíveis, as seções fantasmas, o total do Flávio caindo no painel) é falso como foi dito; o que os arquivos não podem desmentir (uma fraude feita antes do boletim) está em H11 e H18, que ficam como "não sustentado" e "compatível com as duas".
