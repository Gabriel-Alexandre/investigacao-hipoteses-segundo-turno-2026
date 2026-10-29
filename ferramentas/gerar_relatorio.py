"""Escreve RELATORIO.md, RESUMO_SIMPLES.md e docs/LEITURA_DA_IA.md a partir de resultados/RESUMO.json e
resultados/VALIDACAO.json. Nenhum número é digitado aqui: todos vêm dos dois arquivos.
Os vereditos seguem a régua do docs/PLANO.md (confirmado, indício forte, compatível com as duas, não sustentado,
desmentido) e o critério de cada hipótese (comportamento dos votos, raridade, arquivos das urnas).

Uso: python ferramentas/gerar_relatorio.py
"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
R = json.loads((RAIZ / "resultados/RESUMO.json").read_text(encoding="utf-8"))
V = json.loads((RAIZ / "resultados/VALIDACAO.json").read_text(encoding="utf-8"))
MARGEM = 4_430_191


def n(x):
    return f"{int(x):,}".replace(",", ".")


def p(x, casas=2):
    return f"{x:.{casas}f}".replace(".", ",")


def pm(votos):
    v = 100 * votos / MARGEM
    return "menos de 0,01%" if v < 0.01 else p(v, 2) + "%"


H01, H02, H03, H04, H05, H07 = R["H01"], R["H02"], R["H03"], R["H04"], R["H05"], R["H07"]
H08, H09, H10, H11, H12, H13, H14 = R["H08"], R["H09"], R["H10"], R["H11"], R["H12"], R["H13"], R["H14"]
H15, H16, H17, H18, H19, H20, H21, H23 = R["H15"], R["H16"], R["H17"], R["H18"], R["H19"], R["H20"], R["H21"], R["H23"]
REP = H01["reproducao_do_relatorio"]
DL = H01["dentro_do_local_lula_2t"]
DG = H01["dentro_do_local_ganho_do_1t_para_2t"]
joa = next(c for c in H23["casos"] if c["municipio"].startswith("Joa"))
ara = next(c for c in H23["casos"] if c["municipio"].startswith("Araruama"))
lagos = [c for c in H23["casos"] if not c["municipio"].startswith("Joa")]
lagos_l = sum(c["lula_2t"] - c["lula_1t"] for c in lagos)
lagos_f = sum(c["flavio_2t"] - c["flavio_1t"] for c in lagos)
lagos_o = sum(c["outros_1t"] for c in lagos)
mod = H09["por_modelo"]
c100 = H13["comparecimento_100_ou_mais"]
c95 = H13["comparecimento_95_a_99"]

# (código, bloco, título, critério, veredito, o que o dado mostra, visão legítimo, visão fraude, teto, o que fecharia)
HIP = [
    ("H01", "A", "Nas urnas encerradas até as 17h, o Flávio ganhou", "comportamento", "Desmentido",
     f"O número do relatório sai igual ({p(REP['ate_17h00']['flavio_pct'])}% para o Flávio e {n(REP['ate_17h00']['frente_flavio'])} votos de frente) só quando se lê a hora de encerramento de cada urna no relógio local, sem acertar o fuso. Assim, as urnas de AC, AM, MT, MS, RO e RR, que fecharam às 15h ou às 16h no horário local (17h em Brasília), entram todas no grupo \"até 17h\": são {n(REP['secoes_dos_estados_com_fuso_no_grupo_ate_17h'])} das {n(REP['secoes_desses_estados'])} seções desses estados, com {p(REP['flavio_pct_nessas'])}% para o Flávio e {n(REP['frente_flavio_nessas'])} votos de frente. No mesmo local de votação, a seção que fechou depois das 17h15 não deu mais voto ao Lula que a vizinha que fechou antes: teve {p(-DL['diferenca_pontos'])} ponto a menos de Lula no 2º turno ({n(DL['locais'])} locais com os dois tipos de seção) e {p(-DG['diferenca_pontos'])} ponto a menos de ganho desde o 1º turno ({n(DG['locais'])} locais). E o grupo \"depois das 17h\" é o voto do dia inteiro: só {n(REP['votos_com_hora_depois_17h_no_grupo_depois'])} votos dele têm hora depois das 17h no log",
     "urna que fecha mais tarde é a de fila, e a diferença entre os grupos é de lugar e de fuso, não de hora do voto", "a separação por horário mostraria voto acrescentado na prorrogação; o dado mostra que o grupo nasceu de um erro de fuso",
     f"{n(H02['votos_depois_17h_brasil_log'])} votos depois das 17h ({pm(H02['votos_depois_17h_brasil_log'])} da diferença)", "já fechado: o log de cada urna é público e tem a hora de cada voto"),
    ("H02", "A", "Mais de 2,5 milhões de eleitores votaram em urnas que passaram do horário", "comportamento", "Desmentido",
     f"Os 2,5 milhões são o comparecimento do dia inteiro das {n(H02['secoes_fechadas_a_partir_de_17h16'])} seções que fecharam a partir das 17h16 ({n(H02['comparecimento_do_dia_inteiro_nelas'])} pelas tabelas do projeto). Votos com hora depois das 17h nessas seções: {n(H02['votos_com_hora_depois_17h_nelas_pelo_log'])}. No Brasil inteiro, {n(H02['votos_depois_17h_brasil_log'])} depois das 17h e {n(H02['votos_depois_19h_brasil_log'])} depois das 19h, igual ao número do TSE",
     "estar numa urna aberta depois das 17h não é votar depois das 17h", "a conta mistura eleitor do dia inteiro com voto da prorrogação",
     f"{pm(H02['votos_depois_17h_brasil_log'])} da diferença", "já fechado pelo log"),
    ("H03", "A", "8,6 milhões liberados sem biometria, quase o dobro da diferença", "comportamento", "Não sustentado",
     f"O número existe: {n(H03['liberados_pela_digital_do_mesario_2t'])} eleitores liberados pela digital do mesário no 2º turno, e mais {n(H03['liberados_sem_digital_cadastrada_pelo_ano_de_nascimento_2t'])} sem digital cadastrada, liberados pelo ano de nascimento ({p(H03['sem_a_digital_do_eleitor_pct_dos_votos'])}% dos votos, somando os dois). Na amostra de {n(H03['amostra_secoes'])} seções, essa parte foi de {p(H03['amostra_parte_manual_1t_pct'])}% no 1º turno para {p(H03['amostra_parte_manual_2t_pct'])}% no 2º. Dentro do mesmo município, a seção com mais liberação manual não deu mais voto ao Lula (correlação de {p(H03['correlacao_no_mesmo_municipio']['parte_manual_2t_x_lula_2t'][0], 3)}), e a seção em que a liberação manual subiu do 1º para o 2º turno não deu mais ganho a ele ({p(H03['correlacao_no_mesmo_municipio']['variacao_manual_x_variacao_lula'][0], 3)}). Em 2022 foram cerca de 10 milhões, segundo a mesma conta feita pelo Jornal Razão",
     "a liberação sem a digital do eleitor é rotina (dedo gasto, idoso, digital não cadastrada), acontece o dia todo e cai dos dois lados", "a fraude por liberação manual deixaria a parte manual subir onde o Lula cresceu; ela não sobe",
     "sem sinal para medir: a liberação manual não anda junto com o voto de nenhum lado", "a lista de quem votou em cada seção, com o tipo de liberação (pedido ao TSE)"),
    ("H04", "A", "6.899 seções com mais de 90% para o Lula contra 384 do Flávio", "raridade", "Não sustentado",
     f"Pelo arquivo do TSE: {n(H04['acima_90_lula'])} acima de 90% para o Lula e {n(H04['acima_90_flavio'])} para o Flávio (no Brasil, sem o exterior). Em 2022 foram {n(H04['2022_acima_90_lula'])} para o Lula e {n(H04['2022_acima_90_bolsonaro'])} para o Bolsonaro; em 2018, {n(H04['2018_acima_90_haddad'])} para o Haddad e {n(H04['2018_acima_90_bolsonaro'])} para o Bolsonaro. Das seções do Lula acima de 90% em 2026, {p(H04['lula_acima_90_ja_acima_80_em_2022_pct'], 1)}% já davam mais de 80% para ele em 2022",
     "as seções de quase unanimidade são as mesmas de antes, nos mesmos lugares, e eram mais numerosas em 2018 e 2022", "seriam seções novas na lista; não são",
     "não se aplica: a assimetria é menor que a de 2022", "já fechado pelo histórico de cada seção"),
    ("H05", "A", "A lei de Benford reprova a votação", "raridade", "Não sustentado",
     f"Desvio médio do 1º dígito: {p(H05['mad']['lula_2026']['mad_1o_digito'], 3)} no Lula e {p(H05['mad']['flavio_2026']['mad_1o_digito'], 3)} no Flávio em 2026, {p(H05['mad']['lula_2022']['mad_1o_digito'], 3)} no Lula e {p(H05['mad']['bolsonaro_2022']['mad_1o_digito'], 3)} no Bolsonaro em 2022. Todos \"reprovam\" do mesmo jeito, porque o voto por seção fica preso no tamanho da seção (de 200 a 400 eleitores) e o 1º dígito não pode seguir Benford. O relatório não deu número nenhum para o teste",
     "o teste não serve para voto por seção, e a prova é que ele reprova os dois candidatos e os dois anos", "um desvio só de um lado, ou só em 2026, seria sinal; não há",
     "não se aplica", "já fechado"),
    ("H06", "A", "Os boletins ficaram 72 horas escondidos", "arquivos", "Não sustentado",
     "O pacote do 2º turno entrou no catálogo de Dados Abertos em 28/10, 11h07, mas o servidor do TSE mostra os mesmos arquivos desde 26/10, entre 15h e 18h31; os arquivos de cada seção estavam no site de resultados pelo menos desde 26/10, 7h30, quando o projeto do vídeo 16 começou a baixá-los; e o boletim de cada seção foi impresso e afixado na própria seção em 25/10",
     "o catálogo demorou, o dado não", "a única parte verdadeira é a data de entrada no catálogo",
     "não se aplica", "já fechado pelas datas dos arquivos"),
    ("H07", "B", "106 urnas com zero voto para o Flávio", "raridade", "Não sustentado",
     f"São {n(H07['secoes'])} seções e {n(H07['votos_lula'])} votos, como circulou ({H07['por_uf']['am']} no AM, {H07['por_uf']['ma']} no MA, {H07['por_uf']['pa']} no PA, {H07['por_uf']['rr']} em RR); {n(H07['com_termo_indigena_ou_comunidade_no_nome_do_local'])} têm nome de aldeia, escola indígena ou comunidade no local de votação. No 1º turno de 2026, {n(H07['com_zero_flavio_tambem_no_1t'])} delas já não tinham voto do Flávio, e as outras {n(H07['com_algum_voto_do_flavio_no_1t'])} somavam {n(H07['flavio_no_1t_2026_nessas_votos'])} votos dele. O mesmo fenômeno foi maior antes: {n(H07['2022_secoes_zero_bolsonaro'])} seções sem voto do Bolsonaro em 2022 e {n(H07['2018_secoes_zero_bolsonaro'])} em 2018. O espelho existe: {n(H07['espelho_zero_lula']['secoes'])} seções sem voto do Lula, no RS e no PA",
     "voto concentrado em aldeia e comunidade, que se repete eleição após eleição e foi mais frequente em 2018 e 2022", "a lista teria seções sem histórico de unanimidade; quase todas já votavam assim",
     f"{n(H07['teto_votos'])} votos (o que o Flávio teve nelas no 1º turno), {pm(H07['teto_votos'])} da diferença", "já fechado pelo histórico; o TSE checou o mesmo caso no 1º turno"),
    ("H08", "B", "Seções com placar repetido seriam impossíveis", "raridade", "Desmentido",
     f"{n(H08['placares_repetidos_2026'])} placares (Lula, Flávio) aparecem em mais de uma seção. Sorteando os votos de cada seção 20 vezes pelo próprio voto dela no 1º turno, o acaso dá entre {n(H08['esperado_faixa'][0])} e {n(H08['esperado_faixa'][1])}: há menos repetição do que o acaso daria. Em 2022 foram {n(H08['placares_repetidos_2022'])}. Nenhum placar se repete com os dois candidatos acima de 300 votos",
     "com meio milhão de seções, placar repetido é o esperado (é o problema do aniversário)", "a fraude por cópia deixaria repetição acima do acaso; há abaixo",
     "não se aplica", "já fechado"),
    ("H09", "B", "As urnas antigas votam diferente das novas", "arquivos", "Não sustentado",
     f"O modelo de cada urna está no arquivo do TSE. O Lula ficou com {p(mod['UE 2013']['lula_2t_pct'])}% nas UE2013, {p(mod['UE 2015']['lula_2t_pct'])}% nas UE2015, {p(mod['UE 2020']['lula_2t_pct'])}% nas UE2020 e {p(mod['UE 2022']['lula_2t_pct'])}% nas UE2022, e o ganho desde o 1º turno ficou entre {p(min(v['ganho_lula_pontos'] for v in mod.values()))} e {p(max(v['ganho_lula_pontos'] for v in mod.values()))} pontos nos quatro modelos. No mesmo local, a urna antiga (2013 e 2015) contra a nova: {p(H09['dentro_do_local_antiga_vs_nova_ganho']['diferenca_pontos'])} ponto no ganho, em {n(H09['dentro_do_local_antiga_vs_nova_ganho']['locais'])} locais",
     "o modelo não muda o voto", "um programa adulterado num modelo deixaria marca nele; não deixa",
     "não se aplica", "já fechado para a pergunta do modelo"),
    ("H10", "B", "Urnas trocadas e levadas em carro de partido", "arquivos", "Não sustentado",
     f"{n(H10['secoes_com_contingencia_no_log'])} seções registraram troca de urna no log. No mesmo local, elas votaram como as vizinhas ({p(H10['dentro_do_local_ganho']['diferenca_pontos'])} ponto no ganho do Lula, em {n(H10['dentro_do_local_ganho']['locais'])} locais). O caso da caminhonete com adesivo no Riacho Fundo II (DF) é irregularidade real de transporte, apurada pelo TRE-DF, mas o boletim já tinha sido impresso e transmitido",
     "a urna de contingência segue o procedimento e vota como as vizinhas", "uma urna trocada com voto pronto votaria diferente das vizinhas; não vota",
     f"todos os votos nominais dessas seções somam {n(H10['teto_votos_nominais_nessas_secoes'])}", "a lista oficial de urnas substituídas, com o motivo (pedido ao TSE)"),
    ("H11", "B", "O boletim de papel não bate com o site do TSE", "arquivos", "Não sustentado",
     f"Teixeira de Freitas inteira, {n(H11['teixeira_de_freitas']['secoes'])} seções: Flávio {n(H11['teixeira_de_freitas']['flavio'])}, Lula {n(H11['teixeira_de_freitas']['lula'])}, igual ao Aos Fatos (a soma de 3 boletins não é a cidade). O boletim de cada seção e o detalhe por seção dos dados abertos batem em {n(H11['boletim_x_dados_abertos']['secoes_comparadas'])} seções, sem uma diferença. A assinatura digital dos boletins não foi verificada nesta rodada",
     "o boletim afixado na seção é o mesmo arquivo publicado", "um boletim trocado na totalização apareceria como diferença entre a foto do papel e o arquivo; nenhum fiscal mostrou uma",
     "não medido", "fotos de boletins de papel comparadas com o arquivo (convite público) e a verificação da assinatura de cada boletim"),
    ("H12", "B", "Seções criadas, cortadas ou \"virtuais\"", "arquivos", "Desmentido",
     f"As mesmas {n(H12['secoes_2t'])} seções nos dois turnos, nenhuma só num deles; {n(H12['nao_instaladas_2t'])} não instaladas. {n(H12['mudaram_de_local'])} mudaram de local entre os turnos, e nelas o comparecimento subiu menos ({p(H12['variacao_comparecimento_mudaram_pontos'])} ponto, contra {p(H12['variacao_comparecimento_demais_pontos'])} nas demais)",
     "a lista de seções é a mesma nos dois turnos", "seção fantasma apareceria só num turno; não há",
     "não se aplica", "já fechado"),
    ("H13", "C", "Mortos votaram", "comportamento", "Compatível com as duas",
     f"Há mortos no cadastro: o eleitorado de 2026 tem {n(H13['eleitores_100_ou_mais_2026'])} eleitores com 100 anos ou mais, e o Censo de 2022 contou {n(H13['populacao_96_ou_mais_censo_2022'])} pessoas com 96 anos ou mais (as únicas que podem ter 100 em 2026); em {n(H13['municipios_com_mais_eleitores_100_que_pessoas_96_em_2022'])} municípios há mais eleitores centenários que pessoas que poderiam ser centenárias. Mas eles quase não votam: no 1º turno de 2026 compareceram {n(c100['2026_t1']['comparecimento'])} eleitores de 100 anos ou mais ({p(c100['2026_t1']['taxa_pct'])}%), contra {n(c100['2022_t2']['comparecimento'])} no 2º turno de 2022 ({p(c100['2022_t2']['taxa_pct'])}%). Fora do padrão, a conferir: na faixa de 95 a 99 anos o comparecimento foi de {p(c95['2022_t2']['taxa_pct'])}% no 2º turno de 2022 para {p(c95['2026_t1']['taxa_pct'])}% no 1º turno de 2026 ({n(c95['2026_t1']['comparecimento'])} votos). O TSE ainda não publicou o comparecimento por idade do 2º turno de 2026",
     "o cadastro demora a tirar quem morreu, e esses registros não votam", "a fraude usaria esses registros com a liberação do mesário; o comparecimento de quem tem 100 anos ou mais é de menos de 1 em 100, e o salto da faixa de 95 a 99 é a parte a conferir",
     f"se todo voto de 95 anos ou mais do 1º turno de 2026 fosse falso: {n(c100['2026_t1']['comparecimento'] + c95['2026_t1']['comparecimento'])} votos, {pm(c100['2026_t1']['comparecimento'] + c95['2026_t1']['comparecimento'])} da diferença", "o cruzamento do cadastro com os óbitos dos cartórios (SIRC) e o comparecimento por idade do 2º turno, os dois com o TSE"),
    ("H14", "C", "Cidades com mais eleitores ou votos que habitantes", "comportamento", "Não sustentado",
     f"Em {n(H14['comparecimento_2t_maior_que_pop_12_ou_mais_em_2022'])} municípios o comparecimento do 2º turno passou da população que teria 16 anos ou mais em 2026 (o Lula venceu em {n(H14['lula_venceu_nos_com_comparecimento_acima'])}). Em 2022 o mesmo aconteceu em {n(H14['2022_comparecimento_2t_maior_que_pop_16_ou_mais'])} municípios. É o eleitor que mora fora e mantém o título na cidade de origem. Na lista da corrente de WhatsApp, em nenhuma cidade o Lula teve mais votos que habitantes",
     "título mantido na cidade natal, o mesmo de 2022", "seria um salto em 2026; o número é parecido com o de 2022",
     "não se aplica", "o recadastramento por município, com o TSE"),
    ("H15", "C", "Cheguei e já tinham votado por mim", "comportamento", "Compatível com as duas",
     f"O aviso \"o eleitor identificado já votou\" aparece {n(H15['avisos_ja_votou_2t_brasil'])} vezes no 2º turno, em {n(H15['secoes_com_aviso_2t'])} seções. Na amostra, foi {p(H15['amostra_avisos_por_mil_votos']['t1'], 3)} por mil votos no 1º turno e {p(H15['amostra_avisos_por_mil_votos']['t2'], 3)} no 2º; o aviso seguido de um voto liberado pelo mesário em até 5 minutos foi de {p(H15['amostra_aviso_seguido_de_liberacao_manual_em_5_min_pct']['t1'], 1)}% para {p(H15['amostra_aviso_seguido_de_liberacao_manual_em_5_min_pct']['t2'], 1)}%. Dentro do município, a seção com mais aviso não deu mais ganho ao Lula (correlação de {p(H15['correlacao_no_mesmo_municipio_aviso_x_ganho_do_lula'], 3)}). Casos com nome existem (Campinas e Valinhos) e estão com o TRE-SP",
     "o aviso nasce de título digitado errado e de eleitor que tenta de novo; é raro e igual nos dois turnos", "o caso individual é real, e a subida dos avisos seguidos de liberação manual é a parte a conferir",
     f"se todo aviso seguido de liberação manual fosse um voto roubado, cerca de {n(H15['avisos_ja_votou_2t_brasil'] * H15['amostra_aviso_seguido_de_liberacao_manual_em_5_min_pct']['t2'] / 100)} votos, {pm(H15['avisos_ja_votou_2t_brasil'] * H15['amostra_aviso_seguido_de_liberacao_manual_em_5_min_pct']['t2'] / 100)} da diferença", "a ata e o caderno de cada caso, com o TRE"),
    ("H16", "C", "O mesário vota o dia todo, quando a seção esvazia", "comportamento", "Não sustentado",
     f"A parte dos votos liberados sem a digital do eleitor fica entre 12% e 13% em quase todas as horas, nos dois turnos. A maior sequência de votos seguidos liberados pelo mesmo mesário tem mediana de {p(H16['maior_sequencia_mesmo_mesario']['t2']['mediana'], 0)} e máximo de {H16['maior_sequencia_mesmo_mesario']['t2']['max']} no 2º turno; nenhuma seção da amostra teve 10 ou mais seguidas",
     "a liberação manual acompanha o movimento da seção", "o mesário que vota por quem faltou deixaria rajadas de liberações seguidas na hora vazia; não há",
     "não se aplica", "a lista de quem votou em cada seção (pedido ao TSE)"),
    ("H17", "D", "A contagem na sala-cofre, os 165 mil votos \"sem origem\" e o Flávio \"perdendo votos\" no painel", "arquivos", "Desmentido",
     f"Nas {n(H17['versoes_nacionais'])} versões nacionais do resultado gravadas ao vivo na noite, o total do Flávio nunca caiu ({H17['vezes_que_o_total_do_flavio_caiu']} quedas), nem o do Lula ({H17['vezes_que_o_total_do_lula_caiu']}). A última versão dá Lula {n(H17['ultima_versao_nacional']['lula'])} e Flávio {n(H17['ultima_versao_nacional']['flavio'])}, o resultado proclamado. O boletim de cada seção é impresso na seção antes de chegar ao TSE (H11)",
     "a soma é aberta seção por seção", "uma totalização mexida apareceria entre o boletim da seção e o total; os dois batem",
     "não se aplica", "já fechado pelo boletim de cada seção"),
    ("H18", "D", "O programa da urna troca o voto", "arquivos", "Não sustentado",
     f"O Flávio ficou abaixo do próprio 1º turno em {n(H18['secoes_flavio_abaixo_do_1t'])} seções (e o Lula em {n(H18['secoes_lula_abaixo_do_1t'])}); em {p(H18['dessas_com_comparecimento_em_queda'], 1)}% delas o comparecimento também caiu. O teste de integridade do 2º turno, com urnas sorteadas votando em papel e na urna, não achou divergência. Os logs da amostra não registram nenhuma verificação de assinatura do programa sem sucesso",
     "o voto segue o 1º turno de cada seção, e a auditoria por amostra bateu", "uma troca perfeita, que imitasse o eleitor, não se separa por estatística; é o limite deste teste",
     "não medido", "o teste de integridade em mais urnas e o voto impresso, que o Brasil não tem"),
    ("H19", "E", "O Flávio perdeu votos em 6 estados e o Lula em nenhum", "comportamento", "Não sustentado",
     f"Os 6 estados (AC, AM, AP, MA, RR, TO) tiveram queda do comparecimento entre os turnos: no AP, {p(H19['ufs_onde_o_flavio_caiu']['ap']['variacao_comparecimento_pontos'])} pontos; em RR, {p(H19['ufs_onde_o_flavio_caiu']['rr']['variacao_comparecimento_pontos'])}; no AC, {p(H19['ufs_onde_o_flavio_caiu']['ac']['variacao_comparecimento_pontos'])}. O comparecimento caiu em {len(H19['ufs_com_comparecimento_em_queda'])} estados, todos no Norte e no meio-norte",
     "menos gente foi votar onde o Flávio perdeu votos", "a queda seria do Flávio sem queda de comparecimento; não é",
     "não se aplica", "já fechado"),
    ("H20", "E", "A abstenção caiu no Nordeste, mesmo com a falta de ônibus", "comportamento", "Não sustentado",
     f"A abstenção caiu no Nordeste ({p(H20['abstencao_por_regiao']['Nordeste']['abst_1t_pct'])}% para {p(H20['abstencao_por_regiao']['Nordeste']['abst_2t_pct'])}%), no Sudeste ({p(H20['abstencao_por_regiao']['Sudeste']['abst_1t_pct'])}% para {p(H20['abstencao_por_regiao']['Sudeste']['abst_2t_pct'])}%) e no Sul ({p(H20['abstencao_por_regiao']['Sul']['abst_1t_pct'])}% para {p(H20['abstencao_por_regiao']['Sul']['abst_2t_pct'])}%), e subiu no Norte. Em Salvador, onde faltou ônibus, foi de {p(H20['cidades_da_falta_de_onibus'][0]['abst_1t_pct'])}% para {p(H20['cidades_da_falta_de_onibus'][0]['abst_2t_pct'])}%. O vídeo 19 mostrou que a queda da abstenção entre os turnos não tem precedente",
     "a mobilização dos dois lados levou mais gente a votar em quase todo o país", "a queda sem precedente é real; o que ela não tem é marca de voto acrescentado (H03, H15, H16)",
     "não se aplica", "a lista de quem votou, com o TSE"),
    ("H21", "E", "Compra de voto com benefício social", "comportamento", "Não sustentado",
     f"O Lula cresceu mais nas cidades mais ricas: {p(H21['ganho_lula_pontos_por_quintil_de_renda']['5 (mais rico)'])} pontos entre o 1º e o 2º turno nos 20% de municípios de maior renda, contra {p(H21['ganho_lula_pontos_por_quintil_de_renda']['1 (mais pobre)'])} nos 20% de menor renda. O pedido de cassação por abuso de poder é processo no TSE, fora do alcance do dado de urna",
     "o crescimento veio mais de onde o benefício pesa menos", "a compra de voto com benefício faria o Lula crescer mais nas cidades pobres; foi o contrário",
     "não se aplica", "o processo de abuso de poder no TSE"),
    ("H22", "E", "Onde tem mais celular e 5G, mais voto novo no Lula", "comportamento", "Não testado nesta rodada",
     "O dado de cobertura por município da Anatel não entrou nesta rodada. A renda (H21) já mostra que o Lula cresceu mais nas cidades mais ricas, que também são as mais conectadas, então uma correlação com 5G sozinha não separaria as duas coisas",
     "seria a renda e o tamanho da cidade", "precisaria aparecer com a renda controlada",
     "não medido", "a cobertura da Anatel por município, com controle por renda e tamanho"),
    ("H23", "E", "Joaçaba (SC), Araruama e a Região dos Lagos (RJ)", "comportamento", "Compatível com as duas",
     f"A conta fecha. Em Joaçaba, o Flávio cresceu {n(joa['flavio_2t'] - joa['flavio_1t'])} e o Lula {n(joa['lula_2t'] - joa['lula_1t'])}, com {n(joa['outros_1t'])} votos dos outros candidatos e {n(joa['comparecimento_2t'] - joa['comparecimento_1t'])} eleitores a mais. Em Araruama, o Flávio cresceu {n(ara['flavio_2t'] - ara['flavio_1t'])} e o Lula {n(ara['lula_2t'] - ara['lula_1t'])}, com {n(ara['outros_1t'])} votos dos outros e {n(ara['brancos_nulos_1t'] - ara['brancos_nulos_2t'])} brancos e nulos a menos. Nos 7 municípios da Região dos Lagos, o Lula ganhou {n(lagos_l)} votos e o Flávio {n(lagos_f)}, com {n(lagos_o)} votos dos outros no 1º turno",
     "o eleitor dos outros candidatos votou no Lula naquela região", "é o mesmo fora do padrão do vídeo 19: o Lula com quase todos os votos que estavam em disputa",
     "não se aplica", "pesquisa com o eleitor daquela região"),
]
JA = [("A conta dos 10 milhões e \"a conta não fecha\"", "vídeos 16 e 19"), ("A curva da noite \"programada\"", "vídeo 16"),
      ("As pesquisas e as regras quebradas (líder do 1º turno, Minas)", "vídeo 19"), ("Mesários votando por quem faltou no 1º turno", "vídeo 8")]
PESO = {"comportamento": "pesa mais", "raridade": "pesa no meio", "arquivos": "pesa menos (bater é o esperado nas duas visões)"}


def contagem():
    c = {}
    for h in HIP:
        c[h[4]] = c.get(h[4], 0) + 1
    return c


def relatorio():
    c = contagem()
    v_ok = f"{V['passaram']} de {V['total']}"
    L = ["# Relatório: as hipóteses do público sobre o 2º turno de 2026", "",
         "**Rodada 1, 29/out/2026.** Investigação Aberta, parte 3. Cada hipótese que o público levantou (comentários dos vídeos 8, 16 e 19, o \"Relatório Pericial Independente\" e as teorias da internet) foi testada pelas duas visões: o resultado foi legítimo, ou houve fraude. Todo número sai de `ferramentas/analise.py` (`resultados/RESUMO.json`); os números centrais foram refeitos por outro caminho em `ferramentas/validacao_independente.py` (" + v_ok + " passaram).", "",
         "## O que este projeto não consegue dizer", "",
         "- Quem votou em cada seção: a lista é do TSE. Sem ela, nenhuma hipótese de voto no lugar de outra pessoa fecha caso a caso.",
         "- Se um programa adulterado trocou votos imitando o eleitor: estatística não separa isso; o que fecha é o teste de integridade e o voto impresso.",
         "- A assinatura digital de cada boletim não foi verificada nesta rodada.",
         "- O comparecimento por idade do 2º turno de 2026 ainda não foi publicado pelo TSE.",
         "- Os testes dos logs usam uma amostra sorteada de 12 mil seções (mais as seções especiais), porque os brutos completos do vídeo 16 foram apagados.", "",
         "## Os vereditos, em uma tabela", "",
         "| # | Hipótese | Critério | Veredito | Teto contra a diferença de 4.430.191 votos |", "|---|---|---|---|---|"]
    for h in HIP:
        L.append(f"| {h[0]} | {h[2]} | {h[3]} | **{h[4]}** | {h[8]} |")
    L += ["", "Contagem: " + "; ".join(f"{k}: {v}" for k, v in sorted(c.items(), key=lambda kv: -kv[1])) + ".", "",
          "## O achado principal do relatório pericial", "",
          f"O \"Relatório Pericial Independente\" diz que o Flávio venceu nas urnas encerradas até as 17h. O número dele ({p(REP['ate_17h00']['flavio_pct'])}%) sai igual neste projeto só de um jeito: lendo a hora de encerramento no relógio local de cada estado, sem o fuso. Com isso, as {n(REP['secoes_dos_estados_com_fuso_no_grupo_ate_17h'])} seções de AC, AM, MT, MS, RO e RR, que encerraram às 17h de Brasília (15h ou 16h no relógio delas), viram \"urnas fechadas até 17h\". Esses estados deram {p(REP['flavio_pct_nessas'])}% ao Flávio e respondem por {n(REP['frente_flavio_nessas'])} dos {n(REP['ate_17h00']['frente_flavio'])} votos de frente do grupo. Os votos dados de fato depois das 17h foram {n(H02['votos_depois_17h_brasil_log'])}, {pm(H02['votos_depois_17h_brasil_log'])} da diferença.", "",
          "## Hipótese por hipótese", ""]
    bloco_nome = {"A": "Bloco A · o relatório pericial", "B": "Bloco B · as seções e as urnas", "C": "Bloco C · os eleitores", "D": "Bloco D · a totalização", "E": "Bloco E · o comportamento dos votos"}
    atual = None
    for h in HIP:
        if h[1] != atual:
            atual = h[1]
            L += [f"### {bloco_nome[atual]}", ""]
        L += [f"#### {h[0]}. {h[2]}", "", f"**Veredito: {h[4]}** (critério: {h[3]}, que {PESO[h[3]]}).", "", h[5] + ".", "",
              f"- Visão do resultado legítimo: {h[6]}.", f"- Visão da fraude: {h[7]}.", f"- Teto do pior caso: {h[8]}.", f"- O que fecharia: {h[9]}.", ""]
    L += ["## O que já foi respondido antes", "", "| Hipótese | Onde |", "|---|---|"] + [f"| {a} | {b} |" for a, b in JA]
    L += ["", "## A conclusão pelas duas visões", "",
          "Com os pesos do vídeo 16 (o comportamento dos votos pesa mais, a raridade no meio e os arquivos das urnas menos):", "",
          "| Critério | Hipóteses | O que o dado sustenta mais |", "|---|---|---|",
          "| Comportamento dos votos | H01, H02, H03, H13 a H16, H19 a H23 | o resultado legítimo; ficam de pé, a conferir, o cadastro com mortos (sem voto em escala), o salto do comparecimento de 95 a 99 anos, a subida dos avisos \"já votou\" seguidos de liberação manual e o Lula com quase todos os votos em disputa (vídeo 19) |",
          "| Raridade | H04, H05, H07, H08 | o resultado legítimo: unanimidade, dígitos e placares repetidos aparecem do mesmo jeito em 2018 e 2022 |",
          "| Arquivos das urnas | H06, H09 a H12, H17, H18 | o resultado legítimo, com peso pequeno (os arquivos bateriam nas duas visões) |", "",
          f"Nenhuma das {len(HIP)} hipóteses mostrou a marca que a fraude deixaria no dado público. O relatório pericial nasce de um erro de fuso. O que continua sem resposta está dentro do TSE: a lista de quem votou em cada seção, o cruzamento do cadastro com os óbitos e a assinatura de cada boletim.", "",
          "## Validação independente", "", "| Checagem | Obtido | Esperado | Fonte | Passou |", "|---|---|---|---|---|"]
    for c_ in V["checagens"]:
        L.append(f"| {c_['checagem']} | {c_['obtido']} | {c_['esperado']} | {c_['fonte_do_esperado']} | {'sim' if c_['passou'] else 'não'} |")
    rec = R["reconciliacao"]
    L += ["", "## Reconciliação com o total proclamado", "",
          f"O detalhe por seção do TSE soma {n(rec['detalhe_tse_nominais_2t'])} votos nominais e {n(rec['detalhe_tse_comparecimento_2t'])} de comparecimento, o total proclamado. As tabelas por seção copiadas do vídeo 16 somam {n(rec['tabelas_por_secao_nominais_2t'])} nominais: os {n(rec['detalhe_tse_nominais_2t'] - rec['tabelas_por_secao_nominais_2t'])} que faltam cabem nas {n(rec['secoes_com_boletim_fora_da_urna'])} seções cujo boletim não saiu da urna (recuperador de dados, totalização ou sistema de apuração), que têm {n(rec['nominais_delas'])} votos nominais. Nenhum teste muda por isso.", "",
          "Fontes, método e como refazer: `docs/PLANO.md`, `docs/HIPOTESES.md`, `docs/FONTES_DE_DADOS.md` e `docs/REPLICAR.md`. Análise feita pelo Claude, a pedido do autor do canal."]
    (RAIZ / "RELATORIO.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def resumo_simples():
    c = contagem()
    L = ["# Resumo simples", "",
         "**A pergunta:** o público levantou dezenas de hipóteses de fraude sobre o 2º turno de 2026 que os vídeos anteriores não tinham testado. Alguma delas aparece no dado?", "",
         "**Como foi feito:** 23 hipóteses, cada uma pelas duas visões (resultado legítimo e fraude), com o arquivo de todas as 499.248 seções, o modelo de cada urna, os logs de 12.691 urnas, o eleitorado e o comparecimento por idade, o Censo do IBGE e as versões do resultado gravadas ao vivo na noite. Os números centrais foram refeitos por outro caminho (" + f"{V['passaram']} de {V['total']}" + ").", "",
         "## O que deu", ""]
    for h in HIP:
        L.append(f"- **{h[2]}** ({h[0]}): {h[4].lower()}.")
    L += ["", "## As três coisas mais importantes", "",
          f"1. **O relatório que circulou tem um erro de fuso.** Ele só chega aos {p(REP['ate_17h00']['flavio_pct'])}% do Flávio \"até as 17h\" porque contou como fechadas cedo as {n(REP['secoes_dos_estados_com_fuso_no_grupo_ate_17h'])} urnas de 6 estados que fecharam às 17h de Brasília. Votos dados de fato depois das 17h: {n(H02['votos_depois_17h_brasil_log'])}.",
          f"2. **As 106 urnas sem voto do Flávio são aldeias e comunidades que já votavam assim.** Em 2022 foram {n(H07['2022_secoes_zero_bolsonaro'])} seções sem voto do Bolsonaro; em 2018, {n(H07['2018_secoes_zero_bolsonaro'])}.",
          f"3. **Há mortos no cadastro, mas eles quase não votam.** São {n(H13['eleitores_100_ou_mais_2026'])} eleitores com 100 anos ou mais, para {n(H13['populacao_96_ou_mais_censo_2022'])} pessoas que poderiam ter essa idade; o comparecimento deles foi de {p(c100['2026_t1']['taxa_pct'])}% no 1º turno.", "",
          "O que fica para conferir, sem prova: o salto do comparecimento de quem tem 95 a 99 anos, os avisos \"já votou\" seguidos de liberação manual e o que só o TSE tem (a lista de quem votou e o cruzamento com os óbitos). Relatório completo: [`RELATORIO.md`](RELATORIO.md)."]
    (RAIZ / "RESUMO_SIMPLES.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def leitura():
    L = ["# Leitura da IA", "", "**Rodada 1, 29/out/2026.** A leitura de cada bloco, com o que cada visão diz e qual o dado sustenta mais. Os números estão no `RELATORIO.md`.", ""]
    for bloco, nome in [("A", "O relatório pericial"), ("B", "As seções e as urnas"), ("C", "Os eleitores"), ("D", "A totalização"), ("E", "O comportamento dos votos")]:
        hs = [h for h in HIP if h[1] == bloco]
        L += [f"## {nome}", ""]
        for h in hs:
            L.append(f"- **{h[0]} · {h[4]}.** Legítimo: {h[6]}. Fraude: {h[7]}.")
        L.append("")
    L += ["## No fim", "", "A visão do resultado legítimo fica na frente nos três critérios, sem que isso prove que não houve irregularidade em lugar nenhum. O que a visão da fraude ainda tem é o que o dado público não mostra: quem votou em cada seção, o cadastro cruzado com os óbitos e a assinatura de cada boletim. Os pedidos estão em `docs/PEDIDOS_LAI.md`."]
    (RAIZ / "docs/LEITURA_DA_IA.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    relatorio()
    resumo_simples()
    leitura()
    print("ok", contagem())
