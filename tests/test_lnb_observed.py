from cbb.extractors.lnb_observed import parse_report


GAME = {"id": "1", "score": [3, 0]}
EVENTS = """
<div id="movethemove"><div class="move_action_scroll">
  <div class="move_action"><strong class="quarter">4</strong><strong class="points">3 x 0</strong></div>
  <div class="move_action"><strong class="quarter">3</strong><strong class="points">3 x 0</strong></div>
  <div class="move_action"><strong class="quarter">2</strong><strong class="points">3 x 0</strong></div>
  <div class="move_action"><strong class="quarter">1</strong><strong class="points">0 x 0</strong></div>
</div></div>
"""
SHOTS = """
<div class="quadra">
  <ul class="players_block_left"><li idj="17"><span class="name">Atleta A</span></li></ul>
  <ul class="players_block_right"><li idj="18"><span class="name">Atleta B</span></li></ul>
  <ul class="graphic_gym">
    <li idj="17" idp="2" ide="1" class="3pt correct" style="top: 12%; left: 75.5%;"></li>
    <li idj="18" idp="3" ide="2" class="2pt incorrect" style="top: %; left: %;"></li>
    <li idj="17" idp="2" ide="1" class="ll incorrect"></li>
  </ul>
</div>
"""


def test_report_separates_field_goals_and_keeps_missing_locations():
    result = parse_report(GAME, EVENTS + SHOTS)
    assert result["play_by_play_events"] == 4
    assert result["players"] == {"17": "Atleta A", "18": "Atleta B"}
    assert result["shots"] == [
        [0, "17", 2, 3, 1, 75.5, 12.0],
        [1, "18", 3, 2, 0, None, None],
    ]


def test_empty_report_and_mismatched_play_by_play_are_distinct():
    assert parse_report(GAME, "")["play_by_play_events"] is None
    result = parse_report({**GAME, "score": [4, 0]}, EVENTS + SHOTS)
    assert result["play_by_play_events"] is None
    assert len(result["shots"]) == 2


def schedule_row(game_id='101', score_a='84', score_b='73', url='/noticias/jogo/', season='2026/2027'):
    return f'''<tr><td class="position_value" data-real-id="{game_id}">1</td>
      <td class="date_value"><span>17/10/2026</span></td>
      <td class="home_team_value"><span class="team-shortname">Mogi</span></td>
      <td class="score_value"><a class="match_score_relatorio" href="{url}">
        <span class="home">{score_a}</span> X <span class="away">{score_b}</span></a></td>
      <td class="visitor_team_value"><span class="team-shortname">Corinthians</span></td>
      <td class="champ_value">{season}</td></tr>'''


def test_schedule_collects_only_completed_games_and_official_urls():
    from cbb.extractors.lnb_observed import parse_schedule
    html = '<table>' + schedule_row() + schedule_row('102', '', '') + schedule_row('103', '0', '0') + schedule_row('104', '40', '30', 'https://example.org/fake') + '</table>'
    games = parse_schedule(html, 'NBB')
    assert [game['id'] for game in games] == ['101', '104']
    assert games[0]['score'] == [84, 73]
    assert games[0]['teams'] == ['Mogi', 'Corinthians']
    assert games[0]['season'] == '2026-2027'
    assert games[0]['url'] == 'https://lnb.com.br/noticias/jogo/'
    assert games[1]['report_available'] is False
    assert games[1]['url'] == 'https://lnb.com.br/nbb/tabela-de-jogos/'


def test_season_discovery_keeps_only_the_requested_competition():
    from cbb.extractors.lnb_observed import season_urls
    html = '''<label><input name="season[]" value="106">NBB 2026/2027</label>
              <label><input name="season[]" value="97">NBB 2025/2026</label>
              <label><input name="season[]" value="104">LDB 2026</label>'''
    urls = season_urls(html, 'NBB')
    assert len(urls) == 2
    assert all('lnb.com.br/nbb/tabela-de-jogos/' in url for url in urls)
    assert 'season%5B0%5D=97' in urls[1]


def test_failed_table_preserves_old_games_and_other_competitions(tmp_path, monkeypatch):
    import json
    from cbb.extractors import lnb_observed
    path = tmp_path / 'nbb.json'
    old = {'id': 'old', 'competition': 'LDB', 'season': '2025', 'date': '2025-06-01',
           'teams': ['A', 'B'], 'score': [70, 60], 'url': 'https://lnb.com.br/old/',
           'play_by_play_events': 100, 'shots': [[0, 'p', 1, 2, 1, 10, 20]],
           'players': {'p': 'Atleta'}, 'boxscore': [None, None]}
    path.write_text(json.dumps({'games': [old]}), encoding='utf-8')
    monkeypatch.setattr(lnb_observed, 'SNAPSHOT_PATH', path)
    def fetch(url):
        if '/ldb/' in url:
            raise OSError('source temporarily unavailable')
        return ('<table>' + schedule_row() + '</table>').encode()
    monkeypatch.setattr(lnb_observed, 'fetch_url', fetch)
    result = lnb_observed.refresh_snapshot(max_reports=0)
    assert {game['id'] for game in result['games']} == {'old', '101'}
    retained = next(game for game in result['games'] if game['id'] == 'old')
    assert retained['shots'] == old['shots']
    assert len(result['discovery_failures']) == 1
    assert result['coverage']['reports_checked'] == 1


def test_season_players_parses_sibling_label_and_official_averages():
    from cbb.extractors.lnb_observed import parse_season_players
    columns = ['Jogador', 'Equipe', 'JO', 'Min', 'PTS', '3PC', '3PT', '3P%', '2PC', '2PT', '2P%', 'LLC', 'LLT', 'LL%']
    cells = ['<a href="/atletas/a/">Atleta A</a>', 'Cruzeiro', '16', '32.29', '21.06', '2.13', '7.19', '29.57', '5.25', '10.31', '50.91', '4.19', '5.38', '77.91']
    html = '<div><input name="season[]" id="season-1" checked><label for="season-1">LDB 2026</label></div><table><thead><tr>' + ''.join('<th>'+x+'</th>' for x in columns) + '</tr></thead><tbody><tr>' + ''.join('<td>'+x+'</td>' for x in cells) + '</tr></tbody></table>'
    record = parse_season_players(html, 'LDB', 'https://lnb.com.br/ldb/estatisticas/arremessos/')
    assert record['season'] == '2026'
    assert record['players'][0]['team'] == 'Cruzeiro'
    assert record['players'][0]['games'] == 16
    assert record['players'][0]['points_pg'] == 21.06
