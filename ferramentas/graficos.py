"""Gráficos 1920x1080 do vídeo e do relatório, a partir de resultados/RESUMO.json. Cores iguais às dos outros
projetos (Lula #C8553D, Flávio #2D6A8A, base #6B6B6B); fonte e link do repositório no rodapé.

Uso: python ferramentas/graficos.py   ->  resultados/figuras/gNN_<nome>.png
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
R = json.loads((RAIZ / "resultados/RESUMO.json").read_text(encoding="utf-8"))
OUT = RAIZ / "resultados/figuras"
LULA, FLAVIO, BASE, FUNDO, TEXTO = "#C8553D", "#2D6A8A", "#6B6B6B", "#FFFFFF", "#1E1E1E"
REPO = "github.com/Gabriel-Alexandre/investigacao-hipoteses-segundo-turno-2026"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 22, "axes.edgecolor": "#BBBBBB", "axes.labelcolor": TEXTO,
                     "xtick.color": TEXTO, "ytick.color": TEXTO, "axes.spines.top": False, "axes.spines.right": False})


def n(x):
    return f"{int(x):,}".replace(",", ".")


def fig(titulo, subtitulo=None):
    f = plt.figure(figsize=(16, 9), dpi=120, facecolor=FUNDO)
    f.text(0.05, 0.93, titulo, fontsize=34, weight="bold", color=TEXTO, va="top")
    if subtitulo:
        f.text(0.05, 0.855, subtitulo, fontsize=21, color=BASE, va="top")
    return f


def rodape(f, fonte):
    f.text(0.05, 0.035, f"Fonte: {fonte}. Análise feita pelo Claude. {REPO}", fontsize=11.5, color=BASE)


def salvar(f, nome):
    OUT.mkdir(parents=True, exist_ok=True)
    f.savefig(OUT / f"{nome}.png", dpi=120, facecolor=FUNDO)
    plt.close(f)


def g01_fuso():
    rep = R["H01"]["reproducao_do_relatorio"]
    f = fig("Como o relatório chegou aos 52,39% do Flávio", "Ele leu a hora de encerramento no relógio local, sem o fuso")
    ax = f.add_axes([0.05, 0.2, 0.9, 0.5])
    fu = rep["secoes_dos_estados_com_fuso_no_grupo_ate_17h"]
    total = rep["ate_17h00"]["secoes"]
    ax.barh([1], [fu], color=FLAVIO, height=0.45)
    ax.barh([1], [total - fu], left=[fu], color="#9DB9C9", height=0.45)
    ax.text(0, 0.68, f"{n(fu)} urnas de AC, AM, MT, MS, RO e RR,\nque fecharam às 17h de Brasília\n(15h ou 16h no relógio delas)",
            ha="left", va="top", color=FLAVIO, fontsize=19, weight="bold")
    ax.text(total, 0.68, f"{n(total - fu)} urnas do resto do país\nque fecharam até 17h00", ha="right", va="top", color=TEXTO, fontsize=19)
    ax.text(0, 1.32, "As urnas que o relatório contou como \"encerradas até as 17h\"", fontsize=20, color=BASE)
    ax.set_xlim(0, total)
    ax.set_ylim(0.0, 1.5)
    ax.set_xticks([])
    ax.set_yticks([])
    for lado in ("bottom", "left"):
        ax.spines[lado].set_visible(False)
    f.text(0.05, 0.17, f"Nos 6 estados: {str(rep['flavio_pct_nessas']).replace('.', ',')}% para o Flávio\n"
           f"e {n(rep['frente_flavio_nessas'])} dos {n(rep['ate_17h00']['frente_flavio'])} votos de frente do grupo",
           fontsize=21, color=TEXTO, weight="bold", va="center")
    rodape(f, "TSE, boletim de urna de cada seção (hora de encerramento)")
    salvar(f, "g01_o_erro_de_fuso")


def g02_17h():
    h = R["H02"]
    f = fig("Quantos votos vieram depois das 17h", "Contados no log de cada urna. O relatório chamou de prorrogação o voto do dia inteiro")
    ax = f.add_axes([0.08, 0.17, 0.86, 0.6])
    vals = [h["comparecimento_do_dia_inteiro_nelas"], h["votos_depois_17h_brasil_log"] + R["H02_oeste_do_amazonas"]["votos_depois_17h_brasilia"], 4430191]
    rot = ["\"mais de 2,5 milhões\" do relatório:\no dia inteiro das urnas que fecharam tarde", "votos com hora depois das 17h\nno Brasil inteiro", "diferença entre\nLula e Flávio"]
    cores = [BASE, LULA, "#333333"]
    ax.bar(range(3), vals, color=cores, width=0.6)
    for i, v in enumerate(vals):
        ax.text(i, v * 1.02, n(v), ha="center", fontsize=24, weight="bold")
    ax.set_xticks(range(3), rot, fontsize=17)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    rodape(f, "TSE, log de cada urna do 2º turno")
    salvar(f, "g02_votos_depois_das_17h")


def g03_unanimidade():
    h4, h7 = R["H04"], R["H07"]
    f = fig("A unanimidade foi menor que em 2018 e 2022", "Seções com mais de 90% para um candidato, e seções com zero voto")
    ax = f.add_axes([0.07, 0.17, 0.4, 0.58])
    anos = ["2018", "2022", "2026"]
    pt = [h4["2018_acima_90_haddad"], h4["2022_acima_90_lula"], h4["acima_90_lula"]]
    dr = [h4["2018_acima_90_bolsonaro"], h4["2022_acima_90_bolsonaro"], h4["acima_90_flavio"]]
    x = range(3)
    ax.bar([i - 0.2 for i in x], pt, width=0.4, color=LULA, label="candidato do PT")
    ax.bar([i + 0.2 for i in x], dr, width=0.4, color=FLAVIO, label="candidato da direita (PSL em 2018, PL depois)")
    for i in x:
        ax.text(i - 0.2, pt[i] * 1.02, n(pt[i]), ha="center", fontsize=16)
        ax.text(i + 0.2, dr[i] * 1.02, n(dr[i]), ha="center", fontsize=16)
    ax.set_xticks(list(x), anos)
    ax.set_title("mais de 90% dos votos", fontsize=20, color=BASE)
    ax.legend(frameon=False, fontsize=13, loc="upper right")
    ax.set_ylim(0, max(pt) * 1.35)
    ax.set_yticks([])
    ax2 = f.add_axes([0.56, 0.17, 0.4, 0.58])
    z = [h7["2018_secoes_zero_bolsonaro"], h7["2022_secoes_zero_bolsonaro"], h7["secoes"]]
    ax2.bar(list(x), z, color=FLAVIO, width=0.55)
    for i in x:
        ax2.text(i, z[i] * 1.02, n(z[i]), ha="center", fontsize=20, weight="bold")
    ax2.set_xticks(list(x), anos)
    ax2.set_title("zero voto para o candidato da direita", fontsize=20, color=BASE)
    ax2.set_ylim(0, max(z) * 1.18)
    ax2.set_yticks([])
    rodape(f, "TSE, votação por seção do 2º turno de 2018, 2022 e 2026")
    salvar(f, "g03_unanimidade_no_tempo")


def g04_benford():
    d = R["H05"]["distribuicao_1o_digito"]
    f = fig("Benford reprova os dois do mesmo jeito", "1º dígito dos votos de cada seção no 2º turno de 2026")
    ax = f.add_axes([0.08, 0.17, 0.86, 0.6])
    dig = [str(k) for k in range(1, 10)]
    ax.bar([int(k) - 0.2 for k in dig], [d["lula_2026"].get(k, 0) for k in dig], width=0.4, color=LULA, label="Lula")
    ax.bar([int(k) + 0.2 for k in dig], [d["flavio_2026"].get(k, 0) for k in dig], width=0.4, color=FLAVIO, label="Flávio")
    ax.plot([int(k) for k in dig], [d["benford"][k] for k in dig], color="#222222", lw=3, marker="o", label="o que Benford espera")
    ax.set_xticks(range(1, 10))
    ax.set_yticks([])
    ax.legend(frameon=False, fontsize=18)
    ax.set_xlabel("primeiro dígito do número de votos da seção")
    rodape(f, "TSE, boletim de urna de cada seção")
    salvar(f, "g04_benford")


def g05_repetidos():
    h = R["H08"]
    f = fig("Placares repetidos entre seções: menos que o acaso", "Quantos placares (Lula, Flávio) aparecem em mais de uma seção")
    ax = f.add_axes([0.08, 0.17, 0.86, 0.6])
    vals = [h["placares_repetidos_2026"], h["esperado_pelo_acaso_media"], h["placares_repetidos_2022"]]
    ax.bar(range(3), vals, color=[LULA, BASE, "#999999"], width=0.55)
    for i, v in enumerate(vals):
        ax.text(i, v * 1.01, n(v), ha="center", fontsize=24, weight="bold")
    ax.set_xticks(range(3), ["2026, o que aconteceu", "2026, o que o acaso daria\n(média de 20 sorteios)", "2022, o que aconteceu"])
    ax.set_ylim(0, max(vals) * 1.15)
    ax.set_yticks([])
    rodape(f, "TSE, boletim de cada seção; sorteio pelo 1º turno de cada seção")
    salvar(f, "g05_placares_repetidos")


def g06_modelo():
    m = R["H09"]["por_modelo"]
    f = fig("O modelo da urna não muda o voto", "Quanto o Lula ganhou do 1º para o 2º turno, por modelo de urna")
    ax = f.add_axes([0.08, 0.17, 0.86, 0.6])
    ks = ["UE 2013", "UE 2015", "UE 2020", "UE 2022"]
    vals = [m[k]["ganho_lula_pontos"] for k in ks]
    ax.bar(range(4), vals, color=LULA, width=0.55)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.15, f"{str(v).replace('.', ',')} pontos", ha="center", fontsize=22, weight="bold")
    ax.set_xticks(range(4), [f"{k}\n{n(m[k]['secoes'])} seções" for k in ks])
    ax.set_ylim(0, max(vals) * 1.25)
    ax.set_yticks([])
    rodape(f, "TSE, detalhe da votação por seção (modelo da urna) e boletim de cada seção")
    salvar(f, "g06_modelo_da_urna")


def g07_centenarios():
    h = R["H13"]
    f = fig("Registros de mortos no cadastro quase não votam", "Eleitores com 100 anos ou mais e quem pode ter essa idade")
    ax = f.add_axes([0.07, 0.17, 0.44, 0.58])
    vals = [h["eleitores_100_ou_mais_2026"], h["populacao_96_ou_mais_censo_2022"]]
    c = h["comparecimento_por_idade"]["100 ou mais"]
    ax.bar([0, 1], vals, color=[BASE, "#333333"], width=0.55)
    for i, v in enumerate(vals):
        ax.text(i, v * 1.02, n(v), ha="center", fontsize=24, weight="bold")
    ax.set_xticks([0, 1], ["eleitores com 100 anos\nou mais em 2026", "pessoas com 96 anos\nou mais no Censo 2022"], fontsize=17)
    ax.set_yticks([])
    ax2 = f.add_axes([0.58, 0.17, 0.38, 0.58])
    rot = ["2022\n1º turno", "2022\n2º turno", "2026\n1º turno"]
    tx = [c["2022_t1"]["taxa_pct"], c["2022_t2"]["taxa_pct"], c["2026_t1"]["taxa_pct"]]
    ax2.bar(range(3), tx, color=LULA, width=0.55)
    for i, v in enumerate(tx):
        ax2.text(i, v + 0.03, f"{str(v).replace('.', ',')}%", ha="center", fontsize=22, weight="bold")
    ax2.set_xticks(range(3), rot)
    ax2.set_title("quantos deles foram votar", fontsize=20, color=BASE)
    ax2.set_ylim(0, 2)
    ax2.set_yticks([])
    rodape(f, "TSE, eleitorado e comparecimento por idade; IBGE, Censo 2022")
    salvar(f, "g07_centenarios")


def g08_manual_por_hora():
    h = R["H16"]["parte_manual_por_hora_pct"]
    f = fig("A liberação sem a digital do eleitor ao longo do dia", "Parte dos votos liberados pelo mesário ou pelo ano de nascimento, por hora (Brasília)")
    ax = f.add_axes([0.08, 0.17, 0.86, 0.6])
    for t, cor, nome in (("t1", BASE, "1º turno"), ("t2", LULA, "2º turno")):
        hs = [k for k in sorted(h[t]) if 8 <= int(k) <= 16]
        ax.plot([int(k) for k in hs], [h[t][k] for k in hs], marker="o", lw=4, color=cor, label=nome)
    ax.set_ylim(0, 20)
    ax.set_yticks(range(0, 21, 5), [f"{v}%" for v in range(0, 21, 5)])
    ax.set_xticks(range(8, 17), [f"{k}h" for k in range(8, 17)])
    ax.set_ylabel("% dos votos")
    ax.legend(frameon=False)
    rodape(f, "TSE, log de 12 mil urnas sorteadas")
    salvar(f, "g08_liberacao_manual_por_hora")


def g09_estados():
    u = R["H19"]["ufs_onde_o_flavio_caiu"]
    f = fig("Onde o Flávio perdeu votos, menos gente foi votar", "Os 6 estados em que o Flávio teve menos votos no 2º turno que no 1º")
    ax = f.add_axes([0.1, 0.17, 0.84, 0.6])
    ks = sorted(u, key=lambda k: u[k]["variacao_comparecimento_pontos"])
    ax.barh(range(len(ks)), [u[k]["variacao_comparecimento_pontos"] for k in ks], color=BASE)
    for i, k in enumerate(ks):
        v = u[k]["variacao_comparecimento_pontos"]
        rot = f"{str(v).replace('.', ',')} pontos  (Flávio {n(u[k]['votos'])})"
        if v < -3:
            ax.text(v / 2, i, rot, va="center", ha="center", fontsize=17, color="white", weight="bold")
        else:
            ax.text(v - 0.1, i, rot, va="center", ha="right", fontsize=17, color=TEXTO)
    ax.set_yticks(range(len(ks)), [k.upper() for k in ks])
    ax.set_xlabel("variação do comparecimento entre os turnos")
    ax.set_xlim(-9, 0)
    rodape(f, "TSE, boletim de urna de cada seção nos dois turnos")
    salvar(f, "g09_estados_onde_o_flavio_caiu")


def g10_renda():
    q = R["H21"]["ganho_lula_pontos_por_quintil_de_renda"]
    f = fig("A renda não decide a pergunta do benefício", "Por faixa de renda do município: o ganho em pontos e a parte do saldo que foi para o Lula")
    s_ = R["H21"]["parte_do_saldo_que_foi_para_o_lula_pct_por_quintil"]
    ax2 = f.add_axes([0.56, 0.17, 0.4, 0.58])
    ax2.bar(range(5), [s_[k] for k in q], color="#9B3A2A", width=0.6)
    for i, k in enumerate(q):
        ax2.text(i, s_[k] + 2, f"{str(s_[k]).replace('.', ',')}%", ha="center", fontsize=18, weight="bold")
    ax2.set_xticks(range(5), ["20% mais\npobres", "2º", "3º", "4º", "20% mais\nricos"], fontsize=16)
    ax2.set_yticks([])
    ax2.set_ylim(0, 125)
    ax2.set_title("parte do saldo para o Lula", fontsize=20, color=BASE)
    ax = f.add_axes([0.07, 0.17, 0.42, 0.58])
    ax.set_title("ganho em pontos", fontsize=20, color=BASE)
    ks = list(q)
    ax.bar(range(5), [q[k] for k in ks], color=LULA, width=0.6)
    for i, k in enumerate(ks):
        ax.text(i, q[k] + 0.15, f"{str(q[k]).replace('.', ',')}", ha="center", fontsize=18, weight="bold")
    ax.set_xticks(range(5), ["20% mais\npobres", "2º", "3º", "4º", "20% mais\nricos"], fontsize=16)
    ax.set_ylim(0, max(q.values()) * 1.25)
    ax.set_yticks([])
    rodape(f, "TSE, resultado por município; IBGE, Censo 2022 (renda domiciliar por pessoa)")
    salvar(f, "g10_renda_e_saldo")


CURTO = {"H01": "Flávio venceu até as 17h", "H02": "2,5 milhões depois do horário", "H03": "8,6 milhões sem biometria", "H04": "6.899 seções acima de 90%",
         "H05": "A lei de Benford", "H06": "Boletins escondidos 72 horas", "H07": "106 urnas sem voto do Flávio", "H08": "Placares repetidos",
         "H09": "Urna antiga contra nova", "H10": "Urnas trocadas", "H11": "Boletim de papel e site", "H12": "Seções fantasmas",
         "H13": "Mortos votaram", "H14": "Mais votos que habitantes", "H15": "Já tinham votado por mim", "H16": "Mesário votando o dia todo",
         "H17": "Sala-cofre e painel", "H18": "Programa troca o voto", "H19": "Flávio perdeu votos em 6 estados", "H20": "Abstenção no Nordeste",
         "H21": "Compra de voto com benefício", "H22": "Celular e 5G", "H23": "Joaçaba e Região dos Lagos"}


def g11_vereditos():
    import re
    texto = (RAIZ / "RELATORIO.md").read_text(encoding="utf-8")
    linhas = [(a, b, d) for a, b, _, d in re.findall(r"^\| (H\d\d) \| (.+?) \| (.+?) \| \*\*(.+?)\*\* \|", texto, re.M)]
    cores = {"Desmentido": "#2E7D32", "Não sustentado": "#7CB342", "Compatível com as duas": "#F9A825", "Não testado nesta rodada": "#9E9E9E"}
    f = plt.figure(figsize=(16, 9), dpi=120, facecolor=FUNDO)
    f.text(0.05, 0.95, "As 23 hipóteses, uma a uma", fontsize=32, weight="bold", va="top")
    for i, (h, t, v) in enumerate(linhas):
        col, lin = i // 12, i % 12
        x, y = 0.04 + col * 0.49, 0.84 - lin * 0.064
        curto = CURTO.get(h, t)
        f.text(x, y, f"{h}  {curto}", fontsize=14, va="center")
        f.text(x + 0.30, y, v.replace(" nesta rodada", ""), fontsize=14, va="center", weight="bold", color=cores.get(v, TEXTO))
    rodape(f, "resultados/RESUMO.json deste projeto")
    salvar(f, "g11_os_vereditos")


def g12_a_noite():
    import pandas as pd
    c = pd.read_csv(RAIZ / "resultados/tabelas/h17_curva_nacional.csv", parse_dates=["quando"])
    h = R["H17"]
    f = fig("A noite da apuração, versão por versão",
            f"Total de votos de cada candidato nas {h['versoes_nacionais']} versões nacionais gravadas ao vivo")
    ax = f.add_axes([0.09, 0.17, 0.85, 0.6])
    ax.plot(c.quando, c.lula / 1e6, lw=4, color=LULA, label="Lula")
    ax.plot(c.quando, c.flavio / 1e6, lw=4, color=FLAVIO, label="Flávio")
    ax.set_ylabel("milhões de votos")
    ax.xaxis.set_major_formatter(__import__("matplotlib.dates", fromlist=["DateFormatter"]).DateFormatter("%Hh%M"))
    ax.legend(frameon=False, loc="upper left")
    quedas = h["vezes_que_o_total_do_flavio_caiu"] + h["vezes_que_o_total_do_lula_caiu"]
    ax.text(0.98, 0.06, f"vezes que um total caiu de uma versão pra outra: {quedas}", transform=ax.transAxes,
            ha="right", fontsize=18, color=TEXTO, weight="bold")
    rodape(f, "TSE, resultados divulgados na noite de 25/10/2026 (cópia com sha256 no projeto)")
    salvar(f, "g12_a_noite")


if __name__ == "__main__":
    for g in (g01_fuso, g02_17h, g03_unanimidade, g04_benford, g05_repetidos, g06_modelo, g07_centenarios, g08_manual_por_hora, g09_estados, g10_renda, g11_vereditos, g12_a_noite):
        g()
    print("ok", len(list(OUT.glob("*.png"))))
