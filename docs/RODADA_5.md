# Rodada 5 · 17/11/2026 · a resposta do TRE-PE e os comentários depois do vídeo 26

**Pedido:** o episódio seguinte do Investigação Aberta, com a resposta do TRE de Pernambuco ao pedido por Lei de Acesso à Informação (protocolo 82034721135306, resposta de 13/11/2026) e as hipóteses dos comentários que a série ainda não tinha testado. Sem pré-registro (padrão de rodadas).

**Dados novos:**

| O quê | Onde | Observação |
|---|---|---|
| a resposta do TRE-PE, transcrita sem dado pessoal | `docs/lai/TRE_PE_RESPOSTA_2026-11-13.md` | 20 zonas eleitorais, 41 seções |
| a resposta, seção a seção | `dados/lai/tre_pe_resposta_2026-11-13.csv` | uma linha por seção do pedido, com o que cada zona disse |
| o log e o `aux.json` do 1º turno das 41 seções, mais a seção 24 da zona 121 | `dados/brutos/rodada5/` (fora do git: o log traz o número do título digitado) | baixados de novo do TSE em 17/11; endereço e sha256 de cada arquivo em `dados/MANIFESTO_RODADA5.json` |

**Código:** `ferramentas/rodada_5_coletar.py`, `ferramentas/rodada_5.py` (resultados em `resultados/RODADA5.json` e `resultados/tabelas/r5_*.csv`), `ferramentas/validacao_rodada_5.py` (9 de 9) e `ferramentas/graficos_rodada_5.py` (g28 a g33).

⚠️ **O pedido ao TRE-PE é do 1º turno.** As 41 seções vieram da lista do projeto `alegacoes-fraude-eleicoes-2026` (`resultados/a1_secoes_marcadas.csv`): seções com 5 ou mais liberações sem a digital seguidas depois das 17h, ou com muitas tentativas de dado que não conferia. Por isso o pior caso desta rodada **não entra** na soma do 2º turno.

## H37 · A resposta do TRE-PE

### O que chegou

| Tipo de resposta | Seções | Zonas |
|---|---|---|
| responderam sobre a seção, por e-mail ou com a ata | **27** | 61, 121, 105, 106, 125, 85, 11, 101, 147, 54, 88, 78, 55, 81, 71 |
| pediram um pedido novo (petição no cartório ou identificação por e-mail) | **12** | 118 (10 seções em Jaboatão), 7 e 9 (Recife) |
| a ata está disponível só no cartório | 1 | 18 |
| responderam que a informação está no site do TSE | 1 | 3 |

O caderno de votação e a ata não estão no site do TSE. Os 4 anexos são atas de 7 seções: zona 11 (seções 55, 56, 103 e 283), 78 (23), 85 (314) e 125 (22). O e-mail e as atas, com tarja em todo dado pessoal, estão em [`dados/lai/tre-pe-2026-11-13/`](../dados/lai/tre-pe-2026-11-13/LEIA-ME.md).

⚠️ A 121ª zona respondeu sobre a **seção 24**; o pedido era da **274**. A resposta (*"todos os eleitores habilitados sem biometria assinaram"*) vale para a 24, que teve 17 eleitores liberados sem a digital; a 274 teve 110 e ficou sem resposta.

### Impugnação e protesto

**0** registro de impugnação ou protesto nas **24** seções em que a zona respondeu esse item ou em que a ata foi lida. A 105ª zona disse que a resposta dela não afirma nada sobre impugnação (3 seções).

### Fiscais de partido

O cartório não tem a lista de fiscais por seção (as credenciais saem dos partidos, art. 132 da Res. TSE 23.736/2024). O número veio da ata em **17 seções**:

| Fiscais | Seções |
|---|---|
| 0 | 5 (zona 11: 55, 56, 103 e 283; zona 78: 23). Na 283, a presidente da mesa escreveu na ata que não houve fiscal na seção |
| 1 | 3 (zona 85: 314, PSD; zona 125: 22, PSD; zona 88: 26) |
| 2 | 5 (zona 121; zona 105: 247; zona 106: 321; zona 81: 15, União Progressista; zona 54: 185, PSD) |
| 3 ou mais | 3 (zona 105: 318 e 356; zona 106: 325) |
| 4 | 1 (zona 61: 124, Bom Conselho: 2 do PL, 1 do PSD e 1 sem partido informado) |

### Caderno de votação contra o log da urna

A regra, nas palavras das próprias zonas: o eleitor liberado pela digital não assina o caderno; o eleitor liberado **sem** a digital (a digital falhou, ou ele não tem digital cadastrada) digita o ano de nascimento, mostra documento com foto e **deve assinar**. Várias zonas escreveram que *"a contagem de assinaturas no Caderno não serve como um indicador de auditoria"* e que os dados com fé pública são o boletim de urna e o log.

**O número do log bate com o que os cartórios contaram quando os dois contam a mesma coisa:**

| Seção | O cartório | O log da urna (e o boletim) |
|---|---|---|
| 101/724 | 97 habilitações sem biometria | 97 sem digital cadastrada |
| 105/356 | 5 no Boletim de Eleitores com Habilitação Biográfica (BEHB) | 5 com a digital do eleitor falhando |
| 105/247 | 24 no BEHB | 25 |
| 106/321 | 29 no BEHB | 25 |
| 106/325 | 14 no BEHB | 11 |

O BEHB é impresso pela própria urna; o número dele no boletim (campo `QT_ELEITORES_BIOMETRIA_NH`) é igual ao log nas 41 seções. As diferenças de 247, 321 e 325 ficam na contagem do cartório, a conferir com a cópia do BEHB.

**O que falta no caderno.** O BEHB lista só quem tem digital cadastrada e não foi reconhecido. Quem **não tem** digital cadastrada também é liberado pelo ano de nascimento e também precisa assinar, e não aparece no BEHB. Contando os dois grupos pelo log:

| Seção | Liberados sem a digital (log) | Assinaturas (cartório) | Mínimo sem assinatura |
|---|---|---|---|
| 101/724 Jaboatão | 108 (97 sem digital cadastrada + 11 com a digital falhando) | 104 | **4** (o cartório comparou só com os 97) |
| 105/247 Caruaru | 24 no BEHB (e mais 79 sem digital cadastrada, sem resposta) | 18 dos 24 | **6** (contados pelo cartório) |
| 105/318 Caruaru | 36 com a digital falhando | 4 assinaturas achadas desse grupo | **32** (o cartório diz que a conta dele, sozinha, não confirma a correspondência) |
| 106/321 Caruaru | 123 (98 + 25) | 95 | **28** |
| 106/325 Caruaru | 167 (156 + 11) | 163 | **4** |

**Pelo menos 74** pessoas liberadas sem a digital não têm assinatura no caderno nessas 5 seções. É um piso: supõe que nenhum eleitor liberado pela digital assinou, e o próprio cartório diz que muitos assinaram. Em 106/325, o cartório afirma que a maioria das 163 assinaturas é de quem votou pela digital; como ele mediu *"sem biometria"* pelo BEHB, os 156 eleitores sem digital cadastrada podem ter sido contados como se tivessem digital. Só a cópia do caderno separa as duas leituras.

Três seções disseram que todos os liberados sem a digital assinaram: 54/185, 88/26 e a seção 24 da zona 121.

### As seções que as atas explicam

- **54/185, Jataúba** (a seção mais fora do padrão de Pernambuco: 94 liberações sem digital depois das 17h). Segundo a ata, a urna foi trocada antes de abrir, o leitor de digital do terminal do mesário não funcionou desde o 1º eleitor, a votação parou das 9h08 às 9h21, e o juiz, o promotor e 2 fiscais do PSD acompanharam. O log confirma: 288 votos, só 4 pela digital do eleitor (98,6% sem); a urna nova começa às 8h10 e reinicia às 8h56 e às 9h18; nenhum voto entre 9h08 e 9h21; último voto às 20h07.
- **11/56, Jaboatão.** A ata registra *"17:10 Foi distribuído senha para os eleitores que estavam na fila. 7 senha ao todo"* e término às 17h30. O log registra 16 votos depois das 17h10 (o último às 17h29), 8 deles pela digital do próprio eleitor e 8 pelo ano de nascimento. Só as digitais reconhecidas já passam das 7 senhas, então a anotação da ata não é a contagem de quem votou depois das 17h10. Quem estava na fila, só o caderno mostra. A mesma ata registra muitos idosos e eleitores com acompanhante.
- **11/283, Jaboatão.** Sem fiscal (a presidente escreveu isso na ata), com 3 mesários em vez de 4 e o botão de confirmar duro; a ata atribui o atraso aos eleitores com acompanhante.
- **78/23, Parnamirim.** A ata não tem nenhuma ocorrência escrita e nenhum fiscal. O log tem 42 eleitores com a digital falhando (o item 2.9 da ata pede o nome de cada um), 40 sem digital cadastrada e 94 votos depois das 17h; o último às 20h16. O Lula teve 91,8% dos votos válidos na seção e 85,8% no município; o comparecimento foi de 78,9% e 80,0%. A 78ª zona não explicou a ata vazia; em Caruaru, a 105ª zona disse que orientou os mesários dela a deixar esse registro para o BEHB, e não para a ata.
- **125/22, Condado.** A ata lista cerca de 23 eleitores com *"biometria não reconhecida"*, mais que os 15 do log; a página com as linhas 28 a 52 não veio no PDF, e a anonimização do cartório (iniciais sobrepostas) deixa a contagem incerta. A conferir.
- **105/318, Caruaru.** Os 36 eleitores com a digital falhando passaram todos pelo mesmo caminho: o ano de nascimento digitado errado uma vez, depois certo, depois a digital do mesário. Depois do último voto (18h40), o log registra **7 avisos de "eleitor já votou" entre 18h43 e 18h47**. O dado público não diz se foram eleitores chegando ou a mesa conferindo nomes; a ata dessa seção não veio.

### Veredito

| | |
|---|---|
| O fato que circula (*"mesários votaram por quem faltou, e o caderno provaria"*) | **meio certo**: o caderno não fecha com a urna em 5 das 9 seções com conta, e as zonas dizem que ele não serve de auditoria |
| A leitura de fraude | **compatível com as duas, a conferir** |
| A favor do resultado legítimo | 0 impugnação em 24 seções; o log bate com o que o cartório contou quando os dois contam a mesma coisa; a seção mais extrema tem a falha registrada com juiz e promotor presentes; as marcadas votaram como as vizinhas da mesma escola (projeto `alegacoes-fraude-eleicoes-2026`) |
| A favor da leitura de fraude | pelo menos 74 liberações sem digital sem assinatura; 5 de 17 seções sem nenhum fiscal; a ata da 56 não fecha com a urna depois das 17h10; 7 avisos de "já votou" seguidos na 318; 12 seções sem resposta |
| Pior caso | 74 votos no 1º turno (fora da soma do 2º turno) |
| O que fecharia | a cópia do caderno das 5 seções e das que não responderam, para ver se cada liberação sem digital tem assinatura; a ata da 105/318 e o motivo dos 7 avisos |

## H38 · "Os votos de 2022 foram reescritos em 2026"

Pedido de um comentário no vídeo 26: votos do Lula de 2022 teriam sido regravados com a data de 2026. Se o número de 2022 tivesse sido copiado para a mesma seção, a diferença entre 2026 e 2022 teria um pico no zero.

| Diferença na mesma seção (2º turno) | −3 | −2 | −1 | **0** | +1 | +2 | +3 |
|---|---|---|---|---|---|---|---|
| Lula 2026 menos Lula 2022 | 12.129 | 12.220 | 12.798 | **13.004** | 13.109 | 12.988 | 13.034 |
| Flávio 2026 menos Bolsonaro 2022 | 12.312 | 12.429 | 12.570 | **12.752** | 12.666 | 12.394 | 12.482 |

Em 461.195 seções casadas, o número igual aparece tanto quanto o de 1 voto a mais ou a menos (razão de 1,02 contra os vizinhos, nos dois lados). O boletim inteiro (Lula, Flávio, branco e nulo) repete o de 2022 em **9** seções. **Fato: errado. Leitura de fraude: desmentida.**

## O que os comentários pediram e onde está

Lidos os 53 comentários do vídeo 26 e os 121 novos dos vídeos 8, 16 e 20 entre 11 e 17/11 (os nomes ficam no repositório de documentação do canal).

| Pedido | Onde |
|---|---|
| *"na minha seção o comprovante foi dado sem assinatura"* | H37 (a regra: quem vota pela digital não assina) |
| votos de 2022 reescritos em 2026 | H38 |
| *"300 urnas sem voto do Bolsonaro em 2018"* | já na H07: 328 seções sem voto do Bolsonaro em 2018, 141 em 2022 e 106 sem voto do Flávio em 2026 |
| quantas pessoas votaram sem a digital liberadas pela mesa | H27 (12,3% e 12,5%) e H37 |
| mesários votando por quem faltou | H37 e o vídeo 8 |
| *"a urna troca o voto depois de 9 horas ligada"* | sem como testar com dado público (o voto não tem hora); a H33 mostra que as seções que fecharam tarde cresceram para o Lula igual às outras |
| pendrive ou cartão trocado, código-fonte | H18 (compatível com as duas; quem testa é o teste de integridade) |
| mortos votando | H13 |
| a pausa do 1º turno | pedido ao TSE, ainda sem resposta |

## Contagem da série

35 linhas: **9 desmentidas**, **19 não sustentadas**, **5 compatíveis com as duas** (H14, H15, H18, H23 e H37), **2 não testadas**. A soma do pior caso do 2º turno não muda: 383.588 votos (8,66%), com a ressalva da nota N4 da rodada 4 (o item do *"já votou"* é piso).

## Validação (`resultados/VALIDACAO_RODADA5.json`)

9 de 9: votos do log iguais ao comparecimento do boletim (41 de 41); liberações com a digital do mesário iguais ao campo do boletim (41 de 41); contagem direta dos eventos igual ao classificador (41 de 41); a transcrição com as 41 seções e as 20 zonas; a H38 refeita com chave numérica (461.195 seções, 13.004 e 12.752 iguais).

## Os pedidos que seguem

| Protocolo | Situação em 17/11 |
|---|---|
| TSE · 82032521133805 | processo administrativo (23/10); prazo até 20/11 |
| TRE-BA · 82034321135124 | sem resposta; prazo até 20/11 |
| TRE-PE · 82034721135306 | **respondido em 13/11** |
