"""
HTML Dashboard Generator for Basquete BR — Atlas Tático.
Exports self-contained HTML and JSON packages for local and GitHub Pages deployment.
"""
from pathlib import Path
import json
import os
from typing import Dict, Any

from cbb.config import DOCS_DIR, EXPORTS_DIR, BASE_DIR
from cbb.metric_definitions import METRIC_CATALOG
from cbb.extractors.fallback_data import get_complete_fallback_dataset
from cbb.analysis.markov_possession import BasketballMarkovModel, TRANSIENT_STATES, ABSORBING_STATES
from cbb.analysis.four_factors import compute_cohort_four_factors
from cbb.database.repository import default_repo

def generate_master_payload() -> Dict[str, Any]:
    """
    Compiles all analytical, spatial, Markov, team, player, and historical data
    into a unified payload.
    """
    fallback = get_complete_fallback_dataset()
    teams = fallback["teams"]
    hall_of_fame = fallback["hall_of_fame"]
    all_shots = fallback["all_shots"]
    
    # 1. Markov Models for each team
    markov_models = {}
    baseline_markov = BasketballMarkovModel("Padrão Liga (CBB)")
    markov_models["baseline"] = baseline_markov.compute_analytics()
    
    for t in teams:
        ff = t["four_factors"]
        tm_model = BasketballMarkovModel(t["name"])
        tm_model.calibrate_for_team(
            three_pt_pct=ff["efg_pct"] * 0.75,
            two_pt_pct=ff["efg_pct"],
            ft_rate=ff["ftr"],
            tov_rate=ff["tov_pct"],
            orb_rate=ff["orb_pct"],
            three_pt_freq=0.40
        )
        markov_models[t["name"]] = tm_model.compute_analytics()

    # 2. Four factors cohort rankings
    cohort = compute_cohort_four_factors(teams)
    
    # 3. Flatted player list for rankings
    all_players = []
    for t in teams:
        for p in t["roster"]:
            adv = p.get("advanced", {})
            all_players.append({
                "name": p["name"],
                "team": t["name"],
                "number": p["num"],
                "pos": p["pos"],
                "mp": p["mp"],
                "pts": p["pts"],
                "reb": p["reb"],
                "ast": p["ast"],
                "fg3_pct": p["fg3_pct"],
                "fg2_pct": p["fg2_pct"],
                "ft_pct": p["ft_pct"],
                "ts_pct": adv.get("ts_pct", 0.0),
                "usg_pct": adv.get("usg_pct", 0.0),
                "ast_pct": adv.get("ast_pct", 0.0),
                "trb_pct": adv.get("trb_pct", 0.0),
                "fiba_pir": adv.get("fiba_pir", 0.0),
                "game_score": adv.get("game_score", 0.0),
                "ci_3p_lower": adv.get("ci_3p_lower", 0.0),
                "ci_3p_upper": adv.get("ci_3p_upper", 0.0),
                "shrunk_3p_pct": adv.get("shrunk_3p_pct", 0.0),
            })
            
    # Sort players by FIBA PIR desc
    all_players.sort(key=lambda x: x["fiba_pir"], reverse=True)
    
    # 4. Sample Matches with Box Scores and Win Probability
    sample_matches = [
        {
            "match_id": "nbb_2026_fla_mtc",
            "competition": "NBB Caixa 2026–2027",
            "date": "2026-11-03",
            "team_home": "Flamengo",
            "team_away": "Minas Tênis Clube",
            "score_home": 84,
            "score_away": 81,
            "quarters": {"q1": [22, 19], "q2": [18, 24], "q3": [23, 20], "q4": [21, 18]},
            "win_prob_series": [
                {"min": 0, "wp": 0.54, "score_diff": 0},
                {"min": 10, "wp": 0.62, "score_diff": 3},
                {"min": 20, "wp": 0.44, "score_diff": -3},
                {"min": 30, "wp": 0.52, "score_diff": 0},
                {"min": 38, "wp": 0.78, "score_diff": 4},
                {"min": 40, "wp": 1.00, "score_diff": 3},
            ],
            "stats_home": teams[0]["four_factors"],
            "stats_away": teams[2]["four_factors"],
            "top_scorer_home": "Gui Deodato (21 pts, 5 reb, 4 ast)",
            "top_scorer_away": "Chuzito González (19 pts, 3 reb, 3 ast)"
        },
        {
            "match_id": "nbb_2026_fra_spfc",
            "competition": "NBB Caixa 2026–2027",
            "date": "2026-11-01",
            "team_home": "Sesi Franca",
            "team_away": "São Paulo FC",
            "score_home": 89,
            "score_away": 82,
            "quarters": {"q1": [26, 21], "q2": [20, 22], "q3": [21, 19], "q4": [22, 20]},
            "win_prob_series": [
                {"min": 0, "wp": 0.58, "score_diff": 0},
                {"min": 10, "wp": 0.72, "score_diff": 5},
                {"min": 20, "wp": 0.65, "score_diff": 3},
                {"min": 30, "wp": 0.74, "score_diff": 5},
                {"min": 38, "wp": 0.92, "score_diff": 8},
                {"min": 40, "wp": 1.00, "score_diff": 7},
            ],
            "stats_home": teams[1]["four_factors"],
            "stats_away": teams[3]["four_factors"],
            "top_scorer_home": "Lucas Dias (24 pts, 9 reb, 4 ast)",
            "top_scorer_away": "Miller (22 pts, 4 reb, 2 ast)"
        }
    ]

    return {
        "metadata": {
            "title": "Basquete BR — Atlas Tático",
            "subtitle": "Scouting Tático Independente • Modelagem Estocástica de Markov, Four Factors e Eficiência Espacial",
            "version": "1.0.0",
            "season": "2026–2027",
            "disclaimer": "Projeto independente de ciência de dados esportivos. Dados abertos consolidados de súmulas oficiais CBB e LNB/NBB.",
            "updated_at": "2026-11-05T10:00:00Z"
        },
        "teams": teams,
        "cohort": cohort,
        "players": all_players,
        "markov_models": markov_models,
        "all_shots": all_shots,
        "matches": sample_matches,
        "hall_of_fame": hall_of_fame,
        "metric_catalog": METRIC_CATALOG,
        "transient_states": TRANSIENT_STATES,
        "absorbing_states": ABSORBING_STATES
    }

def export_dashboard(target_html_path: Path = None):
    """
    Compiles data and exports:
    - docs/exports/*.json
    - docs/index.html (GitHub Pages)
    - index.html (Workspace Root)
    """
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    data = generate_master_payload()
    
    # Write partitioned JSON files for clean API consumption
    (EXPORTS_DIR / "atlas_payload.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    (EXPORTS_DIR / "teams_advanced.json").write_text(json.dumps(data["teams"], ensure_ascii=False, indent=2), encoding="utf-8")
    (EXPORTS_DIR / "players_advanced.json").write_text(json.dumps(data["players"], ensure_ascii=False, indent=2), encoding="utf-8")
    (EXPORTS_DIR / "markov_models.json").write_text(json.dumps(data["markov_models"], ensure_ascii=False, indent=2), encoding="utf-8")
    (EXPORTS_DIR / "metric_catalog.json").write_text(json.dumps(data["metric_catalog"], ensure_ascii=False, indent=2), encoding="utf-8")
    
    # Touch .nojekyll
    (DOCS_DIR / ".nojekyll").touch(exist_ok=True)
    (BASE_DIR / ".nojekyll").touch(exist_ok=True)

    # Render HTML from template
    template_path = Path(__file__).parent / "templates" / "dashboard.html"
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found at {template_path}")
        
    template_html = template_path.read_text(encoding="utf-8")
    json_str = json.dumps(data, ensure_ascii=False)
    
    # Embed payload directly
    rendered_html = template_html.replace("__ATLAS_DATA_JSON__", json_str)
    
    # Output to both index.html (root) and docs/index.html (Pages)
    (BASE_DIR / "index.html").write_text(rendered_html, encoding="utf-8")
    (DOCS_DIR / "index.html").write_text(rendered_html, encoding="utf-8")
    
    if target_html_path:
        target_html_path.write_text(rendered_html, encoding="utf-8")
        
    print(f"Exported dashboard successfully to index.html and docs/index.html")
    return rendered_html
