# Plano: as hipóteses do público sobre o 2º turno de 2026 (vídeo longo 20)

**Rodada 0, 29/out/2026.** Terceira parte da série **Investigação Aberta** sobre o 2º turno. A parte das pesquisas e do resultado é o projeto `pesquisas-e-resultado-segundo-turno-2026` (vídeo 19, publicado primeiro); a parte das urnas é `investigacao-segundo-turno-2026` (vídeo 16). Esta parte pega **o que o público levantou e as duas partes não testaram**, uma hipótese por vez, cada uma pelas duas visões.

## 1. O pedido, nas palavras dele

- *"uma complementação, passando por todos os pontos que a internet tem falado que são muito relevantes"*, a partir dos comentários dos vídeos 16, 19 e dos mesários, dos relatórios de comentários, do relatório que circulou e da internet.
- *"teve várias urnas que tiveram apenas voto do Lula e zero votos do Flávio [...] uma análise bem aprofundada"*; *"pessoas que estavam mortas votaram"*; o relatório do vídeo anexo, com o autor ou a fonte identificados.
- *"a ideia do vídeo vai ser basicamente analisar essas hipóteses [...] ainda que o vídeo fique um pouco maior"*, *"naquele mesmo estilo, de se for legítimo, se for fraude, colocando uma outra para revisar"*.
- Os prints de quem comentou como asset (rosto borrado quando há foto), trechos de vídeo para o trailer, e um repositório novo e **público**.

## 2. O método (o mesmo dos vídeos 16 e 17)

1. **Duas visões com o mesmo rigor**, cada uma dada como verdadeira por vez: o resultado foi legítimo; houve fraude. Para cada hipótese, o que cada visão espera ver no dado (`docs/HIPOTESES.md`).
2. **Três papéis de IA**, como no vídeo 17: uma defende o resultado legítimo, uma defende a fraude, e uma terceira confere as duas (método, conta e linguagem). As duas defesas ficam publicadas (`docs/REVISAO_ADVERSARIAL.md`).
3. **Régua de cinco vereditos por hipótese** (skill `planejamento-investigativo`): confirmado, indício forte, compatível com as duas, não sustentado, desmentido. Toda hipótese fecha com o **teto do pior caso** contra os 4.430.191 votos de diferença, **o que fecharia** de vez (documento e órgão) e **quem deveria responder**.
4. **Os critérios e pesos do vídeo 16** (emenda 4, decisão dele): comportamento dos votos pesa mais, raridade em seguida, arquivos das urnas menos (bater é o esperado nas duas visões). Cada hipótese é encaixada num dos três.
5. **Controles que mais rendem**: o mesmo local de votação (tira renda, região e idade de uma vez), a mesma seção no 1º turno e em 2022, o espelho (o mesmo teste para o Flávio) e o placebo (a conta numa região onde a alegação não se aplica). Confundidor nomeado antes de rodar (ex.: em H01, o tamanho da fila; em H13, a idade do eleitorado).
6. **Conclusão sempre** (*"sempre tem como chegar a uma conclusão"*): quando a prova não fecha, a conta fecha (o teto) e o caminho fecha (o que falta e quem tem).

## 3. Rodadas ou pré-registro (decisão dele)

| Opção | Como fica | O que muda |
|---|---|---|
| Rodadas (o padrão desde 26/out) | a regra de cada teste vai no relatório da rodada; cada retorno dele vira rodada nova em `docs/RODADAS.md` | mais rápido; a credibilidade vem de tudo estar no git com hora |
| Pré-registro | as regras do §5 viram `docs/PRE_REGISTRO.md` em commit **antes** de qualquer conta nova; mudança vira emenda datada | o caminho dos vídeos 8, 14 e 16 (investigação de alegação); a rodada 0 já viu parte dos números (`resultados/SONDAGEM.json`) e isso fica declarado |

## 4. Os dados

| Dado | Para | Estado |
|---|---|---|
| Tabelas por seção do 1º e do 2º turno e de 2022 (boletim, RDV, resumo do log) | H01 a H08, H10, H15, H16, H19 | ✅ copiadas do projeto do vídeo 16 com sha256 (`dados/MANIFESTO_COPIAS.json`) |
| Log, BU e RDV de cada seção do 2º turno (o bruto, ~85 GB) | modelo da urna (H09), assinatura do BU (H11), contexto do aviso "já votou" (H15), mesário por hora e digital repetida (H16), hashes do programa (H18) | ⬜ baixar de novo (os brutos do vídeo 16 foram apagados); um coletor só, por causa do 429 do TSE; o código de coleta do vídeo 16 é copiado com a origem anotada |
| Log do 1º turno de 2026 | espelho de H15 e H16 | ⬜ baixar (os do vídeo 8 foram apagados) |
| Local de votação (nome e endereço de cada seção) | H07, H12 | ⬜ dado aberto do TSE |
| Seções de 2018 | H07 (histórico das zeradas) | ⬜ dado aberto do TSE |
| Eleitorado por idade e comparecimento por idade | H13, H14 | ⬜ dados abertos do TSE |
| População por idade e município (Censo 2022, estimativa 2025) | H13, H14 | ⬜ IBGE |
| A curva oficial da noite (2.554 arquivos) | H17 | ✅ no repositório `apuracao-segundo-turno-2026` (copiar com hash) |
| Chave pública e assinatura dos BUs | H11 | ⬜ documentação do TSE |
| Bolsa Família por município | H21 | ⬜ Portal da Transparência |
| Cobertura de celular e 5G por município | H22 | ⬜ Anatel |
| O relatório pericial (PDF) | Bloco A | ver `docs/pesquisa/RELATORIO_PERICIAL_ORIGEM_E_ALEGACOES.md` |

## 5. A ordem de execução

| Fase | O que sai |
|---|---|
| 1. Coleta | os dados do §4 com endereço, hora, tamanho e sha256 em `dados/MANIFESTO.json` |
| 2. Validação do dado | reconciliação com o total proclamado pelo TSE (diferença de 4.430.191); a soma das tabelas copiadas do vídeo 16 dá Lula 64.255.787 e Flávio 59.825.688 (diferença 4.430.099), e os 445 e 353 votos que faltam precisam de causa nomeada antes de seguir; dois leitores para o log novo (o modelo da urna e o aviso "já votou"); leitura à mão de uma amostra com todas as categorias, até "outra" |
| 3. Bloco A (o relatório) | refazer cada número do relatório com o mesmo arquivo, dizer o que bate e o que não bate, e só então testar a conclusão dele |
| 4. Blocos B a E | um script por hipótese (`ferramentas/hNN-<nome>.py`), saída em CSV e em `resultados/RESUMO.json` |
| 5. Validação independente | os números centrais refeitos por outro caminho (`ferramentas/validacao-independente.py`) |
| 6. Revisão adversarial | as três IAs do §2 |
| 7. Relatório por script | `RELATORIO.md`, `RESUMO_SIMPLES.md`, `docs/LEITURA_DA_IA.md`, gráficos 1920x1080 com as cores de sempre (Lula `#C8553D`, Flávio `#2D6A8A`) |
| 8. Pedidos e convite | `docs/PEDIDOS_LAI.md` (óbitos no cadastro, urnas substituídas, seções com fiscal, cadernos e atas dos casos citados) e `docs/CONVITE_PUBLICO.md` (fotos de boletim de papel para comparar com o arquivo) |

## 6. O que vai para o vídeo (proposta, a decisão é dele)

| Peso no público | Hipóteses | Por quê |
|---|---|---|
| Maior | H01 a H05 (o relatório), H07 (106 urnas), H13 (mortos) | são as que ele citou, as que mais circularam e as mais pedidas nos comentários |
| Médio | H08, H09, H11, H15, H16, H18 | pedidas com detalhe nos comentários e testáveis com dado novo |
| Menor | H06, H10, H12, H14, H17, H19 a H23 | casos pontuais ou já respondidos em parte; entram numa frase ou num bloco rápido |

Os prints dos comentários (80 até agora, separados por hipótese) e os trechos de vídeo para o trailer ficam no repositório de documentação, na pasta do vídeo 20.

## 7. Travas

As do assunto (`CLAUDE.md` §4D do repositório de documentação): sem "mentiu N vezes", sem recomendação de voto, sem julgar intenção, sem checar um lado só. Seção marcada por teste é "fora do padrão, a conferir", nunca "fraudulenta". "Fraude" só como nome de uma das duas visões. Identificador de mesário ou eleitor nunca publicado. Texto público em português e sem travessão.
