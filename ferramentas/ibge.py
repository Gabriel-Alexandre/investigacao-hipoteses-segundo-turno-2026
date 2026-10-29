"""População do Censo 2022 por município e idade (IBGE, tabela 9514, API de agregados v3), para H13 e H14.

Pega o total, as idades de 0 a 11 (quem tinha menos de 12 em 2022 não tem 16 em 2026), as idades simples de 86 a 99
e "100 anos ou mais". Guarda cada resposta em dados/brutos/ibge/ (com sha256 no MANIFESTO.json) e escreve
dados/derivados/ibge_municipio.csv com: cod_ibge, municipio, pop_total, pop_12_ou_mais, pop_86_ou_mais, pop_96_ou_mais.

Uso: python ferramentas/ibge.py
"""
import hashlib
import json
import time
import urllib.request
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
BR = RAIZ / "dados/brutos/ibge"
MAN = RAIZ / "dados/MANIFESTO.json"
BASE = "https://servicodados.ibge.gov.br/api/v3/agregados/9514/periodos/2022/variaveis/93?localidades=N6%5BN3%5B{uf}%5D%5D&classificacao=2%5B6794%5D%7C286%5B113635%5D%7C287%5B{ids}%5D"
UFS_IBGE = [11, 12, 13, 14, 15, 16, 17, 21, 22, 23, 24, 25, 26, 27, 28, 29, 31, 32, 33, 35, 41, 42, 43, 50, 51, 52, 53]
GRUPOS = {
    "total": [100362],
    "menos_de_12": [93070, 93084, 6567, 6568],  # 0 a 4, 5 a 9, 10, 11
    "12_a_15": [6569, 6570, 6571, 6572],          # 12 a 15 anos (para a população de 16 anos ou mais em 2022)
    "86_a_95": list(range(6639, 6649)),          # 86 a 95 anos
    "96_ou_mais": [6649, 6650, 6651, 6652, 6653],  # 96, 97, 98, 99, 100 ou mais
}


def pedir(nome, ids):
    """Uma resposta por UF (a consulta do país inteiro de uma vez estoura o tempo da API)."""
    BR.mkdir(parents=True, exist_ok=True)
    alvo = BR / f"censo2022_9514_{nome}.json"
    if not alvo.exists():
        juntas = []
        for uf in UFS_IBGE:
            url = BASE.format(uf=uf, ids="%2C".join(map(str, ids)))
            corpo = None
            for t in range(5):
                try:
                    corpo = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "investigacao-hipoteses-segundo-turno-2026"}), timeout=300).read()
                    break
                except Exception as e:  # noqa: BLE001
                    print("tentativa", t + 1, nome, uf, e, flush=True)
                    time.sleep(15)
            if corpo is None:
                raise RuntimeError(f"IBGE sem resposta: {nome} {uf}")
            juntas.append(json.loads(corpo))
        alvo.write_text(json.dumps(juntas, ensure_ascii=False), encoding="utf-8")
    man = json.loads(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    man[f"ibge_{nome}"] = {"url": BASE.format(uf="<uf>", ids="%2C".join(map(str, ids))), "arquivo": str(alvo.relative_to(RAIZ)).replace("\\", "/"),
                           "bytes": alvo.stat().st_size, "sha256": hashlib.sha256(alvo.read_bytes()).hexdigest()}
    MAN.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    return json.loads(alvo.read_text(encoding="utf-8"))


def somar(resp):
    out = {}
    nomes = {}
    for bloco in [b for r in resp for b in r[0]["resultados"]]:
        for s in bloco["series"]:
            cod = s["localidade"]["id"]
            nomes[cod] = s["localidade"]["nome"]
            v = s["serie"]["2022"]
            out[cod] = out.get(cod, 0) + (int(v) if v not in ("-", "...", "X", None) else 0)
    return out, nomes


def main():
    tabelas, nomes = {}, {}
    for nome, ids in GRUPOS.items():
        tabelas[nome], n = somar(pedir(nome, ids))
        nomes.update(n)
        print("ok", nome, len(tabelas[nome]), flush=True)
    df = pd.DataFrame({"cod_ibge": list(nomes), "municipio": [nomes[c] for c in nomes]})
    for nome in GRUPOS:
        df[nome] = df.cod_ibge.map(tabelas[nome]).fillna(0).astype(int)
    df["pop_12_ou_mais"] = df.total - df.menos_de_12
    df["pop_86_ou_mais"] = df["86_a_95"] + df["96_ou_mais"]
    df["pop_16_ou_mais"] = df.pop_12_ou_mais - df["12_a_15"]
    df = df.rename(columns={"total": "pop_total", "96_ou_mais": "pop_96_ou_mais"})[
        ["cod_ibge", "municipio", "pop_total", "pop_16_ou_mais", "pop_12_ou_mais", "pop_86_ou_mais", "pop_96_ou_mais"]]
    df.to_csv(RAIZ / "dados/derivados/ibge_municipio.csv", index=False)
    print(df[["pop_total", "pop_16_ou_mais", "pop_12_ou_mais", "pop_86_ou_mais", "pop_96_ou_mais"]].sum().to_dict())


if __name__ == "__main__":
    main()
