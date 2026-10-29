"""H06: quando os arquivos do 2º turno ficaram públicos. Lê a captura do catálogo de Dados Abertos (campo `created`)
e pergunta ao servidor do TSE a data de cada pacote (`Last-Modified`), e grava
dados/brutos/relatorio-pericial/capturas/linha_do_tempo.json (horas em Brasília).

Uso: python ferramentas/linha_do_tempo.py
"""
import datetime as dt
import email.utils
import json
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CAP = RAIZ / "dados/brutos/relatorio-pericial/capturas"
BRT = dt.timezone(dt.timedelta(hours=-3))


def urls_do_catalogo():
    d = json.loads((CAP / "ckan_arq.json").read_text(encoding="utf-8"))
    out = []

    def walk(o):
        if isinstance(o, dict):
            if isinstance(o.get("url"), str) and "_2t_" in o["url"] and o["url"].endswith(".zip"):
                out.append((o["url"], o.get("created")))
                return
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(d)
    return out


def main():
    criados, servidor = [], []
    for url, criado in urls_do_catalogo():
        criados.append(dt.datetime.fromisoformat(criado).replace(tzinfo=dt.timezone.utc).astimezone(BRT))
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "investigacao-hipoteses-segundo-turno-2026"})
        lm = urllib.request.urlopen(req, timeout=60).headers.get("Last-Modified")
        servidor.append(email.utils.parsedate_to_datetime(lm).astimezone(BRT))
    fmt = "%d/%m %Hh%M"
    out = {"pacotes": len(criados),
           "entrada_no_catalogo_de_dados_abertos": {"primeiro": min(criados).strftime(fmt), "ultimo": max(criados).strftime(fmt)},
           "data_dos_arquivos_no_servidor_do_tse": {"primeiro": min(servidor).strftime(fmt), "ultimo": max(servidor).strftime(fmt)},
           "arquivos_por_secao_no_site_de_resultados": "o projeto investigacao-segundo-turno-2026 começou a baixá-los em 26/10 às 7h30 (docs/PRE_REGISTRO.md de lá)",
           "boletim_impresso_na_secao": "25/10, no encerramento de cada seção",
           "lido_em": dt.datetime.now(BRT).strftime("%d/%m/%Y %Hh%M")}
    (CAP / "linha_do_tempo.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
