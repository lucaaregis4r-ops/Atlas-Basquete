"""
FIBA Basketball Court Graphics and Spatial Analytics Generator.
Powered by mplbasketball (Maple Leaf Sports & Entertainment / MLSE) and Matplotlib.
"""
from typing import Dict, List, Any, Tuple
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mplbasketball.court import Court
import io

def generate_fiba_court_svg(
    court_color: str = "#0b0e15",
    paint_color: str = "#141c2c",
    line_color: str = "#94a3b8",
    line_width: float = 1.6,
    orientation: str = "vu"
) -> str:
    """
    Renders an official FIBA court SVG via mplbasketball.
    """
    c = Court(court_type="fiba", units="m", origin="center")
    fig, ax = c.draw(
        orientation=orientation,
        court_color=court_color,
        paint_color=paint_color,
        line_color=line_color,
        line_width=line_width,
        pad=1.2,
        hoop_alpha=1.0
    )
    
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", facecolor=court_color, edgecolor="none")
    plt.close(fig)
    return buf.getvalue()

def compute_hexbin_analytics(
    shots: List[Dict[str, Any]],
    gridsize: int = 14,
    min_count: int = 2
) -> List[Dict[str, Any]]:
    """
    Calculates 2D hexagonal bins across FIBA half-court.
    Computes attempt volume and points-per-shot efficiency surplus (Goldsberry SES).
    """
    if not shots:
        return []
        
    xs = np.array([s["x"] for s in shots])
    ys = np.array([s["y"] for s in shots])
    pts = np.array([s["pts"] for s in shots])
    
    # Half court FIBA bounds in meters: x in [-7.5, 7.5], y in [0, 14]
    fig, ax = plt.subplots()
    hb = ax.hexbin(xs, ys, gridsize=gridsize, extent=[-7.5, 7.5, 0, 14], mincnt=min_count)
    counts = hb.get_array()
    offsets = hb.get_offsets()
    plt.close(fig)
    
    # Baseline league average points per shot
    league_avg_pps = 1.02
    
    hexbins = []
    total_shots = len(shots)
    for (x, y), count in zip(offsets, counts):
        if count < min_count:
            continue
        # Find shots falling inside this bin radius
        dist = np.sqrt((xs - x)**2 + (ys - y)**2)
        in_bin = dist < 1.1
        bin_pts = pts[in_bin]
        pps = np.mean(bin_pts) if len(bin_pts) > 0 else 0.0
        ses = pps - league_avg_pps
        
        freq = count / total_shots
        # Radius scales with shot frequency (Kirk Goldsberry method)
        radius = min(0.65, max(0.20, float(0.20 + (count / np.max(counts)) * 0.45)))
        
        status = "hot" if ses >= 0.10 else ("cold" if ses <= -0.10 else "neutral")
        
        hexbins.append({
            "x": round(float(x), 2),
            "y": round(float(y), 2),
            "count": int(count),
            "freq": round(float(freq), 4),
            "pps": round(float(pps), 3),
            "ses": round(float(ses), 3),
            "radius": round(radius, 2),
            "status": status
        })
        
    return hexbins
