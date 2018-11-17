import json
from overwatch.league import MapScore, Map, MapResult, Team, Competitor


def convert_json():
    with open(f'results.json', 'r') as json_file:
        match_data_json = json_file.read()

    return json.loads(match_data_json)


class Match:
    rounds: int


class Top24:

    def __init__(self):
        matches: list

    def _setup(self):
        match_data = convert_json()
        bracket = match_data['brackets'][0]
        for match in bracket.get('matches', {})[:1]:
            match
