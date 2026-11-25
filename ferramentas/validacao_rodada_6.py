"""Validação da rodada 6 por outro caminho (24/11/2026).

1. H39: o buraco das 19h31m50 às 19h59m22 aparece também no outro campo de hora (o "recebido" do aux.json de cada
   seção, guardado no t1_secoes.parquet), que não é o do arquivo de detalhe usado na análise?
2. H39 e H42: a soma dos boletins de cada seção dá o total oficial do 1º e do 2º turno publicado pelo TSE (a tabela por
   abrangência do projeto pesquisas-e-resultado-segundo-turno-2026)?
3. H40: com o resultado oficial por estado (e não com a soma das seções), os 6 estados com 2º turno para governador
   continuam com a mesma mudança do Lula que os outros?
4. H41: contando de novo, direto no texto de cada log e sem o leitor de eventos, todo número de 12 dígitos que aparece
   em mais de um município, quantos são e em quantos deles o número liberou eleitor nas 2 pontas?
Saída: resultados/VALIDACAO_RODADA6.json
"""
from __future__ import annotations

import hashlib
import hmac
import io
import json
import re
import sqlite3
import zipfile
from collections import defaultdict
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
R6 = json.loads((RAIZ / "resultados" / "RODADA6.json").read_text(encoding="utf-8"))
OUTRO = RAIZ.parent / "investigacao-segundo-turno-2026" / "dados" / "derivados"
ABR = RAIZ.parent / "pesquisas-e-resultado-segundo-turno-2026" / "dados" / "derivados" / "presidente_abrangencia.csv"


def check(nome, ok, detalhe):
    return {"teste": nome, "ok": bool(ok), "detalhe": detalhe}


def main():
    cs = []
    # 1. o buraco no outro campo de hora
    t1 = pd.read_parquet(OUTRO / "t1_secoes.parquet")
    ts = pd.to_datetime(t1.recebido, errors="coerce").dropna().sort_values()
    dentro = int(((ts > "2026-10-04 19:31:50") & (ts < "2026-10-04 19:59:22")).sum())
    cs.append(check("buraco também no campo recebido do aux.json", dentro == 0,
                    f"{dentro} boletins entre 19:31:50 e 19:59:22 em {len(ts)} seções com esse campo"))
    # 2. a soma das seções contra o oficial
    abr = pd.read_csv(ABR)
    br1 = abr[(abr.turno == 1) & (abr.abr == "br")].iloc[0]
    br2 = abr[(abr.turno == 2) & (abr.abr == "br")].iloc[0]
    det = pd.read_parquet(RAIZ / "dados" / "derivados" / "detalhe_secao_2026.parquet")
    v2 = int(det[det.turno == "2"].nominais.sum())
    cs.append(check("2º turno: válidos somados seção a seção = oficial", v2 == int(br2.validos), f"seções {v2}; oficial {int(br2.validos)}"))
    h44 = R6["H42"]
    falta = int(br2.lula + br2.flavio) - (h44["boletins_eletronicos_lula"] + h44["boletins_eletronicos_flavio"])
    cs.append(check("2º turno: o que falta nos boletins eletrônicos é o voto das seções sem boletim eletrônico", falta == h44["secoes_sem_boletim_eletronico"]["votos_validos"],
                    f"faltam {falta} votos; as {h44['secoes_sem_boletim_eletronico']['total']} seções sem boletim eletrônico somam {h44['secoes_sem_boletim_eletronico']['votos_validos']}"))
    # 1º turno: o percentual do Lula na soma das seções contra o oficial (2 casas)
    l1 = round(100 * t1.lula.sum() / t1[["lula", "flavio", "renan", "caiado", "cury", "demais", "zema"]].sum().sum(), 2)
    cs.append(check("1º turno: Lula na soma das seções = oficial, com 2 casas", l1 == round(100 * br1.lula / br1.validos, 2),
                    f"seções {l1}%; oficial {round(100 * br1.lula / br1.validos, 2)}%"))
    # 3. H40 com o oficial por estado
    uf1 = abr[(abr.turno == 1) & (abr.abr.str.len() == 2) & (abr.abr != "br")].set_index("abr")
    uf2 = abr[(abr.turno == 2) & (abr.abr.str.len() == 2) & (abr.abr != "br")].set_index("abr")
    dl = 100 * uf2.lula / uf2.validos - 100 * uf1.lula / uf1.validos
    com = R6["H40"]["2026"]["com_2t_governador"]["estados"]
    med_com, med_sem = float(dl[dl.index.isin(com)].median()), float(dl[~dl.index.isin(com) & (dl.index != "zz")].median())
    cs.append(check("H40 pelo oficial: a diferença entre os grupos fica abaixo de 0,5 ponto", abs(med_com - med_sem) < 0.5,
                    f"mediana com 2º turno para governador {med_com:.2f}, sem {med_sem:.2f} (análise: "
                    f"{R6['H40']['2026']['com_2t_governador']['lula_mudou_pontos_mediana_dos_estados']} e {R6['H40']['2026']['sem_2t_governador']['lula_mudou_pontos_mediana_dos_estados']})"))
    # 4. H41 refeito direto no texto
    m6 = RAIZ / "resultados" / "RODADA6_MESARIOS.json"
    if m6.exists():
        k = (RAIZ / "dados" / "chave-local.txt").read_text().strip().encode()
        cod = lambda x: hmac.new(k, x.encode(), hashlib.sha256).hexdigest()[:12]
        onde = defaultdict(set)
        hab = defaultdict(lambda: defaultdict(int))
        con = sqlite3.connect(f"file:{RAIZ / 'dados/brutos/rodada6/logs.sqlite'}?mode=ro", uri=True)
        for url, body in con.execute("SELECT url, body FROM raw WHERE status=200 AND url LIKE '%.jez'"):
            p = url.split("/")
            chave_lugar = (p[-8], p[-6], p[-5])
            z = zipfile.ZipFile(io.BytesIO(body))
            txt = z.read(next(n for n in z.namelist() if n.lower().endswith(".dat"))).decode("latin-1")
            for linha in txt.splitlines():
                if "esário" not in linha and "esario" not in linha and "encerramento" not in linha:
                    continue
                for num in re.findall(r"(?<!\d)(\d{12})(?!\d)", linha):
                    c = (p[-8], cod(num))
                    onde[c].add(chave_lugar)
                    if "habilitou o eleitor" in linha:
                        hab[c][chave_lugar] += 1
        multi = [c for c, s in onde.items() if len({x[2] for x in s}) >= 2]
        nas_duas = sum(1 for c in multi if sum(1 for v in hab[c].values() if v > 0) >= 2)
        r = json.loads(m6.read_text(encoding="utf-8"))["mesario_em_2_ou_mais_municipios"]
        cs.append(check("H41: números em 2+ municípios, contados direto no texto", len(multi) == r["codigos"],
                        f"texto {len(multi)}; análise {r['codigos']}"))
        cs.append(check("H41: liberou eleitor nas 2 pontas", nas_duas == r["atuou_em_2_ou_mais_municipios"],
                        f"texto {nas_duas}; análise {r['atuou_em_2_ou_mais_municipios']}"))
    out = {"conferidos": len(cs), "ok": sum(c["ok"] for c in cs), "testes": cs}
    (RAIZ / "resultados" / "VALIDACAO_RODADA6.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    for c in cs:
        print("OK " if c["ok"] else "ERRO", c["teste"], "·", c["detalhe"])
    print(f"{out['ok']} de {out['conferidos']}")


if __name__ == "__main__":
    main()
