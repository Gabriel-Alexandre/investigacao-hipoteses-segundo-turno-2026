"""Graficos 1920x1080 da rodada 4 (H25 a H29), a partir de resultados/RODADA4.json. Mesmo padrao de graficos.py.

Uso: python ferramentas/graficos_rodada_4.py   ->  resultados/figuras/g17 a g22
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
R = json.loads((RAIZ / "resultados/RODADA4.json").read_text(encoding="utf-8"))
RB = json.loads((RAIZ / "resultados/RODADA4B.json").read_text(encoding="utf-8")) if (RAIZ / "resultados/RODADA4B.json").exists() else {}
OUT = RAIZ / "resultados/figuras"
LULA, FLAVIO, BASE, FUNDO, TEXTO, AMARELO, VERDE = "#C8553D", "#2D6A8A", "#6B6B6B", "#FFFFFF", "#1E1E1E", "#E0B400", "#3D7A4F"
REPO = "github.com/Gabriel-Alexandre/investigacao-hipoteses-segundo-turno-2026"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 22, "axes.edgecolor": "#BBBBBB", "axes.labelcolor": TEXTO,
                     "xtick.color": TEXTO, "ytick.color": TEXTO, "axes.spines.top": False, "axes.spines.right": False})


def n(x):
    return f"{int(x):,}".replace(",", ".")


def d(x, c=1):
    return f"{x:.{c}f}".replace(".", ",")


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


def g17_campos():
    h = R["H25"]
    c = h["conta_do_post"]
    f = fig("Campos: de onde podia vir o ganho do Lula", "A abstenção subiu; o Lula ficou com 86% de quem podia mudar")
    ax = f.add_axes([0.05, 0.18, 0.9, 0.55])
    partes = [("Votos dos outros candidatos no 1º turno", c["votos_dos_outros_candidatos_no_1t"], "#9DB9C9"),
              ("Brancos e nulos que sumiram", c["brancos_e_nulos_que_sumiram"], "#BBBBBB"),
              ("Votos que o Flávio perdeu", -c["flavio_variou"], FLAVIO)]
    x = 0
    for i_, (nome, v, cor) in enumerate(partes):
        ax.barh([1], [v], left=[x], color=cor, height=0.5)
        ax.text(x + v / 2, 1, n(v), ha="center", va="center", color=TEXTO if cor != FLAVIO else "white", fontsize=17 if cor == FLAVIO else 20, weight="bold")
        ax.text(x + v / 2 - (0 if i_ < 2 else 2800), 0.62 - 0.22 * (i_ == 2), nome, ha="center", va="top", color=BASE, fontsize=15)
        x += v
    ax.barh([2.1], [c["lula_ganhou"]], color=LULA, height=0.5)
    ax.text(c["lula_ganhou"] / 2, 2.1, f"O Lula ganhou {n(c['lula_ganhou'])}", ha="center", va="center", color="white", fontsize=22, weight="bold")
    ax.text(x, 1.58, f"Quem podia mudar: {n(x)}", ha="right", va="bottom", color=TEXTO, fontsize=19)
    ax.text(c["lula_ganhou"] + 600, 2.1, f"= {c['lula_ficou_com_pct_do_pool']:.0f}%".replace(".", ","), ha="left", va="center", color=LULA, fontsize=26, weight="bold")
    ax.set_xlim(0, x * 1.03)
    ax.set_ylim(0.2, 2.6)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    f.text(0.05, 0.1, f"Abstenção: {n(h['campos']['abstencao_1t'])} no 1º turno, {n(h['campos']['abstencao_2t'])} no 2º (subiu {n(c['abstencao_variou_para_cima'])}). "
           f"Nas cidades com mais de 100 mil eleitores, o Lula ficou com {h['mediana_lula_do_pool_grandes_pct']:.0f}% (mediana).", fontsize=15, color=TEXTO)
    rodape(f, "TSE (resultados por município e por seção) e IBGE")
    salvar(f, "g17_campos_dos_goytacazes")


def g18_municipios():
    h = R["H26"]
    f = fig("Eleitores e habitantes: 835 dos 5.570 municípios", "Já era assim em 2022; 120 têm mais votantes que habitantes")
    ax = f.add_axes([0.1, 0.29, 0.85, 0.48])
    rot = ["Eleitorado maior\nque a população", "Comparecimento maior\nque a população"]
    v22 = [h["eleitorado_maior_que_populacao_2022_2t"], h["comparecimento_maior_que_populacao_2022_2t"]]
    v26 = [h["eleitorado_maior_que_populacao_2026_2t"], h["comparecimento_maior_que_populacao_2026_2t"]]
    xs = [0, 1]
    w = 0.34
    b1 = ax.bar([x - w / 2 for x in xs], v22, w, color="#BBBBBB", label="2022 (2º turno)")
    b2 = ax.bar([x + w / 2 for x in xs], v26, w, color=LULA if False else FLAVIO, label="2026 (2º turno)")
    for b, v in list(zip(b1, v22)) + list(zip(b2, v26)):
        ax.text(b.get_x() + b.get_width() / 2, v + 12, str(v), ha="center", fontsize=22, weight="bold")
    ax.set_xticks(xs)
    ax.set_xticklabels(rot, fontsize=20)
    ax.legend(frameon=False, fontsize=18, loc="upper right")
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    f.text(0.05, 0.1, f"Os 120 somam {n(h['votos_acima_da_populacao_soma_2026'])} votos acima da população: {d(h['votos_acima_da_populacao_pct_da_diferenca'], 2)}% da diferença de 4.430.191. " +
           f"Os 835 têm {d(h['pct_do_eleitorado_do_pais_nesses_municipios'])}% do eleitorado do país.", fontsize=15, color=TEXTO)
    rodape(f, "TSE e Censo 2022 (IBGE); 2022: boletins por seção do TSE")
    salvar(f, "g18_eleitores_e_habitantes")


def g19_abstencao():
    h = R["H29"]
    f = fig("Onde a abstenção caiu mais, o Lula não cresceu mais", "Seção a seção, dentro do mesmo município: 2026 contra 2022")
    ax = f.add_axes([0.1, 0.29, 0.85, 0.48])
    vals = [h["2022"]["inclinacao_pontos_do_lula_por_ponto_de_queda_da_abstencao"], h["2026"]["inclinacao_pontos_do_lula_por_ponto_de_queda_da_abstencao"]]
    cis = [h["2022"]["intervalo_95_bootstrap_por_municipio"], h["2026"]["intervalo_95_bootstrap_por_municipio"]]
    for i, (v, ci, cor) in enumerate(zip(vals, cis, ["#BBBBBB", LULA])):
        ax.bar([i], [v], color=cor, width=0.5)
        ax.errorbar([i], [v], yerr=[[v - ci[0]], [ci[1] - v]], color=TEXTO, capsize=10, lw=2)
        ax.text(i, ci[1] + 0.003, f"{v:.3f}".replace(".", ","), ha="center", fontsize=24, weight="bold")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["2022", "2026"], fontsize=22)
    ax.set_ylim(0, 0.07)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    f.text(0.05, 0.1, "Pontos a mais de voto no Lula por ponto a mais de queda da abstenção. Se votassem pelos ausentes, 2026 seria bem maior que 2022.\n"
           f"Abstenção nacional: {d(h['abstencao_1t_pct'], 2)}% → {d(h['abstencao_2t_pct'], 2)}% em 2026; {d(h['abstencao_1t_2022_pct'], 2)}% → {d(h['abstencao_2t_2022_pct'], 2)}% em 2022.", fontsize=14.5, color=TEXTO)
    rodape(f, "TSE, 499.095 seções de 2026 e 472.026 de 2022; barra: intervalo de 95%")
    salvar(f, "g19_abstencao_e_voto_do_lula")


def g20_escolas():
    h = R["H28"]
    f = fig("Seções da mesma escola: o 2º turno não ficou mais desigual", "Dentro de cada escola, quanto uma seção se afasta das outras")
    ax = f.add_axes([0.1, 0.29, 0.85, 0.48])
    vals = [h["1t"]["z_maior_que_4_pct"], h["2t"]["z_maior_que_4_pct"]]
    for i, (v, cor) in enumerate(zip(vals, [FLAVIO, LULA])):
        ax.bar([i], [v], color=cor, width=0.5)
        ax.text(i, v + 0.02, f"{v:.2f}%".replace(".", ","), ha="center", fontsize=26, weight="bold")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["1º turno", "2º turno"], fontsize=22)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    f.text(0.05, 0.1, f"Parte das seções muito fora do padrão da própria escola ({n(h['1t']['secoes'])} seções, {n(h['1t']['locais'])} escolas). Correlação entre os turnos: {d(h['correlacao_do_z_entre_turnos'], 2)}. " +
           f"Fora do padrão só no 2º turno: {h['z_extremo_no_2t_e_normal_no_1t']}; só no 1º: {h['z_extremo_no_1t_e_normal_no_2t']}.", fontsize=15, color=TEXTO)
    rodape(f, "TSE, locais de votação e resultados por seção")
    salvar(f, "g20_secoes_da_mesma_escola")


def g21_sem_digital():
    h = R["H27"]
    f = fig("Votos liberados sem a digital: igual nos dois turnos", "Por hora do dia, amostra de 11,9 mil seções")
    ax = f.add_axes([0.08, 0.29, 0.87, 0.48])
    hs = list(h["liberacao_manual_por_hora_pct"]["t1"].keys())
    ax.plot(hs, list(h["liberacao_manual_por_hora_pct"]["t1"].values()), color=FLAVIO, lw=4, marker="o", label="1º turno")
    ax.plot(hs, list(h["liberacao_manual_por_hora_pct"]["t2"].values()), color=LULA, lw=4, marker="o", label="2º turno")
    ax.set_ylim(8, 18)
    ax.legend(frameon=False, fontsize=20)
    ax.set_ylabel("% dos votos da hora", fontsize=18)
    ax.tick_params(labelsize=16)
    f.text(0.05, 0.1, f"Total: {d(h['por_turno']['t1']['sem_digital_pct'])}% no 1º, {d(h['por_turno']['t2']['sem_digital_pct'])}% no 2º. A seção que tinha mais no 1º tinha mais no 2º (correlação {d(h['correlacao_do_sem_digital_entre_turnos'], 2)}). " +
           "A hora das 17h do 2º turno (a prorrogação) destoa.", fontsize=15, color=TEXTO)
    rodape(f, "logs das urnas (amostra sorteada) e TSE")
    salvar(f, "g21_sem_digital_por_hora")


def g22_tamanho():
    t = RB["H26b"]["parcela_acima_por_tamanho"]
    f = fig("É um fenômeno de cidade pequena", "Parte dos municípios com mais eleitores que habitantes, por tamanho da cidade")
    ax = f.add_axes([0.1, 0.29, 0.85, 0.48])
    rot = list(t.keys())
    vals = [t[k]["pct"] for k in rot]
    nomes = {"ate 5 mil": "até 5 mil" + chr(10) + "habitantes", "5 a 20 mil": "5 a 20 mil", "20 a 100 mil": "20 a 100 mil", "mais de 100 mil": "mais de" + chr(10) + "100 mil"}
    for i, v in enumerate(vals):
        ax.bar([i], [v], color=FLAVIO if i == 0 else "#9DB9C9", width=0.55)
        ax.text(i, v + 1.2, f"{d(v)}%", ha="center", fontsize=26, weight="bold")
    ax.set_xticks(range(len(rot)))
    ax.set_xticklabels([nomes[k] for k in rot], fontsize=19)
    ax.set_ylim(0, 56)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    h = RB["H26b"]
    f.text(0.05, 0.1, f"Dos 835, {h['dos_835_ja_tinham_mais_eleitores_que_habitantes_em_2022']} já estavam assim em 2022. Piauí, Paraíba, Rio Grande do Norte e Goiás têm de 35% a 38% dos municípios.\nO ganho do Lula nesses municípios foi {d(h['ganho_medio_do_lula_nos_835_pontos'])} pontos, contra {d(h['ganho_medio_do_lula_nos_demais_pontos'])} nos demais.", fontsize=14.5, color=TEXTO)
    rodape(f, "TSE, Censo 2022 (IBGE) e boletins de 2022 por seção")
    salvar(f, "g22_cidade_pequena")


def main():
    g17_campos()
    g18_municipios()
    g19_abstencao()
    g20_escolas()
    g21_sem_digital()
    if RB:
        g22_tamanho()
    print("g17 a g22 em resultados/figuras")


if __name__ == "__main__":
    main()
