import pytest
from pathlib import Path
from cbb.export.html_dashboard import export_dashboard, generate_master_payload
from cbb.config import DOCS_DIR, BASE_DIR

def test_generate_payload():
    payload = generate_master_payload()
    assert "teams" in payload
    assert len(payload["teams"]) >= 8
    assert "markov_models" in payload
    assert "players" in payload
    assert len(payload["players"]) > 20
    assert "hall_of_fame" in payload
    assert len(payload["hall_of_fame"]) >= 5

def test_export_dashboard():
    export_dashboard()
    assert (BASE_DIR / "index.html").exists()
    assert (DOCS_DIR / "index.html").exists()
    assert (DOCS_DIR / ".nojekyll").exists()
    
    html = (BASE_DIR / "index.html").read_text(encoding="utf-8")
    assert "Basquete BR" in html
    assert "Four Factors" in html
    assert "Cadeias de Markov" in html
