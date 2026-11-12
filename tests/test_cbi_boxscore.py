import json
import pytest
from cbb.extractors.cbi_observed import parse_boxscore, collect_boxscores


def stream(home_points=10, away_points=8, player_points=10):
    def team(name, total, player):
        return {"teamName": name, "totals": {"points": str(total)}, "rows": [
            {"playerId": name, "name": name + " atleta", "stats": {"points": str(player), "game_played": "1"}}
        ]}
    payload = json.dumps({"home": team("Casa", home_points, player_points),
                          "away": team("Fora", away_points, away_points)})
    return 'self.__next_f.push([1,' + json.dumps(payload) + '])'


def test_boxscore_requires_points_to_match_official_score():
    game = {"home_score": 10, "away_score": 8}
    box = parse_boxscore(stream(), game)
    assert box["home"]["players"][0]["stats"]["points"] == "10"
    with pytest.raises(ValueError):
        parse_boxscore(stream(player_points=9), game)
    with pytest.raises(ValueError):
        parse_boxscore(stream(home_points=11, player_points=11), game)


def test_cached_boxscore_reused_only_when_result_matches():
    cached = {"id": "g", "home_score": 10, "away_score": 8, "boxscore": {"home": {}}}
    current = {"id": "g", "home_score": 10, "away_score": 8, "is_finished": True}
    comps = [{"games": [current]}]
    coverage = collect_boxscores(comps, {"competitions": [{"games": [cached]}]}, limit=0)
    assert current["boxscore"] == cached["boxscore"]
    assert coverage["boxscores"] == 1
    current = {"id": "g", "home_score": 11, "away_score": 8, "is_finished": True}
    collect_boxscores([{"games": [current]}], {"competitions": [{"games": [cached]}]}, limit=0)
    assert "boxscore" not in current


def test_collection_spreads_requests_across_competitions(monkeypatch):
    from cbb.extractors import cbi_observed
    calls = []
    def fetch(url):
        calls.append(url)
        return stream()
    monkeypatch.setattr(cbi_observed, '_fetch', fetch)
    def game(id, date):
        return {'id': id, 'date': date, 'url': id, 'home_score': 10,
                'away_score': 8, 'is_finished': True}
    comps = [{'games': [game('a1', '2026-10-02'), game('a2', '2026-10-01')]},
             {'games': [game('b1', '2026-09-02'), game('b2', '2026-09-01')]}]
    result = collect_boxscores(comps, limit=2)
    assert set(calls) == {'a1', 'b1'}
    assert result['boxscores'] == 2
    assert result['completed_games'] == 4
