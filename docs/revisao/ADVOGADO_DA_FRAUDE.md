# Revisão adversarial: o advogado da visão da fraude

**29/out/2026, sobre a rodada 1** (`RELATORIO.md`, `resultados/RESUMO.json`, `ferramentas/analise.py`, `resultados/VALIDACAO.json`, `docs/HIPOTESES.md`).

**O papel.** Procurar, com a maior força possível e com honestidade, o que o projeto deixou de ver a favor da hipótese de fraude, onde ele descartou rápido demais e onde o veredito ficou mais forte que o número. Não é uma defesa de que houve fraude: quando a conta que eu fiz enfraqueceu a visão da fraude, isso está escrito na seção 3.

**De onde saem os números.** Os números com "calculado aqui" foram feitos por mim, com scripts fora do repositório, lendo só `dados/copias/`, `dados/derivados/` e os logs da amostra em `dados/brutos/t2/amostra.sqlite` (o mesmo leitor `hipoteses/log.py`). Nenhum arquivo do projeto foi alterado. O que eu não calculei está dito como não calculado.

---

## 1. As objeções, em uma tabela

| # | Hipótese | Objeção | Gravidade |
|---|---|---|---|
| 1 | H11, H17, H18 (e a conclusão) | O veredito contradiz a régua do próprio projeto: se "bater é o esperado nas duas visões", um teste que só confere arquivo do TSE contra arquivo do TSE não pode dar "não sustentado" nem "desmentido". E são exatamente os únicos caminhos cujo teto poderia passar da diferença | alta |
| 2 | H15 | O teto (19.830 votos) mede a coisa errada; pela história da própria alegação, o voto roubado é o que veio **antes** do aviso. E os avisos que não são repetição subiram 44% do 1º para o 2º turno, sinal que o projeto não viu | alta |
| 3 | H13 | Há pelo menos 148.553 registros de 100 anos ou mais sem pessoa viva possível, o número cresceu 62% desde 2022, o teto foi calculado no turno errado (o 1º) e o dado que decide (comparecimento por idade no 2º turno) não existe ainda | alta |
| 4 | H18 | O teste do Flávio "abaixo do 1º turno" não tem controle de 2022 no projeto; com o controle, a taxa geral é igual, mas as **quedas grandes** do Flávio com comparecimento estável são 2,2 a 2,8 vezes as do Lula em 2022. E o teste de integridade citado auditou 389 votos | média |
| 5 | H21 | O veredito depende da medida: em pontos o Lula cresceu mais nas cidades ricas; na parte do saldo, ele ficou com 102% do saldo nas cidades mais pobres e 68% nas mais ricas. E o dado do benefício não entrou; o certo é "não testado" | média |
| 6 | H17 | Os 165.699 votos "sem origem" não aparecem no relatório; o descompasso entre o painel nacional e a soma das UFs chegou a 1,42 milhão na noite, há uma janela de 1h55 sem versão nacional, e a soma final não fecha por 6.402 votos (explicável, mas não explicado) | média |
| 7 | H01, H09, H10, H03 | O controle "dentro do mesmo local" e o "contra o próprio 1º turno" apagam uma fraude que atinja o local inteiro ou os dois turnos; no nível do município, o ganho do Lula sobe com a parte de votos depois das 17h (5,21, 6,71, 7,47 pontos) | média |
| 8 | H16 | A hora das 17h é a exceção que o texto apaga ("entre 12% e 13% em quase todas as horas"): 16,3% de liberação sem digital na amostra e 15,91% na população, contra 11,97% no 1º turno; e o projeto usou a amostra onde o log do 2º turno inteiro existe | baixa |
| 9 | H02, conclusão | Rótulos mais fortes que o número: H02 é "desmentido" embora os 2,5 milhões confiram (2.537.055); a conclusão diz que nenhuma hipótese mostrou a marca, com 3 "compatível com as duas", 1 não testada e 2 com teto não medido | média |
| 10 | H03 | Teste de baixa potência feito na amostra quando a população do 2º turno estava nos dados; a referência de 2022 é de terceiro e não foi recalculada | baixa |

---

## 2. As objeções, uma a uma

### Objeção 1 · H11, H17, H18: o veredito contradiz a régua do próprio projeto (alta)

**A régua.** O `PLANO.md` (item 4) e o relatório dizem que o critério "arquivos das urnas" pesa menos porque *"bater é o esperado nas duas visões"*. Se o resultado esperado é o mesmo nas duas visões, o teste não separa as duas, e o veredito honesto é **compatível com as duas** (ou não testado), nunca "não sustentado" ou "desmentido".

**Onde isso quebra.**

- **H11 (boletim de papel × site).** O único teste de escala é o BU contra o "detalhe por seção" dos dados abertos: dois produtos do mesmo TSE, gerados do mesmo boletim (497.897 seções, zero diferença). Teixeira de Freitas bateu com o Aos Fatos, que também soma o arquivo do TSE. Nenhuma foto de boletim de papel foi comparada e a assinatura digital não foi verificada (o próprio relatório diz). A visão da fraude ("boletim trocado na totalização") prevê exatamente o que foi observado: arquivos do TSE batendo entre si. Veredito defensável: **não testado** (teto: não medido).
- **H17 (sala-cofre, 165 mil, Flávio perdendo votos).** "Desmentido" se apoia em duas coisas: o total nunca caiu (346 versões) e a última versão é igual à soma das seções. A segunda só vale se as seções forem as verdadeiras, que é a H11, não verificada. Uma totalização adulterada que gravasse os boletins já mexidos passa nos dois testes. O próprio texto diz *"O que fecharia: já fechado pelo boletim de cada seção (H11)"*, ou seja, a H17 herda a H11 aberta.
- **H18 (o programa troca o voto).** O `HIPOTESES.md` diz que *"uma troca que imitasse o comportamento do eleitor não se separa por estatística"*. Mesmo assim saiu "não sustentado", com o teto "não medido". O apoio externo é o teste de integridade: **389 votos auditados no TSE** e 33 urnas no TRE-SP (`docs/pesquisa/TEORIAS_NA_INTERNET.md`), contra 497.897 seções. É evidência real, mas pequena e feita pelo próprio órgão.

**Por que é a objeção mais forte.** Somei os tetos de todos os caminhos que acrescentam voto, cada um na leitura mais generosa para a fraude: votos depois das 17h (34.393), todos os registros de 100 anos ou mais sem pessoa viva possível votando (148.553, objeção 3), todo aviso "já votou" como voto roubado (113.315, objeção 2), as quedas grandes do Flávio como troca (23.747 votos, que valem o dobro na diferença: 47.494, objeção 4). Dá cerca de 343 mil votos, **7,8% da diferença**. Ou seja: nenhum caminho de voto acrescentado chega perto dos 4.430.191. Os únicos caminhos que, em tese, chegariam são o programa (H18) e a totalização (H11, H17), e são justamente os três em que o projeto não tem teste que separe as visões. Rotular esses três como "não sustentado" e "desmentido" passa ao leitor uma segurança que o dado público não dá.

**Variante proposta.** H11: **não testado**; H17: **desmentido no que é dado público** (o total nunca cai, o descompasso dos painéis é de horário, ver objeção 6), **não testado** na parte da contagem; H18: **compatível com as duas**, critério "arquivos", com o teto escrito como "não mensurável por estatística".

**O que fecharia.** Verificar a assinatura de cada BU com a chave pública do TSE (já está no plano); o convite público de fotos de boletim de papel; os hashes de lacração contra os hashes no log de cada urna (público); o relatório consolidado do teste de integridade das 27 UFs.

### Objeção 2 · H15: o teto mede a coisa errada, e há um sinal que o projeto não viu (alta)

**O teto.** O projeto escreve: *"se todo aviso seguido de liberação manual fosse um voto roubado, cerca de 19.830 votos"* (113.315 × 17,5%). Mas a alegação é *"cheguei e já tinham votado por mim"*: o voto falso aconteceu **antes** do aviso, e o aviso é o rastro do eleitor verdadeiro. O voto liberado pelo mesário nos 5 minutos **seguintes** não tem relação com a história. No pior caso da própria alegação, cada aviso que não é repetição é um voto roubado:

| Teto, pela leitura da alegação | Votos | Parte da diferença |
|---|---|---|
| todo aviso do 2º turno (o projeto mostra o número, não usa como teto) | 113.315 | 2,56% |
| só os avisos que não são repetição (calculado aqui, ver abaixo) | cerca de 72.500 | 1,64% |
| o excesso de avisos que não são repetição sobre a taxa do 1º turno (calculado aqui) | cerca de 20.400 | 0,46% |

E um limite que o projeto não diz: quem teve o voto roubado e **não foi votar** não deixa aviso nenhum. Esse caminho não tem teto pelo log.

**O sinal novo (calculado aqui, amostra sorteada, 11.879 seções no 1º turno e 12.000 no 2º).** Separei cada aviso pelo tempo desde o último voto computado na seção. Aviso até 60 segundos depois de um voto é quase sempre repetição (o eleitor que acabou de votar, ou o mesário que digitou de novo):

| | 1º turno | 2º turno |
|---|---|---|
| avisos | 2.484 | 2.686 |
| repetição (até 60 s depois de um voto) | 1.294 (52,1%) | 967 (36,0%) |
| **não repetição** | **1.190** (399 por milhão de votos) | **1.719** (558 por milhão de votos) |
| isolados (nenhum voto nos 180 s anteriores) | 677 (27,3%) | 1.053 (39,2%) |
| isolados antes das 17h (hora local) | 193 | 513 |

A parte de avisos isolados subiu 12,0 pontos (bootstrap por seção, 2.000 sorteios: de 8,4 a 15,7 pontos). Os avisos que não são repetição subiram 40% por voto e 44% em número. A visão da fraude espera exatamente isso: mais gente chegando e achando o voto já dado. Há explicação legítima possível que eu **não testei**: com o voto concentrado de manhã no 2º turno, a tarde fica vazia, e o eleitor que volta depois de alguns minutos aparece "isolado" com mais facilidade; e digitação errada que cai num eleitor que já votou fica mais provável quando mais gente já votou. O projeto não separou repetição de não repetição, que é o recorte que a alegação pede.

**Um padrão estranho no fim do dia (calculado aqui).** Depois das 17h (hora local), o 2º turno teve 561 avisos "já votou" na amostra para só 719 votos (no 1º turno: 743 avisos para 84.647 votos). Em 51 seções houve 3 ou mais avisos depois das 17h; no log de uma delas (RN), o mesário digita CPFs em sequência entre 17h00 e 17h04 e recebe "já votou" e "identificador inválido" seguidos. A leitura da fraude seria o mesário tentando votar por quem faltou. **O que pesa contra:** nessas 51 seções houve 2 votos depois das 17h, nenhum liberado sem digital. As tentativas não viraram voto. Fica como padrão a explicar (procedimento de encerramento, justificativa, registro de mesário), não como sinal de voto.

**O que eu testei e não ajuda a fraude, honestamente.** (a) A subida do aviso seguido de liberação manual (12,7% para 17,5%), que o projeto deixou "a conferir", é explicada pelo ritmo de votação: a chance de vir um voto sem digital nos 5 minutos depois de **qualquer** voto foi de 19,7% para 26,2% (×1,33), quase a mesma subida (×1,38); e nos dois turnos o aviso fica **abaixo** do acaso. (b) Na população do 2º turno (497.877 seções), dentro do mesmo local, a parte de avisos não anda com o ganho do Lula (r = −0,0003) nem com a subida do comparecimento (r = −0,003); as 243 seções com 10 ou mais avisos deram ganho de 6,49 pontos ao Lula, contra 6,53 no Brasil.

**Variante proposta.** Manter "compatível com as duas", trocar o teto por 113.315 (2,56%) como pior caso e cerca de 72.500 (1,64%) sem as repetições, e trocar o "a conferir" (aviso seguido de manual, já explicado pelo ritmo) pelo sinal que sobra: a subida dos avisos que não são repetição.

**O que fecharia.** A ata de cada seção com aviso (o mesário registra o eleitor que não pôde votar) e o caderno de votação, com o TRE; a lista de quem votou, com o TSE.

### Objeção 3 · H13: o cadastro inflado ficou com destaque menor e o teto está no turno errado (alta)

**O que o dado mostra (do `RESUMO.json` e calculado aqui).**

| | 2022 | 2026 |
|---|---|---|
| eleitores de 100 anos ou mais | 184.330 | **297.977** (+62%) |
| pessoas de 96 anos ou mais no Censo 2022 (as únicas que podem ter 100 em 2026) | | 149.424 |
| registros de 100 ou mais **sem pessoa viva possível** (mínimo, sem contar morte nenhuma desde 2022) | | **pelo menos 148.553** |
| eleitores de 95 a 99 anos | 466.703 | 337.136 |
| comparecimento de 95 a 99 (1º turno) | 7.434 (1,60%) | 14.661 (4,35%) |

O número de 148.553 é um piso: ele supõe que nenhuma das 149.424 pessoas de 96 anos ou mais morreu em quatro anos. Não calculei a sobrevivência (precisaria de tábua de vida por idade simples), mas qualquer mortalidade aumenta o número de registros fantasmas.

**As objeções.**

1. **O teto está no turno errado.** O relatório escreve *"se todo voto de 95 anos ou mais do 1º turno de 2026 fosse falso: 16.802 votos"*. A eleição contestada é o 2º turno, e o comparecimento por idade do 2º turno não foi publicado. Pela leitura da fraude, o teto honesto é o estoque de registros sem pessoa viva: **148.553 votos, 3,35% da diferença**, se todos tivessem "votado" pelo mesário no 2º turno. É improvável, mas é o pior caso que a alegação admite, e é maior que o teto de 16.802.
2. **O cadastro piorou, não melhorou.** O projeto chama de "cadastro que demora a tirar quem morreu", mas o estoque de centenários cresceu 62% em quatro anos, enquanto a população que pode ser centenária é a metade dele. Isso é um fato de destaque, não uma nota.
3. **O salto de 95 a 99 é o único teste com dado, e ele aponta para cima.** O comparecimento quase triplicou em taxa (1,60% para 4,35%, mesmo turno) e dobrou em número (7.434 para 14.661), com 129.567 registros a menos na faixa.

**O que eu testei e pesa contra a fraude, honestamente.** (a) O salto não é só da faixa de 95 a 99: o comparecimento do 1º turno subiu de 2022 para 2026 em todas as faixas idosas (90 a 94: de 6,64% para 13,47%; 85 a 89: de 15,57% para 24,32%; 80 a 84: de 26,80% para 37,16%), em gradiente com a idade; (b) os eleitores de 95 a 99 com biometria dobraram (45.591 em 2022, 93.734 em 2026), e biometria exige a pessoa presente; (c) o arquivo de 2022 não tem eleitor de 95 anos ou mais no DF (0 aptos), então parte do salto nacional é falha do arquivo: Brasília passou de 0 para 351 votos dessa faixa, de um salto total de 4.763; (d) o comparecimento de 100 anos ou mais **caiu** (1,13% no 2º turno de 2022, 0,72% no 1º de 2026). O veredito "compatível com as duas" está certo; o que está errado é o teto e o destaque.

**O que fecharia.** O comparecimento por idade do 2º turno de 2026 (TSE, ainda não publicado: o projeto deveria rodar de novo quando sair) e o cruzamento do cadastro com os óbitos do SIRC (pedido por LAI). Dá para fazer já: por município, o comparecimento de 100 anos ou mais no 1º turno contra a razão entre eleitores centenários e pessoas de 96 ou mais (não calculei).

### Objeção 4 · H18: o controle de 2022 que faltou, e a cauda que ele revela (média)

O projeto mostra que o Flávio ficou abaixo do próprio 1º turno em 82.155 seções e que em 53,5% delas o comparecimento caiu. O `HIPOTESES.md` diz que a marca da troca seria *"o Flávio cai abaixo do 1º turno em seções onde nada mudou no comparecimento"*. São as outras 46,5%: **38.226 seções e 126.384 votos** (calculado aqui), que o relatório não destaca. O projeto não comparou com 2022, quando o líder do 1º turno também perdeu o 2º.

**Calculado aqui, a mesma conta nos dois anos (seções do Brasil casadas entre os turnos):**

| | 2026, Flávio | 2022, Lula (o líder do 1º turno) |
|---|---|---|
| seções com comparecimento igual ou maior que no 1º turno | 80,2% | 61,6% |
| entre elas, o líder do 1º turno perdeu voto | **9,57%** | **9,37%** |
| líder perdeu voto com o comparecimento subindo 5 ou mais | 19.789 seções | 8.448 seções |
| **queda grande** (perdeu 10% ou mais de pelo menos 30 votos, comparecimento estável ou maior) | **3.092 seções, 23.747 votos** | **1.095 seções, 9.983 votos** |

Na taxa geral, 2026 é igual a 2022, o que enfraquece a fraude. Na cauda das quedas grandes, 2026 tem 2,8 vezes mais seções (2,2 vezes, se eu corrigir pela parte maior de seções com comparecimento estável em 2026). É uma cauda pequena: tratada como troca, ela vale 47.494 votos na diferença (1,07%). Mas é o tipo de cauda que o projeto disse que procuraria, e não procurou.

**Variante proposta.** Veredito "compatível com as duas" (ver objeção 1), com a cauda descrita e o espelho de 2022 na tabela.

**O que fecharia.** O local de votação e o modelo da urna dessas 3.092 seções contra as vizinhas (não calculei); os hashes de lacração no log delas (precisa do log de cada uma).

### Objeção 5 · H21: a medida escolhida decide o veredito, e o dado do benefício não entrou (média)

O relatório conclui *"o crescimento veio mais de onde o benefício pesa menos"* porque o Lula cresceu mais **pontos** nos municípios ricos (7,27) que nos pobres (4,45). Mas nos municípios pobres o Lula partia de 69,5% no 1º turno: há teto para crescer em pontos. Medindo **para onde foi o saldo do 1º para o 2º turno** (votos que o Lula ganhou sobre a soma do que os dois ganharam), a ordem se inverte (calculado aqui, quintis de renda do Censo 2022):

| Quintil de renda | Lula no 1º turno | Parte do Lula no saldo | Subida do comparecimento |
|---|---|---|---|
| 1 (mais pobre) | 69,5% | **102,1%** (o Flávio perdeu voto líquido) | −0,09% |
| 2 | 62,1% | 90,1% | 1,73% |
| 3 | 45,5% | 78,8% | 2,03% |
| 4 | 37,8% | 71,2% | 2,34% |
| 5 (mais rico) | 37,7% | 67,6% | 3,12% |

Nenhuma das duas medidas testa compra de voto: a renda é um substituto do benefício, a análise é por município (ecológica) e o voto dos outros candidatos nas cidades pobres pode já ser mais próximo do Lula. O ponto é que o veredito "não sustentado" se apoia numa medida que, trocada por outra igualmente razoável, aponta na direção contrária.

**Variante proposta.** **Não testado nesta rodada**, como a H22, até entrar o dado de beneficiários por município (Bolsa Família, Pé-de-Meia) com 2022 como controle.

### Objeção 6 · H17: os 165.699 votos não aparecem, e o descompasso dos painéis ficou sem explicação escrita (média)

A alegação T6 (`TEORIAS_NA_INTERNET.md`) é: somando os estados e o exterior no painel, faltam 165.699 votos do Lula em relação ao total nacional. O relatório da H17 não menciona o número. Com os 2.554 arquivos da noite, refiz a conta: a cada versão nacional, o total nacional menos a soma da última versão de cada UF publicada até aquele instante (calculado aqui):

- às 19h17min06 a diferença do Lula era 164.784 (o número da alegação é desse tamanho);
- o máximo da noite foi **1.419.782** votos do Lula e 1.346.137 do Flávio;
- só em 2 das 345 versões nacionais a diferença foi zero para os dois;
- entre a 1ª versão nacional (17h07, 0,29% das seções) e a 2ª (19h01min56) há **1h55 sem versão nacional**, a janela do bloqueio de recebimento de boletins durante a prorrogação (fala do presidente do TSE no `TEORIAS_NA_INTERNET.md`);
- na última versão, a soma das UFs fica 6.402 votos abaixo no Lula e 3.185 no Flávio. Conferi: a diferença é exatamente o que falta nas últimas versões capturadas de MG (5.150 e 2.798), MA, PA, BA e AM, que foram gravadas antes de chegar a 100%. É falha de captura, não de soma.

O descompasso tem a cara de horário de publicação (o nacional fica sempre à frente da soma das UFs, e fecha no fim), e isso favorece a visão legítima. Mas o projeto tinha o dado, não fez a conta e chamou de "desmentido" sem mostrá-la; e o `RESUMO.json` guarda a diferença de 6.402 votos sem nenhuma nota. Quem levanta a alegação vai achar esses números e vai dizer que o projeto escondeu.

**Variante proposta.** Pôr no relatório a série "nacional menos soma das UFs" e a explicação da diferença final, e separar a parte da janela de 1h55, que nenhum arquivo público cobre.

### Objeção 7 · O controle "dentro do mesmo local" e o "contra o 1º turno" apagam a fraude que atinge o lugar inteiro (média)

Os testes de H01, H09 e H10 comparam seções **vizinhas no mesmo local de votação**, e os de H03, H09, H10 e H18 usam o **1º turno da mesma seção** como controle. Os dois são bons contra confusão, mas cada um tem um ponto cego: uma fraude que atinja o local, a zona ou o município inteiro some no primeiro; uma fraude que estivesse nos dois turnos some no segundo.

**Calculado aqui, no nível do município (o que o controle por local não vê), H01:**

| Parte dos votos do município com hora depois das 17h | Municípios | Ganho do Lula do 1º para o 2º turno |
|---|---|---|
| nenhum | 2.235 | 5,21 pontos |
| até 0,1% | 3.279 | 6,71 pontos |
| de 0,1% a 0,5% | 55 | 7,47 pontos |

Municípios com alguma seção fechada depois das 17h15: 7,22 pontos, contra 5,90 nos outros. A visão da fraude leria isso como a prorrogação valendo onde o Lula precisava.

**O que eu testei e enfraquece essa leitura, honestamente.** Boa parte é tamanho de cidade: dentro de cada décimo de eleitorado, os municípios com seção fechada tarde têm ganho **menor** em 7 dos 9 décimos comparáveis; dentro da mesma UF e do mesmo décimo de tamanho, sobra +0,41 ponto (141 células, sem erro calculado). Usando 2022 como controle (Lula de 2026 menos Lula de 2022 na mesma seção), dentro do mesmo local: seção fechada tarde −0,26 ponto (1.384 locais), urna antiga +0,10 (882 locais), urna de contingência −0,06 (1.581 locais). Nenhum sinal. E o teto de H01 e H02 não depende de controle nenhum: é a hora de cada voto no log (34.393 depois das 17h).

**Variante proposta.** Rodar cada teste também no nível da zona e do município (com controle de tamanho e renda) e com 2022 como segundo controle; e dizer no relatório o que cada controle não vê.

### Objeção 8 · H16: a hora das 17h é a exceção, e o texto a apaga (baixa)

O relatório diz que a liberação sem a digital do eleitor *"fica entre 12% e 13% em quase todas as horas"*. A própria tabela do `RESUMO.json` mostra **16,3% na hora das 17h** do 2º turno (124 de 763 votos da amostra), contra 12,0% no 1º. Na população (log do 2º turno inteiro, que o projeto tem): 5.472 de 34.393 votos depois das 17h, **15,91%**, contra 12,42% no dia; na amostra do 1º turno, depois das 17h, 11,97% (calculado aqui; a hora da amostra é a local e a da população é a de Brasília, então a comparação é aproximada). É exatamente o horário da prorrogação e o horário do "mesário pianista". O tamanho é pequeno: o excesso sobre a média do dia é de cerca de 1.200 votos (0,03% da diferença). Mas o texto deveria mostrar a exceção em vez de dizer que ela não existe.

A maior sequência de votos seguidos liberados pelo mesmo mesário também mudou: mediana de 1 no 1º turno e 2 no 2º (`RESUMO.json`), sem comentário no relatório. O máximo caiu (13 para 7), então não é rajada; fica sem explicação.

### Objeção 9 · Rótulos mais fortes que o número (média)

- **H02, "desmentido".** O número da alegação confere: 2.537.055 eleitores compareceram nas 8.848 seções fechadas a partir das 17h16. Errada é a leitura (comparecer numa urna aberta depois das 17h não é votar depois das 17h). O veredito certo é sobre a inferência; o texto deveria dizer *"o número confere, a conclusão não"*, porque "desmentido" faz parecer que o número foi inventado.
- **H03, "não sustentado".** Idem: os 8,6 milhões existem (8.615.564 pelo log).
- **A conclusão.** *"Nenhuma das 23 hipóteses mostrou a marca que a fraude deixaria no dado público"* convive com 3 hipóteses "compatível com as duas" (H13, H15, H23), 1 não testada (H22) e 2 com teto não medido (H11, H18). "Compatível com as duas" quer dizer que o dado não separa: não é ausência de marca, é marca ambígua. A frase honesta seria: *"Nenhuma mostrou marca de voto acrescentado em escala que chegue perto da diferença; três ficaram compatíveis com as duas visões, e o caminho do programa e da totalização não se testa com dado público."*

### Objeção 10 · H03: amostra onde havia população, e 2022 de terceiro (baixa)

O teste de H03 usa 11.864 seções sorteadas, porque precisa do 1º turno no mesmo log. Mas o log do 2º turno está agregado para 497.895 seções em `t2_secoes.parquet` (`log_manual_mesario`, `log_manual_sem_digital`), e a pergunta "a seção com mais liberação manual deu mais voto novo ao Lula?" se responde com a população inteira, usando o 1º turno da votação (não do log) como base. Também separa as duas liberações, que o projeto soma: a do mesário (8,6 milhões) e a sem digital cadastrada (7,2 milhões), que é onde estariam os registros antigos e de mortos.

**Calculado aqui, população, dentro do mesmo local:** parte liberada pelo mesário × ganho do Lula em pontos: r = −0,049 (o sinal é o contrário do que a fraude espera); parte sem digital cadastrada × ganho do Lula: r = +0,027, com inclinação de 0,0145 (10 pontos a mais de liberação sem digital, 0,15 ponto a mais de ganho do Lula; é pequeno e tem explicação legítima: jovem de 16 e 17 anos ainda sem biometria). As 111 seções com liberação pelo mesário 25 pontos acima do próprio local tiveram ganho do Lula 0,06 ponto **menor** que as vizinhas. A população confirma o resultado da amostra. A objeção é de método: o número de 2022 (10.011.347 sem biometria) é do Jornal Razão e não foi recalculado, e a frase "escala inédita não se sustenta" depende dele.

---

## 3. O que eu testei e não ajuda a visão da fraude

Para a revisão ser honesta, também ficam aqui as contas que fiz procurando sinal e que deram o contrário:

| Hipótese | O que eu calculei | Resultado |
|---|---|---|
| H07 | quantas seções sem voto do Flávio o acaso daria, pelo voto de cada uma no 1º turno (binomial, com o crescimento do Flávio por UF) | entre as seções em que o Flávio teve voto no 1º turno, o acaso dá cerca de 81 zeros; foram 56. Para o Lula, o acaso dá 3,1; foram 0. Há **menos** unanimidade que o acaso |
| H20 | para onde foi o comparecimento novo, dentro do mesmo local: votos ganhos por cada voto a mais de comparecimento | 2026: 0,55 para o Lula e 0,39 para o Flávio; 2022 (dentro do município): 0,53 para o Lula e 0,44 para o Bolsonaro. O eleitor novo se dividiu como em 2022, não foi quase todo para um lado |
| H20, nacional | parte do saldo que ficou com quem estava atrás no 1º turno | 2026: o Lula ficou com 73,7% (10,33 de 14,03 milhões); 2022: o Bolsonaro ficou com 69,8% (7,11 de 10,18 milhões) |
| H14 | eleitorado maior que a população com 16 anos ou mais, 2022 contra 2026 | 3.805 municípios em 2022, 2.898 em 2026. É verdade que o Lula fez 6,0 milhões de frente nesses 2.898 municípios (e o Flávio 1,6 milhão no resto), número que a visão da fraude vai usar; mas, dentro da mesma UF, quanto maior a razão entre comparecimento e população, **menor** o ganho do Lula (r = −0,18) e menor a subida do comparecimento (r = −0,25); nos 579 com comparecimento acima da população, o comparecimento ficou parado (−0,06%) e o ganho do Lula foi menor (5,2 contra 6,7 pontos) |
| H18 | o líder do 1º turno perdendo voto com comparecimento estável, 2026 contra 2022 | 9,57% contra 9,37%: igual (a cauda fica na objeção 4) |
| H12 | as 431 seções que mudaram de local, contra o próprio município | ganho do Lula +0,02 ponto e comparecimento igual: nada |
| H01, H09, H10 | com 2022 como controle, dentro do mesmo local | −0,26, +0,10 e −0,06 ponto: nada |
| H15 | aviso seguido de liberação manual contra o acaso | abaixo do acaso nos dois turnos; a subida é a do ritmo de votação |
| H19 | a conta dos 6 estados | o Lula ganhou 408.963 e o Flávio perdeu 52.336 votos, com 501.096 votos dos outros e 190.933 eleitores a menos: a conta fecha com eleitor do Flávio ficando em casa no Norte |
| H05, H08 | não refiz | os espelhos do projeto (Flávio, 2022, simulação) já respondem; não achei objeção |

---

## 4. O que seria preciso para fechar, pela visão da fraude

| O que falta | Quem tem | Fecha |
|---|---|---|
| a assinatura digital de cada BU, verificada com a chave pública | público (o projeto pode fazer) | H11, H17 |
| fotos de boletins de papel comparadas com o arquivo da seção | fiscais e eleitores (convite público) | H11 |
| os hashes da lacração contra os hashes no log de cada urna | público (cerimônia + log) | H18 |
| o relatório consolidado do teste de integridade das 27 UFs | TSE e TCU | H18 |
| o comparecimento por idade do 2º turno de 2026 | TSE (ainda não publicado) | H13 |
| o cruzamento do cadastro com os óbitos do SIRC | TSE (LAI) | H13 |
| a ata de cada seção com aviso "já votou" e o caderno de votação | TREs | H15 |
| a lista de quem votou em cada seção, com o tipo de liberação | TSE (LAI) | H03, H13, H15, H16 |
| beneficiários por município, com 2022 como controle | MDS e MEC (dado aberto) | H21 |
| o log inteiro do 2º turno de novo, para repetir na população o recorte de aviso por repetição | público (85 GB) | H15, H16 |

---

## 5. Em uma frase

O projeto acerta onde o dado separa as duas visões (o fuso do relatório pericial, a unanimidade, os placares, o eleitor novo dividido como em 2022), e o pior caso de todo caminho de voto acrescentado, somado, fica em cerca de 7,8% da diferença; mas ele chama de "não sustentado" e "desmentido" os três caminhos que o dado público não testa (o programa, a totalização e o boletim de papel), subestima o teto de H13 e H15, e deixou de ver a subida dos avisos "já votou" que não são repetição e a cauda das quedas grandes do Flávio.
