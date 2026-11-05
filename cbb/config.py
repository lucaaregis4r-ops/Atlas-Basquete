"""
Configuration and constants for Basquete BR — Atlas Tático.
Follows FIBA official court rules and modern basketball research standards.
"""
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
EXPORTS_DIR = BASE_DIR / "docs" / "exports"
LOCAL_EXPORTS_DIR = BASE_DIR / "exports"
DOCS_DIR = BASE_DIR / "docs"

# Database
DB_PATH = os.getenv("CBB_DB_PATH", str(DATA_DIR / "basquete_atlas.duckdb"))

# Remote Endpoints
CBB_ARCHIVE_URL = "https://www.cbbarchive.online"
CBB_OFFICIAL_URL = "https://www.cbb.com.br"
LNB_URL = "https://lnb.com.br"

# FIBA Standard Regulations (28.0m x 15.0m Court)
FIBA_COURT_LENGTH_M = 28.0
FIBA_COURT_WIDTH_M = 15.0
FIBA_HALF_COURT_LENGTH_M = 14.0
FIBA_RIM_HEIGHT_M = 3.05
FIBA_RIM_DISTANCE_FROM_BASELINE_M = 1.575
FIBA_THREE_POINT_ARC_RADIUS_M = 6.75
FIBA_THREE_POINT_CORNER_DISTANCE_M = 6.60
FIBA_CORNER_THREE_CUTOFF_M = 2.99
FIBA_RESTRICTED_AREA_RADIUS_M = 1.25
FIBA_KEY_WIDTH_M = 4.90
FIBA_KEY_LENGTH_M = 5.80
FIBA_FREE_THROW_LINE_M = 5.80
FIBA_CENTER_CIRCLE_RADIUS_M = 1.80

# Basketball Analytics Constants
FIBA_GAME_MINUTES = 40.0
NBA_GAME_MINUTES = 48.0
PYTHAGOREAN_EXPONENT = 13.91  # Daryl Morey / Dean Oliver basketball exponent
FTA_POSSESSION_WEIGHT = 0.44  # Kubatko, Oliver et al. (2007)

# Shot Zones
SHOT_ZONES = [
    "Restricted Area (<1.25m)",
    "Paint (Non-RA)",
    "Mid-Range Left",
    "Mid-Range Center",
    "Mid-Range Right",
    "Corner 3 Left",
    "Corner 3 Right",
    "Above Break 3 Left",
    "Above Break 3 Center",
    "Above Break 3 Right",
]
