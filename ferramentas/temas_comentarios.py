"""Primeira passada nos comentarios: marca cada comentario (e cada resposta) com os temas
que ele toca, por palavra-chave, para a leitura a mao comecar pelos que levantam hipotese.
A classificacao final e a leitura humana (docs/COMENTARIOS.md); isto so ordena a pilha.

Uso: python ferramentas/temas_comentarios.py dados/brutos/comentarios dados/derivados/comentarios_temas.jsonl
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

VIDEOS = {"GMi7q2QetgQ": "08", "l0WeS4f09Fw": "16", "30FYWMAOb3Y": "19"}

TEMAS = {
    "mortos": r"mort[oa]s?\b|falecid|defunt|obito|cemiterio|finad",
    "unanimidade": r"zero voto|0 voto|nenhum voto|100 ?%|100 por cento|so (?:teve|tinha) voto|todos os votos|unanim|sessoes? com mais de 9\d|secoes? com mais de 9\d|9\d ?%",
    "horario_prorrogacao": r"prorrog|17 ?h|17:00|cinco da tarde|5 da tarde|19 ?h|depois das 17|apos as 17|horario|duas horas a mais|2 horas a mais|zanin",
    "biometria": r"biometri|sem digital|digital|impressao digital|liberad[oa]s? (?:sem|pelo)",
    "codigo_software": r"codigo|fonte|hacker|algoritm|programad|software|sala secreta|servidor|apuracao secreta|sistema|computador",
    "voto_impresso_auditoria": r"impresso|auditor|auditavel|contagem publica|recontagem|recontar|papel",
    "abstencao_comparecimento": r"abstenc|compareci|faltos|ausent|nao foram votar|nao votou",
    "mesario": r"mesari",
    "exterior": r"exterior|fora do pais|consulado",
    "compra_de_voto": r"compra de voto|compraram|comprad|bolsa familia|\bpix\b|transporte|onibus|cesta basica|dinheiro|pagar(?:am)? (?:pra|para) votar|beneficio|auxilio",
    "pesquisas": r"pesquisa|datafolha|quaest|atlas|paran[aá] pesquisa|ipec|instituto",
    "benford": r"benford",
    "urna_trocada": r"urna(?:s)? (?:trocad|substitu|de contingencia)|contingencia|urna quebr|urna com defeito|trocaram a urna",
    "votou_e_sumiu": r"meu voto|votei e|nao apareceu|sumiu|nao contou|nao computad|justific|aparece(?:u)? como (?:ausente|falt)",
    "cadastro_fantasma": r"fantasma|cadastro|titulo|cpf|eleitores? a mais|mais eleitores|mais votos que|populacao|ibge|recadastr",
    "boletim_de_urna": r"boletim|\bbu\b|\bbus\b|zeresima|impresso da urna",
    "curva_apuracao": r"curva|apuracao|grafico|virada|vir(?:ou|ar) (?:o jogo|a eleicao)|liderou|na frente ate",
    "nordeste_regiao": r"nordest|norte|bahia|maranhao|piaui|ceara|pernambuco|minas",
    "estrangeiro_venezuela": r"venezuel|maduro|smartmatic|positivo|china|chines|russ",
    "judiciario": r"\bstf\b|moraes|xandao|\btse\b|carmen|carmem|ministro|juiz|justica eleitoral",
    "pedido_analise": r"analis|investig|verific|faz(?:er)? um video|sugest|deveria|pode(?:ria)? ver|olha(?:r)? (?:isso|tambem)|confer|checa|pesquis[ae] (?:isso|sobre)|explica",
    "relatorio_pericial": r"relatorio|pericia|pericial|mannarino|americano|joey",
    "fraude_generica": r"fraud|roub|golpe|manipul|armad|marmelada|ladr",
}
COMPILADOS = {k: re.compile(v) for k, v in TEMAS.items()}


def norm(t):
    t = unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", t)


def temas(texto):
    n = norm(texto)
    return [k for k, rx in COMPILADOS.items() if rx.search(n)]


def main():
    pasta, saida = Path(sys.argv[1]), Path(sys.argv[2])
    saida.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with saida.open("w", encoding="utf-8") as f:
        for arq in sorted(pasta.glob("full_*.json")):
            vid = arq.stem.replace("full_", "")
            for c in json.loads(arq.read_text(encoding="utf-8")):
                filas = [(c, None)] + [(r, c["id"]) for r in c.get("r", [])]
                for item, pai in filas:
                    if item.get("o"):
                        continue  # o proprio canal
                    linha = {"video": VIDEOS.get(vid, vid), "videoId": vid, "id": item.get("id"), "pai": pai,
                             "autor": item.get("a"), "quando": item.get("w"), "respostas": item.get("rc", 0),
                             "texto": item.get("m", ""), "temas": temas(item.get("m", ""))}
                    f.write(json.dumps(linha, ensure_ascii=False) + "\n")
                    n += 1
        extras = pasta / "zernio_extras.json"
        if extras.exists():  # retidos ou apagados depois: vistos so pelo Zernio nas triagens anteriores
            for x in json.loads(extras.read_text(encoding="utf-8")):
                linha = {"video": VIDEOS.get(x["v"], x["v"]), "videoId": x["v"], "id": x["id"], "pai": x.get("pai"),
                         "autor": x.get("a"), "quando": x.get("t") or x.get("w"), "respostas": 0,
                         "texto": re.sub(r"<br>", "\n", x.get("m", "")), "temas": temas(x.get("m", "")), "so_zernio": True}
                f.write(json.dumps(linha, ensure_ascii=False) + "\n")
                n += 1
    print("comentarios", n)


if __name__ == "__main__":
    main()
