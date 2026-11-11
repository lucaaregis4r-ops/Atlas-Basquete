"""Regression checks for official CBI Sub-15 participant registry."""
import json
from pathlib import Path

from cbb.export.html_dashboard import CBI_SUB15_PATH
from cbb.extractors.fallback_data import COMPETITIONS_DATA


def test_cbi_2026_directory_has_source_and_separate_genders():
    data = json.loads(CBI_SUB15_PATH.read_text(encoding="utf-8"))
    groups = {g["id"]: g for g in data["groups"]}
    assert len(groups["masculino"]["teams"]) == 16
    assert len(groups["feminino"]["teams"]) == 26
    assert all(g.get("source_url", "").startswith("https://") for g in groups.values())
    assert all(len(g["teams"]) == len({t["name"] for t in g["teams"]}) for g in groups.values())
    assert any(t["name"] == "Olympico Club" for t in groups["masculino"]["teams"])
    assert any(t["name"] == "Sociedade Thalia" for t in groups["feminino"]["teams"])
    assert all("ortg" not in t and "efg_pct" not in t and "sample_games" not in t
               for g in groups.values() for t in g["teams"])


def test_cbi_demo_does_not_claim_a_champion_before_december():
    demo = next(c for c in COMPETITIONS_DATA if c["id"] == "cbi-sub15")
    assert all("Campeão" not in t["name"] for t in demo["teams"])


def test_dashboard_template_has_unique_ids_and_cbi_data_placeholder():
    html = (Path(__file__).resolve().parents[1] /
            "cbb" / "export" / "templates" / "dashboard.html").read_text(encoding="utf-8")
    import re
    ids = re.findall(r'\\bid="([^"]+)"', html)
    assert len(ids) == len(set(ids))
    assert "__CBI_SUB15_JSON__" in html
    assert 'id="tab-cbi-sub15"' in html
