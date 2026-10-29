# Dados locais (fora do git)

| Pasta | O quê | Tamanho | Pode apagar? |
|---|---|---|---|
| `dados/brutos/tse/` | os 8 arquivos abertos do TSE | ~1,7 GB | sim; `python ferramentas/coletar.py` baixa de novo e confere o tamanho (o hash está no manifesto) |
| `dados/brutos/t2/amostra.sqlite` | os logs das 13.221 seções da amostra (12.691 da 1ª passada e as do oeste do Amazonas) | ~2,3 GB | sim, se o TSE mantiver os arquivos por seção no ar; `python ferramentas/amostra_logs.py` |
| `dados/brutos/comentarios/` | os comentários dos vídeos 8, 16 e 19, com o @ de cada pessoa | ~0,5 MB | não apagar antes do vídeo: os prints e o índice dependem deles |
| `dados/chave-local.txt` | a chave do HMAC dos mesários | pequeno | não: sem ela, o código de mesário muda |

No git ficam as tabelas derivadas leves, as cópias de outros projetos, as respostas do IBGE e as imagens do relatório pericial.
