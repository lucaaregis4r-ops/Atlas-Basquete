import pytest
import numpy as np
from cbb.analysis.markov_possession import BasketballMarkovModel, TRANSIENT_STATES, ABSORBING_STATES

def test_markov_baseline_properties():
    model = BasketballMarkovModel("Test Model")
    analytics = model.compute_analytics()
    
    # EPV should be in realistic basketball range (between 0.85 and 1.35 pts per possession)
    epv = analytics["overall_possession_epv"]
    assert 0.85 <= epv <= 1.35
    
    # State EPV for paint should exceed mid-range
    state_epv = analytics["state_epv"]
    assert state_epv["S6_Shot_Paint"] > state_epv["S5_Shot_MidRange"]
    
    # Steps to absorption should be positive
    steps = analytics["steps_to_absorption"]
    for s, st in steps.items():
        assert st > 0

def test_markov_stochastic_calibration():
    model = BasketballMarkovModel("Elite 3PT Team")
    model.calibrate_for_team(
        three_pt_pct=0.42,
        two_pt_pct=0.55,
        ft_rate=0.28,
        tov_rate=0.11,
        orb_rate=0.30,
        three_pt_freq=0.45
    )
    # Check that rows sum to 1.0 (stochastic property)
    for i in range(model.num_transient):
        row_sum = np.sum(model.Q[i, :]) + np.sum(model.R[i, :])
        assert abs(row_sum - 1.0) < 1e-5
        
    analytics = model.compute_analytics()
    assert analytics["overall_possession_epv"] > 1.0
