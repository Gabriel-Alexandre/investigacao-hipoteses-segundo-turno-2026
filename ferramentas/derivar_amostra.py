"""Lê os logs da amostra (dados/brutos/t2/amostra.sqlite) e escreve uma linha por seção e por turno em
dados/derivados/amostra_logs.parquet. O log de 2026 traz os dois turnos quando a urna é a mesma; o 1º turno só
conta quando o dia 04/10 tem votos no log (urna trocada entre os turnos fica sem 1º turno).

Colunas: chave da seção, grupo da amostra, turno, modelo da urna, versão do programa, verificações de assinatura
que não deram SUCESSO, votos (total, digital, mesário, sem digital cadastrada, outra), votos depois das 17h e das
19h, votos por hora (h06 a h20, hora local), liberações pelo mesário por hora, avisos "eleitor já votou", avisos
seguidos de voto liberado pelo mesário em até 5 minutos, a maior sequência de votos seguidos liberados pelo mesmo
mesário, e se houve contingência. Identificador de mesário vira HMAC com dados/chave-local.txt (fora do git).

Uso: python ferramentas/derivar_amostra.py
"""
import collections
import re
import secrets
import sqlite3
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from hipoteses.log import ler_jez, ler_log  # noqa: E402

FUSO = {"ac": 2, "am": 1, "ro": 1, "rr": 1, "mt": 1, "ms": 1}
RE_URL = re.compile(r"/dados/(\w\w)/(\d+)/(\d+)/(\d+)/")
RE_MODELO = re.compile(r"Modelo de Urna: (UE\d{4})")
RE_VERSAO = re.compile(r"Vers.o da aplica..o: ([\d.]+)")
DIAS = {"t1": "04/10/2026", "t2": "25/10/2026"}


def chave():
    p = RAIZ / "dados/chave-local.txt"
    if not p.exists():
        p.write_text(secrets.token_hex(32))
    return p.read_text().strip().encode()


def maior_sequencia(eleitores):
    melhor, atual, ant = 0, 0, None
    for e in eleitores:
        cod = e[3] if e[1] == "manual_mes" else None
        if cod and cod == ant:
            atual += 1
        else:
            atual = 1 if cod else 0
        ant = cod
        melhor = max(melhor, atual)
    return melhor


def linha(uf, mun, zona, secao, turno, linhas, k, off_h):
    dia = DIAS[turno]
    do_dia = [ln for ln in linhas if ln.startswith(dia)]
    modelos = collections.Counter(m.group(1) for ln in do_dia for m in [RE_MODELO.search(ln)] if m)
    versoes = collections.Counter(m.group(1) for ln in do_dia for m in [RE_VERSAO.search(ln)] if m)
    falha_ass = sum(1 for ln in do_dia if "Verifica" in ln and "assinatura" in ln and "SUCESSO" not in ln)
    lt = ler_log(linhas, k, dia=dia)
    off = off_h * 3600  # horas atrás de Brasília, pela hora de abertura da urna (rodada 2: o oeste do AM está 2 horas atrás)
    r = {"uf": uf, "municipio": mun, "zona": zona, "secao": secao, "turno": turno,
         "modelo": modelos.most_common(1)[0][0] if modelos else None, "versao": versoes.most_common(1)[0][0] if versoes else None,
         "assinatura_sem_sucesso": falha_ass, "contingencia": bool(lt.contingencia), "votos": len(lt.eleitores),
         "encerrar_s_bsb": (lt.encerrar_s + off) if lt.encerrar_s is not None else None}
    tipos = collections.Counter(e[1] for e in lt.eleitores)
    for t in ("biometrica", "manual_mes", "manual_sem", "outra"):
        r[t] = tipos.get(t, 0)
    r["votos_depois_17h"] = sum(1 for e in lt.eleitores if e[0] + off >= 17 * 3600)
    r["votos_depois_19h"] = sum(1 for e in lt.eleitores if e[0] + off >= 19 * 3600)
    for h in range(6, 21):
        r[f"h{h:02d}"] = sum(1 for e in lt.eleitores if (e[0] + off) // 3600 == h)
        r[f"m{h:02d}"] = sum(1 for e in lt.eleitores if (e[0] + off) // 3600 == h and e[1] != "biometrica")
    r["ja_votou"] = len(lt.ja_votou)
    votos_mes = [e[0] for e in lt.eleitores if e[1] != "biometrica"]
    r["ja_votou_seguido_de_manual"] = sum(1 for s in lt.ja_votou if any(0 <= v - s <= 300 for v in votos_mes))
    # régua de comparação (rodada 2): depois de um voto qualquer, vem um voto liberado sem a digital em até 5 minutos?
    tv = sorted(e[0] for e in lt.eleitores)
    r["votos_seguidos_de_manual"] = sum(1 for t0 in tv[:-1] if any(0 < v - t0 <= 300 for v in votos_mes))
    r["votos_com_seguinte"] = max(0, len(tv) - 1)
    # o próximo voto depois do aviso foi liberado sem a digital?
    prox = [min((e for e in lt.eleitores if e[0] >= s), key=lambda e: e[0], default=None) for s in lt.ja_votou]
    r["ja_votou_proximo_voto_manual"] = sum(1 for e in prox if e is not None and e[1] != "biometrica")
    r["ja_votou_com_proximo_voto"] = sum(1 for e in prox if e is not None)
    # aviso isolado: não repete um aviso dos 2 minutos anteriores (a repetição é o mesmo eleitor tentando de novo)
    av = sorted(lt.ja_votou)
    r["ja_votou_isolado"] = sum(1 for i, s in enumerate(av) if i == 0 or s - av[i - 1] > 120)
    r["maior_sequencia_mesmo_mesario"] = maior_sequencia(lt.eleitores)
    return r


def main():
    con = sqlite3.connect(RAIZ / "dados/brutos/t2/amostra.sqlite")
    amostra = pd.read_csv(RAIZ / "dados/derivados/amostra_secoes.csv", dtype=str)
    t2 = pd.read_parquet(RAIZ / "dados/copias/t2_secoes.parquet", columns=["uf", "municipio", "zona", "secao", "abertura"])
    h_ab = pd.to_datetime(t2.abertura, errors="coerce").dt.hour
    offs = {tuple(x): (8 - h if h in (6, 7, 8) else FUSO.get(x[0], 0)) for x, h in zip(t2[["uf", "municipio", "zona", "secao"]].itertuples(index=False), h_ab)}
    grupo = {tuple(x[:4]): x[4] for x in amostra.itertuples(index=False)}
    k = chave()
    linhas_out = []
    for url, corpo in con.execute("SELECT url, body FROM raw WHERE status=200 AND url LIKE '%-log.jez'"):
        uf, mun, zona, secao = RE_URL.search(url).groups()
        linhas = ler_jez(corpo)
        for turno in ("t1", "t2"):
            r = linha(uf, mun, zona, secao, turno, linhas, k, offs.get((uf, mun, zona, secao), FUSO.get(uf, 0)))
            r["grupo"] = grupo.get((uf, mun, zona, secao))
            linhas_out.append(r)
    df = pd.DataFrame(linhas_out)
    df.to_parquet(RAIZ / "dados/derivados/amostra_logs.parquet", index=False)
    print(df.groupby("turno")[["votos", "biometrica", "manual_mes", "manual_sem", "ja_votou"]].sum())
    print(df[df.turno == "t2"].modelo.value_counts(dropna=False).to_dict())


if __name__ == "__main__":
    main()
