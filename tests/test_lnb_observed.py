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
