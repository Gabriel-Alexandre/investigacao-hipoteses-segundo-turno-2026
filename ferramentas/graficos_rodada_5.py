"""Graficos 1920x1080 da rodada 5 (a resposta do TRE-PE e H38), a partir de resultados/RODADA5.json.

Uso: python ferramentas/graficos_rodada_5.py   ->  resultados/figuras/g28 a g33
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

R = json.loads((RAIZ / "resultados/RODADA5.json").read_text(encoding="utf-8"))
REPO = "github.com/Gabriel-Alexandre/investigacao-hipoteses-segundo-turno-2026"
CINZA_CLARO = "#D9D9D9"


def rodape(f, fonte):
    f.text(0.05, 0.035, f"Fonte: {fonte}. Análise com a ajuda do Claude. {REPO}", fontsize=11.5, color=BASE)


def g28_resposta():
    h = R["H37"]
    c = h["cobertura"]
    partes = [("Responderam sobre a seção\n(e-mail ou ata)", c.get("conteudo", 0) + c.get("ata", 0), VERDE),
              ("Pediram um pedido novo\n(petição ou identificação)", c.get("peticao", 0) + c.get("identificacao", 0), AMARELO),
              ("Ata só no cartório", c.get("ata_presencial", 0), BASE),
              ("\"Está no site do TSE\"", c.get("site_tse", 0), "#9E9E9E")]
    f = fig("O que o TRE-PE respondeu sobre as 41 seções", "Pedido por LAI de 21/10; resposta de 13/11, com as respostas de 20 zonas e 4 PDFs de ata")
    ax = f.add_axes([0.05, 0.42, 0.9, 0.2])
    x = 0
    for nome, v, cor in partes:
        ax.barh([0], [v], left=[x], color=cor, height=0.6)
        ax.text(x + v / 2, 0, str(v), ha="center", va="center", color="white", fontsize=30, weight="bold")
        x += v
    ax.set_xlim(0, 41)
    ax.axis("off")
    xs = 0.05
    for nome, v, cor in partes[:2]:
        w = 0.9 * v / 41
        f.text(xs + w / 2, 0.38, nome, ha="center", va="top", fontsize=15, color=TEXTO)
        xs += w
    f.text(0.95, 0.66, "1 ata só no cartório  ·  1 \"está no site do TSE\"", ha="right", va="bottom", fontsize=15, color=BASE)
    i = h["impugnacao_ou_protesto"]
    fz = h["fiscais"]
    f.text(0.05, 0.2, f"Impugnação ou protesto registrado: 0 nas {i.get('nao', 0)} seções com essa informação.", fontsize=21, color=TEXTO, weight="bold")
    f.text(0.05, 0.14, f"Fiscal de partido: {fz['secoes_com_numero']} seções com o número; em {fz['secoes_sem_fiscal']} não havia nenhum. "
           f"O PL aparece em {fz['secoes_com_fiscal_do_pl']} (Bom Conselho, {fz['fiscais_do_pl']} fiscais).", fontsize=17, color=TEXTO)
    rodape(f, "e-mail do TRE-PE de 13/11/2026 e as atas enviadas")
    salvar(f, "g28_resposta_do_tre_pe")


def g29_caderno():
    t = pd.DataFrame(R["H37"]["caderno"]["tabela"])
    t = t[t.minimo_sem_assinatura.notna() & (t.minimo_sem_assinatura > 0)].copy()
    ordem = [(101, 724), (105, 247), (105, 318), (106, 321), (106, 325)]
    t["o"] = [ordem.index((r.zona, r.secao)) for r in t.itertuples()]
    t = t.sort_values("o")
    f = fig("Caderno de votação contra o diário da urna", "Quem é liberado sem a digital tem de assinar o caderno. Onde dá para contar, faltam assinaturas")
    ax = f.add_axes([0.07, 0.2, 0.88, 0.52])
    rot = []
    for i, r in enumerate(t.itertuples()):
        ref = r.log_digital_falhou if (r.zona, r.secao) == (105, 318) else (r.tre_behb if (r.zona, r.secao) == (105, 247) else r.log_deviam_assinar)
        falta = r.minimo_sem_assinatura
        ax.bar(i, ref, color=CINZA_CLARO, width=0.6)
        ax.bar(i, falta, color=LULA, width=0.6)
        ax.text(i, ref + 3, n(ref), ha="center", fontsize=17, color=BASE)
        ax.text(i, falta + 3 if falta < 20 else falta / 2, f"{n(falta)}", ha="center", va="bottom" if falta < 20 else "center",
                fontsize=24, weight="bold", color=LULA if falta < 20 else "white")
        rot.append(f"{r.municipio.replace('Jaboatao dos Guararapes', 'Jaboatão')}\nzona {r.zona}, seção {r.secao}")
    ax.set_xticks(range(len(rot)))
    ax.set_xticklabels(rot, fontsize=14)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_ylim(0, max(t.log_deviam_assinar) * 1.15)
    f.text(0.07, 0.755, "cinza: quem precisava assinar (pelo diário da urna; em Caruaru 247, a lista do cartório)", fontsize=14, color=BASE)
    f.text(0.07, 0.725, "vermelho: o mínimo sem assinatura", fontsize=14, color=LULA)
    f.text(0.07, 0.1, f"Somando: pelo menos {n(R['H37']['caderno']['soma_minimo_sem_assinatura'])} pessoas liberadas sem a digital não têm assinatura no caderno, nessas 5 seções do 1º turno.", fontsize=17, color=TEXTO)
    rodape(f, "e-mail do TRE-PE de 13/11/2026 e logs das urnas do TSE (1º turno)")
    salvar(f, "g29_caderno_contra_a_urna")


def g30_jatauba():
    s = pd.DataFrame(R["H37"]["por_secao"])
    j = s[(s.zona == 54) & (s.secao == 185)].iloc[0]
    out = s[~((s.zona == 54) & (s.secao == 185))]
    f = fig("Jataúba: a seção mais fora do padrão de Pernambuco", "O leitor de digital não funcionou o dia inteiro, com o juiz e o promotor na seção")
    ax = f.add_axes([0.07, 0.2, 0.55, 0.52])
    v = [float(out.pct_sem_digital.median()), float(j.pct_sem_digital)]
    ax.bar(["as outras 40 seções\ndo pedido (mediana)", "Jataúba\nzona 54, seção 185"], v, color=[BASE, AMARELO], width=0.55)
    for i, x in enumerate(v):
        ax.text(i, x + 2, d(x) + "%", ha="center", fontsize=28, weight="bold")
    ax.set_ylim(0, 115)
    ax.set_yticks([])
    ax.set_title("% dos votos liberados sem a digital do eleitor", fontsize=18, color=BASE)
    tx = 0.66
    linhas = ["O que a ata diz, segundo o cartório:", "urna trocada antes de abrir", "leitor sem funcionar desde o 1º eleitor",
              "pausa das 9h08 às 9h21", "2 fiscais do PSD, juiz e promotor", "", "O que o diário da urna mostra:",
              f"{n(j.votos)} votos, só {n(j.biometrica)} pela digital", "reiniciou às 8h56 e às 9h18", "nenhum voto entre 9h08 e 9h21"]
    for k, l in enumerate(linhas):
        f.text(tx, 0.7 - k * 0.048, l, fontsize=16, color=TEXTO, weight="bold" if l.endswith(":") else "normal")
    rodape(f, "e-mail do TRE-PE de 13/11/2026 (54ª zona) e log da urna do TSE")
    salvar(f, "g30_jatauba")


def g31_secao_56():
    f = fig("Jaboatão, seção 56: a ata e a urna depois das 17h10", "A ata diz que 7 senhas foram distribuídas às 17h10. A urna registrou 16 votos depois disso")
    from hipoteses.log import ler_jez
    linhas = ler_jez((RAIZ / "dados/brutos/rodada5/11-56-log.jez").read_bytes())
    seq, cur = [], "?"
    for ln in linhas:
        if not ln.startswith("04/10/2026"):
            continue
        p = ln.split("\t")
        if len(p) < 5:
            continue
        h, m = p[0][11:19], p[4]
        if m.startswith("Aguardando digita"):
            cur = "?"
        if "[biom" in m:
            cur = "digital"
        if "Ano de nascimento digitado" in m and "igual" in m:
            cur = "ano"
        if "habilitou o eleitor" in m:
            cur = "mesario"
        if "foi computado" in m and h >= "17:10:00":
            seq.append((h, cur))
    ax = f.add_axes([0.05, 0.3, 0.9, 0.36])
    for i, (h, tp) in enumerate(seq):
        cor = VERDE if tp == "digital" else AMARELO
        ax.scatter(i, 0, s=1300, color=cor)
        ax.text(i, -0.55, h[:5], ha="center", fontsize=13, color=TEXTO, rotation=0)
    ax.set_xlim(-0.8, len(seq) - 0.2)
    ax.set_ylim(-1, 0.8)
    ax.axis("off")
    nd = sum(1 for _, tp in seq if tp == "digital")
    f.text(0.05, 0.72, f"verde: liberado pela digital do próprio eleitor ({nd})   amarelo: liberado pelo ano de nascimento ({len(seq) - nd})", fontsize=16, color=TEXTO)
    f.text(0.05, 0.18, f"Só as digitais reconhecidas pela urna depois das 17h10 já são {nd}, mais que as 7 senhas.", fontsize=18, color=TEXTO, weight="bold")
    f.text(0.05, 0.13, "A anotação da ata não fecha com a urna. Quem estava na fila, só o caderno mostra.", fontsize=18, color=TEXTO, weight="bold")
    rodape(f, "ata da seção 56 da 11ª zona (TRE-PE, 13/11/2026) e log da urna do TSE")
    salvar(f, "g31_secao_56_depois_das_17h")
    return seq


def g32_copia():
    h = R["H38"]
    f = fig("Os números de 2022 foram copiados em 2026?", "Diferença entre o voto de 2026 e o de 2022 na mesma seção: uma cópia faria um pico no zero")
    for j, (chave, nome, cor) in enumerate([("pico_lula", "Lula 2026 menos Lula 2022", LULA), ("pico_flavio", "Flávio 2026 menos Bolsonaro 2022", FLAVIO)]):
        ax = f.add_axes([0.06 + j * 0.47, 0.2, 0.42, 0.5])
        c = h[chave]["contagem_-3_a_3"]
        ks = sorted(int(k) for k in c)
        ax.bar(ks, [c[str(k)] if str(k) in c else c[k] for k in ks], color=[cor if k == 0 else CINZA_CLARO for k in ks], width=0.7)
        for k in ks:
            v = c[str(k)] if str(k) in c else c[k]
            ax.text(k, v + 150, n(v), ha="center", fontsize=12.5)
        ax.set_ylim(0, max(c.values()) * 1.18)
        ax.set_yticks([])
        ax.set_xticks(ks)
        ax.set_xticklabels([("+" if k > 0 else "") + str(k) for k in ks], fontsize=15)
        ax.set_title(nome, fontsize=17, color=BASE)
        ax.set_xlabel("votos de diferença", fontsize=14, color=BASE)
    f.text(0.06, 0.11, "Nenhum pico: o número igual aparece tanto quanto o de 1 voto a mais ou a menos, para os 2 lados.", fontsize=16, color=TEXTO)
    f.text(0.06, 0.075, f"Boletim inteiro igual ao de 2022: {h['boletim_inteiro_igual']} de {n(h['secoes_casadas_2022_2026'])} seções.", fontsize=16, color=TEXTO)
    rodape(f, "TSE, boletins por seção do 2º turno de 2022 e de 2026")
    salvar(f, "g32_copia_de_2022")


def g33_vereditos():
    from graficos import CURTO
    texto = (RAIZ / "RELATORIO.md").read_text(encoding="utf-8")
    base = {h: v for h, _, _, v in re.findall(r"^\| (H\d\d) \| (.+?) \| (.+?) \| \*\*(.+?)\*\* \|", texto, re.M)}
    novas = {"H25": ("Campos dos Goytacazes", "Não sustentado"), "H27": ("Voto sem digital entre os turnos", "Não sustentado"),
             "H28": ("Seções da mesma escola", "Não sustentado"), "H29": ("Abstenção e ganho do Lula", "Não sustentado"),
             "H30": ("Urnas substituídas dobraram", "Não sustentado"), "H32": ("O ritmo entre os votos", "Não sustentado"),
             "H33": ("Seções abertas depois das 17h", "Não sustentado"), "H34": ("Mudança de local", "Não sustentado"),
             "H35": ("Cidades bolsonaristas", "Não sustentado"),
             "H37": ("Caderno e ata (TRE-PE, 1º turno)", "Compatível com as duas"), "H38": ("Votos de 2022 copiados", "Desmentido")}
    linhas = [(h, CURTO[h], base[h]) for h in sorted(base) if h in CURTO] + [(h, t, v) for h, (t, v) in novas.items()]
    assert len(linhas) == 35, len(linhas)
    cores = {"Desmentido": "#2E7D32", "Não sustentado": "#7CB342", "Compatível com as duas": "#F9A825", "Não testado nesta rodada": "#9E9E9E"}
    nomes = {"Desmentido": "desmentidas", "Não sustentado": "não sustentadas", "Compatível com as duas": "compatíveis com as duas", "Não testado nesta rodada": "não testadas"}
    cont = {k: sum(1 for _, _, v in linhas if v == k) for k in cores}
    f = plt.figure(figsize=(16, 9), dpi=120, facecolor=FUNDO)
    f.text(0.05, 0.95, "As 35 hipóteses, uma a uma", fontsize=32, weight="bold", color=TEXTO, va="top")
    x0 = 0.05
    for k, cor in cores.items():
        f.patches.append(plt.Rectangle((x0, 0.855), 0.014, 0.025, transform=f.transFigure, color=cor))
        t = f"{cont[k]} {nomes[k]}"
        f.text(x0 + 0.02, 0.8675, t, fontsize=15, va="center", color=TEXTO)
        x0 += 0.02 + 0.0105 * len(t) + 0.03
    for i, (h, t, v) in enumerate(linhas):
        col, lin = i // 12, i % 12
        x, y = 0.05 + col * 0.325, 0.79 - lin * 0.0605
        f.patches.append(plt.Rectangle((x, y - 0.013), 0.012, 0.026, transform=f.transFigure, color=cores[v]))
        f.text(x + 0.02, y, f"{h}  {t}", fontsize=13, va="center", color=TEXTO, weight="bold" if h in ("H37", "H38") else "normal")
    rodape(f, "RELATORIO.md, docs/RODADA_4.md e docs/RODADA_5.md")
    salvar(f, "g33_as_35_hipoteses")
    return cont


if __name__ == "__main__":
    g28_resposta()
    g29_caderno()
    g30_jatauba()
    s = g31_secao_56()
    g32_copia()
    print(g33_vereditos(), len(s))
