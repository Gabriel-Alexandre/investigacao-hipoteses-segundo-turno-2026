"""Gráficos 1920x1080 da rodada 6 (a resposta do TSE, o 2º turno para governador, o mesmo mesário em 2 cidades e as
hipóteses da série), a partir de resultados/RODADA6.json e resultados/RODADA6_MESARIOS.json.

Uso: python ferramentas/graficos_rodada_6.py   ->  resultados/figuras/g34 a g38
"""
import json
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "ferramentas"))
sys.path.insert(0, str(RAIZ))
from graficos_rodada_4 import AMARELO, BASE, FLAVIO, FUNDO, LULA, TEXTO, VERDE, d, fig, n, salvar  # noqa: E402

R = json.loads((RAIZ / "resultados/RODADA6.json").read_text(encoding="utf-8"))
REPO = "github.com/Gabriel-Alexandre/investigacao-hipoteses-segundo-turno-2026"


def rodape(f, fonte):
    f.text(0.05, 0.035, f"Fonte: {fonte}. Análise com a ajuda do Claude. {REPO}", fontsize=10, color=BASE)


def g34_noite():
    """A curva das seções totalizadas no 1º turno, minuto a minuto, com o que o TSE disse por cima."""
    dd = pd.read_parquet(RAIZ / "dados/derivados/detalhe_secao_2026.parquet", columns=["turno", "recebido_tse"])
    dd = dd[dd.turno == "1"]
    ts = pd.to_datetime(dd.recebido_tse, format="%d/%m/%Y %H:%M:%S").sort_values().reset_index(drop=True)
    pct = (pd.Series(range(1, len(ts) + 1)) / len(ts) * 100)
    f = fig("A noite do 1º turno, boletim por boletim", "Seções totalizadas pela hora de cada boletim no arquivo público do TSE, e o que o TSE respondeu")
    ax = f.add_axes([0.07, 0.15, 0.86, 0.62])
    ax.plot(ts, pct, color=FLAVIO, lw=3)
    h = lambda x: pd.Timestamp("2026-10-04 " + x)
    ax.axvspan(h("19:31:50"), h("19:59:22"), color=AMARELO, alpha=0.25)
    for a, b in (("18:01:00", "18:08:47"), ("18:49:47", "18:53:59")):
        ax.axvspan(h(a), h(b), color=BASE, alpha=0.18)
    ax.text(h("17:38"), 32, "2 paradas menores\n(18h01 e 18h50),\nque a resposta\nnão cita", ha="center", fontsize=13, color=BASE)
    ax.text(h("19:45:30"), 40, "nenhum boletim\nentre 19h31m50\ne 19h59m22\n\nTSE: totalização\nsuspensa das\n19h32 às 19h59",
            ha="center", fontsize=15, color=TEXTO)
    for x, y, rot, lado in [("19:03:56", 64.81, "64,81% na tela\n(o arquivo nacional\nparou aqui)", "right"),
                            ("19:31:11", 84.96, "84,96% na tela\nàs 20h04\n(o que já estava\ntotalizado às 19h31)", "right")]:
        ax.scatter([h(x)], [y], s=160, color=LULA, zorder=5)
        ax.text(h(x) - pd.Timedelta(minutes=2), y + 2, rot, ha=lado, va="bottom", fontsize=15, color=LULA)
    ax.set_xlim(h("17:00"), h("21:30"))
    ax.set_ylim(0, 102)
    ax.set_ylabel("% das seções")
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%Hh%M"))
    rodape(f, "TSE, hora de cada boletim no arquivo por seção; resposta ao protocolo 82032521133805")
    salvar(f, "g34_a_noite_do_1o_turno")


def g35_tela():
    """Os números da tela contra a soma dos boletins até aquela hora."""
    p = pd.DataFrame(R["H39"]["pontos_da_tela"])
    f = fig("O que a tela mostrou é a soma dos boletins", "Cada ponto publicado pela imprensa contra a soma das seções já totalizadas naquele instante")
    cols = ["% das seções", "totalizado até", "Flávio: dado × tela", "Lula: dado × tela"]
    xs = [0.07, 0.27, 0.48, 0.72]
    for x, c in zip(xs, cols):
        f.text(x, 0.74, c, fontsize=20, weight="bold", color=TEXTO)
    for i, r in enumerate(p.itertuples()):
        y = 0.66 - i * 0.09
        vals = [d(r.pct_secoes, 2) + "%", r.corresponde_ao_totalizado_ate[:5].replace(":", "h"),
                f"{d(r.flavio_dado, 2)} × {d(r.flavio_tela, 2)}", f"{d(r.lula_dado, 2)} × {d(r.lula_tela, 2)}"]
        for x, v in zip(xs, vals):
            f.text(x, y, v, fontsize=22, color=TEXTO)
    f.text(0.07, 0.14, "As diferenças são do arredondamento da fonte (o último ponto foi publicado com 1 casa).", fontsize=16, color=BASE)
    rodape(f, "TSE, boletim e hora de cada seção; pontos publicados pela imprensa")
    salvar(f, "g35_a_tela_e_a_soma_dos_boletins")


def g36_governador():
    t = pd.read_csv(RAIZ / "resultados/tabelas/r6_h40_uf_2026.csv", index_col=0)
    t = t[t.index != "zz"].sort_values("dlula_pontos")
    f = fig("O 2º turno para governador mudou o voto do Lula?", "Mudança do voto do Lula entre os turnos de 2026, em pontos dos votos válidos, por estado")
    ax = f.add_axes([0.07, 0.13, 0.88, 0.58])
    cores = [AMARELO if g else BASE for g in t.gov2t]
    ax.bar(range(len(t)), t.dlula_pontos, color=cores)
    ax.set_xticks(range(len(t)))
    ax.set_xticklabels([u.upper() for u in t.index], fontsize=15)
    ax.set_ylabel("pontos")
    g = R["H40"]["2026"]
    f.text(0.07, 0.765, f"Com 2º turno para governador (amarelo): mediana de +{d(g['com_2t_governador']['lula_mudou_pontos_mediana_dos_estados'], 1)} ponto  ·  "
           f"sem: +{d(g['sem_2t_governador']['lula_mudou_pontos_mediana_dos_estados'], 1)}", fontsize=19, color=TEXTO)
    rodape(f, "TSE, resultado por seção dos 2 turnos de 2026")
    salvar(f, "g36_segundo_turno_para_governador")


def g37_mesario():
    m = json.loads((RAIZ / "resultados/RODADA6_MESARIOS.json").read_text(encoding="utf-8"))
    r = m["mesario_em_2_ou_mais_municipios"]
    nome = {"BRAGANCA": "Bragança", "RIO MARIA": "Rio Maria", "DIADEMA": "Diadema", "GUARACI": "Guaraci", "ATALEIA": "Ataléia",
            "GOIANESIA": "Goianésia", "MOGI MIRIM": "Mogi Mirim", "PETROPOLIS": "Petrópolis", "JOSE BONIFACIO": "José Bonifácio",
            "SAO VICENTE": "São Vicente", "PORTO SEGURO": "Porto Seguro", "CASA NOVA": "Casa Nova", "CAMACAN": "Camacan",
            "JUAZEIRO": "Juazeiro", "ALAGOINHAS": "Alagoinhas"}
    tempo = lambda s: f"{s} s" if s < 60 else f"{round(s / 60)} min"
    lib = {}
    for c in m["casos"]:
        for l in c["lugares"]:
            lib[(c["codigo"], l["municipio"])] = l["habilitou_eleitores"]
    f = fig("O mesmo mesário em 2 cidades?", f"{n(m['secoes_lidas'])} urnas lidas nas cidades dos reels, sem as capitais; o número vira código e nunca é mostrado")
    f.text(0.05, 0.75, f"{r['codigos']} números em 2 cidades", fontsize=26, weight="bold", color=TEXTO)
    f.text(0.05, 0.69, f"liberaram eleitor nas 2: {r['atuou_em_2_ou_mais_municipios']}", fontsize=22, weight="bold", color=LULA)
    f.text(0.05, 0.64, f"liberaram numa cidade só: {r['atuou_em_1_e_so_foi_digitado_no_outro']}", fontsize=20, color=VERDE)
    f.text(0.05, 0.595, f"não liberaram ninguém: {r['nao_atuou_em_nenhum']}", fontsize=20, color=BASE)
    cols = [0.05, 0.41, 0.55, 0.70, 0.85]
    y = 0.50
    for x, t in zip(cols, ["Par do reel", "O reel diz", "O diário", "Eleitores liberados", ""]):
        f.text(x, y, t, fontsize=15, weight="bold", color=TEXTO)
    for p in m["pares_dos_reels"]:
        if not p["detalhe"]:
            continue
        y -= 0.052
        d0 = p["detalhe"][0]
        la, lb = lib.get((d0["codigo"], p["a"]), 0), lib.get((d0["codigo"], p["b"]), 0)
        f.text(cols[0], y, f"{nome[p['a']]} e {nome[p['b']]} ({p['turno']}º turno)", fontsize=15, color=TEXTO)
        f.text(cols[1], y, p["o_reel_diz"], fontsize=15, color=TEXTO)
        f.text(cols[2], y, tempo(p["menor_intervalo_s"]), fontsize=15, color=TEXTO)
        f.text(cols[3], y, f"{la} e {lb}", fontsize=15, weight="bold", color=VERDE if (la == 0 or lb == 0) else LULA)
    rodape(f, "TSE, o diário (log) de cada urna, rodada 6")
    salvar(f, "g37_mesmo_mesario_em_2_cidades")

def g38_vereditos():
    from graficos import CURTO
    texto = (RAIZ / "RELATORIO.md").read_text(encoding="utf-8")
    base = {h: v for h, _, _, v in re.findall(r"^\| (H\d\d) \| (.+?) \| (.+?) \| \*\*(.+?)\*\* \|", texto, re.M)}
    novas = {"H25": ("Campos dos Goytacazes", "Não sustentado"), "H27": ("Voto sem digital entre os turnos", "Não sustentado"),
             "H28": ("Seções da mesma escola", "Não sustentado"), "H29": ("Abstenção e ganho do Lula", "Não sustentado"),
             "H30": ("Urnas substituídas dobraram", "Não sustentado"), "H32": ("O ritmo entre os votos", "Não sustentado"),
             "H33": ("Seções abertas depois das 17h", "Não sustentado"), "H34": ("Mudança de local", "Não sustentado"),
             "H35": ("Cidades bolsonaristas", "Não sustentado"),
             "H37": ("Caderno e ata (TRE-PE, 1º turno)", "Compatível com as duas"), "H38": ("Votos de 2022 copiados", "Desmentido"),
             "H39": ("A pausa do 1º turno (TSE)", "Desmentido"),
             "H40": ("2º turno para governador", "Não sustentado"),
             "H41": ("O mesmo mesário em 2 cidades", "Desmentido"),
             "H42": ("Votos trocados no TSE (DE-PARA)", "Desmentido")}
    linhas = [(h, CURTO[h], base[h]) for h in sorted(base) if h in CURTO] + [(h, t, v) for h, (t, v) in novas.items()]
    assert len(linhas) == 39, len(linhas)
    cores = {"Desmentido": "#2E7D32", "Não sustentado": "#7CB342", "Compatível com as duas": "#F9A825", "Não testado nesta rodada": "#9E9E9E"}
    nomes = {"Desmentido": "desmentidas", "Não sustentado": "não sustentadas", "Compatível com as duas": "compatíveis com as duas", "Não testado nesta rodada": "não testadas"}
    cont = {k: sum(1 for _, _, v in linhas if v == k) for k in cores}
    f = plt.figure(figsize=(16, 9), dpi=120, facecolor=FUNDO)
    f.text(0.05, 0.95, "As 39 hipóteses, uma a uma", fontsize=32, weight="bold", color=TEXTO, va="top")
    x0 = 0.05
    for k, cor in cores.items():
        f.patches.append(plt.Rectangle((x0, 0.855), 0.014, 0.025, transform=f.transFigure, color=cor))
        t = f"{cont[k]} {nomes[k]}"
        f.text(x0 + 0.02, 0.8675, t, fontsize=15, va="center", color=TEXTO)
        x0 += 0.02 + 0.0105 * len(t) + 0.03
    for i, (h, t, v) in enumerate(linhas):
        col, lin = i // 13, i % 13
        x, y = 0.05 + col * 0.325, 0.79 - lin * 0.056
        f.patches.append(plt.Rectangle((x, y - 0.012), 0.012, 0.024, transform=f.transFigure, color=cores[v]))
        f.text(x + 0.02, y, f"{h}  {t}", fontsize=12.5, va="center", color=TEXTO,
               weight="bold" if h in ("H39", "H40", "H41", "H42") else "normal")
    rodape(f, "RELATORIO.md e docs/RODADA_4.md a docs/RODADA_6.md")
    salvar(f, "g38_as_39_hipoteses")
    return cont


if __name__ == "__main__":
    g34_noite()
    g35_tela()
    g36_governador()
    if (RAIZ / "resultados/RODADA6_MESARIOS.json").exists():
        g37_mesario()
    print(g38_vereditos())
    print("ok")
