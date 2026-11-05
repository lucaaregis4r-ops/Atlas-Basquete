"""
Parser and Extractor for Brazilian League (CBB / NBB) Match Reports and Box Scores.
Parses the official FIBA 17-column box score table.
"""
import re
import urllib.request
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
from cbb.analysis.four_factors import compute_four_factors
from cbb.analysis.player_advanced import compute_player_advanced_metrics

def parse_stat_split(text: str) -> tuple[int, int]:
    """
    Parses 'C/T' format like '5/9' or '12/20' or '0/0' -> (5, 9).
    """
    if not text:
        return 0, 0
    match = re.search(r"(\d+)\s*/\s*(\d+)", text)
    if match:
        return int(match.group(1)), int(match.group(2))
    digits = re.findall(r"\d+", text)
    if digits:
        return int(digits[0]), int(digits[0])
    return 0, 0

def parse_rebounds_split(text: str) -> tuple[int, int, int]:
    """
    Parses 'RO+RD RT' format like '2+5 7' -> (2, 5, 7).
    """
    match = re.search(r"(\d+)\s*\+\s*(\d+)\s+(\d+)", text)
    if match:
        return int(match.group(1)), int(match.group(2)), int(match.group(3))
    digits = [int(d) for d in re.findall(r"\d+", text)]
    if len(digits) >= 3:
        return digits[0], digits[1], digits[2]
    elif len(digits) == 1:
        return 0, digits[0], digits[0]
    return 0, 0, 0

def parse_minutes(text: str) -> float:
    """
    Parses '28:35' -> 28.58 minutes.
    """
    parts = text.strip().split(":")
    if len(parts) == 2:
        try:
            return round(float(parts[0]) + float(parts[1]) / 60.0, 2)
        except ValueError:
            return 0.0
    try:
        return float(text)
    except ValueError:
        return 0.0

def parse_html_boxscore(html_content: str, match_id: str, team_home: str, team_away: str) -> Dict[str, Any]:
    """
    Parses raw match HTML containing 'real_time_table_stats tablesorter' tables.
    Returns structured team and player records.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    tables = soup.find_all("table", class_=re.compile("real_time_table_stats"))
    
    players: List[Dict[str, Any]] = []
    teams_stats = {
        team_home: {"is_home": True, "pts": 0, "fgm": 0, "fga": 0, "fg3m": 0, "fg3a": 0, "ftm": 0, "fta": 0, "orb": 0, "drb": 0, "trb": 0, "ast": 0, "stl": 0, "blk": 0, "tov": 0, "pf": 0, "fd": 0},
        team_away: {"is_home": False, "pts": 0, "fgm": 0, "fga": 0, "fg3m": 0, "fg3a": 0, "ftm": 0, "fta": 0, "orb": 0, "drb": 0, "trb": 0, "ast": 0, "stl": 0, "blk": 0, "tov": 0, "pf": 0, "fd": 0}
    }
    
    assigned_teams = [team_home, team_away]
    for idx, table in enumerate(tables[:2]):
        current_team = assigned_teams[idx] if idx < len(assigned_teams) else f"Time_{idx}"
        tbody = table.find("tbody")
        if not tbody:
            continue
            
        for row in tbody.find_all("tr"):
            cols = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
            if len(cols) < 10 or "Total" in cols[1]:
                continue
                
            number = cols[0]
            name = cols[1]
            mp = parse_minutes(cols[2])
            
            # Pts
            pts_val = int(re.search(r"^\d+", cols[3]).group(0)) if re.search(r"^\d+", cols[3]) else 0
            # 3P
            fg3m, fg3a = parse_stat_split(cols[4])
            # 2P
            fg2m, fg2a = parse_stat_split(cols[5])
            # LL
            ftm, fta = parse_stat_split(cols[6])
            
            fgm = fg2m + fg3m
            fga = fg2a + fg3a
            
            # Rebounds
            orb, drb, trb = parse_rebounds_split(cols[7])
            
            # Counting stats
            ast = int(cols[8]) if len(cols) > 8 and cols[8].isdigit() else 0
            stl = int(cols[9]) if len(cols) > 9 and cols[9].isdigit() else 0
            blk = int(cols[10]) if len(cols) > 10 and cols[10].isdigit() else 0
            pf = int(cols[11]) if len(cols) > 11 and cols[11].isdigit() else 0
            fd = int(cols[12]) if len(cols) > 12 and cols[12].isdigit() else 0
            tov = int(cols[13]) if len(cols) > 13 and cols[13].isdigit() else 0
            dunks = int(cols[14]) if len(cols) > 14 and cols[14].isdigit() else 0
            plus_minus = int(cols[15].replace("+", "")) if len(cols) > 15 and re.search(r"[+-]?\d+", cols[15]) else 0
            fiba_pir = float(cols[16]) if len(cols) > 16 and re.search(r"[+-]?\d+", cols[16]) else 0.0
            
            p_metrics = compute_player_advanced_metrics(
                pts=pts_val, fga=fga, fgm=fgm, fg3a=fg3a, fg3m=fg3m,
                fta=fta, ftm=ftm, orb=orb, drb=drb, trb=trb,
                ast=ast, stl=stl, blk=blk, tov=tov, pf=pf, fd=fd, mp=mp
            )
            
            player_record = {
                "id": f"{match_id}_{name.replace(' ', '_')}",
                "match_id": match_id,
                "player_name": name,
                "team_name": current_team,
                "number": number,
                "min_played": mp,
                "pts": pts_val,
                "fgm": fgm,
                "fga": fga,
                "fg3m": fg3m,
                "fg3a": fg3a,
                "ftm": ftm,
                "fta": fta,
                "orb": orb,
                "drb": drb,
                "trb": trb,
                "ast": ast,
                "stl": stl,
                "blk": blk,
                "tov": tov,
                "pf": pf,
                "fd": fd,
                "dunks": dunks,
                "plus_minus": plus_minus,
                "fiba_pir": p_metrics["fiba_pir"],
                "game_score": p_metrics["game_score"],
                "ts_pct": p_metrics["ts_pct"],
                "usg_pct": p_metrics["usg_pct"]
            }
            players.append(player_record)
            
            # Aggregate to team
            if current_team in teams_stats:
                t = teams_stats[current_team]
                t["pts"] += pts_val
                t["fgm"] += fgm
                t["fga"] += fga
                t["fg3m"] += fg3m
                t["fg3a"] += fg3a
                t["ftm"] += ftm
                t["fta"] += fta
                t["orb"] += orb
                t["drb"] += drb
                t["trb"] += trb
                t["ast"] += ast
                t["stl"] += stl
                t["blk"] += blk
                t["tov"] += tov
                t["pf"] += pf
                t["fd"] += fd

    # Compute team Four Factors
    team_results = []
    for t_name in [team_home, team_away]:
        opp_name = team_away if t_name == team_home else team_home
        t_data = teams_stats.get(t_name, {})
        opp_data = teams_stats.get(opp_name, {})
        
        ff = compute_four_factors(
            fgm=t_data.get("fgm", 0), fga=t_data.get("fga", 0), fg3m=t_data.get("fg3m", 0),
            ftm=t_data.get("ftm", 0), fta=t_data.get("fta", 0),
            orb=t_data.get("orb", 0), opp_drb=opp_data.get("drb", 0),
            tov=t_data.get("tov", 0),
            pts=t_data.get("pts", 0), opp_pts=opp_data.get("pts", 0)
        )
        t_data.update(ff)
        t_data["match_id"] = match_id
        t_data["team_name"] = t_name
        team_results.append(t_data)
        
    return {
        "match_id": match_id,
        "team_home": team_home,
        "team_away": team_away,
        "team_stats": team_results,
        "players": players
    }
