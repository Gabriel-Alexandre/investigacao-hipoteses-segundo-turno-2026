# "Relatório Pericial Independente": origem, rastro, alegações e checagens

**Pesquisa feita em 29/10/2026, das 13h às 15h10 (horário de Brasília).** Só leitura na internet, sem login, sem conta, nada publicado. Horário de Brasília (UTC-3) em todo o arquivo, salvo quando escrito UTC.

**Regra usada:** número só entra com a frase lida na página (ou no arquivo baixado). O que veio só de resumo automático de busca está na tabela (d), como não confirmado.

---

## 0. Resumo em 10 linhas

1. O documento **não é um PDF encontrado**: o que circula são **imagens de páginas**. A versão completa que achei tem **7 páginas** (mais uma imagem de tweet), no carrossel do Instagram de Joey Mannarino. O TSE descreve uma versão de **4 páginas** "divulgada na plataforma X".
2. O post mais antigo que consegui provar é **um post do X de 28/10 às 13h28min33s**, hoje **indisponível** (apagado, restrito ou de conta suspensa; autor desconhecido). Ele só aparece porque o perfil @Gigapardos o citou às **16h28** com o título do relatório.
3. O post de Mannarino no Instagram é de **28/10 às 17h00min41s**, ou seja, **depois** da circulação no X. Ele próprio escreve que não é o autor (*"This was sent in by a follower"*).
4. A página 6 (anexo) começa com *"Diante da repercussão do dossiê"*: o anexo foi escrito **depois** de o documento já circular. Há pelo menos duas versões.
5. Nenhuma imagem tem metadado (EXIF, XMP), e o documento não tem autor. A página 4 diz que os gráficos "dependiam de imagens anexas à análise original", o que indica que é cópia reformatada de outra análise, não localizada.
6. O número da biometria (**8.632.488**, 6,73%) **existe nos boletins**: o Jornal Razão chegou ao mesmo total somando os 499.205 BUs. Mas em 2022 o número foi **maior** (10.011.347, 8,06%), e a identificação não muda o voto.
7. O capítulo 1 e 2 (as "duas eleições" antes e depois das 17h) somam **o dia inteiro** das seções que fecharam depois das 17h. Pela própria tabela do relatório, esse grupo tem **70,7%** dos eleitores. O TSE contou **34.393 votos** registrados depois das 17h e diz que **497.333 seções** tiveram o encerramento registrado depois das 17h.
8. O "apagão de 72 horas" é **em parte verdade e em parte falso**: o pacote consolidado entrou no catálogo de Dados Abertos em **28/10, 11h07** (o do 1º turno entrou 2 dias depois), mas os arquivos já estavam no servidor do TSE desde **26/10 à tarde**, os BUs saíram impressos nas seções e no site Resultados em 25/10.
9. Checagem **direta** do relatório: só a da **Justiça Eleitoral (Fato ou Boato)**, 28/10 21h49. Aos Fatos, AFP, Estadão Verifica e TSE checaram o ponto das 17h, não o relatório. Não achei checagem de g1, Comprova, UOL Confere, Reuters nem Boatos.org.
10. Repost maior que achei: **Chequei Brasil** (121 mil seguidores no X), 28/10 20h07, **1.004.953 visualizações**, com fotos de banco de imagem, não as páginas.

---

## (a) Origem e rastro

### a.1 Linha do tempo (o que consegui provar)

O horário de post do X vem do próprio número do post (o ID do X carrega o milissegundo de criação; conta: `(ID >> 22) + 1288834974657`), conferido com o horário que a página mostra quando ela abre.

| Quando (Brasília) | Onde | Quem | O quê | Prova | Situação |
|---|---|---|---|---|---|
| 28/10, 13:28:33 | X, post `2115480851681255899` | **desconhecido** | o post mais antigo ligado ao relatório que consegui achar | é o post citado pelo @Gigapardos (campo `qrtURL` na API do vxTwitter); horário pelo ID | ⛔ **indisponível**: "Página não encontrada" no X; a API do fxTwitter responde 404 |
| 28/10, 16:28:50 | [X, @Gigapardos](https://x.com/Gigapardos/status/2115526222847385763) | Gigapardos (5.214 seguidores) | *"🚨 Relatório Pericial Independente mostra que as eleições foram fraudadas"*, citando o post acima | a página mostra "16:28 · 28 de out. de 2026" e "Este post está indisponível" no lugar da citação | 22.447 visualizações, 826 curtidas, 122 repostagens, 13 respostas |
| 28/10, 16:37:02 | [X, resposta do @Gigapardos](https://x.com/Gigapardos/status/2115528285568586237) | Gigapardos | resume 3 números: "Mais de 7.000 seções [...] 18:1", "Mais de 8 milhões de votos sem biometria", "Mais de 2,5 milhões de votos após as 17h" | API do fxTwitter | 1.127 visualizações |
| 28/10, 16:41:20 | [X, resposta do @Gigapardos](https://x.com/Gigapardos/status/2115529365991960585) | Gigapardos | *"não há nada provado ainda, pra provar uma fraude teria que ser apresentada a metodologia"* | API do fxTwitter | 888 visualizações |
| 28/10, 17:00:41 | [Instagram, post `DfDPdFODrGI`](https://www.instagram.com/p/DfDPdFODrGI/) | **Joey Mannarino** (@joeymannarinous) | carrossel de 8 imagens: as 7 páginas do relatório e um print de tweet dele | atributo `datetime="2026-10-28T20:00:41.000Z"` da página; texto do post lido na página | **295.246 curtidas e 11.009 comentários** quando li (29/10, por volta de 15h) |
| 28/10, "16h36" | [Via Pantanal (Campo Grande, MS)](https://viapantanal.com/noticia/51397/relatorio-que-aponta-8-6-milhoes-de-votos-sem-biometria-no-2o-turno-viraliza-nas-redes-veja-o-que-diz-o-documento) | Redação Digital | primeira matéria que achei; embute o post do Instagram | a página diz "28/10/2026 às 16h36" | ⚠️ o horário impresso vem antes do post do Instagram (17h00). Mato Grosso do Sul fica uma hora atrás de Brasília (16h36 de lá = 17h36 de Brasília), o que bate com o texto *"Em menos de meia hora, a postagem somava milhares de curtidas"*. Não confirmado qual fuso o site usa |
| 28/10, 20:07:46 | [X, @brasilchequei](https://x.com/brasilchequei/status/2115581317077430501) | Chequei Brasil (121.401 seguidores) | *"Mais de 8 milhões de pessoas foram permitidas a votar sem usar biometria [...] segundo relatório"* | API do fxTwitter | **1.004.953 visualizações, 40.422 curtidas, 7.620 repostagens, 998 respostas**. As 2 imagens anexas são foto do Lula e foto de urna, não páginas do relatório |
| 28/10, 21:49 | [Justiça Eleitoral, Fato ou Boato](https://www.justicaeleitoral.jus.br/fato-ou-boato/checagens/2026/relatorio-apocrifo-distorce-dados-para-sugerir-fraude-nas-eleicoes-2026) | TSE | checagem do relatório (atualizada em 29/10, 14h53) | texto lido | ver (c) |

### a.2 O que o documento diz de si mesmo

| Item | O que está nas imagens |
|---|---|
| Título | "RELATÓRIO PERICIAL INDEPENDENTE", subtítulo "Com Base em Microdados Oficiais do TSE" |
| Lema da capa | "AUTÓPSIA DE NARRATIVAS E ESTRUTURAS DE PODER" e "Fatos primeiro. Efeitos de 2ª ordem. Ruído excluído." |
| Data | "Data da análise: 28 de outubro de 2026" |
| Fonte declarada | "Repositório oficial de Dados Abertos do TSE", "Boletins de Urna (BWeb)", hashes ".sha512" |
| Autor | **nenhum**. Fala em "equipe de inteligência" e "a perícia" |
| Rodapé | "Documento baseado em dados públicos do TSE, Outubro/2026" e, na página 7, "Este documento não constitui laudo judicial" |
| Páginas | 7 numeradas (capa, introdução e capítulos 1 a 2, capítulos 2 e 3, capítulos 4 a 6, fim do 6 e conclusão, anexo parte 1, anexo parte 2) |
| Sinal de versão | a página 6 abre com *"Diante da repercussão do dossiê estatístico"*: o anexo é posterior à primeira circulação. O TSE descreve **4 páginas** no X; a versão do Instagram tem **7** |
| Sinal de cópia | página 4: *"Os gráficos do teste de Benford e da correlação biométrica não foram incluídos neste documento, pois dependiam de imagens anexas à análise original"* |
| Aparência | letra parecida com a DejaVu Sans, cabeçalho e rodapé fixos; isso é comum em PDF gerado por programa, e **não prova autoria nem ferramenta** |

### a.3 Arquivos baixados (não achei PDF)

Pasta: `C:/Users/Gabriel/Downloads/repositorios/investigacao-hipoteses-segundo-turno-2026/dados/brutos/relatorio-pericial/`

| Arquivo | O que é | sha256 |
|---|---|---|
| `instagram-joeymannarinous-DfDPdFODrGI/slide_01.jpg` | página 1 (capa), 2400×2400 | `b8d4353ee43cd5f42d4e320c663e6a30a15eaf15b9affd229771263c1f99631a` |
| `.../slide_02.jpg` | página 2 | `08e1af8dd4739c7cddbe81bc95beee5d6c8f6b3debc0fc892ec769b4a3dd4b0c` |
| `.../slide_03.jpg` | página 3 | `12e7b3154c4526b45a101c5dd75c870f0471192948a1d497c3eefb5c0404f3cb` |
| `.../slide_04.jpg` | página 4 | `3fe4eeccf5dc5be87b433911402c1b9ede3f46c00bcd09d8feb0bc98c325e1f4` |
| `.../slide_05.jpg` | página 5 | `e0c2e590d68fba5649d766ba40509e2e42b5f279bb42c256fbef085959d9157c` |
| `.../slide_06.jpg` | página 6 (anexo) | `cdd82912ff712fbfa5e593a2d0f57cd0866f9a4a466962912ac266c6fecb95cc` |
| `.../slide_07.jpg` | página 7 (anexo, fim) | `c3722ec401f8c8c2209f8d6649910cc0b3aa2072eb726968971bd749e10c1cfe` |
| `.../slide_08.jpg` | print de um tweet de Mannarino ("Follow my Instagram page @JoeyMannarinoUS [...] They are banning Brazilian pages") | `58abd8d98b15c04fc4054c9881745f7d4fd8a3acdd3308d7b5e22273987bee88` |
| `x-chequei-brasil-2115581317077430501/img1_HVwN_cMXIAAZ6l7.jpg` | foto do Lula anexada pelo Chequei Brasil (não é página do relatório) | `af6355a3918311e876c019a7f9495c8e5a4a9c2dcbf946d5dbb99b7352acfa93` |
| `x-chequei-brasil-2115581317077430501/img2_HVwN_cOW8AEYd9f.jpg` | foto de urna com leitor biométrico (não é página do relatório) | `241d9165d0be948f55f5b97109dfca28f8b12c0013d639f8d923e34c8e2152b5` |
| `capturas/fx_*.json` | respostas da API do fxTwitter (texto, horário, números) dos posts do X citados | ver `sha256sum` na pasta |
| `capturas/tse_fatoboato_jina2.md` | texto da checagem do TSE (versão de 29/10, 14h53) | `6068f8fcd14fbd49dc8f5fb075e356d2406558ad4c5dfcf0dbe1562cb2ed4bd6` |
| `capturas/ckan_arq.json` | catálogo do Dados Abertos do TSE (arquivos transmitidos para totalização), com a data de entrada de cada arquivo | `f5dc5de59fc94ce401d21c8c5973e3027d33fa3dfbae65ac9b66680274401895` |

**Metadados de autoria:** nenhum. As 10 imagens não têm EXIF, XMP nem perfil ICC (o Instagram e o X apagam). Sem PDF, não há campo de autor, programa ou data de criação para ler.

### a.4 Onde procurei e não achei

| Lugar | Resultado |
|---|---|
| PDF do relatório (busca pelo título, pelas frases "não constitui laudo judicial", "apagão de setenta e duas horas", "Autópsia de narrativas e estruturas de poder", "aberrações de unanimidade") | nenhum resultado indexado |
| Telegram | **não procurado a fundo** (sem canal de partida; busca aberta não indexa) |
| Perfil de Mannarino no X | a página sem login mostra só o post fixado; **não confirmado** se ele postou as páginas também no X. O print da página 8 é de um tweet dele pedindo que sigam o Instagram |
| Wayback Machine | fora do ar durante a pesquisa (erro 429 e "Temporarily Offline"); não deu para recuperar o post apagado das 13h28 |

---

## (a.5) Quem é Joey Mannarino

| Fato | Fonte 1 | Fonte 2 |
|---|---|---|
| Comentarista e ativista americano, de direita, pró-Trump | perfil do X: *"Co-Founder of The Overton Institute. Host on @Newsforce. American citizen. Political strategist & commentator working with right-wing movements in the US & EU."* (lido pela API do fxTwitter, 29/10) | [IBTimes UK, 26/10](https://www.ibtimes.co.uk/pro-trump-commentator-calls-action-against-lula-1827911): "Pro-Trump Commentator" |
| Nasceu na Filadélfia, cofundador do Overton Institute, apresentador na Newsforce | bio do Instagram: *"Born In Philadelphia, USA. Co-Founder @OvertonInstitute. Host on @Newsforce.Live."* | perfil do X (acima) |
| Tamanho | X: **732.849 seguidores**, conta verificada, desde 2009 | Instagram: a página mostra **"1 mi seguidores"**; a descrição em cache da mesma página dizia 864 mil (o número subiu nesses dias) |
| O que ele disse sobre a eleição antes do relatório | 26/10: *"It's time for President Trump to send in a team for Lula just how he did for Maduro"*, post com 2 milhões de visualizações segundo o IBTimes | [Correio Braziliense, 27/10](https://1news.correiobraziliense.com.br/noticia/902701/noticias/aliado-de-trump-diz-que-flavio-lutara-batalha-do-exterior-em-seguranca-e-provoca-moraes-nas-redes-27102026): "influenciador Joey Mannarino, apresentado como aliado de Trump", sobre Rubio e a saída de Flávio |
| O post do relatório | Instagram `DfDPdFODrGI`, 28/10 17h00: *"Share this everywhere & encourage as many to follow my account (@JoeyMannarinoUS) [...] For the purpose of this battle for democracy, we are all Brazilian! [...] This was sent in by a follower, I don't take credit for the work."* | Via Pantanal, 28/10: "publicado no Instagram pelo comentarista americano Joey Mannarino, que afirmou tê-lo recebido de um seguidor" |

**Outros perfis grandes que repostaram:** o maior que confirmei foi o **Chequei Brasil** (1 milhão de visualizações; ver a.1). ⛔ **Não confirmado** repost de deputados ou influenciadores brasileiros conhecidos (Nikolas Ferreira, Eduardo Bolsonaro, Paulo Figueiredo, Allan dos Santos) nem de americanos além de Mannarino. O Estadão Verifica cita Nikolas Ferreira, Thiago Medina e Rony Gabriel espalhando a tese do resultado "matematicamente impossível", que é **outra alegação**, não este relatório.

---

## (b) As alegações, capítulo por capítulo

"O que precisaria no dado" é o que teria de aparecer nos arquivos para a alegação ser verdade como está escrita. A coluna "conta nossa" usa só os números do próprio relatório.

| Nº | Capítulo (página) | Alegação, com o número exato | O que precisaria no dado para ser verdade |
|---|---|---|---|
| 1 | Introdução (p. 2) | Os microdados de cada urna "foram trancados em sigilo técnico por quase três dias"; os BWeb saíram "apenas na manhã desta quarta-feira, 28 de outubro"; "setenta e duas horas" sem acesso | Nenhum arquivo por seção público entre 25/10 e 28/10. ⚠️ O pacote consolidado entrou no catálogo de Dados Abertos em **28/10, 11h07** (campo `created`, 28/10 14:07 UTC; o do 1º turno entrou em 06/10, dois dias depois da eleição), mas o servidor do TSE informa que os mesmos arquivos estão lá desde **26/10, entre 15h03 e 18h31** (cabeçalho `Last-Modified` dos 28 zips); os arquivos por seção do 2º turno estavam em `resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3221/` e o projeto `investigacao-segundo-turno-2026` começou a baixá-los em **26/10 às 7h30** (`docs/PRE_REGISTRO.md` de lá). ⬜ Não confirmei a data do CSV "BWeb" do 2º turno: ele não aparece no catálogo consultado |
| 2 | Introdução (p. 2) | Processou "499.205 seções eleitorais e 128.236.074 votos apurados" | 499.205 BUs e comparecimento de 128.236.074. ✅ O Jornal Razão diz ter somado "os 499.205 boletins do país e do exterior" e cita 128.236.074 que compareceram |
| 3 | Cap. 1 (p. 2) | Pelo campo `DT_ENCERRAMENTO`, nas "urnas encerradas até as 17h00", "Flávio Bolsonaro venceu com 52,39% dos votos válidos, abrindo uma frente de quase 1,8 milhão de votos" | Um grupo real de seções fechadas até 17h00 com esse resultado, **e** que o horário de encerramento separe votos dados antes e depois das 17h. Conta nossa: se o resto do país é o grupo "até 17h", ele teria 150.807 seções e 37.633.219 eleitores (29%). ⚠️ O TSE diz que **497.333** seções tiveram o encerramento registrado **depois** das 17h e que a urna "só pode ser encerrada a partir das 17h": o grupo "até 17h00" do relatório não bate com o dado oficial |
| 4 | Cap. 1 (p. 2) | Nas "urnas encerradas após as 17h00 (prorrogação)", "Lula obteve uma explosão atípica de mais de 6,1 milhões de votos de vantagem"; "A vitória de Lula foi fabricada exclusivamente no universo de urnas que encerraram as votações após o horário limite legal" | Que esses votos tivessem sido **dados** depois das 17h. ⚠️ O grupo soma o **dia inteiro** dessas seções. Conta nossa com a tabela do cap. 2: 348.398 seções e 90.602.855 eleitores, **70,7%** do comparecimento. Fechar às 17h05 não é prorrogação |
| 5 | Cap. 2 (p. 2 e 3) | Desmente "o mito dos trinta e quatro mil votos"; tabela: 17h01 a 17h15: 339.593 seções, 88.071.750 eleitores, 53,46% Lula; 17h16 a 18h59: 2.472 seções, 674.799 eleitores, 57,16%; após 19h00: 6.333 seções, 1.856.306 eleitores, sem porcentagem | Que o número de eleitores da seção fosse o número de votos depois das 17h. ⚠️ O TSE, pelo horário de cada voto no log, conta **34.393** votos depois das 17h (32.399 entre 17h e 18h, 1.981 entre 18h e 19h, 13 depois das 19h) e **6.766** seções fechadas depois das 19h, com **4.773** votos depois das 17h nelas |
| 6 | Cap. 2 (p. 3) | "Mais de dois milhões e meio de eleitores votaram em urnas que extrapolaram os limites normais" | Conta nossa: 674.799 + 1.856.306 = **2.531.105**, o comparecimento do dia inteiro nas seções fechadas depois das 17h16. Não é número de votos depois das 17h |
| 7 | Cap. 2 (p. 3) | Seções após 19h e % para Lula: Bahia 936 e 72,31%; Pernambuco 657 e 65,70%; Maranhão (sem número) e 83,31%; São Paulo 1.571 e 57,46%; "contrariando o comportamento eleitoral do restante do estado" | A lista por seção com o horário. ⚠️ Esses estados já votam no Lula acima da média (BA, PE, MA); comparar com o resto do estado exige controle por lugar (capital e periferia fecham mais tarde por fila). O TSE dá números diferentes por estado (SP 6.093 seções abertas depois das 17h10 com 2.496 votos depois das 17h; BA 3.787 e 1.656; PE 1.872 e 577) |
| 8 | Cap. 3 (p. 3) | Campo `QT_ELEI_BIOM_SEM_HABILITACAO`: "8.632.488 votos (6,73% do comparecimento nacional)" liberados sem biometria, "por liberação manual do mesário, mediante a simples digitação do ano de nascimento" | ✅ O total existe: Jornal Razão chega a **8.632.488**, 6,73%. ⚠️ Em 2022 foram **10.011.347** (8,06%), pela mesma fonte. Para virar fraude, teria de haver voto em nome de quem não foi votar (o ano de nascimento é dito pelo eleitor, com documento com foto e assinatura no caderno) |
| 9 | Cap. 3 (p. 3) | Margem de 4.430.191 votos; a liberação manual é "quase o dobro da diferença total da eleição" | Conta nossa: 8.632.488 ÷ 4.430.191 = **1,95**. A comparação só faria sentido se todos esses votos fossem irregulares e todos de um lado. O TSE: os arquivos "não fornecem uma lista que indique em quem votou cada pessoa habilitada sem reconhecimento biométrico" |
| 10 | Cap. 3 (p. 3) e anexo (p. 7) | "A perícia realizou o teste de correlação estatística entre o percentual de votos manuais e o percentual de votos obtidos por Lula"; no anexo: onde a liberação manual passa de 20%, 30% ou 50%, "a votação de Lula disparou em linha reta, atingindo picos de mais de sessenta e um por cento" | O gráfico e o número da correlação (não estão no documento) **e** o mesmo teste com controle por lugar. Correlação entre lugares não diz em quem votou cada pessoa (o TSE diz isso). ⚠️ Sem o espelho: idade e região pesam nas duas coisas; precisaria mostrar que não aparece o mesmo em 2022 |
| 11 | Cap. 4 (p. 4) | Seções com 100% dos válidos: **106 para Lula, 4 para Flávio** (26,5 : 1); com mais de 90%: **6.899 para Lula, 384 para Flávio** (18 : 1) | As listas por seção. ⚠️ O TSE diz que seção com votos para um só candidato "não é uma situação incomum": em 2022, 143 seções para o hoje reeleito e 4 para o opositor. O TSE lista os estados das de 2026 (30 no Alto Solimões, AM; 20 MA; 16 PA; 8 RR; 7 TO e outras), e as 4 do Flávio em Arroio do Padre (RS), Cândido Godói (RS), Jacareacanga (PA) e Chaves (PA). ⬜ Os totais 106 e 6.899/384 não foram conferidos aqui |
| 12 | Cap. 4 (p. 4) | Essas seções "coincidem com zonas rurais de baixíssima fiscalização partidária", "onde a taxa de liberação sem biometria atinge seus picos mais elevados" | Dado de fiscal por seção (não existe nos BUs) e o cruzamento mostrado. ⚠️ Não há tabela nem número para isso no documento |
| 13 | Cap. 4 (p. 4) | Em eleição polarizada "os percentuais de votação seguem distribuições gaussianas suaves em torno da média" | É premissa, não dado. Voto por seção no Brasil é bimodal por região (Nordeste e Sul), e isso já aparecia em 2022 |
| 14 | Cap. 5 (p. 4) | Teste do 1º dígito de Benford nas 499.205 seções, "ferramenta matemática consagrada internacionalmente para detectar manipulação"; **nenhum resultado numérico** é dado, e os gráficos "não foram incluídos" | O resultado (estatística e valor-p) e o mesmo teste em 2022. ⚠️ O TSE: aplicar o padrão "apenas no primeiro dígito [...] é totalmente inapropriado"; votos por seção têm tamanho limitado (seção de 300 a 400 eleitores), o que quebra o pressuposto de Benford |
| 15 | Cap. 6 (p. 4) | "A Ordem dos Sete Minutos": Moraes "assinou o cancelamento dos passaportes de Flávio Bolsonaro exatamente sete minutos após a proclamação das urnas" | Hora da decisão. ⚠️ O registro do projeto `geopolitica-eleicao-2026` (rodada 3, 28/10) diz que foi o **pedido da PF** que foi assinado às 21h16, 7 minutos depois da confirmação matemática do TSE, e que a hora da decisão do Moraes não foi divulgada |
| 16 | Cap. 6 (p. 4) | "Uma ala da Polícia Federal articulou a prisão cautelar do principal líder da oposição com base em boatos de imprensa, forçando a sua extração do país sob proteção diplomática dos Estados Unidos" | Não é alegação de dado eleitoral. Exige documento da PF e dos EUA |
| 17 | Cap. 6 (p. 4 e 5) | "Cortina de Fumaça sobre o Banco Master": a ação contra a oposição veio na semana das apurações sobre Daniel Vorcaro "e os quarenta milhões de dólares repassados à família de magistrados do tribunal superior" | Não é alegação de dado eleitoral. A Lupa (28/10) diz que Moraes "foi citado em um relatório de inteligência" no caso Master, "mas não é formalmente alvo de nenhum inquérito" |
| 18 | Cap. 6 (p. 5) | "Donald Trump classificou a eleição como manchada por fraude decorrente da prorrogação e a Argentina acolheu a oposição, a mídia estatal chinesa admitiu que a extensão de duas horas impulsionou a virada governista" | Fontes de cada frase. ⬜ Não conferido aqui; o projeto `geopolitica-eleicao-2026` registra a fala de Trump de 26/10 e a mensagem de Xi; "a mídia chinesa admitiu" não foi confirmado |
| 19 | Conclusão (p. 5) | "A eleição regulamentar até as 17h00 foi vencida por Flávio Bolsonaro"; "A virada ocorreu exclusivamente em urnas encerradas após o prazo legal"; "Mais de oito milhões e seiscentos mil votos foram emitidos sem verificação biométrica"; "Milhões de votos foram computados na calada da noite sob picos de mais de setenta por cento pró governo"; "Os dados foram sonegados da sociedade por setenta e duas horas" | Repete 3, 4, 8, 7 e 1. ⚠️ "Computados na calada da noite" confunde a hora em que o BU entrou no painel com a hora do voto (o TSE suspendeu a recepção dos BUs entre 17h e 19h) |
| 20 | Conclusão (p. 5) | *"O resultado proclamado pelo sistema não possui integridade matemática, quebrou os protocolos mais elementares de controle biométrico e foi viabilizado por uma intervenção judicial monocrática que alterou as regras no meio do jogo."* | Depende de 3, 4, 8 a 10. Nenhum número do documento mostra voto alterado |
| 21 | Anexo (p. 6) | "O estudo não investigou [...] invasão de hackers, adulteração de código fonte ou manipulação de sistemas por satélite"; o alvo é "a substituição do controle biométrico digital pela liberação manual do mesário", "explorada em escala inédita no segundo turno" | "Escala inédita" exige comparar com 2022. ⚠️ Em 2022 foram 10.011.347 liberações sem digital (8,06%), mais que em 2026 (Jornal Razão) |
| 22 | Anexo (p. 6) | "Quando a digital do eleitor falha quatro vezes no leitor, a urna autoriza o mesário a liberar a votação mediante a simples digitação do ano de nascimento" | ✅ Procedimento real (Res. TSE 23.759/2026, segundo a Via Pantanal; e o TSE). ⚠️ O documento omite a conferência do documento com foto, a assinatura no caderno e a identificação do mesário (TSE) |
| 23 | Anexo (p. 6) | Método: arquivos "BWeb do segundo turno", "checados contra os seus respectivos hashes criptográficos originais (.sha512)"; "cem por cento das 499.205 seções"; 3 variáveis: `QT_ELEI_BIOM_SEM_HABILITACAO`, `DT_ENCERRAMENTO`, `QT_VOTOS` | O código e os arquivos usados (não publicados). Sem eles o "método é replicável" do fim não se cumpre |
| 24 | Anexo (p. 7) | As seções que fecharam depois das 17h "coincidem de forma assustadora com os municípios e zonas de maior taxa de votos sem biometria e de menor presença de fiscais partidários independentes" | Dado de fiscal por seção (não existe nos BUs) e o cruzamento mostrado. Nenhum número |
| 25 | Anexo (p. 7) | "Quase nove milhões foram chancelados sem a conferência eletrônica da identidade do votante sob a proteção da escuridão de uma prorrogação" | Mistura 8 (liberação sem digital, que acontece **o dia todo**) com a prorrogação (34.393 votos depois das 17h, TSE). Os dois números não se somam |
| 26 | Anexo (p. 7) | "Os dados estão disponíveis, o método é replicável e os números falam por si mesmos" | Código, arquivo e autor publicados. ⛔ Nenhum dos três existe |

---

## (c) Checagens e respostas oficiais

| Quem | Data e hora | Link | O que checou | Frase-chave (curta, lida na página) |
|---|---|---|---|---|
| **Justiça Eleitoral, Fato ou Boato** | 28/10 21h49 (atualizado 29/10 14h53) | [Relatório apócrifo distorce dados...](https://www.justicaeleitoral.jus.br/fato-ou-boato/checagens/2026/relatorio-apocrifo-distorce-dados-para-sugerir-fraude-nas-eleicoes-2026) | **o relatório**, ponto a ponto | "o documento inventa dados ao vincular os votos registrados após as 17h a uma candidatura" |
| idem | idem | idem | 17h e totalização | "votos incorporados ao painel depois das 19h não são necessariamente votos registrados pelos eleitores depois das 17h" |
| idem | idem | idem | biometria | "a forma de identificação da pessoa não altera o registro de sua escolha na urna eletrônica" |
| idem | idem | idem | Benford | aplicar "apenas no primeiro digito [...] é totalmente inapropriado" |
| idem | 29/10 (acréscimo) | idem | apagão de 72 h | "Não houve um 'apagão de dados'" (BUs afixados nas seções e no site Resultados em 25/10) |
| idem | idem | idem | unanimidade | "Não é uma situação incomum no pleito" (143 seções e 4 seções em 2022) |
| **TSE, nota oficial** | 27/10 15h21 (atualizada 18h18) | [Mais de 34 mil votos foram registrados após as 17h](https://www.tse.jus.br/comunicacao/noticias/2026/Outubro/eleicoes-2026-mais-de-34-mil-votos-foram-registrados-apos-as-17h-no-2o-turno) | 17h (anterior ao relatório) | "34.393 votos após as 17h"; "6.766 seções encerraram a votação após as 19h"; urnas "só podem ser encerradas a partir das 17h" |
| **Justiça Eleitoral, Fato ou Boato** | 28/10 18h25 | [É falso que 2 milhões de votos tenham sido lançados manualmente na Bahia após as 17h](https://www.justicaeleitoral.jus.br/fato-ou-boato/checagens/2026/e-falso-que-2-milhoes-de-votos-tenham-sido-lancados-manualmente-na-bahia-apos-as-17h) | alegação vizinha (Bahia) | "Na Bahia, o Tribunal identificou 1.656 votos registrados a partir das 17h" |
| **Justiça Eleitoral, Fato ou Boato** | 28/10 14h59 | [É falso que virada de votos no segundo turno seja impossível...](https://www.justicaeleitoral.jus.br/fato-ou-boato/checagens/2026/e-falso-que-virada-de-votos-no-segundo-turno-seja-impossivel-ou-comprove-fraude-nas-eleicoes) | virada | abstenção de 21,08% para 19,22% |
| **Aos Fatos** | 26 ou 27/10 (data não lida na página) | [Votos registrados após as 17h não mudam resultado das eleições](https://aosfatos.org/noticias/votos-registrados-apos-as-17h-nao-mudam-resultado-das-eleicoes) | 17h | "A diferença entre as candidaturas é aproximadamente 128 vezes maior que todos os votos registrados após as 17h" |
| **AFP Checamos** | 26/10, atualizada 27/10 | [Prorrogação do segundo turno teve pouco mais de 34 mil votos...](https://checamos.afp.com/doc.afp.com.D4HN663) | 17h, recontado por Álvaro Justen (Brasil.IO) e Pedro Burgos | "Ambos confirmaram que pouco mais de 34 mil votos foram computados nas duas horas de prorrogação" |
| **Estadão Verifica** | 27/10 9h55 | [Campanha de desinformação impulsiona falsa tese de vitória 'matematicamente impossível' de Lula](https://www.estadao.com.br/estadao-verifica/campanha-de-desinformacao-impulsiona-falsa-tese-de-vitoria-matematicamente-impossivel-de-lula/) | virada e 17h | cita o Monitor do Debate Político da USP: "34,7 mil votos foram depositados nas urnas eletrônicas após às 17h" |
| **Lupa** | 28/10 19h32 | [Após fuga do Brasil, Flávio Bolsonaro mente sobre eleições em carta...](https://www.agencialupa.org/checagem/2026/10/28/apos-fuga-do-brasil-flavio-bolsonaro-mente-sobre-eleicoes-em-carta-com-teor-golpista/) | carta do Flávio (não o relatório) | "Não há qualquer prova de fraude nas eleições do 2º turno" |
| **Via Pantanal** (imprensa, não checagem) | 28/10 "16h36" | [Relatório que aponta 8,6 milhões...](https://viapantanal.com/noticia/51397/relatorio-que-aponta-8-6-milhoes-de-votos-sem-biometria-no-2o-turno-viraliza-nas-redes-veja-o-que-diz-o-documento) | descreve o relatório | "documento, por si só, não comprova irregularidade" |
| **Jornal Razão** (imprensa, Santa Catarina) | 29/10 10h16 | [Problemas na biometria: mais de 8,6 milhões votaram sem a digital no 2º turno](https://jornalrazao.com/politica/biometria-milhoes-votaram-sem-digital-segundo-turno-tse) | **recontou** a biometria nos 499.205 BUs | "foram 8.632.488 pessoas, o equivalente a 6,73%"; em 2022, "10.011.347 eleitores [...] 8,06%" |
| **g1 Fato ou Fake, Comprova, UOL Confere, Reuters, Boatos.org** | | | | ⛔ nada encontrado sobre o relatório até 29/10, 15h (o site da Reuters bloqueia a ferramenta de busca usada) |

---

## (d) O que fica não confirmado

| Item | Por quê |
|---|---|
| **Autor do relatório** | sem nome no documento, sem metadado nas imagens, sem PDF |
| **Primeiro post e quem fez** | o post do X de 28/10 13h28 está indisponível; a Wayback Machine estava fora do ar |
| **Se existe PDF** | o TSE fala em "imagens de um documento"; nenhuma busca achou PDF |
| **A versão de 4 páginas do X** | o TSE diz 4 páginas; só achei a de 7. Não confirmado quais páginas formam a de 4 |
| **Telegram, WhatsApp, Kwai, TikTok** | não verificado |
| **Repost por políticos e grandes perfis brasileiros ou americanos (além de Mannarino e Chequei Brasil)** | não confirmado |
| **Se Mannarino postou as páginas no X** | só confirmado no Instagram; a página 8 é print de um tweet dele pedindo que sigam o Instagram |
| **Data de publicação do CSV "BWeb" do 2º turno** | o catálogo do Dados Abertos consultado só lista o BWeb do 1º turno; o pacote "arquivos transmitidos" do 2º turno entrou em 28/10 11h07, com arquivos no servidor desde 26/10 |
| **"1,8 milhão de votos" atribuído ao TSE** | aparece em resumos automáticos de busca como frase da checagem do TSE, mas **não está no texto da página** lido em 29/10 |
| **"106 seções" para o Lula com 100%** | é número do relatório; a lista do TSE soma 101 seções nos estados que ela cita, e a página não dá o total. Não recontado aqui |
| **Os números do capítulo 1 (52,39%, 1,8 mi, 6,1 mi) e do capítulo 2 (339.593, 2.472, 6.333 seções)** | não recontados aqui; pela nota do TSE, o grupo "até 17h00" quase não existe (497.333 seções com encerramento depois das 17h) |
| **Fuso usado pela Via Pantanal** | o horário 16h36 vem antes do post de 17h00; se o site usa o horário de MS, são 17h36 de Brasília |
| **Frases do capítulo 6 (Trump, Argentina, mídia chinesa, US$ 40 milhões)** | fora do escopo desta pesquisa; conferir no projeto `geopolitica-eleicao-2026` |

---

## Conferências feitas

- Os 4.430.191 da margem: 64.256.232 menos 59.826.041 (números do TSE no Fato ou Boato e no Estadão Verifica). Bate.
- 8.632.488 ÷ 128.236.074 = 6,73%. Bate com o relatório e com o Jornal Razão.
- 106 ÷ 4 = 26,5 e 6.899 ÷ 384 = 17,97 (o relatório arredonda para 18). Bate com o próprio relatório.
- Soma da tabela do capítulo 2: 348.398 seções e 90.602.855 eleitores (70,7% do comparecimento); 674.799 + 1.856.306 = 2.531.105 (os "mais de 2,5 milhões").
- Horários do X: pelo ID de cada post, conferidos com o horário que o X mostra (16:28 do @Gigapardos).
- Horário do Instagram: atributo `datetime` da página do post.
- Datas de entrada no Dados Abertos: API do catálogo (`dadosabertos.tse.jus.br/api/3/action/package_show`), campo `created`; datas no servidor: cabeçalho `Last-Modified` de `cdn.tse.jus.br/.../arqurnatot/bu_imgbu_logjez_rdv_vscmr_2026_2t_<UF>.zip`, lidos em 29/10 às 15h07.
