"""Tabelas leves dos arquivos abertos do TSE baixados por coletar.py (dados/derivados/, no git):

  detalhe_secao_2026.parquet   uma linha por seção e turno, só Presidente: aptos, comparecimento, abstenção, brancos,
                               nulos, local de votação (número e nome), modelo da urna, origem do voto, situação
  local_votacao_2026.parquet   uma linha por seção e turno: tipo de local, latitude, longitude, tipo de seção agregada
  eleitorado_idade.csv         eleitores por município e faixa de idade, 2022 e 2026
  comparecimento_idade.csv     aptos e comparecimento por município, turno e faixa de idade, 2022 e 2026
  secoes_2018_t2.parquet       votos de Haddad e Bolsonaro por seção no 2º turno de 2018

Uso: python ferramentas/derivar_tse.py
"""
import zipfile
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
B = RAIZ / "dados/brutos/tse"
D = RAIZ / "dados/derivados"


def csvs(zipnome):
    z = zipfile.ZipFile(B / zipnome)
    for n in z.namelist():
        # o arquivo _BR repete o país inteiro junto dos arquivos de cada UF: ler os dois soma em dobro
        if n.lower().endswith(".csv") and not n.upper().endswith(("_BR.CSV", "_BRASIL.CSV")):
            yield n, z.open(n)


def ler(zipnome, cols, filtro=None, chunks=1_000_000):
    partes = []
    for n, fh in csvs(zipnome):
        for ch in pd.read_csv(fh, sep=";", encoding="latin1", dtype=str, usecols=lambda c: c in cols, chunksize=chunks, keep_default_na=False):
            if filtro is not None:
                ch = filtro(ch)
            partes.append(ch)
    return pd.concat(partes, ignore_index=True)


def ler_todos(zipnome, cols, filtro=None, chunks=1_000_000):
    """Para o arquivo que só existe como _BR (a votação por seção de 2018)."""
    z = zipfile.ZipFile(B / zipnome)
    partes = []
    for n in z.namelist():
        if n.lower().endswith(".csv"):
            for ch in pd.read_csv(z.open(n), sep=";", encoding="latin1", dtype=str, usecols=lambda c: c in cols, chunksize=chunks, keep_default_na=False):
                partes.append(filtro(ch) if filtro is not None else ch)
    return pd.concat(partes, ignore_index=True)


def chave(df, uf="SG_UF", mun="CD_MUNICIPIO", zona="NR_ZONA", secao="NR_SECAO"):
    df["uf"] = df[uf].str.lower()
    df["municipio"] = df[mun].str.zfill(5)
    df["zona"] = df[zona].str.zfill(4)
    df["secao"] = df[secao].str.zfill(4)
    return df


def detalhe():
    cols = ["NR_TURNO", "SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "CD_CARGO", "QT_APTOS", "QT_COMPARECIMENTO", "QT_ABSTENCOES",
            "QT_VOTOS_NOMINAIS", "QT_VOTOS_BRANCOS", "QT_VOTOS_NULOS", "NR_LOCAL_VOTACAO", "NM_LOCAL_VOTACAO", "DS_ORIGEM_VOTO",
            "ST_SECAO_INSTALADA", "ST_SECAO_ANULADA", "CD_MODELO_URNA", "DS_MODELO_URNA", "DT_RECEBIMENTO_BU_HOR_TSE"]
    df = ler_todos("detalhe_votacao_secao_2026.zip", cols, lambda c: c[c.CD_CARGO == "1"])  # Presidente só vem no _BR
    df = chave(df)
    for c in ["QT_APTOS", "QT_COMPARECIMENTO", "QT_ABSTENCOES", "QT_VOTOS_NOMINAIS", "QT_VOTOS_BRANCOS", "QT_VOTOS_NULOS"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.rename(columns={"NR_TURNO": "turno", "QT_APTOS": "aptos", "QT_COMPARECIMENTO": "comparecimento", "QT_ABSTENCOES": "abstencoes",
                            "QT_VOTOS_NOMINAIS": "nominais", "QT_VOTOS_BRANCOS": "brancos", "QT_VOTOS_NULOS": "nulos",
                            "NR_LOCAL_VOTACAO": "local", "NM_LOCAL_VOTACAO": "nome_local", "DS_ORIGEM_VOTO": "origem",
                            "ST_SECAO_INSTALADA": "instalada", "ST_SECAO_ANULADA": "anulada", "CD_MODELO_URNA": "modelo_cd",
                            "DS_MODELO_URNA": "modelo", "DT_RECEBIMENTO_BU_HOR_TSE": "recebido_tse"})
    df = df[["uf", "municipio", "zona", "secao", "turno", "aptos", "comparecimento", "abstencoes", "nominais", "brancos", "nulos", "local",
             "nome_local", "origem", "instalada", "anulada", "modelo_cd", "modelo", "recebido_tse"]].drop_duplicates()
    df.to_parquet(D / "detalhe_secao_2026.parquet", index=False)
    print("detalhe", df.groupby("turno").size().to_dict())


def locais():
    cols = ["NR_TURNO", "SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "DS_TIPO_SECAO_AGREGADA", "NR_SECAO_PRINCIPAL", "NR_LOCAL_VOTACAO",
            "NM_LOCAL_VOTACAO", "DS_TIPO_LOCAL", "NR_LATITUDE", "NR_LONGITUDE", "DS_SITU_SECAO", "QT_ELEITOR_SECAO", "NM_BAIRRO"]
    df = chave(ler("eleitorado_local_votacao_2026.zip", cols))
    df = df.rename(columns={"NR_TURNO": "turno", "DS_TIPO_SECAO_AGREGADA": "tipo_secao", "NR_SECAO_PRINCIPAL": "secao_principal",
                            "NR_LOCAL_VOTACAO": "local", "NM_LOCAL_VOTACAO": "nome_local", "DS_TIPO_LOCAL": "tipo_local",
                            "NR_LATITUDE": "lat", "NR_LONGITUDE": "lon", "DS_SITU_SECAO": "situacao_secao", "QT_ELEITOR_SECAO": "eleitores_secao",
                            "NM_BAIRRO": "bairro"})
    df = df[["uf", "municipio", "zona", "secao", "turno", "tipo_secao", "secao_principal", "local", "nome_local", "tipo_local", "bairro",
             "lat", "lon", "situacao_secao", "eleitores_secao"]]
    df.to_parquet(D / "local_votacao_2026.parquet", index=False)
    print("locais", df.groupby("turno").size().to_dict(), df.tipo_local.value_counts().head(8).to_dict())


def eleitorado():
    out = []
    for ano in (2022, 2026):
        df = ler(f"perfil_eleitorado_{ano}.zip", ["SG_UF", "CD_MUNICIPIO", "DS_FAIXA_ETARIA", "QT_ELEITORES", "QT_ELEITORES_BIOMETRIA"])
        df["QT_ELEITORES"] = pd.to_numeric(df.QT_ELEITORES, errors="coerce")
        df["QT_ELEITORES_BIOMETRIA"] = pd.to_numeric(df.QT_ELEITORES_BIOMETRIA, errors="coerce")
        g = df.groupby(["SG_UF", "CD_MUNICIPIO", "DS_FAIXA_ETARIA"], as_index=False)[["QT_ELEITORES", "QT_ELEITORES_BIOMETRIA"]].sum()
        g["ano"] = ano
        out.append(g)
    e = pd.concat(out).rename(columns={"SG_UF": "uf", "CD_MUNICIPIO": "cd_tse", "DS_FAIXA_ETARIA": "faixa", "QT_ELEITORES": "eleitores",
                                      "QT_ELEITORES_BIOMETRIA": "com_biometria"})
    e["uf"] = e.uf.str.lower()
    e["cd_tse"] = e.cd_tse.str.zfill(5)
    e.to_csv(D / "eleitorado_idade.csv", index=False)
    print("eleitorado", e.groupby("ano").eleitores.sum().to_dict())


def comparecimento():
    out = []
    for ano in (2022, 2026):
        df = ler(f"perfil_comparecimento_abstencao_{ano}.zip", ["NR_TURNO", "SG_UF", "CD_MUNICIPIO", "DS_FAIXA_ETARIA", "QT_APTOS", "QT_COMPARECIMENTO"])
        for c in ("QT_APTOS", "QT_COMPARECIMENTO"):
            df[c] = pd.to_numeric(df[c], errors="coerce")
        g = df.groupby(["NR_TURNO", "SG_UF", "CD_MUNICIPIO", "DS_FAIXA_ETARIA"], as_index=False)[["QT_APTOS", "QT_COMPARECIMENTO"]].sum()
        g["ano"] = ano
        out.append(g)
    c = pd.concat(out).rename(columns={"NR_TURNO": "turno", "SG_UF": "uf", "CD_MUNICIPIO": "cd_tse", "DS_FAIXA_ETARIA": "faixa",
                                      "QT_APTOS": "aptos", "QT_COMPARECIMENTO": "comparecimento"})
    c["uf"] = c.uf.str.lower()
    c["cd_tse"] = c.cd_tse.str.zfill(5)
    c.to_csv(D / "comparecimento_idade.csv", index=False)
    print("comparecimento", c.groupby(["ano", "turno"]).comparecimento.sum().to_dict())


def s2018():
    cols = ["NR_TURNO", "SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "CD_CARGO", "NR_VOTAVEL", "QT_VOTOS", "NR_LOCAL_VOTACAO"]
    df = ler_todos("votacao_secao_2018_BR.zip", cols, lambda c: c[(c.CD_CARGO == "1") & (c.NR_TURNO == "2")])
    df = chave(df)
    df["QT_VOTOS"] = pd.to_numeric(df.QT_VOTOS, errors="coerce")
    p = df.pivot_table(index=["uf", "municipio", "zona", "secao"], columns="NR_VOTAVEL", values="QT_VOTOS", aggfunc="sum", fill_value=0)
    p = p.rename(columns={"13": "haddad", "17": "bolsonaro", "95": "branco", "96": "nulo"}).reset_index()
    p.columns.name = None
    p.to_parquet(D / "secoes_2018_t2.parquet", index=False)
    print("2018", len(p), int(p.haddad.sum()), int(p.bolsonaro.sum()))


if __name__ == "__main__":
    detalhe()
    locais()
    eleitorado()
    comparecimento()
    s2018()
