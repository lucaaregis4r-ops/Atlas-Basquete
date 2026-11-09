"""Collect the recorded events and field-goal markers in public LNB reports."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
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


def refresh_snapshot(cache_dir=None):
    games = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))

    def load(game):
        if cache_dir:
            html = (cache_dir / (game["id"] + ".html")).read_bytes()
        else:
            request = Request(game["url"], headers={"User-Agent": "Atlas Basquete / pesquisa pública"})
            with urlopen(request, timeout=30) as response:
                html = response.read()
        return parse_report(game, html)

    with ThreadPoolExecutor(max_workers=4) as pool:
        reports = list(pool.map(load, games))
    if not any(report["play_by_play_events"] for report in reports) or not any(report["shots"] for report in reports):
        raise ValueError("Nenhum registro válido da LNB foi retornado. Snapshot anterior preservado.")
    payload = {"source": "Liga Nacional de Basquete", "competition": "NBB", "games": reports}
    if SNAPSHOT_PATH.exists():
        previous = {game["id"]: game for game in json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))["games"]}
        for report in reports:
            prior = previous.get(report["id"], {})
            if (prior.get("shots") and not report["shots"]) or (prior.get("play_by_play_events") and not report["play_by_play_events"]):
                raise ValueError(f"Cobertura piorou para o jogo {report['id']}. Snapshot anterior preservado.")
    with NamedTemporaryFile(mode="w", encoding="utf-8", dir=SNAPSHOT_PATH.parent, delete=False) as output:
        output.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n")
    Path(output.name).replace(SNAPSHOT_PATH)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Atualiza a amostra observada do NBB")
    parser.add_argument("--cache-dir", type=Path, help="Diretório de relatórios HTML, nomeados pelo ID LNB")
    refresh_snapshot(parser.parse_args().cache_dir)
