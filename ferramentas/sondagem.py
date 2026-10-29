"""Rodada 0 (sondagem): o que as tabelas por seção do projeto do video 16 ja dizem sobre as hipoteses
novas, ANTES de qualquer teste com regra. Serve para saber o que da para testar e com que dado; nenhum
numero daqui e veredito. Fonte: dados/copias/ (copia com sha256 em dados/MANIFESTO_COPIAS.json).

Uso: python ferramentas/sondagem.py   ->  resultados/SONDAGEM.json
"""
import json
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
C = RAIZ / "dados" / "copias"
CHAVE = ["uf", "municipio", "zona", "secao"]
# hora local -> hora de Brasilia (a votacao de 2026 seguiu o horario de Brasilia em todo o pais)
FUSO = {"ac": 2, "am": 1, "ro": 1, "rr": 1, "mt": 1, "ms": 1}


def pct(a, b):
    return round(100 * a / b, 2) if b else None


def main():
    t2 = pd.read_parquet(C / "t2_secoes.parquet")
    t1 = pd.read_parquet(C / "t1_secoes.parquet")
    s22 = pd.read_parquet(C / "s2022_t2.parquet")
    br = t2[t2.uf != "zz"].copy()
    out = {"secoes_t2": int(len(t2)), "secoes_t2_brasil": int(len(br)),
           "situacao": {k: int(v) for k, v in t2.situacao.value_counts().items()}}

    # H01 o relatorio pericial: urnas encerradas ate 17h contra depois
    en = pd.to_datetime(br.encerramento, errors="coerce")
    br["en_bsb"] = en.dt.hour + en.dt.minute / 60 + en.dt.second / 3600 + br.uf.map(FUSO).fillna(0)
    cortes = {}
    for rot, h in [("17h00", 17.0), ("17h01", 17 + 1 / 60), ("17h05", 17 + 5 / 60), ("17h15", 17.25), ("17h30", 17.5), ("19h00", 19.0)]:
        lado = {}
        for nome, g in [("ate", br[br.en_bsb <= h]), ("depois", br[br.en_bsb > h])]:
            L, F = int(g.bu_lula.sum()), int(g.bu_flavio.sum())
            lado[nome] = {"secoes": int(len(g)), "lula_pct_nominais": pct(L, L + F), "margem_lula": L - F,
                          "comparecimento": int(g.comparecimento.sum()),
                          "votos_depois_17h_pelo_log": int(g.log_votos_depois_17h.fillna(0).sum())}
        cortes[rot] = lado
    out["H01_encerramento"] = {"cortes_hora_de_brasilia": cortes,
                               "votos_depois_17h_pelo_log_brasil": int(br.log_votos_depois_17h.fillna(0).sum()),
                               "votos_depois_17h_pelo_log_com_exterior": int(t2.log_votos_depois_17h.fillna(0).sum()),
                               "votos_depois_19h_pelo_log": int(br.log_votos_depois_19h.fillna(0).sum()),
                               "secoes_sem_log": int(br.log_votos.isna().sum())}

    # H03 / H04 liberacao sem digital do eleitor
    out["H04_liberacao"] = {k: int(br[c].fillna(0).sum()) for k, c in
                            [("biometrica", "log_biometrica"), ("manual_mesario", "log_manual_mesario"),
                             ("manual_sem_digital", "log_manual_sem_digital"), ("manuais_depois_17h", "log_manuais_depois_17h")]}

    # H02 unanimidade
    v = br.bu_lula + br.bu_flavio
    m = br.merge(t1, on=CHAVE, suffixes=("", "_t1"), how="left")
    z = m[(m.bu_flavio == 0) & (m.bu_lula > 0)]
    s22b = s22[s22.uf.str.lower() != "zz"]
    out["H02_unanimidade"] = {
        "secoes_mais_de_90_lula": int((br.bu_lula / v > 0.9).sum()), "secoes_mais_de_90_flavio": int((br.bu_flavio / v > 0.9).sum()),
        "secoes_zero_flavio": int(len(z)), "votos_lula_nelas": int(z.bu_lula.sum()),
        "zero_flavio_por_uf": {k: int(x) for k, x in z.uf.value_counts().items()},
        "zero_flavio_casadas_no_1t": int(z.flavio.notna().sum()), "zero_flavio_com_flavio_no_1t": int((z.flavio >= 1).sum()),
        "votos_flavio_no_1t_nessas": int(z.flavio.fillna(0).sum()),
        "secoes_zero_lula": int(((br.bu_lula == 0) & (br.bu_flavio > 0)).sum()),
        "2022_t2_zero_bolsonaro": int(((s22b.bolsonaro == 0) & (s22b.lula > 0)).sum()),
        "2022_t2_zero_lula": int(((s22b.lula == 0) & (s22b.bolsonaro > 0)).sum())}

    # H05 "ja tinham votado por mim": o aviso da urna "O eleitor identificado ja votou"
    out["H05_ja_votou"] = {"avisos": int(br.log_ja_votou.fillna(0).sum()), "secoes_com_aviso": int((br.log_ja_votou > 0).sum())}

    # H06 resultados repetidos entre secoes
    inst = br[br.situacao != "Nao instalada"]
    g = inst.groupby(["bu_lula", "bu_flavio"]).size()
    grandes = inst[(inst.bu_lula >= 300) & (inst.bu_flavio >= 300)].groupby(["bu_lula", "bu_flavio"]).size()
    out["H06_repetidos"] = {"pares_que_se_repetem": int((g >= 2).sum()), "secoes_nesses_pares": int(g[g >= 2].sum()),
                            "pares_repetidos_com_os_dois_acima_de_300": int((grandes >= 2).sum())}

    # H07 / H10 quem perdeu voto do 1o para o 2o turno
    uf = m.groupby("uf")[["bu_flavio", "flavio", "bu_lula", "lula"]].sum()
    out["H07_perdeu_voto"] = {"ufs_onde_flavio_caiu": {k: int(r.bu_flavio - r.flavio) for k, r in uf.iterrows() if r.bu_flavio < r.flavio},
                              "ufs_onde_lula_caiu": {k: int(r.bu_lula - r.lula) for k, r in uf.iterrows() if r.bu_lula < r.lula},
                              "secoes_flavio_caiu": int((m.bu_flavio < m.flavio).sum()), "secoes_lula_caiu": int((m.bu_lula < m.lula).sum())}

    # H17 urna de contingencia
    out["H17_contingencia"] = {"secoes_com_urna_trocada_no_log": int(br.log_contingencia.fillna(0).astype(int).gt(0).sum())}

    (RAIZ / "resultados").mkdir(exist_ok=True)
    (RAIZ / "resultados" / "SONDAGEM.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
