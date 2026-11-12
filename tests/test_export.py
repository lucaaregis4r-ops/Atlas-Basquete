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
    assert "seasons" in payload
    assert len(payload["seasons"]) >= 3
    assert "season_comparisons" in payload
    assert "Sesi Franca" in payload["season_comparisons"]

def test_franca_season_differentiation():
    payload = generate_master_payload()
    franca_comparisons = payload["season_comparisons"]["Sesi Franca"]["seasons"]
    assert len(franca_comparisons) == 3

    s2024 = next(s for s in franca_comparisons if s["season_id"] == "2024-2025")
    s2025 = next(s for s in franca_comparisons if s["season_id"] == "2025-2026")
    s2026 = next(s for s in franca_comparisons if s["season_id"] == "2026-2027")

    # Franca 2024-25 vs 2025-26 differ in Pace, ORtg, Net Rating, FTR
    assert s2024["pace"] != s2025["pace"]
    assert s2024["net_rating"] > s2025["net_rating"]  # 2024 was peak champion +20.3 vs 13.4
    assert s2024["ftr"] > s2025["ftr"]  # 0.315 with Márcio Santos vs 0.272 without
    assert s2025["pace"] > s2024["pace"]  # 2025 accelerated transition

    # Key departures and arrivals are explicitly tracked
    assert any("Márcio Santos" in d for d in s2025["key_departures"])
    assert any("Nathan Mariano" in a for a in s2025["key_arrivals"])

def test_export_dashboard():
    export_dashboard()
    assert (BASE_DIR / "index.html").exists()
    assert (DOCS_DIR / "index.html").exists()
    assert (DOCS_DIR / ".nojekyll").exists()
    
    html = (BASE_DIR / "index.html").read_text(encoding="utf-8")
    assert "Atlas do Basquete" in html
    assert 'id="competition"' in html
    assert 'id="team"' in html
    assert 'id="view-players"' in html
    assert 'id="view-games"' in html
    assert 'id="view-analysis"' in html
    assert 'id="markov-demo-data"' in html
    assert "__ADVANCED_ANALYTICS_JS__" not in html
    assert "Tricampeonato" not in html
