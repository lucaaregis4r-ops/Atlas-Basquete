"""
Spatial Shot Efficiency and FIBA Court Analytics.
References:
- Goldsberry, K. (2012). CourtVision: New visual and spatial analytics for basketball.
  MIT Sloan Sports Analytics Conference.
- Goldsberry, K. (2019). SprawlBall: A Visual Tour of the New Era of the NBA.
"""
from typing import Dict, List, Any, Tuple
import math
from cbb.config import (
    FIBA_COURT_WIDTH_M,
    FIBA_HALF_COURT_LENGTH_M,
    FIBA_RIM_DISTANCE_FROM_BASELINE_M,
    FIBA_THREE_POINT_ARC_RADIUS_M,
    FIBA_THREE_POINT_CORNER_DISTANCE_M,
    FIBA_CORNER_THREE_CUTOFF_M,
    FIBA_RESTRICTED_AREA_RADIUS_M,
    FIBA_KEY_WIDTH_M,
    FIBA_KEY_LENGTH_M
)

# Standard FIBA / CBB League Average Baselines by Zone
LEAGUE_ZONE_BENCHMARKS = {
    "Restricted Area (<1.25m)": {"fg_pct": 0.625, "pps": 1.250, "freq": 0.285},
    "Paint (Non-RA)":           {"fg_pct": 0.410, "pps": 0.820, "freq": 0.160},
    "Mid-Range Left":           {"fg_pct": 0.395, "pps": 0.790, "freq": 0.075},
    "Mid-Range Center":         {"fg_pct": 0.405, "pps": 0.810, "freq": 0.065},
    "Mid-Range Right":          {"fg_pct": 0.390, "pps": 0.780, "freq": 0.075},
    "Corner 3 Left":            {"fg_pct": 0.375, "pps": 1.125, "freq": 0.080},
    "Corner 3 Right":           {"fg_pct": 0.370, "pps": 1.110, "freq": 0.080},
    "Above Break 3 Left":       {"fg_pct": 0.345, "pps": 1.035, "freq": 0.090},
    "Above Break 3 Center":     {"fg_pct": 0.355, "pps": 1.065, "freq": 0.080},
    "Above Break 3 Right":      {"fg_pct": 0.340, "pps": 1.020, "freq": 0.090},
}

def classify_shot_zone(x_m: float, y_m: float) -> str:
    """
    Classifies a shot coordinate (x_m in [-7.5, 7.5], y_m in [0, 14.0])
    into standard FIBA shot zones.
    Center of rim is at (x=0, y=1.575).
    """
    rim_x = 0.0
    rim_y = FIBA_RIM_DISTANCE_FROM_BASELINE_M
    dist_from_rim = math.sqrt((x_m - rim_x)**2 + (y_m - rim_y)**2)
    
    # 1. Restricted Area (<1.25m from rim center)
    if dist_from_rim <= FIBA_RESTRICTED_AREA_RADIUS_M:
        return "Restricted Area (<1.25m)"
    
    # Check if 3-point attempt
    is_corner = (y_m <= FIBA_CORNER_THREE_CUTOFF_M) and (abs(x_m) >= FIBA_THREE_POINT_CORNER_DISTANCE_M)
    is_arc = (y_m > FIBA_CORNER_THREE_CUTOFF_M) and (dist_from_rim >= FIBA_THREE_POINT_ARC_RADIUS_M)
    
    if is_corner:
        return "Corner 3 Left" if x_m < 0 else "Corner 3 Right"
    elif is_arc:
        if x_m < -2.2:
            return "Above Break 3 Left"
        elif x_m > 2.2:
            return "Above Break 3 Right"
        else:
            return "Above Break 3 Center"
            
    # Inside 2-point zone
    # Paint (non-RA): inside key rectangle (|x| <= 2.45, y <= 5.80)
    in_paint = (abs(x_m) <= FIBA_KEY_WIDTH_M / 2.0) and (y_m <= FIBA_KEY_LENGTH_M)
    if in_paint:
        return "Paint (Non-RA)"
        
    # Mid-range
    if x_m < -2.2:
        return "Mid-Range Left"
    elif x_m > 2.2:
        return "Mid-Range Right"
    else:
        return "Mid-Range Center"

def compute_zone_efficiency(shots: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Aggregates shot events and computes spatial efficiency metrics by zone:
    - FGM, FGA, FG%
    - Frequency %
    - Points Per Shot (PPS)
    - Spatial Efficiency Surplus (SES) vs League Benchmark
    """
    zone_counts: Dict[str, Dict[str, int]] = {
        z: {"fga": 0, "fgm": 0, "pts": 0} for z in LEAGUE_ZONE_BENCHMARKS
    }
    
    total_fga = len(shots)
    for s in shots:
        z = s.get("zone")
        if not z:
            x = s.get("x", 0.0)
            y = s.get("y", 0.0)
            z = classify_shot_zone(x, y)
        if z in zone_counts:
            zone_counts[z]["fga"] += 1
            if s.get("made", False):
                pts_val = 3 if "3" in z else 2
                zone_counts[z]["fgm"] += 1
                zone_counts[z]["pts"] += pts_val

    results: Dict[str, Any] = {}
    for z, benchmark in LEAGUE_ZONE_BENCHMARKS.items():
        fga = zone_counts[z]["fga"]
        fgm = zone_counts[z]["fgm"]
        pts = zone_counts[z]["pts"]
        
        fg_pct = fgm / fga if fga > 0 else 0.0
        freq = fga / total_fga if total_fga > 0 else 0.0
        pps = pts / fga if fga > 0 else 0.0
        ses = pps - benchmark["pps"] if fga > 0 else 0.0
        
        # Color status based on Goldsberry SES:
        # hot (> +0.10 pps), neutral (-0.10 to +0.10), cold (< -0.10)
        status = "hot" if ses >= 0.10 else ("cold" if ses <= -0.10 else "neutral")
        
        results[z] = {
            "fga": fga,
            "fgm": fgm,
            "pts": pts,
            "fg_pct": round(fg_pct, 4),
            "freq": round(freq, 4),
            "pps": round(pps, 3),
            "league_pps": benchmark["pps"],
            "league_fg_pct": benchmark["fg_pct"],
            "ses": round(ses, 3),
            "status": status,
        }
        
    return results
