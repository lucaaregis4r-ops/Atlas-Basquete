"""Collect public CBI tournament schedules and results from Go Champs/CBB."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from tempfile import NamedTemporaryFile
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen

from cbb.config import BASE_DIR, EXPORTS_DIR


HUB_URL = "https://go-champs.com/cbb"
SNAPSHOT_PATH = EXPORTS_DIR / "cbi_observed.json"
USER_AGENT = "Atlas Basquete/1.0 (public CBI schedules and results)"
COMPETITION_LABELS = {
    "sub15final": "CBI Super 15 Masculino · Fase final",
    "super15a": "CBI Super 15 Masculino · Classificatória A",
    "super15b": "CBI Super 15 Masculino · Classificatória B",
    "sub17final": "CBI Sub-17 Masculino · Fase final",
    "cbi-es": "CBI Sub-17 Masculino · Classificatória A",
    "cbi-pr": "CBI Sub-17 Masculino · Classificatória B",
    "cbisub17f": "CBI Sub-17 Feminino",
    "cbisub15f": "CBI Sub-15 Feminino",
    "cbi": "CBI Sub-19 Masculino · Fase final",
    "cbisub19": "CBI Sub-19 Masculino · Classificatória B",
    "cbisub19f": "CBI Sub-19 Feminino",
    "sub23": "CBI Sub-23 Feminino",
}


class _LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[str] = []
        self.stages: list[str] = []
        self.stats: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href", "")
            if re.fullmatch(r"/cbb/[a-zA-Z0-9_-]+", href):
                self.links.append("https://go-champs.com" + href)
            elif re.fullmatch(r"/cbb/[a-zA-Z0-9_-]+/stage/[a-f0-9-]+", href, re.I):
                self.stages.append("https://go-champs.com" + href)
            elif re.fullmatch(r"/cbb/[a-zA-Z0-9_-]+/stats", href, re.I):
                self.stats.append("https://go-champs.com" + href)


def _fetch(url: str) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=15) as response:
        return response.read().decode("utf-8", errors="replace")


def _next_data(html: str) -> str:
    # Next.js streams server-rendered props as escaped strings. Decode each
    # string first so that the embedded days/games value is ordinary JSON.
    chunks = [
        json.loads(match.group(1))
        for match in re.finditer(
            r'self\.__next_f\.push\(\[1,("(?:\\.|[^"\\])*")\]\)', html
        )
    ]
    return "\n".join(chunks)


def parse_tournament(url: str, html: str, base_url: str | None = None) -> dict:
    data = _next_data(html)
    start = data.find('"days":')
    if start < 0:
        raise ValueError(f"No public game schedule found at {url}")
    days, _ = json.JSONDecoder().raw_decode(data[start + len('"days":'):])
    title_match = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    source_title = re.sub(r"\s+\|\s+Go Champs\s*$", "", title_match.group(1).strip()) if title_match else url.rsplit("/", 1)[-1]
    slug = (base_url or url).rstrip("/").rsplit("/", 1)[-1]
    title = COMPETITION_LABELS.get(slug, source_title)

    games = []
    teams = {}
    for day in days:
        for game in day.get("games", []):
            home, away = game.get("homeTeam") or {}, game.get("awayTeam") or {}
            if not home.get("name") or not away.get("name"):
                continue
            for team in (home, away):
                teams[team.get("id", team["name"])] = {
                    "id": team.get("id"),
                    "name": team["name"].strip(),
                    "short_name": team.get("triCode", ""),
                    "logo_url": team.get("logoUrl"),
                }
            games.append({
                "id": game["id"],
                "date": (game.get("datetime") or day.get("key", ""))[:10],
                "time_utc": game.get("datetime"),
                "venue": game.get("location", ""),
                "home_team": home["name"].strip(),
                "away_team": away["name"].strip(),
                "home_short_name": home.get("triCode", ""),
                "away_short_name": away.get("triCode", ""),
                "home_score": game.get("homeScore"),
                "away_score": game.get("awayScore"),
                "status": game.get("liveState", "not_started"),
                "is_finished": bool(game.get("isFinished")),
                "url": f"{(base_url or url).rstrip('/')}/game/{game['id']}",
                "stage": title,
            })
    if not games:
        raise ValueError(f"Schedule at {url} contains no games")
    return {
        "id": url.rstrip("/").rsplit("/", 1)[-1],
        "name": title,
        "source_title": source_title,
        "url": url,
        "stats_url": None,
        "teams": sorted(teams.values(), key=lambda team: team["name"].casefold()),
        "games": sorted(games, key=lambda game: (game["date"], game["time_utc"] or "", game["id"])),
    }


def refresh_snapshot(cache_dir: Path | None = None) -> dict:
    hub = (cache_dir / "hub.html").read_text(encoding="utf-8") if cache_dir else _fetch(HUB_URL)
    parser = _LinkParser()
    parser.feed(hub)
    links = list(dict.fromkeys(parser.links))
    if not links:
        raise ValueError("The CBB/Go Champs hub listed no tournament pages")

    def load(url):
        stage_failures = []
        try:
            page = (cache_dir / (url.rsplit("/", 1)[-1] + ".html")).read_text(encoding="utf-8") if cache_dir else _fetch(url)
            competition = parse_tournament(url, page)
            stage_parser = _LinkParser()
            stage_parser.feed(page)
            competition["stats_url"] = next(iter(stage_parser.stats), None)
            for stage_url in dict.fromkeys(stage_parser.stages):
                try:
                    stage_html = (cache_dir / (stage_url.rsplit("/", 1)[-1] + ".html")).read_text(encoding="utf-8") if cache_dir else _fetch(stage_url)
                    stage = parse_tournament(stage_url, stage_html, base_url=url)
                    games = {game["id"]: game for game in competition["games"]}
                    games.update({game["id"]: game for game in stage["games"]})
                    competition["games"] = sorted(games.values(), key=lambda game: (game["date"], game["time_utc"] or "", game["id"]))
                    known_teams = {team["id"] for team in competition["teams"]}
                    competition["teams"].extend(team for team in stage["teams"] if team["id"] not in known_teams)
                except Exception as exc:
                    stage_failures.append({"url": stage_url, "error": str(exc)})
            if stage_failures:
                return None, {
                    "url": url,
                    "error": f"{len(stage_failures)} fase(s) não puderam ser atualizadas",
                }, stage_failures
            return competition, None, stage_failures
        except Exception as exc:
            return None, {"url": url, "error": str(exc)}, stage_failures
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(load, links))
    competitions = [competition for competition, _, _ in results if competition]
    failures = [failure for _, failure, _ in results if failure]
    failures.extend(stage_failure for _, _, stage_failures in results for stage_failure in stage_failures)
    if not competitions:
        raise ValueError("No CBI schedules could be read; existing snapshot was preserved")

    # Keep the last known schedule if one tournament page has a transient error.
    if failures and SNAPSHOT_PATH.exists():
        previous = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
        known = {item["id"] for item in competitions}
        for item in previous.get("competitions", []):
            if item["id"] not in known and any(item["url"] == failure["url"] for failure in failures):
                competitions.append(item)

    payload = {
        "source": "Go Champs — plataforma oficial de competições da CBB",
        "source_url": HUB_URL,
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "competitions": competitions,
        "failures": failures,
    }
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(mode="w", encoding="utf-8", dir=SNAPSHOT_PATH.parent, delete=False) as output:
        output.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n")
    Path(output.name).replace(SNAPSHOT_PATH)
    return payload


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description="Atualiza calendário e resultados públicos dos CBIs")
    cli.add_argument("--cache-dir", type=Path, help="Usa páginas HTML salvas localmente")
    result = refresh_snapshot(cli.parse_args().cache_dir)
    print(f"Atualizadas {len(result['competitions'])} competições e {sum(len(c['games']) for c in result['competitions'])} jogos")
