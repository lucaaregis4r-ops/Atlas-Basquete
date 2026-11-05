import pytest
from cbb.analysis.four_factors import compute_possessions, compute_four_factors

def test_compute_possessions():
    # Standard game: 75 FGA, 20 FTA, 10 ORB, 14 TOV
    poss = compute_possessions(fga=75, fta=20, orb=10, tov=14)
    expected = 75 + 0.44 * 20 - 10 + 14  # 87.8
    assert abs(poss - expected) < 1e-5
    assert poss > 0

def test_compute_four_factors():
    ff = compute_four_factors(
        fgm=32, fga=70, fg3m=10,
        ftm=16, fta=20,
        orb=9, opp_drb=27,
        tov=13,
        pts=90, opp_pts=82,
        mp=40.0
    )
    # eFG% = (32 + 5) / 70 = 37 / 70 = 0.5286
    assert abs(ff["efg_pct"] - 0.5286) < 1e-3
    assert 0.0 <= ff["tov_pct"] <= 1.0
    assert 0.0 <= ff["orb_pct"] <= 1.0
    assert ff["ftr"] == round(20 / 70, 4)
    assert ff["ortg"] > ff["drtg"]
    assert ff["net_rating"] > 0
    assert 0.5 < ff["pythagorean_win_pct"] <= 1.0
