# Fontes de dados

Todo arquivo baixado tem endereço, hora, tamanho e sha256 em `dados/MANIFESTO.json`; toda cópia de outro projeto, em `dados/MANIFESTO_COPIAS.json`.

| Fonte | Endereço | Para |
|---|---|---|
| Boletim, RDV e resumo do log de cada seção do 2º turno e boletim do 1º turno (tabelas por seção) | cópia de `investigacao-segundo-turno-2026/dados/derivados/` (commit no manifesto) | H01 a H04, H07, H08, H10, H15, H18, H19 |
| Seções de 2022 (1º e 2º turnos) | cópia do mesmo projeto | H04, H07, H08, H14 |
| Votação por seção de 2018 | `cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2018_BR.zip` | H04, H07 |
| Votação por seção de 2026 (dados abertos) | `cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2026_BR.zip` | validação independente |
| Detalhe da votação por seção de 2026 (comparecimento, local, modelo da urna, origem do boletim) | `cdn.tse.jus.br/estatistica/sead/odsele/detalhe_votacao_secao/detalhe_votacao_secao_2026.zip` | H09, H10, H11, H12, reconciliação |
| Eleitorado por local de votação de 2026 | `cdn.tse.jus.br/estatistica/sead/odsele/eleitorado_locais_votacao/eleitorado_local_votacao_2026.zip` | H07 (nome do local) |
| Perfil do eleitorado de 2022 e 2026 (idade) | `cdn.tse.jus.br/estatistica/sead/odsele/perfil_eleitorado/` | H13, H14 |
| Comparecimento e abstenção por perfil, 2022 e 2026 (idade) | `cdn.tse.jus.br/estatistica/sead/odsele/perfil_comparecimento_abstencao/` | H13 |
| Log da urna de 12.691 seções (amostra) | `resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3221/dados/...` (`ferramentas/amostra_logs.py`) | H03, H15, H16, validação |
| Versões do resultado de Presidente gravadas ao vivo na noite (2.554) | cópia de `investigacao-segundo-turno-2026/dados/noite/versoes-tse/` | H17 |
| Resultado por município e renda do Censo 2022 | cópia de `pesquisas-e-resultado-segundo-turno-2026/dados/derivados/` | H14, H20, H21, H23 |
| População por idade e município, Censo 2022 (tabela 9514) | `servicodados.ibge.gov.br/api/v3/agregados/9514` (`ferramentas/ibge.py`) | H13, H14 |
| O "Relatório Pericial Independente" (7 imagens) e as capturas dos posts | Instagram do Joey Mannarino e X (`dados/brutos/relatorio-pericial/`) | Bloco A |
| Checagens e notas oficiais | `docs/pesquisa/` (endereços e datas em cada tabela) | todas |

⚠️ O arquivo de cada UF e o `_BRASIL` do mesmo pacote do TSE repetem as mesmas linhas: ler os dois soma em dobro (`ferramentas/derivar_tse.py` lê só um). A votação de Presidente do detalhe por seção só vem no arquivo `_BR`.
