"""Conferências que não dependem de dado novo: as cópias batem com o manifesto e a sondagem fecha com o TSE."""
import hashlib
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def test_copias_batem_com_o_manifesto():
    man = json.loads((RAIZ / "dados/MANIFESTO_COPIAS.json").read_text())
    for nome, info in man["arquivos"].items():
        assert hashlib.sha256((RAIZ / "dados/copias" / nome).read_bytes()).hexdigest() == info["sha256"], nome


def test_sondagem_bate_com_numeros_publicos():
    s = json.loads((RAIZ / "resultados/SONDAGEM.json").read_text(encoding="utf-8"))
    assert s["H01_encerramento"]["votos_depois_17h_pelo_log_brasil"] == 34393  # nota do TSE de 28/10
    assert s["H02_unanimidade"]["secoes_zero_flavio"] == 106
    assert s["H02_unanimidade"]["votos_lula_nelas"] == 14860


def test_texto_publico_sem_travessao():
    for p in [RAIZ / "README.md", RAIZ / "ESTADO.md", *(RAIZ / "docs").rglob("*.md")]:
        assert "—" not in p.read_text(encoding="utf-8"), p.name
