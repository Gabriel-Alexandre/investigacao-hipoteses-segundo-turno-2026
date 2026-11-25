"""Rodada 6 (24/11/2026): a resposta do TSE sobre a pausa de 04/10 (H39), a resposta do TRE-BA (andamento do pedido, sem
linha própria), o 2º turno nos estados com e sem 2º turno para governador (H40) e o "DE-PARA" (H42). O teste do "mesmo
mesário em 2 cidades" (H41) é o rodada_6_mesarios.py.

H39 refaz a noite do 1º turno pela hora de cada boletim no arquivo público (detalhe_secao_2026.parquet, campo
recebido_tse) e pelos votos de cada seção (t1_secoes.parquet do projeto investigacao-segundo-turno-2026), e confere
contra as afirmações do TSE (a falha às 19h14 com 64,81%; a totalização suspensa das 19h32 às 19h59; a volta às 20h04
com 84,96%) e contra os pontos da tela publicados pela imprensa (apuracao-eleicoes-2026, dados/pontos-da-tela.csv).

H40 compara, por estado, a mudança do comparecimento e do voto do Lula entre os turnos de 2026 nos 6 estados com 2º turno
para governador e nos outros 21 (mais o exterior, que fica fora), com o espelho de 2022 (12 estados com 2º turno).

Saída: resultados/RODADA6.json e resultados/tabelas/r6_*.csv.
Uso: python ferramentas/rodada_6.py
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
OUTRO = RAIZ.parent / "investigacao-segundo-turno-2026" / "dados" / "derivados"
APUR = RAIZ.parent / "apuracao-eleicoes-2026" / "dados" / "pontos-da-tela.csv"
GOV = RAIZ.parent / "pesquisas-e-resultado-segundo-turno-2026" / "dados" / "derivados" / "governador.csv"
TAB = RAIZ / "resultados" / "tabelas"
CAND1 = ["lula", "flavio", "renan", "caiado", "cury", "demais", "zema"]
GOV_2T_2022 = ["al", "am", "ba", "es", "ms", "pb", "pe", "ro", "rs", "sc", "se", "sp"]  # TSE, eleições 2022
REGIAO = {**{u: "Norte" for u in ["ac", "am", "ap", "pa", "ro", "rr", "to"]},
          **{u: "Nordeste" for u in ["al", "ba", "ce", "ma", "pb", "pe", "pi", "rn", "se"]},
          **{u: "Centro-Oeste" for u in ["df", "go", "ms", "mt"]},
          **{u: "Sudeste" for u in ["es", "mg", "rj", "sp"]}, **{u: "Sul" for u in ["pr", "rs", "sc"]}}


def h39() -> dict:
    d = pd.read_parquet(RAIZ / "dados" / "derivados" / "detalhe_secao_2026.parquet",
                        columns=["uf", "municipio", "zona", "secao", "turno", "recebido_tse"])
    d = d[d.turno == "1"].copy()
    d["ts"] = pd.to_datetime(d.recebido_tse, format="%d/%m/%Y %H:%M:%S")
    t = pd.read_parquet(OUTRO / "t1_secoes.parquet")
    for c, n in (("municipio", 5), ("zona", 4), ("secao", 4)):
        t[c] = t[c].astype(str).str.zfill(n)
    m = d.merge(t[["uf", "municipio", "zona", "secao"] + CAND1], on=["uf", "municipio", "zona", "secao"], how="left")
    sem_voto = int(m.lula.isna().sum())
    m = m.fillna(0).sort_values("ts").reset_index(drop=True)
    m["val"] = m[CAND1].sum(axis=1)
    m["cv"], m["cl"], m["cf"] = m.val.cumsum(), m.lula.cumsum(), m.flavio.cumsum()
    n = len(m)

    def ate(h: str) -> dict:
        k = int((m.ts <= pd.Timestamp("2026-10-04 " + h)).sum())
        return {"hora": h, "secoes": k, "pct": round(100 * k / n, 2)}

    # a pausa no arquivo: o maior buraco sem nenhum boletim entre 19h e 21h
    noite = m[(m.ts >= "2026-10-04 19:00") & (m.ts <= "2026-10-04 21:00")].ts
    gaps = noite.diff()
    i = gaps.idxmax()
    buraco = {"de": str(m.ts[i - 1].time()), "ate": str(m.ts[i].time()), "minutos": round(gaps[i].total_seconds() / 60, 1)}
    depois = m[(m.ts >= m.ts[i]) & (m.ts < m.ts[i] + pd.Timedelta(minutes=4))]
    # todos os buracos de mais de 2 minutos entre 17h e 23h (a resposta do TSE só fala de um)
    noite2 = m[(m.ts >= "2026-10-04 17:00") & (m.ts <= "2026-10-04 23:00")].ts.reset_index(drop=True)
    g2 = noite2.diff()
    buracos = [{"de": str(noite2[j - 1].time()), "ate": str(noite2[j].time()), "minutos": round(g2[j].total_seconds() / 60, 1),
                "pct_antes": round(100 * int((m.ts <= noite2[j - 1]).sum()) / n, 2)}
               for j in g2[g2 > pd.Timedelta(minutes=2)].index]
    ritmo_antes = int(((m.ts >= "2026-10-04 19:25") & (m.ts < "2026-10-04 19:31")).sum() / 6)
    ritmo_depois = int(((m.ts >= "2026-10-04 20:04") & (m.ts < "2026-10-04 20:10")).sum() / 6)

    tela = pd.read_csv(APUR)
    pontos = []
    for p in tela.itertuples():
        if p.pct_meia_largura > 0.01:  # só os pontos com 2 casas (as fontes que publicaram o percentual exato)
            continue
        k = int(round(p.pct_secoes / 100 * n)) - 1
        r = m.iloc[k]
        pontos.append({"ponto": p.ponto, "hora_na_tela": p.hora_publicada_brt, "pct_secoes": p.pct_secoes,
                       "corresponde_ao_totalizado_ate": str(r.ts.time()),
                       "flavio_dado": round(100 * r.cf / r.cv, 2), "flavio_tela": p.flavio_pct,
                       "lula_dado": round(100 * r.cl / r.cv, 2), "lula_tela": p.lula_pct})
    # quem entrou no "salto": do 64,81% ao 84,96%
    k1, k2 = int(round(0.6481 * n)), int(round(0.8496 * n))
    salto = m.iloc[k1:k2]
    antes = m.iloc[:k1]
    reg = lambda x: (x.uf.map(REGIAO).fillna("Exterior").value_counts(normalize=True) * 100).round(1).to_dict()
    return {
        "secoes_1t": n, "secoes_sem_voto_casado": sem_voto,
        "ate": [ate(h) for h in ("19:14:00", "19:31:50", "19:59:22", "20:04:00")],
        "buraco_no_arquivo": buraco,
        "todos_os_buracos_de_mais_de_2_min": buracos,
        "o_que_a_resposta_nao_explica": ["os 2 buracos menores (18h01 a 18h09 e 18h50 a 18h54)",
                                         "o item 2 do pedido: o que o campo de hora do arquivo público registra (a resposta não diz; o dado mostra que ele para quando a totalização para)"],
        "boletins_nos_4_min_depois_do_buraco": int(len(depois)),
        "ritmo_por_minuto_antes_19h25_19h31": ritmo_antes, "ritmo_por_minuto_20h04_20h10": ritmo_depois,
        "pontos_da_tela": pontos,
        "salto_64_81_a_84_96": {"secoes": int(len(salto)), "das": str(salto.ts.min().time()), "ate": str(salto.ts.max().time()),
                                "lula_pct_no_salto": round(100 * salto.lula.sum() / salto.val.sum(), 2),
                                "flavio_pct_no_salto": round(100 * salto.flavio.sum() / salto.val.sum(), 2),
                                "regiao_no_salto_pct": reg(salto), "regiao_antes_pct": reg(antes)},
        "afirmacoes_do_tse": {"falha_arquivo_nacional": "~19h14, com 64,81%", "totalizacao_suspensa": "19h32 a 19h59",
                              "volta_do_arquivo_nacional": "20h04, com 84,96%"},
    }


def por_uf(t1: pd.DataFrame, t2: pd.DataFrame, cols1: dict, cols2: dict) -> pd.DataFrame:
    a = t1.groupby("uf").agg(aptos1=("aptos", "sum"), comp1=("comparecimento", "sum"), **cols1)
    b = t2.groupby("uf").agg(aptos2=("aptos", "sum"), comp2=("comparecimento", "sum"), **cols2)
    u = a.join(b)
    u["dcomp_pontos"] = 100 * (u.comp2 / u.aptos2 - u.comp1 / u.aptos1)
    u["lula1_pct"] = 100 * u.lula1 / u.val1
    u["lula2_pct"] = 100 * u.lula2 / u.val2
    u["dlula_pontos"] = u.lula2_pct - u.lula1_pct
    return u


def resumo_grupos(u: pd.DataFrame, com: list[str]) -> dict:
    u = u[u.index != "zz"].copy()
    u["gov2t"] = u.index.isin(com)
    out = {}
    for k, g in u.groupby("gov2t"):
        out["com_2t_governador" if k else "sem_2t_governador"] = {
            "estados": sorted(g.index.tolist()),
            "comparecimento_mudou_pontos": round(100 * (g.comp2.sum() / g.aptos2.sum() - g.comp1.sum() / g.aptos1.sum()), 2),
            "lula_mudou_pontos_mediana_dos_estados": round(float(g.dlula_pontos.median()), 2),
            "lula_mudou_pontos_somado": round(100 * (g.lula2.sum() / g.val2.sum() - g.lula1.sum() / g.val1.sum()), 2),
        }
    # dentro da mesma região, para não comparar Norte com Sul
    reg = []
    for r, g in u.groupby(u.index.map(REGIAO)):
        if g.gov2t.any() and (~g.gov2t).any():
            reg.append({"regiao": r, "com": sorted(g[g.gov2t].index), "sem": sorted(g[~g.gov2t].index),
                        "dcomp_com": round(float(g[g.gov2t].dcomp_pontos.median()), 2), "dcomp_sem": round(float(g[~g.gov2t].dcomp_pontos.median()), 2),
                        "dlula_com": round(float(g[g.gov2t].dlula_pontos.median()), 2), "dlula_sem": round(float(g[~g.gov2t].dlula_pontos.median()), 2)})
    out["dentro_da_regiao"] = reg
    return out


def h40() -> dict:
    gov = pd.read_csv(GOV)
    com26 = sorted(gov[(gov.turno == 1) & (gov.situacao == "2º turno")].uf.unique())
    t1 = pd.read_parquet(OUTRO / "t1_secoes.parquet")
    t2 = pd.read_parquet(OUTRO / "t2_secoes.parquet")
    t1["val"] = t1[CAND1].sum(axis=1)
    t2["val"] = t2[["bu_lula", "bu_flavio"]].sum(axis=1)
    u26 = por_uf(t1, t2, {"val1": ("val", "sum"), "lula1": ("lula", "sum")}, {"val2": ("val", "sum"), "lula2": ("bu_lula", "sum")})
    a = pd.read_parquet(OUTRO / "s2022_t1.parquet")
    b = pd.read_parquet(OUTRO / "s2022_t2.parquet")
    a["uf"], b["uf"] = a.uf.str.lower(), b.uf.str.lower()
    a["val"] = a[["lula", "bolsonaro", "ciro", "tebet", "outros"]].sum(axis=1)
    b["val"] = b[["lula", "bolsonaro"]].sum(axis=1)
    u22 = por_uf(a, b, {"val1": ("val", "sum"), "lula1": ("lula", "sum")}, {"val2": ("val", "sum"), "lula2": ("lula", "sum")})
    TAB.mkdir(parents=True, exist_ok=True)
    u26.assign(gov2t=u26.index.isin(com26)).round(3).to_csv(TAB / "r6_h40_uf_2026.csv")
    u22.assign(gov2t=u22.index.isin(GOV_2T_2022)).round(3).to_csv(TAB / "r6_h40_uf_2022.csv")
    return {"2026": resumo_grupos(u26, com26), "2022": resumo_grupos(u22, GOV_2T_2022),
            "fonte_2t_governador_2026": "pesquisas-e-resultado-segundo-turno-2026, dados/derivados/governador.csv (TSE)",
            "fonte_2t_governador_2022": "TSE, eleições 2022: AL, AM, BA, ES, MS, PB, PE, RO, RS, SC, SE e SP"}


def tre_ba() -> dict:
    return {"protocolo": "82034321135124", "resposta": "2026-11-24 13:11",
            "secoes_pedidas": 26, "itens_negados": "1 a 5 na forma de conferência (caderno contra o log, ocorrências, fiscais)",
            "base_da_negativa": "Lei 12.527/2011 e Res. CNJ 215/2015, art. 12, III (trabalho adicional de análise, interpretação ou consolidação)",
            "pedido_alternativo": "cópia das atas: 'será avaliada a viabilidade de atendimento pelas unidades competentes'",
            "recurso": "10 dias a contar de 24/11/2026 (até 04/12/2026), pela opção de recurso do próprio e-mail",
            "comparacao_tre_pe": "o TRE-PE respondeu 27 de 41 seções e mandou 4 PDFs de ata (rodada 5)"}


def h42() -> dict:
    """O "DE-PARA": os votos teriam sido trocados ao chegar no TSE. Se fosse assim, o total oficial não seria a soma dos
    boletins de cada seção, que são os assinados pela urna e os mesmos do papel afixado na seção."""
    t2 = pd.read_parquet(OUTRO / "t2_secoes.parquet")
    for c, w in (("municipio", 5), ("zona", 4), ("secao", 4)):
        t2[c] = t2[c].astype(str).str.zfill(w)
    det = pd.read_parquet(RAIZ / "dados" / "derivados" / "detalhe_secao_2026.parquet")
    det = det[det.turno == "2"]
    abr = pd.read_csv(RAIZ.parent / "pesquisas-e-resultado-segundo-turno-2026" / "dados" / "derivados" / "presidente_abrangencia.csv")
    br = abr[(abr.turno == 2) & (abr.abr == "br")].iloc[0]
    sem = t2[t2.bu_lula.isna()][["uf", "municipio", "zona", "secao"]].merge(det, on=["uf", "municipio", "zona", "secao"], how="left")
    lula, flavio = int(t2.bu_lula.sum()), int(t2.bu_flavio.sum())
    ok = t2.dropna(subset=["rdv_lula", "bu_lula"])
    return {"secoes": int(len(t2)),
            "validos_soma_de_todas_as_secoes": int(det.nominais.sum()), "validos_oficial": int(br.validos),
            "soma_igual_ao_oficial": int(det.nominais.sum()) == int(br.validos),
            "boletins_eletronicos_lula": lula, "boletins_eletronicos_flavio": flavio,
            "oficial_lula": int(br.lula), "oficial_flavio": int(br.flavio),
            "secoes_sem_boletim_eletronico": {"total": int(len(sem)), "por_origem": sem.origem.value_counts().to_dict(),
                                              "votos_validos": int(sem.nominais.sum())},
            "diferenca_lula_mais_flavio": int(br.lula + br.flavio) - (lula + flavio),
            "lula_pct_boletins": round(100 * lula / (lula + flavio), 2),
            "rdv_igual_ao_boletim_secoes": int(((ok.rdv_lula == ok.bu_lula) & (ok.rdv_flavio == ok.bu_flavio)).sum()),
            "secoes_com_rdv": int(len(ok))}


def main() -> None:
    r = {"H39": h39(), "TRE_BA": tre_ba(), "H40": h40(), "H42": h42()}
    (RAIZ / "resultados" / "RODADA6.json").write_text(json.dumps(r, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(json.dumps(r, ensure_ascii=False, indent=1, default=str)[:6000])


if __name__ == "__main__":
    main()
