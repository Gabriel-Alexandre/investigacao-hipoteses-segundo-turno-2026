"""Escreve RELATORIO.md, RESUMO_SIMPLES.md e docs/LEITURA_DA_IA.md a partir de resultados/RESUMO.json e
resultados/VALIDACAO.json. Os números vêm desses arquivos (a linha do tempo de H06 entra no RESUMO.json por
linha_do_tempo.py); os únicos números escritos aqui são a diferença da eleição e citações de terceiros marcadas como tal.
Cada hipótese tem duas respostas separadas: se o fato que circula está certo, e o veredito sobre a leitura de fraude
(confirmado, indício forte, compatível com as duas, não sustentado, desmentido), com o critério de peso do vídeo 16.

Uso: python ferramentas/gerar_relatorio.py
"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
R = json.loads((RAIZ / "resultados/RESUMO.json").read_text(encoding="utf-8"))
V = json.loads((RAIZ / "resultados/VALIDACAO.json").read_text(encoding="utf-8"))
R3 = json.loads((RAIZ / "resultados/RODADA3.json").read_text(encoding="utf-8"))
VV, C26, C22, C18 = R3["versoes_ao_vivo_2026"], R3["curva"]["2026_chegada"], R3["curva"]["2022_chegada"], R3["curva"]["2018_encerramento"]
I26, I22, I18 = R3["identicas"]["2026"], R3["identicas"]["2022"], R3["identicas"]["2018"]
MARGEM = 4_430_191


def n(x):
    return f"{int(round(x)):,}".replace(",", ".")


def p(x, casas=2):
    return f"{x:.{casas}f}".replace(".", ",")


def pm(votos):
    v = 100 * votos / MARGEM
    return "menos de 0,01%" if v < 0.01 else p(v, 2) + "%"


H = {k: R[k] for k in R if k.startswith("H")}
REP = H["H01"]["reproducao_do_relatorio"]
CO = H["H01"]["cortes"]["ate_17h00min59"]
DL, DG = H["H01"]["dentro_do_local_lula_2t"], H["H01"]["dentro_do_local_ganho_do_1t_para_2t"]
OE = H["H02_oeste_do_amazonas"]
V17 = H["H02"]["votos_depois_17h_brasil_log"] + OE["votos_depois_17h_brasilia"]
mod = H["H09"]["por_modelo"]
cp = H["H13"]["comparecimento_por_idade"]
h13, h14, h15, h18, h23 = H["H13"], H["H14"], H["H15"], H["H18"], H["H23"]
LT = H["H06"]
caso = {c["municipio"].split(" (")[0]: c for c in h23["casos"]}
joa, ara = caso["Joaçaba"], caso["Araruama"]

TETOS_ABERTOS = {
    "votos depois das 17h, todos para um lado (H02)": V17,
    "registros de centenário sem pessoa possível, todos votando (H13)": h13["teto_se_todo_registro_impossivel_votasse"],
    "votos acima da população nos municípios em que isso acontece (H14)": h14["votos_acima_da_pop_total_soma"],
    "cada aviso \"já votou\" como um voto roubado (H15)": h15["teto_se_cada_aviso_fosse_um_voto_roubado"],
    "as quedas grandes do Flávio trocadas para o Lula (H18, cada voto trocado conta 2)": 2 * h18["queda_grande_do_flavio_com_comparecimento_estavel"]["votos"],
    "os votos do Lula acima do esperado na Região dos Lagos (H23)": h23["votos_do_lula_acima_do_esperado_pelos_parecidos"],
    "urnas trocadas, pela diferença contra as vizinhas (H10)": H["H10"]["teto_pela_diferenca_no_mesmo_local_votos"],
    "o que o Flávio tinha nas 106 seções (H07)": H["H07"]["teto_votos"],
}
SOMA_TETOS = sum(TETOS_ABERTOS.values())
LULA_POP = "; ".join(f"{x['municipio'].title().replace(' Do ', ' do ').replace(' Da ', ' da ')}, {n(x['lula_2t'])} votos do Lula para {n(x['pop_total'])} habitantes"
                     for x in h14["municipios_com_mais_votos_do_lula_que_habitantes"])

# (código, bloco, título, critério, o fato que circula, veredito, o que o dado mostra, visão legítimo, visão fraude, teto, o que fecharia)
HIP = [
    ("H01", "A", "Nas urnas encerradas até as 17h, o Flávio ganhou", "comportamento",
     "errado: o 52,39% só sai com o fuso trocado", "Desmentido",
     f"O número do relatório sai igual ({p(REP['ate_17h00']['flavio_pct'])}% para o Flávio e {n(REP['ate_17h00']['frente_flavio'])} votos de frente) só quando se lê a hora de encerramento de cada urna no relógio local, sem acertar o fuso. Assim, as urnas dos estados atrás de Brasília (AC, AM, MT, MS, RO e RR), que fecharam às 15h ou às 16h no relógio delas, às 17h de Brasília, entram todas no grupo \"até 17h\": são {n(REP['secoes_dos_estados_com_fuso_no_grupo_ate_17h'])} das {n(REP['secoes_desses_estados'])} seções desses estados, com {p(REP['flavio_pct_nessas'])}% para o Flávio e {n(REP['frente_flavio_nessas'])} votos de frente. Com o fuso certo, as {n(CO['ate']['secoes'])} seções que fecharam até 17h00min59 de Brasília ainda deram {p(CO['ate']['flavio_pct'])}% ao Flávio: são as seções pequenas, sem fila, que fecham na hora. O teste que separa é o do mesmo local de votação: a seção que fechou depois das 17h15 teve {p(-DL['diferenca_pontos'])} ponto a menos de Lula que a vizinha que fechou antes ({n(DL['locais'])} locais) e {p(-DG['diferenca_pontos'])} ponto a menos de ganho desde o 1º turno ({n(DG['locais'])} locais). E o grupo \"depois das 17h\" é o voto do dia inteiro: só {n(REP['votos_com_hora_depois_17h_no_grupo_depois'])} votos dele têm hora depois das 17h no log",
     "urna que fecha mais tarde é a de fila; a diferença entre os grupos é de tamanho de seção, lugar e fuso, não da hora do voto",
     "se a prorrogação tivesse acrescentado voto, as seções que fecharam tarde dariam mais ao Lula que as vizinhas do mesmo local; dão menos",
     f"{n(V17)} votos depois das 17h ({pm(V17)} da diferença)", "já fechado: o log de cada urna é público e tem a hora de cada voto"),
    ("H02", "A", "Mais de 2,5 milhões de eleitores votaram em urnas que passaram do horário", "comportamento",
     "o número confere, mas é o comparecimento do dia inteiro", "Desmentido",
     f"Os 2,5 milhões são o comparecimento do dia inteiro das {n(H['H02']['secoes_fechadas_a_partir_de_17h16'])} seções que fecharam a partir das 17h16 ({n(H['H02']['comparecimento_do_dia_inteiro_nelas'])} pelas tabelas do projeto). Votos com hora depois das 17h nessas seções: {n(H['H02']['votos_com_hora_depois_17h_nelas_pelo_log'])}. No Brasil inteiro, o log dá {n(H['H02']['votos_depois_17h_brasil_log'])} depois das 17h, o mesmo número do TSE, mais {n(OE['votos_depois_17h_brasilia'])} no oeste do Amazonas, que fica 2 horas atrás de Brasília e a conta anterior tratou com 1 hora ({n(OE['secoes'])} seções relidas nesta rodada). Total: {n(V17)}. Depois das 19h: {n(H['H02']['votos_depois_19h_brasil_log'] + OE['votos_depois_19h_brasilia'])}",
     "estar numa urna aberta depois das 17h não é votar depois das 17h", "a conta mistura o eleitor do dia inteiro com o voto da prorrogação",
     f"{n(V17)} votos ({pm(V17)} da diferença)", "já fechado pelo log"),
    ("H03", "A", "8,6 milhões liberados sem biometria, quase o dobro da diferença", "comportamento",
     "certo: 8,6 milhões liberados pela digital do mesário", "Não sustentado",
     f"O número existe: {n(H['H03']['liberados_pela_digital_do_mesario_2t'])} eleitores liberados pela digital do mesário no 2º turno, e mais {n(H['H03']['liberados_sem_digital_cadastrada_pelo_ano_de_nascimento_2t'])} sem digital cadastrada, liberados pelo ano de nascimento ({p(H['H03']['sem_a_digital_do_eleitor_pct_dos_votos'])}% dos votos, somando os dois; o máximo teórico seria {n(H['H03']['maximo_teorico_votos'])} votos, {p(H['H03']['maximo_teorico_vezes_a_diferenca'])} vezes a diferença). Na amostra de {n(H['H03']['amostra_secoes'])} seções, essa parte foi de {p(H['H03']['amostra_parte_manual_1t_pct'])}% no 1º turno para {p(H['H03']['amostra_parte_manual_2t_pct'])}% no 2º. Dentro do mesmo município, a seção com mais liberação manual não deu mais voto ao Lula (correlação de {p(H['H03']['correlacao_no_mesmo_municipio']['parte_manual_2t_x_lula_2t'][0], 3)}), e a seção em que a liberação manual subiu do 1º para o 2º turno não deu mais ganho a ele ({p(H['H03']['correlacao_no_mesmo_municipio']['variacao_manual_x_variacao_lula'][0], 3)}). O eleitorado com biometria foi de {p(H['H03']['eleitores_com_biometria_pct']['2022'], 1)}% em 2022 para {p(H['H03']['eleitores_com_biometria_pct']['2026'], 1)}% em 2026; o Jornal Razão somou cerca de 10 milhões de liberações em 2022 pela mesma conta (não recalculado aqui)",
     "a liberação sem a digital do eleitor é rotina (dedo gasto, idoso, digital não cadastrada), acontece o dia todo e cai dos dois lados",
     "a fraude por liberação manual deixaria a parte manual subir onde o Lula cresceu; ela não sobe, nem no mesmo município",
     "sem sinal para medir: a liberação manual não anda junto com o voto de nenhum lado", "a lista de quem votou em cada seção, com o tipo de liberação (pedido ao TSE)"),
    ("H04", "A", "6.899 seções com mais de 90% para o Lula contra 384 do Flávio", "raridade",
     f"quase: {n(H['H04']['acima_90_lula'])} e {n(H['H04']['acima_90_flavio'])} no Brasil", "Desmentido",
     f"Pelo arquivo do TSE: {n(H['H04']['acima_90_lula'])} acima de 90% para o Lula e {n(H['H04']['acima_90_flavio'])} para o Flávio, no Brasil (os 6.899 e 384 do relatório não saíram por nenhum recorte testado). Em 2022 foram {n(H['H04']['2022_acima_90_lula'])} para o Lula e {n(H['H04']['2022_acima_90_bolsonaro'])} para o Bolsonaro; em 2018, {n(H['H04']['2018_acima_90_haddad'])} para o Haddad e {n(H['H04']['2018_acima_90_bolsonaro'])} para o Bolsonaro. Das seções do Lula acima de 90% em 2026, {p(H['H04']['lula_acima_90_ja_acima_80_em_2022_pct'], 1)}% já davam mais de 80% para ele em 2022",
     "as seções de quase unanimidade são as mesmas de antes, nos mesmos lugares, e eram mais numerosas em 2018 e 2022", "seriam seções novas na lista; não são",
     "não se aplica: a assimetria é menor que a de 2022", "já fechado pelo histórico de cada seção"),
    ("H05", "A", "A lei de Benford reprova a votação", "raridade",
     "o relatório não mostrou número nenhum", "Não sustentado",
     f"Desvio médio do 1º dígito: {p(H['H05']['mad']['lula_2026']['mad_1o_digito'], 3)} no Lula e {p(H['H05']['mad']['flavio_2026']['mad_1o_digito'], 3)} no Flávio em 2026, {p(H['H05']['mad']['lula_2022']['mad_1o_digito'], 3)} no Lula e {p(H['H05']['mad']['bolsonaro_2022']['mad_1o_digito'], 3)} no Bolsonaro em 2022. Todos \"reprovam\" do mesmo jeito, porque o voto por seção fica preso no tamanho da seção (de 200 a 400 eleitores) e o 1º dígito não pode seguir Benford",
     "o teste não serve para voto por seção; a prova é que ele reprova os dois candidatos e os dois anos", "um desvio só de um lado, ou só em 2026, seria sinal; não há",
     "não se aplica", "já fechado"),
    ("H06", "A", "Os boletins ficaram 72 horas escondidos", "arquivos",
     "meio certo: só a entrada no catálogo foi em 28/10", "Desmentido",
     f"Os {LT['pacotes']} pacotes do 2º turno entraram no catálogo de Dados Abertos em {LT['entrada_no_catalogo_de_dados_abertos']['primeiro']}, mas o servidor do TSE dá a eles a data de {LT['data_dos_arquivos_no_servidor_do_tse']['primeiro']} a {LT['data_dos_arquivos_no_servidor_do_tse']['ultimo']}; os arquivos de cada seção já estavam no site de resultados (o projeto do vídeo 16 começou a baixá-los em 26/10 às 7h30), e o boletim de cada seção foi impresso e afixado na própria seção em 25/10",
     "o catálogo demorou, o dado não", "a única parte verdadeira é a data de entrada no catálogo",
     "não se aplica", "já fechado pelas datas dos arquivos"),
    ("H07", "B", "106 urnas com zero voto para o Flávio", "raridade",
     "certo: 106 seções e 14.860 votos", "Não sustentado",
     f"São {n(H['H07']['secoes'])} seções e {n(H['H07']['votos_lula'])} votos ({H['H07']['por_uf']['am']} no AM, {H['H07']['por_uf']['ma']} no MA, {H['H07']['por_uf']['pa']} no PA, {H['H07']['por_uf']['rr']} em RR); {n(H['H07']['com_termo_indigena_ou_comunidade_no_nome_do_local'])} têm nome de aldeia, escola indígena ou comunidade no local de votação. No 1º turno de 2026, {n(H['H07']['com_zero_flavio_tambem_no_1t'])} delas já não tinham voto do Flávio, e as outras {n(H['H07']['com_algum_voto_do_flavio_no_1t'])} somavam {n(H['H07']['flavio_no_1t_2026_nessas_votos'])} votos dele; pelo acaso, com a divisão do 1º turno, seriam esperadas {p(H['H07']['acaso_esperado_zero_entre_as_que_tinham_voto_no_1t'], 0)} seções zeradas entre as que tinham voto do Flávio. O fenômeno foi maior antes: {n(H['H07']['2022_secoes_zero_bolsonaro'])} seções sem voto do Bolsonaro em 2022 e {n(H['H07']['2018_secoes_zero_bolsonaro'])} em 2018. O espelho existe: {n(H['H07']['espelho_zero_lula']['secoes'])} seções sem voto do Lula, no RS e no PA. As que têm 100% para um candidato, sem branco nem nulo: {I26['sem_voto_da_direita_nem_branco_nem_nulo']} do Lula e {I26['sem_voto_da_esquerda_nem_branco_nem_nulo']} do Flávio em 2026; em 2022, {I22['sem_voto_da_direita_nem_branco_nem_nulo']} do Lula; em 2018, {I18['sem_voto_da_direita_nem_branco_nem_nulo']} do Haddad. Sorteando pelo próprio 1º turno de cada seção, seriam esperadas {I26['acaso_sem_voto_da_direita'][0]} a {I26['acaso_sem_voto_da_direita'][1]} seções sem voto do Flávio, mais do que as {n(H['H07']['secoes'])} que apareceram",
     "voto concentrado em aldeia e comunidade, que se repete eleição após eleição e foi mais frequente em 2018 e 2022", "a lista teria seções sem histórico de unanimidade; quase todas já votavam assim",
     f"{n(H['H07']['teto_votos'])} votos (o que o Flávio teve nelas no 1º turno), {pm(H['H07']['teto_votos'])} da diferença", "já fechado pelo histórico; o TSE checou o mesmo caso no 1º turno"),
    ("H08", "B", "Seções com placar repetido seriam impossíveis", "raridade",
     "existem, e o boletim inteiro igual também (mensagem de um seguidor)", "Desmentido",
     f"{n(H['H08']['placares_repetidos_2026'])} placares (Lula, Flávio) aparecem em mais de uma seção. Sorteando os votos de cada seção 20 vezes pela divisão Lula e Flávio dela no 1º turno, o acaso dá entre {n(H['H08']['esperado_faixa'][0])} e {n(H['H08']['esperado_faixa'][1])}. Em 2022 foram {n(H['H08']['placares_repetidos_2022'])}. Nenhum placar se repete com os dois candidatos acima de 300 votos. Boletim inteiro (Lula, Flávio, branco e nulo iguais): {n(I26['boletins_inteiros_que_se_repetem'])} em 2026, {n(I22['boletins_inteiros_que_se_repetem'])} em 2022 e {n(I18['boletins_inteiros_que_se_repetem'])} em 2018. A subida acompanha a queda dos brancos e nulos ({p(I18['brancos_e_nulos_por_secao'], 1)} por seção em 2018, {p(I22['brancos_e_nulos_por_secao'], 1)} em 2022, {p(I26['brancos_e_nulos_por_secao'], 1)} em 2026), porque com menos branco e nulo há menos combinações possíveis: o sorteio dá {n(I26['acaso_boletins_inteiros_que_se_repetem'][0])} a {n(I26['acaso_boletins_inteiros_que_se_repetem'][1])} em 2026, {n(I22['acaso_boletins_inteiros_que_se_repetem'][0])} a {n(I22['acaso_boletins_inteiros_que_se_repetem'][1])} em 2022 e {n(I18['acaso_boletins_inteiros_que_se_repetem'][0])} a {n(I18['acaso_boletins_inteiros_que_se_repetem'][1])} em 2018. O real passa do sorteio nos 3 anos, e 2026 é o ano em que passa menos ({p(100 * I26['boletins_inteiros_que_se_repetem'] / sum(I26['acaso_boletins_inteiros_que_se_repetem']) * 2 - 100, 0)}% acima, contra {p(100 * I22['boletins_inteiros_que_se_repetem'] / sum(I22['acaso_boletins_inteiros_que_se_repetem']) * 2 - 100, 0)}% em 2022 e {p(100 * I18['boletins_inteiros_que_se_repetem'] / sum(I18['acaso_boletins_inteiros_que_se_repetem']) * 2 - 100, 0)}% em 2018). O maior boletim repetido tem {n(I26['maior_comparecimento_num_boletim_repetido'])} votos",
     "com meio milhão de seções, placar repetido é o esperado (é o problema do aniversário)", "a fraude por cópia deixaria repetição acima do acaso; não há",
     "não se aplica", "já fechado"),
    ("H09", "B", "As urnas antigas votam diferente das novas", "comportamento",
     "os quatro modelos (2013 a 2022) votaram em 2026", "Não sustentado",
     f"O modelo de cada urna está no arquivo do TSE. O Lula ficou com {p(mod['UE 2013']['lula_2t_pct'])}% nas UE2013, {p(mod['UE 2015']['lula_2t_pct'])}% nas UE2015, {p(mod['UE 2020']['lula_2t_pct'])}% nas UE2020 e {p(mod['UE 2022']['lula_2t_pct'])}% nas UE2022, e o ganho desde o 1º turno ficou entre {p(min(v['ganho_lula_pontos'] for v in mod.values()))} e {p(max(v['ganho_lula_pontos'] for v in mod.values()))} pontos nos quatro. No mesmo local, a urna antiga (2013 e 2015) contra a nova: {p(H['H09']['dentro_do_local_antiga_vs_nova_ganho']['diferenca_pontos'])} ponto no ganho, em {n(H['H09']['dentro_do_local_antiga_vs_nova_ganho']['locais'])} locais",
     "o modelo não muda o voto", "um programa adulterado num modelo deixaria marca nele; não deixa",
     "não se aplica", "já fechado para a pergunta do modelo"),
    ("H10", "B", "Urnas trocadas e levadas em carro de partido", "comportamento",
     f"houve {n(H['H10']['secoes_com_contingencia_no_log'])} trocas registradas e um caso real de transporte irregular", "Não sustentado",
     f"{n(H['H10']['secoes_com_contingencia_no_log'])} seções registraram troca de urna no log. No mesmo local, elas votaram como as vizinhas ({p(H['H10']['dentro_do_local_ganho']['diferenca_pontos'])} ponto no ganho do Lula, em {n(H['H10']['dentro_do_local_ganho']['locais'])} locais). O caso da caminhonete com adesivo no Riacho Fundo II (DF) é irregularidade real de transporte, apurada pelo TRE-DF, mas o boletim já tinha sido impresso e transmitido",
     "a urna de contingência segue o procedimento e vota como as vizinhas", "uma urna trocada com voto pronto votaria diferente das vizinhas; não vota",
     f"{n(H['H10']['teto_pela_diferenca_no_mesmo_local_votos'])} votos pela diferença contra as vizinhas ({pm(H['H10']['teto_pela_diferenca_no_mesmo_local_votos'])}); se todos os votos dessas seções fossem falsos, {n(H['H10']['votos_nominais_nessas_secoes'])}", "a lista oficial de urnas substituídas, com o motivo (pedido ao TSE)"),
    ("H11", "B", "O boletim de papel não bate com o site do TSE", "arquivos",
     "o caso que circulou (Teixeira de Freitas) está errado", "Não sustentado",
     f"Teixeira de Freitas inteira, {n(H['H11']['teixeira_de_freitas']['secoes'])} seções: Flávio {n(H['H11']['teixeira_de_freitas']['flavio'])}, Lula {n(H['H11']['teixeira_de_freitas']['lula'])}, igual ao Aos Fatos (a soma de 3 boletins não é a cidade). O boletim de cada seção e o detalhe por seção dos dados abertos batem em {n(H['H11']['boletim_x_dados_abertos']['secoes_comparadas'])} seções, sem uma diferença, mas isso é arquivo do TSE contra arquivo do TSE: bate nas duas visões. O que separa é a foto do boletim de papel e a assinatura digital de cada boletim, que esta rodada não verificou",
     "o boletim afixado na seção é o mesmo arquivo publicado", "um boletim trocado na totalização apareceria entre a foto do papel e o arquivo; nenhuma foto mostrou isso até agora",
     "não medido", "fotos de boletins de papel comparadas com o arquivo (convite público) e a verificação da assinatura de cada boletim"),
    ("H12", "B", "Seções criadas, cortadas ou \"virtuais\"", "arquivos",
     "errado: a lista de seções é a mesma nos dois turnos", "Desmentido",
     f"As mesmas {n(H['H12']['secoes_2t'])} seções nos dois turnos, nenhuma só num deles; {n(H['H12']['nao_instaladas_2t'])} não instaladas. {n(H['H12']['mudaram_de_local'])} mudaram de local entre os turnos, e nelas o comparecimento subiu menos ({p(H['H12']['variacao_comparecimento_mudaram_pontos'])} ponto, contra {p(H['H12']['variacao_comparecimento_demais_pontos'])} nas demais)",
     "a lista de seções é a mesma nos dois turnos", "seção fantasma apareceria só num turno; não há",
     "não se aplica", "já fechado"),
    ("H13", "C", "Mortos votaram", "comportamento",
     f"certo que há registros de mortos no cadastro: pelo menos {n(h13['registros_de_100_ou_mais_sem_pessoa_possivel_2026_piso'])} de centenários", "Não sustentado",
     f"O cadastro tem registros de pessoas que provavelmente já morreram: {n(h13['eleitores_100_ou_mais_2026'])} eleitores com 100 anos ou mais em 2026, quando o Censo de 2022 contou {n(h13['populacao_96_ou_mais_censo_2022'])} pessoas com 96 anos ou mais (as únicas que podem ter 100 em 2026); a diferença, {n(h13['registros_de_100_ou_mais_sem_pessoa_possivel_2026_piso'])}, é o mínimo de registros sem pessoa viva possível. Em 2022 era parecido: {n(h13['eleitores_100_ou_mais_2022'])} eleitores centenários para {n(h13['populacao_100_ou_mais_censo_2022'])} centenários no Censo ({p(h13['razao_eleitores_100_sobre_censo']['2022'], 1)} vezes). Esses registros quase não votam: no 1º turno de 2026 compareceram {n(cp['100 ou mais']['2026_t1']['comparecimento'])} eleitores de 100 anos ou mais ({p(cp['100 ou mais']['2026_t1']['taxa_pct'])}%; no 1º turno de 2022, {p(cp['100 ou mais']['2022_t1']['taxa_pct'])}%). Na faixa de 95 a 99 anos, o comparecimento foi de {p(cp['95 a 99']['2022_t1']['taxa_pct'])}% no 1º turno de 2022 para {p(cp['95 a 99']['2026_t1']['taxa_pct'])}% no 1º de 2026, mas, contado sobre quem tem biometria, ficou parado ({p(cp['95 a 99']['2022_t1']['taxa_sobre_quem_tem_biometria_pct'], 1)}% e {p(cp['95 a 99']['2026_t1']['taxa_sobre_quem_tem_biometria_pct'], 1)}%): o que mudou foi o cadastro, que tirou registros, e não o voto. O TSE ainda não publicou o comparecimento por idade do 2º turno de 2026",
     "o cadastro demora a tirar quem morreu, e esses registros não votam",
     "a fraude usaria esses registros com a liberação do mesário; o comparecimento deles é de menos de 1 em 100, e a subida da faixa de 95 a 99 some quando se olha quem tem biometria",
     f"se todo registro de centenário sem pessoa possível votasse: {n(h13['teto_se_todo_registro_impossivel_votasse'])} votos, {pm(h13['teto_se_todo_registro_impossivel_votasse'])} da diferença (o comparecimento real de todos os centenários foi de {n(cp['100 ou mais']['2026_t1']['comparecimento'])} no 1º turno)",
     "o cruzamento do cadastro com os óbitos dos cartórios (SIRC) e o comparecimento por idade do 2º turno, os dois com o TSE"),
    ("H14", "C", "Cidades com mais eleitores ou votos que habitantes", "comportamento",
     f"certo: {n(h14['comparecimento_2t_maior_que_pop_total'])} municípios com mais votos que habitantes", "Compatível com as duas",
     f"Em {n(h14['comparecimento_2t_maior_que_pop_total'])} municípios o comparecimento do 2º turno passou da população total do Censo 2022 (em 2022 tinham sido {n(h14['2022_comparecimento_2t_maior_que_pop_total'])}); o Lula venceu em {n(h14['lula_venceu_nos_acima_da_pop_total'])} deles. Contra a população de 16 anos ou mais, foram {n(h14['comparecimento_2t_maior_que_pop_16_ou_mais'])} municípios em 2026 e {n(h14['2022_comparecimento_2t_maior_que_pop_16_ou_mais'])} em 2022. Em {len(h14['municipios_com_mais_votos_do_lula_que_habitantes'])} municípios do Piauí o Lula sozinho teve mais votos que habitantes: {LULA_POP}; nos três, ele já tinha votação parecida no 1º turno. É o eleitor que mora fora e mantém o título na cidade de origem, mais comum em cidade pequena do Nordeste, e o próprio Censo pode ter contado menos gente nelas; quanto maior a razão entre votos e população, menor o ganho do Lula (correlação de {p(h14['correlacao_razao_comparecimento_populacao_x_ganho_do_lula'], 2)}). Na lista da corrente de WhatsApp, em nenhuma cidade o Lula teve mais votos que habitantes",
     "título mantido na cidade natal e Censo que conta menos gente em cidade pequena; não é o lugar onde o Lula mais cresceu",
     "o número de municípios acima da população mais que dobrou desde 2022, e três deles deram ao Lula mais votos que habitantes; é a parte a conferir com o cadastro",
     f"{n(h14['votos_acima_da_pop_total_soma'])} votos acima da população, somados nesses municípios ({pm(h14['votos_acima_da_pop_total_soma'])})", "o recadastramento e a lista de quem votou nesses municípios, com o TSE"),
    ("H15", "C", "Cheguei e já tinham votado por mim", "comportamento",
     f"certo: o aviso apareceu {n(h15['avisos_ja_votou_2t_brasil'])} vezes", "Compatível com as duas",
     f"O aviso \"o eleitor identificado já votou\" aparece {n(h15['avisos_ja_votou_2t_brasil'])} vezes no 2º turno, em {n(h15['secoes_com_aviso_2t'])} seções. Na amostra, foi {p(h15['amostra_avisos_por_mil_votos']['t1'], 3)} por mil votos no 1º turno e {p(h15['amostra_avisos_por_mil_votos']['t2'], 3)} no 2º. Tirando as repetições (o mesmo eleitor tentando de novo em até 2 minutos), os avisos isolados foram de {n(h15['amostra_avisos_isolados']['t1'])} para {n(h15['amostra_avisos_isolados']['t2'])}. Depois do aviso, o voto seguinte foi liberado sem a digital em {p(h15['proximo_voto_depois_do_aviso_foi_manual_pct']['t1'], 1)}% das vezes no 1º turno e {p(h15['proximo_voto_depois_do_aviso_foi_manual_pct']['t2'], 1)}% no 2º, contra {p(h15['parte_manual_de_todos_os_votos_pct']['t1'], 1)}% e {p(h15['parte_manual_de_todos_os_votos_pct']['t2'], 1)}% de todos os votos; e um voto liberado sem a digital em até 5 minutos veio depois de {p(h15['amostra_aviso_seguido_de_liberacao_manual_em_5_min_pct']['t2'], 1)}% dos avisos, contra {p(h15['regua_qualquer_voto_seguido_de_liberacao_manual_em_5_min_pct']['t2'], 1)}% depois de um voto qualquer. Dentro do município, a seção com mais aviso não deu mais ganho ao Lula (correlação de {p(h15['correlacao_no_mesmo_municipio_aviso_x_ganho_do_lula'], 3)}). Casos com nome existem (Campinas e Valinhos) e estão com o TRE-SP",
     "o aviso nasce de título digitado errado e de eleitor que tenta de novo; o que vem depois dele é igual ao que vem depois de um voto qualquer",
     "o caso individual é real, os avisos isolados subiram do 1º para o 2º turno, e o voto que veio antes do aviso não aparece no arquivo público",
     f"se cada aviso fosse um voto roubado: {n(h15['teto_se_cada_aviso_fosse_um_voto_roubado'])} votos ({pm(h15['teto_se_cada_aviso_fosse_um_voto_roubado'])})", "a ata e o caderno de cada caso, com o TRE, e a lista de quem votou"),
    ("H16", "C", "O mesário vota o dia todo, quando a seção esvazia", "comportamento",
     "não: a liberação manual acompanha o movimento da seção", "Não sustentado",
     f"A parte dos votos liberados sem a digital do eleitor fica entre 12% e 13% de 8h a 16h, nos dois turnos. Às 17h do 2º turno ela sobe para {p(H['H16']['parte_manual_por_hora_pct']['t2']['17'], 1)}%, mas são {n(H['H16']['votos_por_hora']['t2']['17'])} votos na amostra inteira, os últimos da fila. A maior sequência de votos seguidos liberados pelo mesmo mesário tem mediana de {p(H['H16']['maior_sequencia_mesmo_mesario']['t2']['mediana'], 0)} e máximo de {H['H16']['maior_sequencia_mesmo_mesario']['t2']['max']} no 2º turno (no 1º, uma seção teve {H['H16']['maior_sequencia_mesmo_mesario']['t1']['max']}); nenhuma seção da amostra teve 10 ou mais seguidas no 2º turno",
     "a liberação manual acompanha o movimento da seção", "o mesário que vota por quem faltou deixaria rajadas de liberações seguidas na hora vazia; não há",
     "não se aplica", "a lista de quem votou em cada seção (pedido ao TSE)"),
    ("H17", "D", "O Flávio \"perdendo votos\" no painel, os 165 mil \"sem origem\" e a sala-cofre", "arquivos",
     "errado: o total do Flávio nunca caiu", "Desmentido",
     f"Nas {n(H['H17']['versoes_nacionais'])} versões nacionais do resultado gravadas ao vivo na noite, o total do Flávio nunca caiu ({H['H17']['vezes_que_o_total_do_flavio_caiu']} quedas), nem o do Lula ({H['H17']['vezes_que_o_total_do_lula_caiu']}), e a última dá Lula {n(H['H17']['ultima_versao_nacional']['lula'])} e Flávio {n(H['H17']['ultima_versao_nacional']['flavio'])}, o resultado proclamado. A maior distância entre duas versões nacionais foi de {H['H17']['maior_intervalo_sem_versao_nacional'].split(' ')[-1][:5].replace(':', 'h')}, a suspensão da divulgação depois da prorrogação. Os 165 mil \"sem origem\" foram uma comparação de painéis feita às 17h57, durante essa suspensão: o TSE e o Aos Fatos mostram que o painel nacional já tinha os votos do exterior e os dos estados não estavam atualizados do mesmo jeito (as versões gravadas aqui não têm os painéis de cada estado daquele minuto). A sala-cofre não conta voto: o boletim de cada seção é impresso na seção antes de chegar ao TSE (H11)",
     "a soma é aberta seção por seção, e o painel só cresceu", "uma totalização mexida apareceria entre o boletim da seção e o total; os dois batem, mas isso também bateria numa fraude feita antes do boletim",
     "não se aplica", "já fechado para o painel; para a totalização, a assinatura dos boletins"),
    ("H24", "D", "A linha do Flávio desce como se fosse programada (o zoom na curva)", "comportamento",
     "certo que, com zoom, a porcentagem desce em degraus; o total de votos nunca desce", "Desmentido",
     f"Com muito zoom, a porcentagem do Flávio desce em degraus: caiu em {n(VV['vezes_que_a_porcentagem_do_flavio_caiu'])} e subiu em {n(VV['vezes_que_a_porcentagem_do_flavio_subiu'])} das versões gravadas ao vivo, e o total de votos dele caiu {VV['vezes_que_o_total_de_votos_do_flavio_caiu']} vezes. A curva foi refeita com cada seção repetindo o próprio 1º turno, na mesma ordem de chegada: a própria composição das seções explica {p(C26['parte_dos_passos_explicada_pela_composicao_pct'], 1)}% dos passos em 2026 e {p(C22['parte_dos_passos_explicada_pela_composicao_pct'], 1)}% em 2022 (em 2018, sem hora de chegada no arquivo público, pela hora de encerramento, {p(C18['parte_dos_passos_explicada_pela_composicao_pct'], 1)}%). O Bolsonaro desceu em {p(C22['passos_em_que_a_linha_desce_pct'], 1)}% dos passos em 2022, mais que o Flávio ({p(C26['passos_em_que_a_linha_desce_pct'], 1)}%). Os vales não têm ritmo: o intervalo entre eles varia quase tanto quanto ao acaso ({p(C26['regularidade_dos_vales_real_cv'])} em 2026, {p(C22['regularidade_dos_vales_real_cv'])} em 2022; um relógio daria 0), igual à curva prevista ({p(C26['regularidade_dos_vales_prevista_cv'])} e {p(C22['regularidade_dos_vales_prevista_cv'])}). Dentro da mesma zona, chegar mais tarde não muda o resultado da seção (correlação {p(C26['na_mesma_zona_corr_ordem_x_diferenca_da_prevista'], 3)} em 2026, {p(C22['na_mesma_zona_corr_ordem_x_diferenca_da_prevista'], 3)} em 2022)",
     "a porcentagem desce quando entra seção de lugar que já votava mais no Lula, sem nenhum voto sair", "um programa deixaria passos que a composição não explica, ritmo fixo e desconto crescente com a ordem; nada disso aparece",
     "não se aplica", "já fechado para a curva; um programa agindo dentro da urna é a H18"),
    ("H18", "D", "O programa da urna troca o voto", "arquivos",
     f"certo que o Flávio caiu em {n(h18['secoes_flavio_abaixo_do_1t'])} seções", "Compatível com as duas",
     f"O Flávio ficou abaixo do próprio 1º turno em {n(h18['secoes_flavio_abaixo_do_1t'])} seções; em {p(h18['dessas_com_comparecimento_em_queda_pct'], 1)}% delas o comparecimento também caiu (em todas as seções, a queda do comparecimento aconteceu em {p(h18['todas_as_secoes_com_comparecimento_em_queda_pct'], 1)}%). Em 2022, o Lula, que liderou o 1º turno, ficou abaixo do próprio 1º turno em {n(h18['espelho_2022_lider_do_1t_lula']['secoes_abaixo_do_1t'])} seções. Fora do padrão, a conferir: as quedas grandes do Flávio com comparecimento estável (perdeu 10% ou mais de pelo menos 30 votos) foram {n(h18['queda_grande_do_flavio_com_comparecimento_estavel']['secoes'])} seções e {n(h18['queda_grande_do_flavio_com_comparecimento_estavel']['votos'])} votos, contra {n(h18['espelho_2022_lider_do_1t_lula']['queda_grande_com_comparecimento_estavel']['secoes'])} seções e {n(h18['espelho_2022_lider_do_1t_lula']['queda_grande_com_comparecimento_estavel']['votos'])} votos do Lula em 2022. O teste de integridade do 2º turno, com urnas sorteadas votando em papel e na urna, não achou divergência, mas é pequeno: {h18['teste_de_integridade_2t']['tse_votos_auditados']} votos no TSE e {h18['teste_de_integridade_2t']['tre_sp_urnas']} urnas em São Paulo. Os logs da amostra não registram nenhuma verificação de assinatura do programa sem sucesso",
     "o voto segue o 1º turno de cada seção, o padrão geral é o de 2022 com os lados trocados, e a auditoria por amostra bateu",
     "uma troca que imitasse o eleitor não se separa por estatística, e as quedas grandes do Flávio são mais que as do Lula em 2022",
     f"se as quedas grandes do Flávio fossem votos trocados para o Lula: {n(2 * h18['queda_grande_do_flavio_com_comparecimento_estavel']['votos'])} votos de diferença ({pm(2 * h18['queda_grande_do_flavio_com_comparecimento_estavel']['votos'])})", "o teste de integridade em mais urnas e o voto impresso, que o Brasil não tem"),
    ("H19", "E", "O Flávio perdeu votos em 6 estados e o Lula em nenhum", "comportamento",
     "certo", "Não sustentado",
     f"Os 6 estados (AC, AM, AP, MA, RR, TO) tiveram queda do comparecimento entre os turnos: no AP, {p(H['H19']['ufs_onde_o_flavio_caiu']['ap']['variacao_comparecimento_pontos'])} pontos; em RR, {p(H['H19']['ufs_onde_o_flavio_caiu']['rr']['variacao_comparecimento_pontos'])}; no AC, {p(H['H19']['ufs_onde_o_flavio_caiu']['ac']['variacao_comparecimento_pontos'])}. Em 2022 aconteceu o mesmo com os lados trocados: o Lula perdeu votos em {len(H['H19']['espelho_2022']['ufs_onde_o_lula_caiu'])} estados ({', '.join(x.upper() for x in H['H19']['espelho_2022']['ufs_onde_o_lula_caiu'])}) e o Bolsonaro em {len(H['H19']['espelho_2022']['ufs_onde_o_bolsonaro_caiu'])}",
     "menos gente foi votar onde o Flávio perdeu votos, e em 2022 o mesmo aconteceu com o Lula", "a queda seria do Flávio sem queda de comparecimento; não é",
     "não se aplica", "já fechado"),
    ("H20", "E", "A abstenção caiu no Nordeste, mesmo com a falta de ônibus", "comportamento",
     "certo", "Não sustentado",
     f"A abstenção caiu no Nordeste ({p(H['H20']['abstencao_por_regiao']['Nordeste']['abst_1t_pct'])}% para {p(H['H20']['abstencao_por_regiao']['Nordeste']['abst_2t_pct'])}%), no Sudeste ({p(H['H20']['abstencao_por_regiao']['Sudeste']['abst_1t_pct'])}% para {p(H['H20']['abstencao_por_regiao']['Sudeste']['abst_2t_pct'])}%) e no Sul ({p(H['H20']['abstencao_por_regiao']['Sul']['abst_1t_pct'])}% para {p(H['H20']['abstencao_por_regiao']['Sul']['abst_2t_pct'])}%), e subiu no Norte. Em Salvador, onde faltou ônibus, foi de {p(H['H20']['cidades_da_falta_de_onibus'][0]['abst_1t_pct'])}% para {p(H['H20']['cidades_da_falta_de_onibus'][0]['abst_2t_pct'])}%. O vídeo 19 mostrou que a queda da abstenção entre os turnos não tem precedente; aqui ela não vem acompanhada de nenhuma marca de voto acrescentado (H03, H15, H16)",
     "a mobilização dos dois lados levou mais gente a votar em quase todo o país", "a queda sem precedente é real; o que falta a ela é a marca de voto acrescentado",
     "não se aplica", "a lista de quem votou, com o TSE"),
    ("H21", "E", "Compra de voto com benefício social", "comportamento",
     "não medido: o dado do benefício por município não entrou", "Não testado nesta rodada",
     f"Sem o dado do benefício, a renda do município (Censo 2022) serve só de aproximação, e as duas medidas apontam para lados diferentes: em pontos, o Lula cresceu mais nas cidades mais ricas ({p(H['H21']['ganho_lula_pontos_por_quintil_de_renda']['5 (mais rico)'])} pontos nos 20% de maior renda, contra {p(H['H21']['ganho_lula_pontos_por_quintil_de_renda']['1 (mais pobre)'])} nos 20% de menor renda); na parte do saldo, ficou com {p(H['H21']['parte_do_saldo_que_foi_para_o_lula_pct_por_quintil']['1 (mais pobre)'], 1)}% dos votos novos nas mais pobres (o Flávio perdeu votos nelas) e {p(H['H21']['parte_do_saldo_que_foi_para_o_lula_pct_por_quintil']['5 (mais rico)'], 1)}% nas mais ricas. O pedido de cassação por abuso de poder é processo no TSE, fora do alcance do dado de urna",
     "a renda não separa voto convencido de voto comprado", "a parte do saldo que o Lula levou nas cidades pobres é a que a acusação espera; falta o dado do benefício",
     "não medido", "o pagamento do benefício por município (Portal da Transparência) e o processo de abuso de poder no TSE"),
    ("H22", "E", "Onde tem mais celular e 5G, mais voto novo no Lula", "comportamento",
     "não medido", "Não testado nesta rodada",
     "O dado de cobertura por município da Anatel não entrou nesta rodada. A renda (H21) já mostra que o Lula cresceu mais, em pontos, nas cidades mais ricas, que também são as mais conectadas; uma correlação com 5G sozinha não separaria as duas coisas",
     "seria a renda e o tamanho da cidade", "precisaria aparecer com a renda controlada",
     "não medido", "a cobertura da Anatel por município, com controle por renda e tamanho"),
    ("H23", "E", "Joaçaba (SC), Araruama e a Região dos Lagos (RJ)", "comportamento",
     "certo: a conta fecha", "Compatível com as duas",
     f"Em Joaçaba, o Flávio cresceu {n(joa['flavio_2t'] - joa['flavio_1t'])} e o Lula {n(joa['lula_2t'] - joa['lula_1t'])}, com {n(joa['outros_1t'])} votos dos outros candidatos no 1º turno e {n(joa['comparecimento_2t'] - joa['comparecimento_1t'])} votantes a mais; o Lula ficou com {p(h23['parte_do_saldo_para_o_lula_joacaba_pct'], 1)}% do saldo, exatamente a mediana dos municípios de SC ({p(h23['parte_do_saldo_para_o_lula_mediana_sc_pct'], 1)}%). Em Araruama, o Flávio cresceu {n(ara['flavio_2t'] - ara['flavio_1t'])} e o Lula {n(ara['lula_2t'] - ara['lula_1t'])}, com {n(ara['outros_1t'])} votos dos outros e {n(ara['brancos_nulos_1t'] - ara['brancos_nulos_2t'])} brancos e nulos a menos. Na Região dos Lagos inteira, o Lula ficou com {p(h23['parte_do_saldo_para_o_lula_regiao_dos_lagos_pct'], 1)}% do saldo; nos {h23['municipios_parecidos_no_rj']} municípios do RJ em que o Flávio teve votação parecida no 1º turno (cerca de {p(h23['flavio_1t_regiao_dos_lagos_pct'], 0)}%), foi {p(h23['parte_do_saldo_para_o_lula_parecidos_rj_pct'], 1)}%. A diferença dá {n(h23['votos_do_lula_acima_do_esperado_pelos_parecidos'])} votos do Lula acima do esperado",
     "Joaçaba votou como o resto de SC, e onde o Flávio já tinha quase tudo no 1º turno ele tinha pouco para crescer",
     f"a Região dos Lagos deu ao Lula mais do saldo que as cidades parecidas do RJ, {n(h23['votos_do_lula_acima_do_esperado_pelos_parecidos'])} votos acima",
     f"{n(h23['votos_do_lula_acima_do_esperado_pelos_parecidos'])} votos ({pm(h23['votos_do_lula_acima_do_esperado_pelos_parecidos'])})", "pesquisa com o eleitor daquela região"),
]
JA = [("A conta dos 10 milhões e \"a conta não fecha\"", "vídeos 16 e 19"), 
      ("As pesquisas e as regras quebradas (líder do 1º turno, Minas)", "vídeo 19"), ("Mesários votando por quem faltou no 1º turno", "vídeo 8")]
PESO = {"comportamento": "pesa mais", "raridade": "pesa no meio", "arquivos": "pesa menos (bater é o esperado nas duas visões)"}


def contagem():
    c = {}
    for h in HIP:
        c[h[5]] = c.get(h[5], 0) + 1
    return c


def compat():
    return [h[0] for h in HIP if h[5] == "Compatível com as duas"]


def conclusao():
    c = contagem()
    testadas = len(HIP) - c.get("Não testado nesta rodada", 0)
    cm = compat()
    return (f"Das {testadas} hipóteses testadas, {testadas - len(cm)} não mostraram a marca que a fraude deixaria no dado público "
            f"({c.get('Desmentido', 0)} desmentidas e {c.get('Não sustentado', 0)} não sustentadas), e {len(cm)} ficam compatíveis com as duas visões "
            f"({', '.join(cm)}). O número do relatório pericial sai de um erro de fuso. Mesmo somando o pior caso de todos os caminhos que ainda podem ter "
            f"acrescentado voto, um por cima do outro, dá {n(SOMA_TETOS)} votos, {pm(SOMA_TETOS)} da diferença. O que continua sem resposta está dentro do TSE: "
            "a lista de quem votou em cada seção, o cadastro cruzado com os óbitos, a assinatura de cada boletim e um teste de integridade maior.")


def relatorio():
    c = contagem()
    cm = compat()
    L = ["# Relatório: as hipóteses do público sobre o 2º turno de 2026", "",
         f"**Rodada 3, 30/out/2026.** Investigação Aberta, parte 3. Cada hipótese que o público levantou (comentários dos vídeos 8, 16 e 19, o \"Relatório Pericial Independente\" e as teorias da internet) foi testada pelas duas visões: a do resultado legítimo e a da fraude. A rodada 2 aplicou a revisão de três leitores (`docs/REVISAO_ADVERSARIAL.md`). Todo número sai de `ferramentas/analise.py` (`resultados/RESUMO.json`); os números centrais foram refeitos por outro caminho em `ferramentas/validacao_independente.py` ({V['passaram']} de {V['total']} passaram).", "",
         "## O que este projeto não consegue dizer", "",
         "- Quem votou em cada seção: a lista é do TSE. Sem ela, nenhuma hipótese de voto no lugar de outra pessoa fecha caso a caso.",
         "- Se um programa adulterado trocou votos imitando o eleitor: estatística não separa isso; o que fecha é o teste de integridade e o voto impresso.",
         "- A assinatura digital de cada boletim não foi verificada nesta rodada.",
         "- O comparecimento por idade do 2º turno de 2026 ainda não foi publicado pelo TSE.",
         "- Os testes dos logs usam uma amostra sorteada de 12 mil seções (mais as seções especiais), porque os brutos completos do vídeo 16 foram apagados.",
         "- A comparação dentro do mesmo local de votação e contra o 1º turno não pega uma fraude que atinja o lugar inteiro, ou os dois turnos do mesmo jeito.", "",
         "## Os vereditos, em uma tabela", "",
         "Duas respostas separadas: se o fato que circula está certo, e o que o dado diz sobre a leitura de fraude.", "",
         "| # | Hipótese | O fato que circula | Veredito sobre a fraude | Critério | Teto contra a diferença de 4.430.191 votos |", "|---|---|---|---|---|---|"]
    for h in HIP:
        L.append(f"| {h[0]} | {h[2]} | {h[4]} | **{h[5]}** | {h[3]} | {h[9]} |")
    L += ["", "Contagem: " + "; ".join(f"{k}: {v}" for k, v in sorted(c.items(), key=lambda kv: -kv[1])) + ".", "",
          "## O achado principal do relatório pericial", "",
          f"O \"Relatório Pericial Independente\" diz que o Flávio venceu nas urnas encerradas até as 17h. O número dele ({p(REP['ate_17h00']['flavio_pct'])}%) sai igual neste projeto só de um jeito: lendo a hora de encerramento no relógio local de cada estado, sem o fuso. Com isso, as {n(REP['secoes_dos_estados_com_fuso_no_grupo_ate_17h'])} seções dos estados atrás de Brasília, que encerraram às 17h de Brasília, viram \"urnas fechadas até 17h\". Elas deram {p(REP['flavio_pct_nessas'])}% ao Flávio e respondem por {n(REP['frente_flavio_nessas'])} dos {n(REP['ate_17h00']['frente_flavio'])} votos de frente do grupo. Com o fuso certo, as seções que fecham na hora ainda dão um pouco mais ao Flávio ({p(CO['ate']['flavio_pct'])}%), porque são as pequenas, sem fila; no mesmo local de votação, a seção que fechou tarde dá menos ao Lula, não mais. Os votos dados de fato depois das 17h foram {n(V17)}, {pm(V17)} da diferença.", "",
          "## Hipótese por hipótese", ""]
    nomes = {"A": "Bloco A · o relatório pericial", "B": "Bloco B · as seções e as urnas", "C": "Bloco C · os eleitores", "D": "Bloco D · a totalização", "E": "Bloco E · o comportamento dos votos"}
    atual = None
    for h in HIP:
        if h[1] != atual:
            atual = h[1]
            L += [f"### {nomes[atual]}", ""]
        L += [f"#### {h[0]}. {h[2]}", "", f"**O fato que circula:** {h[4]}. **Veredito sobre a fraude: {h[5]}** (critério: {h[3]}, que {PESO[h[3]]}).", "", h[6] + ".", "",
              f"- Visão do resultado legítimo: {h[7]}.", f"- Visão da fraude: {h[8]}.", f"- Teto do pior caso: {h[9]}.", f"- O que fecharia: {h[10]}.", ""]
    L += ["## O que já foi respondido antes", "", "| Hipótese | Onde |", "|---|---|"] + [f"| {a} | {b} |" for a, b in JA]
    crit = {k: [h[0] for h in HIP if h[3] == k] for k in ("comportamento", "raridade", "arquivos")}
    L += ["", "## A conclusão pelas duas visões", "",
          "Com os pesos do vídeo 16 (o comportamento dos votos pesa mais, a raridade no meio e os arquivos das urnas menos):", "",
          "| Critério | Hipóteses | O que o dado sustenta mais |", "|---|---|---|",
          f"| Comportamento dos votos | {', '.join(crit['comportamento'])} | o resultado legítimo; ficam de pé, a conferir, " + ", ".join(x for x in cm if x in crit["comportamento"]) + " |",
          f"| Raridade | {', '.join(crit['raridade'])} | o resultado legítimo: unanimidade, dígitos e placares repetidos aparecem do mesmo jeito em 2018 e 2022 |",
          f"| Arquivos das urnas | {', '.join(crit['arquivos'])} | o resultado legítimo, com peso pequeno: arquivo do TSE contra arquivo do TSE bateria nas duas visões; fica a conferir " + ", ".join(x for x in cm if x in crit["arquivos"]) + " |", "",
          conclusao(), "", "## O pior caso de cada caminho ainda aberto", "", "| Caminho | Votos |", "|---|---|"]
    L += [f"| {k} | {n(v)} |" for k, v in TETOS_ABERTOS.items()] + [f"| **soma, um por cima do outro** | **{n(SOMA_TETOS)} ({pm(SOMA_TETOS)} da diferença)** |"]
    L += ["", "## Validação independente", "", "| Checagem | Obtido | Esperado | Fonte | Passou |", "|---|---|---|---|---|"]
    for c_ in V["checagens"]:
        L.append(f"| {c_['checagem']} | {c_['obtido']} | {c_['esperado']} | {c_['fonte_do_esperado']} | {'sim' if c_['passou'] else 'não'} |")
    rec = R["reconciliacao"]
    L += ["", "## Reconciliação com o total proclamado", "",
          f"O detalhe por seção do TSE soma {n(rec['detalhe_tse_nominais_2t'])} votos nominais e {n(rec['detalhe_tse_comparecimento_2t'])} de comparecimento, o total proclamado. As tabelas por seção copiadas do vídeo 16 somam {n(rec['tabelas_por_secao_nominais_2t'])} nominais: os {n(rec['detalhe_tse_nominais_2t'] - rec['tabelas_por_secao_nominais_2t'])} que faltam são as {n(rec['secoes_com_voto_no_detalhe_e_fora_das_tabelas'])} seções com voto no detalhe e sem boletim de urna nas tabelas ({n(rec['nominais_delas_fora_das_tabelas'])} votos; {n(rec['dessas_no_exterior'])} delas no exterior, apuradas pelo sistema de apuração). Nenhum teste muda por isso.", "",
          "Fontes, método e como refazer: `docs/PLANO.md`, `docs/HIPOTESES.md`, `docs/FONTES_DE_DADOS.md` e `docs/REPLICAR.md`. Análise feita pelo Claude, a pedido do autor do canal."]
    (RAIZ / "RELATORIO.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def resumo_simples():
    cm = compat()
    L = ["# Resumo simples", "",
         "**A pergunta:** o público levantou dezenas de hipóteses de fraude sobre o 2º turno de 2026 que os vídeos anteriores não tinham testado. Alguma delas aparece no dado?", "",
         f"**Como foi feito:** 24 hipóteses, cada uma pelas duas visões (resultado legítimo e fraude), com o arquivo de todas as 499.248 seções, o modelo de cada urna, os logs de uma amostra de urnas, o eleitorado e o comparecimento por idade, o Censo do IBGE e as versões do resultado gravadas ao vivo na noite. Três leitores revisaram (um pela fraude, um pelo resultado legítimo, um pelo método), e os números centrais foram refeitos por outro caminho ({V['passaram']} de {V['total']}).", "",
         "## O que deu", "", "| Hipótese | O fato que circula | Veredito sobre a fraude |", "|---|---|---|"]
    L += [f"| {h[2]} | {h[4]} | {h[5]} |" for h in HIP]
    L += ["", "## As quatro coisas mais importantes", "",
          f"1. **O relatório que circulou tem um erro de fuso.** Ele só chega aos {p(REP['ate_17h00']['flavio_pct'])}% do Flávio \"até as 17h\" porque contou como fechadas cedo as {n(REP['secoes_dos_estados_com_fuso_no_grupo_ate_17h'])} urnas dos estados atrás de Brasília. Votos dados de fato depois das 17h: {n(V17)}.",
          f"2. **As 106 urnas sem voto do Flávio são aldeias e comunidades que já votavam assim.** Em 2022 foram {n(H['H07']['2022_secoes_zero_bolsonaro'])} seções sem voto do Bolsonaro; em 2018, {n(H['H07']['2018_secoes_zero_bolsonaro'])}.",
          f"3. **Há registros de mortos no cadastro, mas eles quase não votam.** Pelo menos {n(h13['registros_de_100_ou_mais_sem_pessoa_possivel_2026_piso'])} registros de centenário não correspondem a pessoa viva possível (em 2022 eram {n(h13['registros_de_100_ou_mais_sem_pessoa_possivel_2022'])}); o comparecimento de quem tem 100 anos ou mais foi de {p(cp['100 ou mais']['2026_t1']['taxa_pct'])}% no 1º turno.",
          f"4. **O que fica a conferir ({', '.join(cm)}):** {n(h14['comparecimento_2t_maior_que_pop_total'])} municípios com mais votos que habitantes (eram {n(h14['2022_comparecimento_2t_maior_que_pop_total'])} em 2022), os avisos \"já votou\" isolados, que subiram, as quedas grandes do Flávio em parte das seções e a Região dos Lagos. Somando o pior caso de tudo o que ainda está aberto: {pm(SOMA_TETOS)} da diferença.", "",
          "O que só o TSE tem: a lista de quem votou, o cruzamento do cadastro com os óbitos e a assinatura de cada boletim. Relatório completo: [`RELATORIO.md`](RELATORIO.md)."]
    (RAIZ / "RESUMO_SIMPLES.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def leitura():
    L = ["# Leitura da IA", "", "**Rodada 3, 30/out/2026.** A leitura de cada bloco, com o que cada visão diz e qual o dado sustenta mais. Os números estão no `RELATORIO.md`.", ""]
    for bloco, nome in [("A", "O relatório pericial"), ("B", "As seções e as urnas"), ("C", "Os eleitores"), ("D", "A totalização"), ("E", "O comportamento dos votos")]:
        L += [f"## {nome}", ""]
        for h in [x for x in HIP if x[1] == bloco]:
            L.append(f"- **{h[0]} · {h[5]}.** Legítimo: {h[7]}. Fraude: {h[8]}.")
        L.append("")
    L += ["## No fim", "", conclusao(), "", "A visão do resultado legítimo fica na frente nos três critérios, sem que isso prove que não houve irregularidade em lugar nenhum. Os pedidos ao TSE estão em `docs/PEDIDOS_LAI.md`."]
    (RAIZ / "docs/LEITURA_DA_IA.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    relatorio()
    resumo_simples()
    leitura()
    print("ok", contagem(), "soma dos tetos", SOMA_TETOS, pm(SOMA_TETOS))
