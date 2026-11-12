"""Collect the recorded events and field-goal markers in public LNB reports."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from urllib.parse import urlencode, urljoin, urlparse
import json
from pathlib import Path
import re
from tempfile import NamedTemporaryFile
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from cbb.config import BASE_DIR, EXPORTS_DIR


SOURCES_PATH = BASE_DIR / "data" / "nbb_pilot_sources.json"
SNAPSHOT_PATH = EXPORTS_DIR / "nbb_observed.json"


def _coordinates(style):
    position = {}
    for axis, value in re.findall(r"(top|left):\s*(\d+(?:\.\d+)?)\s*%", style):
        position[axis] = float(value)
    if len(position) == 2 and all(0 <= value <= 100 for value in position.values()):
        return [position["left"], position["top"]]
    return [None, None]


def parse_report(game, html):
    soup = BeautifulSoup(html, "html.parser")
    events = soup.select("#movethemove .move_action_scroll .move_action")
    periods = {tag.get_text(strip=True) for tag in soup.select("#movethemove .move_action .quarter")}
    final_score = events[0].select_one(".points") if events else None
    score = [int(part) for part in re.findall(r"\d+", final_score.get_text())] if final_score else []
    event_count = len(events) if {"1", "2", "3", "4"} <= periods and score == game["score"] else None

    rosters = [
        {
            item["idj"]: name.get_text(" ", strip=True)
            for item in soup.select(f".quadra .players_block_{side} li[idj]")
            if (name := item.select_one(".name"))
        }
        for side in ("left", "right")
    ]
    players = {}
    shots = []
    for marker in soup.select(".graphic_gym li[idj][idp][ide]"):
        classes = marker.get("class", [])
        point_value = next((value for value in (2, 3) if f"{value}pt" in classes), None)
        if point_value is None or marker["ide"] not in {"1", "2"} or not marker["idp"].isdigit():
            continue
        if ("correct" in classes) == ("incorrect" in classes):
            continue
        team = int(marker["ide"]) - 1
        player_id = marker["idj"]
        if player_id not in rosters[team]:
            continue
        players[player_id] = rosters[team][player_id]
        shots.append([
            team, player_id, int(marker["idp"]), point_value, int("correct" in classes),
            *_coordinates(marker.get("style", "")),
        ])

    boxscore = []
    for side in ("home", "away"):
        totals = [0, 0, 0, 0]
        rows = soup.select(f'#team_{side}_stats table[idx="general"] tbody tr')
        has_stats = False
        for row in rows:
            cells = [cell.get_text(strip=True) for cell in row.find_all("td", recursive=False)]
            if len(cells) < 9 or not cells[0].startswith("#"):
                continue
            splits = [re.match(r"(\d+)/(\d+)", cells[index]) for index in (8, 7)]
            if all(splits):
                has_stats = True
                totals = [
                    total + int(count)
                    for total, count in zip(totals, splits[0].groups() + splits[1].groups())
                ]
        boxscore.append(totals if has_stats else None)

    if all(boxscore):
        observed = Counter((shot[0], shot[3]) for shot in shots)
        expected = Counter({
            (team, points): boxscore[team][index]
            for team in (0, 1) for points, index in ((2, 1), (3, 3))
        })
        if observed != expected:
            players, shots = {}, []

    return {**game, "play_by_play_events": event_count, "boxscore": boxscore, "players": players, "shots": shots}


TABLES = {
    "NBB": "https://lnb.com.br/nbb/tabela-de-jogos/",
    "LDB": "https://lnb.com.br/ldb/tabela-de-jogos/",
}
PLAYER_TABLES = {
    "NBB": "https://lnb.com.br/nbb/estatisticas/arremessos/",
    "LDB": "https://lnb.com.br/ldb/estatisticas/arremessos/",
}


def fetch_url(url):
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != "lnb.com.br":
        raise ValueError("Apenas fontes oficiais da LNB são aceitas")
    request = Request(url, headers={"User-Agent": "Atlas Basquete / pesquisa pública"})
    with urlopen(request, timeout=25) as response:
        return response.read()


def parse_schedule(html, competition):
    """Read completed games from an official LNB schedule, not future fixtures."""
    soup = BeautifulSoup(html, "html.parser")
    games = []
    for row in soup.select("tr"):
        id_cell = row.select_one("td.position_value[data-real-id]")
        score = row.select_one("td.score_value a.match_score_relatorio")
        home = row.select_one("td.home_team_value .team-shortname")
        away = row.select_one("td.visitor_team_value .team-shortname")
        date = row.select_one("td.date_value span")
        season = row.select_one("td.champ_value")
        if not all((id_cell, score, home, away, date, season)):
            continue
        home_score, away_score = score.select_one("span.home"), score.select_one("span.away")
        if not home_score or not away_score:
            continue
        a, b = home_score.get_text(strip=True), away_score.get_text(strip=True)
        if not a.isdigit() or not b.isdigit() or (int(a) == 0 and int(b) == 0):
            continue
        try:
            day = datetime.strptime(date.get_text(strip=True), "%d/%m/%Y").date().isoformat()
        except ValueError:
            continue
        raw_href = (score.get("href") or "").strip()
        report_available = bool(raw_href and raw_href != "#")
        href = urljoin(TABLES[competition], raw_href if report_available else "")
        if urlparse(href).hostname != "lnb.com.br":
            href, report_available = TABLES[competition], False
        identifier = id_cell.get("data-real-id", "").strip()
        if not identifier or not home.get_text(strip=True) or not away.get_text(strip=True):
            continue
        games.append({"id": identifier, "competition": competition,
                      "season": season.get_text(strip=True).replace("/", "-"),
                      "date": day, "teams": [home.get_text(" ", strip=True), away.get_text(" ", strip=True)],
                      "score": [int(a), int(b)], "url": href, "report_available": report_available})
    return games


def season_urls(html, competition):
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    for item in soup.select('input[name="season[]"]'):
        label = item.find_parent("label") or item.parent
        title = label.get_text(" ", strip=True) if label else ""
        value = item.get("value", "")
        if title.upper().startswith(competition + " ") and value.isdigit():
            urls.append(TABLES[competition] + "?" + urlencode({"season[0]": value}))
    return list(dict.fromkeys(urls))


def parse_season_players(html, competition, source_url):
    """Read the official season-level per-game averages as published by the LNB."""
    soup = BeautifulSoup(html, "html.parser")
    selected = soup.select_one('input[name="season[]"][checked]')
    label = (selected.find_parent("label") or selected.parent.find("label", attrs={"for": selected.get("id")})) if selected else None
    season_text = label.get_text(" ", strip=True) if label else ""
    match = re.search(r"\b(\d{4}(?:/\d{4})?)\b", season_text)
    table = soup.select_one("table")
    if not match or not season_text.upper().startswith(competition + " ") or not table:
        raise ValueError("temporada ou tabela de atletas não reconhecida")
    headers = [th.get_text(" ", strip=True) for th in table.select("thead th")]
    required = ["Jogador", "Equipe", "JO", "Min", "PTS", "3PC", "3PT", "3P%", "2PC", "2PT", "2P%", "LLC", "LLT", "LL%"]
    if any(key not in headers for key in required):
        raise ValueError("colunas oficiais de arremessos não reconhecidas")
    index = {key: headers.index(key) for key in required}
    def number(text):
        text = text.strip().replace(",", ".")
        try:
            value = float(text)
            return value if value >= 0 and value != float("inf") else None
        except ValueError:
            return None
    players = []
    for row in table.select("tbody tr"):
        cells = row.find_all("td", recursive=False)
        if len(cells) <= max(index.values()):
            continue
        athlete = cells[index["Jogador"]].select_one("a[href]")
        team = cells[index["Equipe"]].get_text(" ", strip=True)
        if not athlete or not team:
            continue
        name = athlete.get_text(" ", strip=True)
        stats = {key: number(cells[index[key]].get_text(" ", strip=True)) for key in required[2:]}
        if stats["JO"] is None or stats["JO"] <= 0:
            continue
        url = urljoin(source_url, athlete.get("href", ""))
        if urlparse(url).hostname != "lnb.com.br":
            continue
        players.append({"name": name, "team": team, "url": url,
                        "games": int(stats["JO"]), "minutes_pg": stats["Min"], "points_pg": stats["PTS"],
                        "three_made_pg": stats["3PC"], "three_attempted_pg": stats["3PT"], "three_pct": stats["3P%"],
                        "two_made_pg": stats["2PC"], "two_attempted_pg": stats["2PT"], "two_pct": stats["2P%"],
                        "ft_made_pg": stats["LLC"], "ft_attempted_pg": stats["LLT"], "ft_pct": stats["LL%"]})
    if not players:
        raise ValueError("nenhuma linha de atleta reconhecida")
    return {"competition": competition, "season": match.group(1).replace("/", "-"),
            "source_url": source_url, "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "players": players}


def refresh_player_stats(snapshot, include_history=False, max_history=None):
    previous = {(item.get("competition"), item.get("season")): item for item in snapshot.get("season_player_stats", [])}
    urls = [(code, url) for code, url in PLAYER_TABLES.items()]
    failures = []
    attempted = set(snapshot.get("player_stats_attempted", []))
    history = []
    if include_history:
        for code, table_url in TABLES.items():
            try:
                for season_url in season_urls(fetch_url(table_url), code):
                    url = PLAYER_TABLES[code] + ("?" + urlparse(season_url).query if urlparse(season_url).query else "")
                    if url not in attempted:
                        history.append((code, url))
            except Exception as error:
                failures.append({"source": table_url, "error": str(error)})
    history = list(dict.fromkeys(history))
    if max_history is not None:
        history = history[:max_history]
    urls = list(dict.fromkeys(urls + history))
    def load(item):
        competition, url = item
        try:
            return parse_season_players(fetch_url(url), competition, url), None
        except Exception as error:
            return None, {"source": url, "error": str(error)}
    # Season tables are large HTML documents. Process them one at a time so
    # historical backfills stay within the memory limits of small runners.
    for item in urls:
        record, failure = load(item)
        if item in history:
            attempted.add(item[1])
        if record:
            previous[(record["competition"], record["season"])] = record
        if failure:
            failures.append(failure)
    snapshot["season_player_stats"] = sorted(previous.values(), key=lambda x: (x["competition"], x["season"]), reverse=True)
    snapshot["player_stats_failures"] = failures
    snapshot["player_stats_attempted"] = sorted(attempted)
    return snapshot


def _empty_report(game):
    return {**game, "play_by_play_events": None, "boxscore": [None, None], "players": {}, "shots": []}


def refresh_snapshot(cache_dir=None, include_history=False, max_reports=80):
    previous = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8")) if SNAPSHOT_PATH.exists() else {"games": []}
    prior = {str(g["id"]): g for g in previous.get("games", [])}
    discovered, failures, archive_urls = [], [], []
    if cache_dir:
        discovered = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))
    else:
        for competition, url in TABLES.items():
            try:
                html = fetch_url(url)
                found = parse_schedule(html, competition)
                if not found:
                    raise ValueError("tabela sem jogos finalizados reconhecíveis")
                discovered.extend(found)
                if include_history:
                    archive_urls.extend((competition, u) for u in season_urls(html, competition))
            except Exception as error:
                failures.append({"source": url, "error": str(error)})
        if archive_urls:
            def read_archive(item):
                competition, url = item
                try:
                    games = parse_schedule(fetch_url(url), competition)
                    if not games:
                        return [], {"source": url, "error": "tabela sem resultados reconhecíveis"}
                    return games, None
                except Exception as error:
                    return [], {"source": url, "error": str(error)}
            with ThreadPoolExecutor(max_workers=3) as pool:
                for found, error in pool.map(read_archive, archive_urls):
                    discovered.extend(found)
                    if error:
                        failures.append(error)
    if not discovered and not prior:
        raise ValueError("Nenhuma tabela LNB disponível; snapshot existente preservado")
    # Existing historical games are retained even if a single table is unavailable.
    games = {key: {**game, "competition": game.get("competition", "NBB")} for key, game in prior.items()}
    for game in discovered:
        game = {**game, "competition": game.get("competition", "NBB")}
        key = str(game["id"])
        old = games.get(key, {})
        same = old.get("score") == game["score"] and old.get("teams") == game["teams"]
        if same:
            merged = {**old, **game}
            merged.setdefault("play_by_play_events", None); merged.setdefault("boxscore", [None, None])
            merged.setdefault("players", {}); merged.setdefault("shots", [])
            games[key] = merged
        else:
            games[key] = _empty_report(game)
    # Older failures remain retryable but do not block new games forever.
    def has_report(g):
        return bool(g.get("report_checked_at") or g.get("shots") or g.get("play_by_play_events") is not None or any(g.get("boxscore") or []))
    candidates = sorted(games.values(), key=lambda g: (has_report(g),
                        g.get("report_checked_at") or "", -(int(g.get("date", "0000-00-00").replace("-", "") or 0))))
    candidates = [g for g in candidates if g.get("report_available", True) and (not has_report(g) or g.get("report_error"))]
    candidates = candidates[:max(0, max_reports)]
    def read_report(game):
        try:
            html = (cache_dir / (game["id"] + ".html")).read_bytes() if cache_dir else fetch_url(game["url"])
            report = parse_report(game, html)
            # Keep previously validated data when a source page temporarily regresses.
            for field in ("shots", "players", "boxscore", "play_by_play_events"):
                old = game.get(field)
                new = report.get(field)
                if old and (not new or (field == "boxscore" and not any(new))):
                    report[field] = old
            report["report_checked_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
            report.pop("report_error", None)
            return report
        except Exception as error:
            return {**game, "report_checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "report_error": str(error)}
    season_stats = refresh_player_stats({"season_player_stats": previous.get("season_player_stats", []), "player_stats_attempted": previous.get("player_stats_attempted", [])}, include_history=True, max_history=None if include_history else 2)
    def write_snapshot():
        records = sorted(games.values(), key=lambda g: (g.get("date", ""), str(g["id"])))
        coverage = {"games": len(records), "reports_checked": sum(has_report(g) for g in records),
                    "with_play_by_play": sum(g.get("play_by_play_events") is not None for g in records),
                    "with_shots": sum(bool(g.get("shots")) for g in records),
                    "with_boxscore": sum(any(g.get("boxscore") or []) for g in records),
                    "failed_reports": sum(bool(g.get("report_error")) for g in records)}
        payload = {"source": "Liga Nacional de Basquete", "competition": "NBB e LDB", "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "coverage": coverage, "discovery_failures": failures, "season_player_stats": season_stats["season_player_stats"], "player_stats_failures": season_stats["player_stats_failures"], "player_stats_attempted": season_stats["player_stats_attempted"], "games": records}
        SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile(mode="w", encoding="utf-8", dir=SNAPSHOT_PATH.parent, delete=False) as output:
            output.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n")
        Path(output.name).replace(SNAPSHOT_PATH)
        return payload
    write_snapshot()  # Results become durable before report downloads begin.
    with ThreadPoolExecutor(max_workers=3) as pool:
        for index, report in enumerate(pool.map(read_report, candidates), 1):
            games[str(report["id"])] = report
            if index % 20 == 0:
                write_snapshot()
                print(f"LNB: {index}/{len(candidates)} relatórios processados", flush=True)
    return write_snapshot()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Atualiza jogos e relatórios oficiais NBB e LDB")
    parser.add_argument("--cache-dir", type=Path, help="Diretório de relatórios HTML, nomeados pelo ID LNB")
    parser.add_argument("--all-seasons", action="store_true", help="Descobre temporadas históricas disponíveis")
    parser.add_argument("--max-reports", type=int, default=80, help="Limite de relatórios a consultar nesta execução")
    parser.add_argument("--player-stats-only", action="store_true", help="Atualiza somente as médias oficiais de atletas")
    args = parser.parse_args()
    if args.player_stats_only:
        result = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
        refresh_player_stats(result, include_history=args.all_seasons)
        with NamedTemporaryFile(mode="w", encoding="utf-8", dir=SNAPSHOT_PATH.parent, delete=False) as output:
            output.write(json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n")
        Path(output.name).replace(SNAPSHOT_PATH)
    else:
        result = refresh_snapshot(args.cache_dir, include_history=args.all_seasons, max_reports=args.max_reports)
    print("LNB:", result["coverage"], "falhas nas tabelas:", len(result["discovery_failures"]))
