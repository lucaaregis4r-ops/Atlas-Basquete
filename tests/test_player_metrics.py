import pytest
from cbb.analysis.player_advanced import compute_player_advanced_metrics, compute_wilson_ci, empirical_bayes_shrinkage

def test_wilson_ci_bounds():
    p, low, high = compute_wilson_ci(successes=15, trials=40)
    assert p == 0.375
    assert 0.0 <= low < p < high <= 1.0

def test_empirical_bayes_shrinkage():
    # Small sample: 3 of 4 (75%) should shrink towards league mean 0.35
    shrunk = empirical_bayes_shrinkage(player_made=3, player_attempts=4, league_mean=0.35, m_prior_strength=25.0)
    assert shrunk < 0.75
    assert shrunk > 0.35

def test_player_advanced_metrics():
    res = compute_player_advanced_metrics(
        pts=22, fga=16, fgm=8, fg3a=6, fg3m=3,
        fta=4, ftm=3, orb=2, drb=6, trb=8,
        ast=5, stl=2, blk=1, tov=3, pf=2, fd=4, mp=32.0
    )
    assert 0.0 < res["ts_pct"] < 1.0
    assert 0.0 < res["efg_pct"] < 1.0
    assert res["usg_pct"] > 0
    assert res["fiba_pir"] > 15.0  # Quality game
    assert res["game_score"] > 10.0
