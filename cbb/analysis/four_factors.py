"""
Dean Oliver's Four Factors and Team Efficiency Analytics.
Reference: Oliver, D. (2004). Basketball on Paper.
"""
from typing import Dict, Any, List
import math
from cbb.config import PYTHAGOREAN_EXPONENT, FTA_POSSESSION_WEIGHT, FIBA_GAME_MINUTES

def compute_possessions(fga: float, fta: float, orb: float, tov: float) -> float:
    """
    Standard Dean Oliver possession estimator:
    Poss = FGA + 0.44 * FTA - ORB + TOV
    """
    return max(1.0, fga + FTA_POSSESSION_WEIGHT * fta - orb + tov)

def compute_four_factors(
    fgm: float, fga: float, fg3m: float,
    ftm: float, fta: float,
    orb: float, opp_drb: float,
    tov: float,
    pts: float,
    opp_pts: float,
    mp: float = 40.0
) -> Dict[str, float]:
    """
    Computes Dean Oliver's Four Factors and advanced team ratings for FIBA games.
    """
    poss = compute_possessions(fga, fta, orb, tov)
    
    # 1. Effective Field Goal Percentage (Weight: ~40%)
    efg_pct = (fgm + 0.5 * fg3m) / fga if fga > 0 else 0.0
    
    # 2. Turnover Percentage (Weight: ~25%)
    tov_denom = fga + FTA_POSSESSION_WEIGHT * fta + tov
    tov_pct = tov / tov_denom if tov_denom > 0 else 0.0
    
    # 3. Offensive Rebound Percentage (Weight: ~20%)
    reb_denom = orb + opp_drb
    orb_pct = orb / reb_denom if reb_denom > 0 else 0.0
    
    # 4. Free Throw Rate (Weight: ~15%)
    ftr = fta / fga if fga > 0 else 0.0
    
    # Efficiency Ratings (Per 100 Possessions)
    ortg = 100.0 * (pts / poss) if poss > 0 else 0.0
    drtg = 100.0 * (opp_pts / poss) if poss > 0 else 0.0
    net_rtg = ortg - drtg
    
    # FIBA Pace (standardized to 40 minutes)
    pace = (poss / max(1.0, mp)) * FIBA_GAME_MINUTES
    
    # Pythagorean Win Expectancy (Daryl Morey / Dean Oliver exponent for basketball)
    if ortg > 0 and drtg > 0:
        ortg_pow = ortg ** PYTHAGOREAN_EXPONENT
        drtg_pow = drtg ** PYTHAGOREAN_EXPONENT
        pyth_win_pct = ortg_pow / (ortg_pow + drtg_pow)
    else:
        pyth_win_pct = 0.5
        
    return {
        "possessions": round(poss, 1),
        "pace": round(pace, 1),
        "efg_pct": round(efg_pct, 4),
        "tov_pct": round(tov_pct, 4),
        "orb_pct": round(orb_pct, 4),
        "ftr": round(ftr, 4),
        "ortg": round(ortg, 1),
        "drtg": round(drtg, 1),
        "net_rating": round(net_rtg, 1),
        "pythagorean_win_pct": round(pyth_win_pct, 4),
    }

def compute_cohort_four_factors(teams_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computes cohort averages and percentiles for ranking teams across the Four Factors.
    """
    if not teams_data:
        return {}
    
    keys = ["efg_pct", "tov_pct", "orb_pct", "ftr", "ortg", "drtg", "net_rating", "pace"]
    cohort_stats: Dict[str, Any] = {}
    
    for k in keys:
        values = [t.get("four_factors", {}).get(k, 0.0) for t in teams_data if k in t.get("four_factors", {})]
        if values:
            cohort_stats[k] = {
                "mean": round(sum(values) / len(values), 3),
                "min": round(min(values), 3),
                "max": round(max(values), 3),
            }
            
    return cohort_stats
