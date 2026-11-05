"""
Individual Advanced Metrics, Empirical Bayes Shrinkage, and Wilson Score Intervals.
References:
- Kubatko, J., Oliver, D., Pelton, K., & Rosenbaum, D. (2007).
  A starting point for analyzing basketball statistics. JQAS.
- Hollinger, J. (2005). Pro Basketball Forecast.
- Wilson, E. B. (1927). Probable inference, the law of population and the known proportion.
"""
from typing import Dict, Any, Tuple
import math
from cbb.config import FTA_POSSESSION_WEIGHT

def compute_wilson_ci(successes: int, trials: int, confidence: float = 0.95) -> Tuple[float, float, float]:
    """
    Computes Wilson score interval for binomial proportions (e.g. 3P%, FT%).
    Guarantees mathematically rigorous confidence bounds on small samples.
    Returns: (point_estimate, ci_lower, ci_upper)
    """
    if trials <= 0:
        return 0.0, 0.0, 0.0
    
    z = 1.95996  # 95% confidence
    p = successes / trials
    denom = 1.0 + (z**2) / trials
    center = (p + (z**2) / (2 * trials)) / denom
    diff = (z / denom) * math.sqrt((p * (1.0 - p) / trials) + ((z**2) / (4 * trials**2)))
    
    return round(p, 4), round(max(0.0, center - diff), 4), round(min(1.0, center + diff), 4)

def empirical_bayes_shrinkage(
    player_made: int,
    player_attempts: int,
    league_mean: float = 0.35,
    m_prior_strength: float = 25.0
) -> float:
    """
    Beta-Binomial Empirical Bayes shrinkage for shooting percentages.
    Smooths low-volume noise towards the league baseline.
    """
    if player_attempts <= 0:
        return league_mean
    
    shrunk = (player_made + m_prior_strength * league_mean) / (player_attempts + m_prior_strength)
    return round(shrunk, 4)

def compute_player_advanced_metrics(
    pts: float,
    fga: float, fgm: float,
    fg3a: float, fg3m: float,
    fta: float, ftm: float,
    orb: float, drb: float, trb: float,
    ast: float, stl: float, blk: float,
    tov: float, pf: float, fd: float,
    mp: float,
    # Team context
    tm_mp: float = 200.0,
    tm_fga: float = 70.0, tm_fgm: float = 32.0,
    tm_fta: float = 18.0, tm_tov: float = 14.0,
    tm_trb: float = 40.0, opp_trb: float = 40.0,
    opp_fga: float = 70.0, opp_fta: float = 18.0, opp_tov: float = 14.0
) -> Dict[str, Any]:
    """
    Computes complete individual advanced box score metrics.
    """
    # 1. True Shooting Percentage (TS%)
    ts_denom = 2.0 * (fga + FTA_POSSESSION_WEIGHT * fta)
    ts_pct = pts / ts_denom if ts_denom > 0 else 0.0
    
    # 2. Effective Field Goal Percentage (eFG%)
    efg_pct = (fgm + 0.5 * fg3m) / fga if fga > 0 else 0.0
    
    # 3. Usage Rate (USG%)
    tm_poss_estimate = tm_fga + FTA_POSSESSION_WEIGHT * tm_fta + tm_tov
    player_poss_used = fga + FTA_POSSESSION_WEIGHT * fta + tov
    if mp > 0 and tm_poss_estimate > 0:
        usg_pct = 100.0 * (player_poss_used * (tm_mp / 5.0)) / (mp * tm_poss_estimate)
    else:
        usg_pct = 0.0
        
    # 4. Assist Percentage (AST%)
    ast_denom = ((mp / (tm_mp / 5.0)) * tm_fgm) - fgm if mp > 0 else 0.0
    ast_pct = 100.0 * (ast / ast_denom) if ast_denom > 0 else 0.0
    
    # 5. Total Rebound Percentage (TRB%)
    tot_reb_available = tm_trb + opp_trb
    if mp > 0 and tot_reb_available > 0:
        trb_pct = 100.0 * (trb * (tm_mp / 5.0)) / (mp * tot_reb_available)
    else:
        trb_pct = 0.0
        
    # 6. Official FIBA Performance Index Rating (PIR / Eficiência)
    fiba_pir = (pts + trb + ast + stl + blk + fd) - ((fga - fgm) + (fta - ftm) + tov + pf)
    
    # 7. Hollinger Game Score (GmSc)
    game_score = (
        pts + 0.4 * fgm - 0.7 * fga - 0.4 * (fta - ftm)
        + 0.7 * orb + 0.3 * drb + stl + 0.7 * ast + 0.7 * blk - 0.4 * pf - tov
    )
    
    # 8. Wilson Confidence Interval for 3PT shooting
    _, ci_3p_low, ci_3p_high = compute_wilson_ci(int(fg3m), int(fg3a))
    shrunk_3p = empirical_bayes_shrinkage(int(fg3m), int(fg3a), league_mean=0.35)
    
    return {
        "ts_pct": round(ts_pct, 4),
        "efg_pct": round(efg_pct, 4),
        "usg_pct": round(usg_pct, 1),
        "ast_pct": round(ast_pct, 1),
        "trb_pct": round(trb_pct, 1),
        "fiba_pir": round(fiba_pir, 1),
        "game_score": round(game_score, 1),
        "ci_3p_lower": ci_3p_low,
        "ci_3p_upper": ci_3p_high,
        "shrunk_3p_pct": shrunk_3p
    }
