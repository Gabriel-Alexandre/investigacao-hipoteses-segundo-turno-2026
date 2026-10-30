"""Rodada 3 (30/10/2026), pelo retorno do autor ao roteiro:

  R3a  as "urnas idênticas" (mensagem de um seguidor): seções com 100% para um candidato e 0 para o outro, e seções com
       exatamente o mesmo número de votos e o mesmo percentual. Amplia a H07 e a H08: o boletim inteiro (Lula, Flávio,
       branco, nulo) e não só o placar dos 2, dentro do mesmo local e do mesmo município, contra o acaso, 2022 e 2018.
  R3b  a curva "programada" (H24): com muito zoom, a linha do candidato da direita parece subir um pouco e ser penalizada,
       num ritmo de programa. Faz a curva de 2026, 2022 e 2018 na ordem em que as seções entraram, compara com a curva que
       sairia se cada seção repetisse o próprio 1º turno, e mede o que um programa deixaria: passos que não vêm da
       composição, ritmo fixo, e um desconto que cresce com a ordem de chegada dentro da mesma zona.

Limite: o boletim público de 2018 não traz a hora de chegada (DT_BU_RECEBIDO existe em 2022 e 2026). Em 2018 a ordem é a
hora de encerramento da urna, em horário de Brasília; 2022 e 2026 são medidos também por essa ordem, para comparar igual.

Fontes: dados/copias (2026 e 2022), dados/brutos/bweb2022 (hora de chegada de 2022) e dados/copias/historico2018.
Saída: resultados/RODADA3.json, resultados/tabelas/r3_*.csv
"""
from __future__ import annotations

import hashlib
import io
import json
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.signal import find_peaks

R = Path(__file__).resolve().parents[1]
C = R / "dados/copias"
D = R / "dados/derivados"
T = R / "resultados/tabelas"
B22 = R / "dados/brutos/bweb2022"
H18 = C / "historico2018"
ORIGEM18 = R.parent / "apuracao-eleicoes-2026/dados/derivados/historico"
FONTES = R.parent / "apuracao-eleicoes-2026/dados/fontes-historicas.json"
MAN = R / "dados/MANIFESTO_RODADA3.json"
RNG = np.random.default_rng(20261030)
BIN = 100
UFS_FUSO = {"AC": -2, "AM": -1, "RO": -1, "RR": -1, "MS": -1, "MT": -1, "FN": 1}
UA = {"User-Agent": "investigacao-hipoteses-segundo-turno-2026 (github.com/Gabriel-Alexandre)"}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def preparar():
    """Baixa o boletim de 2022 (hora de chegada), copia o histórico de 2018 e grava os hashes."""
    man = json.loads(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    B22.mkdir(parents=True, exist_ok=True)
    for _, url in json.loads(FONTES.read_text(encoding="utf-8"))["2022-2"]:
        p = B22 / url.rsplit("/", 1)[1]
        if not p.exists():
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as r:
                p.write_bytes(r.read())
        man[f"bweb2022/{p.name}"] = {"url": url, "sha256": sha(p), "bytes": p.stat().st_size}
    H18.mkdir(parents=True, exist_ok=True)
    for t in ("1", "2"):
        for f in ORIGEM18.glob(f"2018-{t}-*.parquet"):
            alvo = H18 / f.name
            if not alvo.exists():
                shutil.copy2(f, alvo)
            man[f"historico2018/{f.name}"] = {"origem": "apuracao-eleicoes-2026/dados/derivados/historico", "sha256": sha(alvo)}
    MAN.write_text(json.dumps(man, indent=1, sort_keys=True), encoding="utf-8")


def texto(d, c):
    d[c] = d[c].astype(str).str.lstrip("0").replace("", "0")


def chave(d):
    d["uf"] = d.uf.astype(str).str.upper()
    for c in ("municipio", "zona", "secao"):
        texto(d, c)
    return d


def carrega_2026():
    d = pd.read_parquet(C / "t2_secoes.parquet", columns=["uf", "municipio", "zona", "secao", "recebido", "encerramento", "bu_lula", "bu_flavio", "bu_branco", "bu_nulo"])
    d = chave(d)
    for c in ("bu_lula", "bu_flavio", "bu_branco", "bu_nulo"):
        d[c] = pd.to_numeric(d[c], errors="coerce").fillna(0)
    d = d.rename(columns={"bu_lula": "esq", "bu_flavio": "dir", "bu_branco": "branco", "bu_nulo": "nulo"})
    d["rec"] = pd.to_datetime(d.recebido, errors="coerce")
    d["enc"] = pd.to_datetime(d.encerramento, errors="coerce")
    t = pd.read_parquet(C / "t1_secoes.parquet", columns=["uf", "municipio", "zona", "secao", "lula", "flavio", "branco", "nulo"])
    t = chave(t)
    for c in ("lula", "flavio", "branco", "nulo"):
        t[c] = pd.to_numeric(t[c], errors="coerce")
    t = t.rename(columns={"lula": "esq1", "flavio": "dir1", "branco": "branco1", "nulo": "nulo1"})
    return d[d.uf != "ZZ"].merge(t, on=["uf", "municipio", "zona", "secao"], how="left")


def carrega_2022():
    partes = []
    for z in sorted(B22.glob("bweb_2t_*.zip")):
        zz = zipfile.ZipFile(z)
        nome = next(n for n in zz.namelist() if n.lower().endswith(".csv"))
        with zz.open(nome) as h:
            d = pd.read_csv(io.TextIOWrapper(h, encoding="latin1"), sep=";", dtype=str,
                            usecols=["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "CD_CARGO_PERGUNTA", "DT_BU_RECEBIDO", "DT_ENCERRAMENTO", "NR_VOTAVEL", "QT_VOTOS"])
        d = d[d.CD_CARGO_PERGUNTA == "1"]
        d["v"] = pd.to_numeric(d.QT_VOTOS, errors="coerce").fillna(0)
        k = ["SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "DT_BU_RECEBIDO", "DT_ENCERRAMENTO"]
        p = d[d.NR_VOTAVEL.isin(["13", "22", "95", "96"])].pivot_table(index=k, columns="NR_VOTAVEL", values="v", aggfunc="sum").fillna(0).reset_index()
        partes.append(p.rename(columns={"13": "esq", "22": "dir", "95": "branco", "96": "nulo"}))
    d = pd.concat(partes, ignore_index=True).rename(columns={"SG_UF": "uf", "CD_MUNICIPIO": "municipio", "NR_ZONA": "zona", "NR_SECAO": "secao"})
    d = chave(d)
    for c in ("branco", "nulo"):
        if c not in d:
            d[c] = 0.0
    d["rec"] = pd.to_datetime(d.DT_BU_RECEBIDO, dayfirst=True, errors="coerce")
    d["enc"] = pd.to_datetime(d.DT_ENCERRAMENTO, dayfirst=True, errors="coerce")
    t = pd.read_parquet(C / "s2022_t1.parquet")
    t = chave(t).rename(columns={"lula": "esq1", "bolsonaro": "dir1", "branco": "branco1", "nulo": "nulo1"})
    return d[d.uf != "ZZ"].merge(t[["uf", "municipio", "zona", "secao", "esq1", "dir1", "branco1", "nulo1"]], on=["uf", "municipio", "zona", "secao"], how="left")


def le_2018(t):
    v = pd.concat(pd.read_parquet(f) for f in sorted(H18.glob(f"2018-{t}-*-votos.parquet")))
    v = v[v.cargo.astype(str) == "1"]
    v["numero"] = v.numero.astype(str)
    p = v[v.numero.isin(["13", "17", "95", "96"])].pivot_table(index=["uf", "mun", "zona", "secao"], columns="numero", values="votos", aggfunc="sum").fillna(0).reset_index()
    return p.rename(columns={"mun": "municipio", "13": "esq", "17": "dir", "95": "branco", "96": "nulo"})


def carrega_2018():
    d = chave(le_2018("2"))
    s = pd.concat(pd.read_parquet(f, columns=["uf", "mun", "zona", "secao", "encerramento"]) for f in sorted(H18.glob("2018-2-*-secoes.parquet")))
    s = chave(s.rename(columns={"mun": "municipio"}))
    s["enc"] = pd.to_datetime(s.encerramento, errors="coerce")
    s["enc"] = s.enc - pd.to_timedelta(s.uf.map(UFS_FUSO).fillna(0), unit="h")  # hora local para Brasília
    d = d.merge(s[["uf", "municipio", "zona", "secao", "enc"]], on=["uf", "municipio", "zona", "secao"], how="left")
    t = chave(le_2018("1")).rename(columns={"esq": "esq1", "dir": "dir1", "branco": "branco1", "nulo": "nulo1"})
    d = d.merge(t, on=["uf", "municipio", "zona", "secao"], how="left")
    d["rec"] = pd.NaT
    return d[d.uf != "ZZ"]


def zera_1o_turno(d):
    """Candidato sem voto na seção aparece vazio na tabela do 1º turno: é 0, desde que a seção exista lá."""
    t = ["esq1", "dir1", "branco1", "nulo1"]
    tem = d[t].notna().any(axis=1)
    for c in t:
        d.loc[tem, c] = d.loc[tem, c].fillna(0)
    return d


def curvas(d, ordem):
    """Curva real e curva prevista (cada seção repete o próprio 1º turno, mais a mudança do país), na ordem dada."""
    s = d.dropna(subset=[ordem]).sort_values([ordem, "uf", "municipio", "zona", "secao"]).reset_index(drop=True)
    tot = (s.esq + s.dir).to_numpy(float)
    p1 = (s.esq1 / (s.esq1 + s.dir1)).to_numpy(float)
    medio = np.nansum(p1 * tot) / np.nansum(np.where(np.isnan(p1), 0, tot))
    p1 = np.where(np.isnan(p1), medio, p1)
    delta = s.esq.sum() / tot.sum() - (p1 * tot).sum() / tot.sum()
    pe = np.clip(p1 + delta, 0, 1) * tot
    dir_real, dir_prev = s.dir.to_numpy(float), tot - pe
    real = np.cumsum(dir_real) / np.maximum(np.cumsum(tot), 1) * 100
    prev = np.cumsum(dir_prev) / np.maximum(np.cumsum(tot), 1) * 100
    return s, tot, dir_real, dir_prev, real, prev


def medidas(d, ordem):
    s, tot, dr, dp, real, prev = curvas(d, ordem)
    n = len(s)
    i1 = n // 100
    b = np.arange(i1, n, BIN)
    rb, pb = real[b], prev[b]
    inc_r, inc_p = np.diff(rb), np.diff(pb)
    ac = lambda x: float(np.corrcoef(x[:-1], x[1:])[0, 1])
    res = {"secoes": int(n), "corr_curvas": round(float(np.corrcoef(real[i1:], prev[i1:])[0, 1]), 4),
           "diferenca_media_pontos": round(float(np.abs(real[i1:] - prev[i1:]).mean()), 3),
           "corr_dos_passos_a_cada_100_secoes": round(float(np.corrcoef(inc_r, inc_p)[0, 1]), 3),
           "passos_em_que_a_linha_desce_pct": round(float((inc_r < 0).mean() * 100), 1),
           "passos_em_que_a_prevista_desce_pct": round(float((inc_p < 0).mean() * 100), 1),
           "autocorrelacao_dos_passos_real": round(ac(inc_r), 3), "autocorrelacao_dos_passos_prevista": round(ac(inc_p), 3)}
    # sem a composição: o que sobra entre a real e a prevista
    res["parte_dos_passos_explicada_pela_composicao_pct"] = round(float(np.corrcoef(inc_r, inc_p)[0, 1] ** 2 * 100), 1)
    # ritmo: vales na linha sem a tendência, e o quanto o intervalo entre eles é regular (0 = relógio, 1 = ao acaso)
    rt = rb - pd.Series(rb).rolling(101, center=True, min_periods=1).mean().to_numpy()
    pt = pb - pd.Series(pb).rolling(101, center=True, min_periods=1).mean().to_numpy()
    for nome, x in (("real", rt), ("prevista", pt)):
        val, _ = find_peaks(-x, prominence=np.std(x) * 0.5)
        iv = np.diff(val)
        res[f"vales_{nome}"] = int(len(val))
        res[f"regularidade_dos_vales_{nome}_cv"] = round(float(iv.std() / iv.mean()), 2) if len(iv) > 1 else None
    # ritmo fixo: o pico mais forte do espectro dos passos, contra os mesmos passos em ordem sorteada
    x = inc_r - inc_r.mean()
    esp = np.abs(np.fft.rfft(x))[1:] ** 2
    nul = []
    for _ in range(200):
        y = RNG.permutation(x)
        nul.append((np.abs(np.fft.rfft(y))[1:] ** 2).max())
    fre = np.fft.rfftfreq(len(x))[1:]
    topo = int(esp.argmax())
    res["pico_do_espectro_periodo_secoes"] = int(round(BIN / fre[topo]))
    res["pico_do_espectro_parte_da_variancia_pct"] = round(float(esp[topo] / esp.sum() * 100), 2)
    resid_p = np.abs(np.fft.rfft(inc_p - inc_p.mean()))[1:] ** 2
    res["na_prevista_pico_no_mesmo_periodo_parte_da_variancia_pct"] = round(float(resid_p[topo] / resid_p.sum() * 100), 2)
    # desconto na ordem de chegada: dentro da mesma zona, a seção que entra depois perde mais que a que entra antes?
    x = pd.DataFrame({"z": s.uf + s.municipio + s.zona, "o": np.arange(n), "r": np.where(tot > 0, (dr - dp) / np.maximum(tot, 1), np.nan), "t": tot})
    x = x[x.t >= 30].dropna()
    x["o_z"] = x.o - x.groupby("z").o.transform("mean")
    x["r_z"] = x.r - x.groupby("z").r.transform("mean")
    x = x[x.groupby("z").o.transform("size") >= 5]
    res["na_mesma_zona_corr_ordem_x_diferenca_da_prevista"] = round(float(np.corrcoef(x.o_z, x.r_z)[0, 1]), 4)
    res["na_mesma_zona_secoes"] = int(len(x))
    # a soma da diferença ao longo da noite (votos): um desconto de programa cresceria sem parar
    acum = np.cumsum(dr - dp)
    res["maior_soma_da_diferenca_votos"] = int(np.abs(acum).max())
    res["soma_da_diferenca_na_metade_votos"] = int(acum[n // 2])
    return res


def amostras_de_zoom(d, ordem, ano):
    """Grava a curva inteira e os trechos de zoom para os gráficos."""
    s, tot, dr, dp, real, prev = curvas(d, ordem)
    n = len(s)
    fra = np.arange(n) / n * 100
    passo = max(n // 3000, 1)
    pd.DataFrame({"pct_secoes": fra[::passo].round(3), "real": real[::passo].round(4), "prevista": prev[::passo].round(4)}).to_csv(T / f"r3_curva_{ano}_{ordem}.csv", index=False)
    c = int(n * 0.55)
    for nome, m in (("zoom1", 0.05), ("zoom2", 0.005)):
        a, b = c, c + int(n * m)
        pd.DataFrame({"pct_secoes": fra[a:b].round(4), "real": real[a:b].round(5), "prevista": prev[a:b].round(5)}).to_csv(T / f"r3_{nome}_{ano}_{ordem}.csv", index=False)


def versoes_ao_vivo():
    """Os totais na tela, nas versões nacionais gravadas ao vivo em 2026."""
    c = pd.read_csv(T / "h17_curva_nacional.csv")
    c = c[c.pst >= 1]
    pc = c.flavio / (c.lula + c.flavio) * 100
    d = pc.diff().dropna()
    return {"versoes_depois_de_1pct": int(len(c)), "vezes_que_o_total_de_votos_do_flavio_caiu": int((c.flavio.diff() < 0).sum()),
            "vezes_que_o_total_de_votos_do_lula_caiu": int((c.lula.diff() < 0).sum()),
            "vezes_que_a_porcentagem_do_flavio_caiu": int((d < 0).sum()), "vezes_que_a_porcentagem_do_flavio_subiu": int((d > 0).sum()),
            "maior_queda_da_porcentagem_em_uma_versao_pontos": round(float(-d.min()), 3)}


def identicas(d, ano):
    """R3a: 100% para um, e boletins iguais, contra o que o próprio 1º turno de cada seção produziria por acaso."""
    x = d[(d.esq + d.dir) > 0].copy()
    x["nom"] = (x.esq + x.dir).astype(int)
    so_esq, so_dir = x[(x.dir == 0)], x[(x.esq == 0)]
    res = {"secoes": int(len(x)), "brancos_e_nulos_por_secao": round(float((x.branco + x.nulo).mean()), 2),
           "secoes_sem_1o_turno": int(x.esq1.isna().sum()) if "esq1" in x else None,
           "sem_voto_da_direita": int(len(so_esq)), "sem_voto_da_esquerda": int(len(so_dir)),
           "sem_voto_da_direita_nem_branco_nem_nulo": int(((x.dir == 0) & (x.branco == 0) & (x.nulo == 0)).sum()),
           "sem_voto_da_esquerda_nem_branco_nem_nulo": int(((x.esq == 0) & (x.branco == 0) & (x.nulo == 0)).sum()),
           "sem_voto_da_direita_com_100_nominais_ou_mais": int((so_esq.nom >= 100).sum())}
    if "dir1" in x:
        ja = so_esq.dir1.dropna()
        res["das_sem_voto_da_direita_ja_tinham_ate_5_no_1o_turno_pct"] = round(float((ja <= 5).mean() * 100), 1)
    cols = ["esq", "dir", "branco", "nulo"]
    x[cols] = x[cols].astype(int)
    g = x.groupby(cols).size()
    res["boletins_inteiros_que_se_repetem"] = int((g >= 2).sum())
    res["secoes_nesses_boletins"] = int(g[g >= 2].sum())
    alto = x[(x.esq >= 100) & (x.dir >= 100)]
    res["boletins_inteiros_repetidos_com_os_2_acima_de_100"] = int((alto.groupby(cols).size() >= 2).sum())
    res["maior_comparecimento_num_boletim_repetido"] = int((x.set_index(cols).index.to_frame().sum(axis=1)[x.set_index(cols).index.duplicated(keep=False)]).max())
    # o mesmo boletim inteiro na mesma cidade e na mesma zona
    res["boletins_iguais_no_mesmo_municipio"] = int((x.groupby(["uf", "municipio"] + cols).size() >= 2).sum())
    res["boletins_iguais_na_mesma_zona"] = int((x.groupby(["uf", "municipio", "zona"] + cols).size() >= 2).sum())
    # mesmo percentual com o mesmo número de votos é o mesmo placar; mesmo percentual exato (2 casas), com placares diferentes
    x["pc"] = (x.esq / x.nom * 100).round(2)
    res["percentuais_exatos_diferentes"] = int(x.pc.nunique())
    # o acaso: cada seção sorteia o próprio placar pelo próprio 1º turno
    if "esq1" in x:
        p = (x.esq1 / (x.esq1 + x.dir1)).to_numpy(float)
        p = np.where(np.isnan(p), x.esq.sum() / x.nom.sum(), p).clip(0.0005, 0.9995)
        # a mudança do país entre os turnos, somada igual em todas (em logito), para o total sorteado bater com o total real
        lg = np.log(p / (1 - p))
        lo, hi = -5.0, 5.0
        for _ in range(50):
            m = (lo + hi) / 2
            if (x.nom.to_numpy() / (1 + np.exp(-(lg + m)))).sum() < x.esq.sum():
                lo = m
            else:
                hi = m
        p = 1 / (1 + np.exp(-(lg + (lo + hi) / 2)))
        pb = (x.branco1 / (x.branco1 + x.nulo1)).to_numpy(float)
        pb = np.where(np.isnan(pb), 0.3, pb).clip(0.01, 0.99)
        cheio, municip, zona, zero_dir = [], [], [], []
        for _ in range(20):
            l = RNG.binomial(x.nom.to_numpy(), p)
            bn = (x.branco + x.nulo).to_numpy()
            b = RNG.binomial(bn, pb)
            s = pd.DataFrame({"u": x.uf.to_numpy(), "m": x.municipio.to_numpy(), "z": x.zona.to_numpy(), "l": l, "f": x.nom.to_numpy() - l, "b": b, "n": bn - b})
            cheio.append(int((s.groupby(["l", "f", "b", "n"]).size() >= 2).sum()))
            municip.append(int((s.groupby(["u", "m", "l", "f", "b", "n"]).size() >= 2).sum()))
            zona.append(int((s.groupby(["u", "m", "z", "l", "f", "b", "n"]).size() >= 2).sum()))
            zero_dir.append(int((s.f == 0).sum()))
        res["acaso_boletins_inteiros_que_se_repetem"] = [int(min(cheio)), int(max(cheio))]
        res["acaso_boletins_iguais_no_mesmo_municipio"] = [int(min(municip)), int(max(municip))]
        res["acaso_boletins_iguais_na_mesma_zona"] = [int(min(zona)), int(max(zona))]
        res["acaso_sem_voto_da_direita"] = [int(min(zero_dir)), int(max(zero_dir))]
    return res


def principal():
    preparar()
    T.mkdir(parents=True, exist_ok=True)
    d26, d22, d18 = zera_1o_turno(carrega_2026()), zera_1o_turno(carrega_2022()), zera_1o_turno(carrega_2018())
    out = {"limite": "2018 sem hora de chegada no boletim público: a ordem é o encerramento da urna em horário de Brasília"}
    out["curva"] = {"2026_chegada": medidas(d26, "rec"), "2022_chegada": medidas(d22, "rec"),
                    "2026_encerramento": medidas(d26, "enc"), "2022_encerramento": medidas(d22, "enc"), "2018_encerramento": medidas(d18, "enc")}
    for d, o, a in ((d26, "rec", 2026), (d22, "rec", 2022), (d18, "enc", 2018)):
        amostras_de_zoom(d, o, a)
    out["versoes_ao_vivo_2026"] = versoes_ao_vivo()
    out["identicas"] = {"2026": identicas(d26, 2026), "2022": identicas(d22, 2022), "2018": identicas(d18, 2018)}
    (R / "resultados/RODADA3.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(principal())
