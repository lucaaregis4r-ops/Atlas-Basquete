"""
DuckDB repository for Basquete BR — Atlas Tático.
"""
from pathlib import Path
import duckdb
from typing import Dict, List, Any, Optional
import json
import hashlib
from cbb.config import DB_PATH, DATA_DIR

class DatabaseRepository:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.init_schema()

    def get_connection(self):
        return duckdb.connect(self.db_path)

    def init_schema(self):
        schema_file = Path(__file__).parent / "schema.sql"
        if schema_file.exists():
            sql = schema_file.read_text(encoding="utf-8")
            with self.get_connection() as conn:
                conn.execute(sql)

    def log_audit(self, source: str, records_count: int, payload: Any, status: str = "SUCCESS"):
        raw_bytes = json.dumps(payload, default=str).encode("utf-8")
        p_hash = hashlib.sha256(raw_bytes).hexdigest()
        event_id = f"aud_{p_hash[:12]}"
        with self.get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO audit_log (event_id, source, records_count, payload_hash, status)
                VALUES (?, ?, ?, ?, ?)
            """, [event_id, source, records_count, p_hash, status])

    def upsert_matches(self, matches: List[Dict[str, Any]]):
        with self.get_connection() as conn:
            for m in matches:
                conn.execute("""
                    INSERT OR REPLACE INTO matches (
                        match_id, competition, season, match_date, phase,
                        team_home, team_away, score_home, score_away, validation_status, source_url, raw_hash
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, [
                    m["match_id"], m.get("competition", "CBB/NBB"), m.get("season", "2026-2027"),
                    m.get("match_date"), m.get("phase", "Fase Regular"),
                    m["team_home"], m["team_away"], m.get("score_home", 0), m.get("score_away", 0),
                    m.get("validation_status", "VALID"), m.get("source_url", ""), m.get("raw_hash", "")
                ])

    def upsert_team_boxscore(self, box: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO team_boxscores (
                    match_id, team_name, season, is_home, pts, fgm, fga, fg3m, fg3a, ftm, fta,
                    orb, drb, trb, ast, stl, blk, tov, pf, fd,
                    possessions, pace, ortg, drtg, net_rating, efg_pct, tov_pct, orb_pct, ftr
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                box["match_id"], box["team_name"], box.get("season", "2026-2027"), box["is_home"],
                box.get("pts", 0), box.get("fgm", 0), box.get("fga", 0),
                box.get("fg3m", 0), box.get("fg3a", 0), box.get("ftm", 0), box.get("fta", 0),
                box.get("orb", 0), box.get("drb", 0), box.get("trb", 0),
                box.get("ast", 0), box.get("stl", 0), box.get("blk", 0),
                box.get("tov", 0), box.get("pf", 0), box.get("fd", 0),
                box.get("possessions", 0.0), box.get("pace", 0.0),
                box.get("ortg", 0.0), box.get("drtg", 0.0), box.get("net_rating", 0.0),
                box.get("efg_pct", 0.0), box.get("tov_pct", 0.0), box.get("orb_pct", 0.0), box.get("ftr", 0.0)
            ])

    def upsert_player_boxscores(self, players: List[Dict[str, Any]]):
        with self.get_connection() as conn:
            for p in players:
                conn.execute("""
                    INSERT OR REPLACE INTO player_boxscores (
                        id, match_id, player_name, team_name, season, number, position, min_played,
                        pts, fgm, fga, fg3m, fg3a, ftm, fta, orb, drb, trb,
                        ast, stl, blk, tov, pf, fd, dunks, plus_minus, fiba_pir, game_score, ts_pct, usg_pct
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, [
                    p["id"], p["match_id"], p["player_name"], p["team_name"],
                    p.get("season", "2026-2027"),
                    p.get("number", ""), p.get("position", "G"), p.get("min_played", 0.0),
                    p.get("pts", 0), p.get("fgm", 0), p.get("fga", 0),
                    p.get("fg3m", 0), p.get("fg3a", 0), p.get("ftm", 0), p.get("fta", 0),
                    p.get("orb", 0), p.get("drb", 0), p.get("trb", 0),
                    p.get("ast", 0), p.get("stl", 0), p.get("blk", 0),
                    p.get("tov", 0), p.get("pf", 0), p.get("fd", 0),
                    p.get("dunks", 0), p.get("plus_minus", 0),
                    p.get("fiba_pir", 0.0), p.get("game_score", 0.0),
                    p.get("ts_pct", 0.0), p.get("usg_pct", 0.0)
                ])

    def upsert_shot_events(self, shots: List[Dict[str, Any]]):
        with self.get_connection() as conn:
            for s in shots:
                conn.execute("""
                    INSERT OR REPLACE INTO shot_events (
                        shot_id, match_id, team_name, player_name, season, period, clock_seconds,
                        x_m, y_m, zone, made, points_value
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, [
                    s["shot_id"], s["match_id"], s["team_name"], s["player_name"],
                    s.get("season", "2026-2027"),
                    s.get("period", 1), s.get("clock_seconds", 0),
                    s.get("x_m", 0.0), s.get("y_m", 0.0), s.get("zone", ""),
                    s.get("made", False), s.get("points_value", 2)
                ])

    def query_all(self, query: str, params: Optional[List[Any]] = None) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            res = conn.execute(query, params or []).fetchdf()
            return json.loads(res.to_json(orient="records", date_format="iso"))

default_repo = DatabaseRepository()
