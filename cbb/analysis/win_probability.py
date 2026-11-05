"""
In-game Win Probability (WP) and Leverage Index (LI) Models for Basketball.
References:
- Stern, H. (1994). A Brownian motion model for basketball games. The American Statistician.
- Deshpande, S. K., & Jensen, S. T. (2016). Estimating an NBA player's impact on win probability.
"""
from typing import List, Dict, Any
import math
from scipy.stats import norm
from cbb.config import FIBA_GAME_MINUTES

def calculate_win_probability(
    score_diff: float,
    seconds_remaining: float,
    has_possession: bool = True,
    total_seconds: float = 2400.0  # 40 mins * 60 = 2400s
) -> float:
    """
    Computes real-time win probability for team A leading by score_diff.
    Uses continuous diffusion with time-decaying variance.
    """
    if seconds_remaining <= 0:
        if score_diff > 0:
            return 1.0
        elif score_diff < 0:
            return 0.0
        else:
            return 0.5  # Overtime
            
    # Possessions bias: having the ball is worth ~0.8 net expected points
    possession_value = 0.8 if has_possession else -0.8
    effective_lead = score_diff + (possession_value * (seconds_remaining / total_seconds))
    
    # Standard deviation of score differential scales with sqrt(t)
    # Empirical standard deviation in 40-min FIBA game: ~10.5 points full game
    full_game_sigma = 10.5
    sigma_t = full_game_sigma * math.sqrt(max(1.0, seconds_remaining) / total_seconds)
    
    # Normal CDF
    wp = norm.cdf(effective_lead / sigma_t)
    return round(float(max(0.001, min(0.999, wp))), 4)

def calculate_leverage_index(score_diff: float, seconds_remaining: float) -> float:
    """
    Computes Leverage Index (LI): importance of the current possession.
    Average possession = 1.0. High clutch moments > 2.5.
    """
    if seconds_remaining <= 0:
        return 0.0
    wp_now = calculate_win_probability(score_diff, seconds_remaining, True)
    wp_swing = calculate_win_probability(score_diff + 2, max(1.0, seconds_remaining - 18), False)
    diff = abs(wp_swing - wp_now)
    # Calibrated against baseline possession swing (~0.035 in normal game state)
    li = diff / 0.035
    return round(float(li), 2)
