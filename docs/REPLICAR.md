# Como refazer tudo

```bash
pip install pandas pyarrow numpy matplotlib aiohttp playwright pillow
python ferramentas/coletar.py              # arquivos abertos do TSE (~1,7 GB)
python ferramentas/ibge.py                 # Censo 2022 por idade e município
python ferramentas/amostra_logs.py         # logs de 12.691 seções (~2,2 GB, um coletor só, teto de 60 por segundo)
python ferramentas/derivar_tse.py          # tabelas leves em dados/derivados/
python ferramentas/derivar_amostra.py      # uma linha por seção e turno da amostra
python ferramentas/sondagem.py             # rodada 0
python ferramentas/analise.py              # rodada 1: resultados/RESUMO.json
python ferramentas/validacao_independente.py
python ferramentas/gerar_relatorio.py
python ferramentas/graficos.py
python -m pytest -q
```

As cópias de outros projetos (`dados/copias/`) estão no git, com o hash em `dados/MANIFESTO_COPIAS.json`. A amostra de logs usa a semente 2026 e a lista sai em `dados/derivados/amostra_secoes.csv`. Os comentários (`ferramentas/temas_comentarios.py`) precisam dos brutos, que ficam fora do git porque têm o @ das pessoas.
