import json
import logging
import typing as t
import tableprint as tp
import os
# from prettytable import PrettyTable
# import enum

logger = logging.getLogger('overwatch-stats')
logger.setLevel(logging.DEBUG)
WORKING_DIR = os.path.dirname(os.path.realpath(__file__))


class Team(t.NamedTuple):
    team: int


class Competitor(t.NamedTuple):
    abbreviated_name: str
    address_country: str
    name: str
    team: Team


class MapScore(t.NamedTuple):
    competitor_one_score: str
    competitor_two_score: str


class Map(t.NamedTuple):
    key: str
    name: str
    score: MapScore


class MapResult(t.NamedTuple):
    map: Map
    score: MapScore


def convert_json():
    with open(f'{WORKING_DIR}/data_files/results.json', 'r') as json_file:
        match_data_json = json_file.read()

    return json.loads(match_data_json)


def get_competitors(match):
    competitor_one = match['competitors'][0]
    competitor_two = match['competitors'][1]
    return Competitor(
        competitor_one['abbreviatedName'],
        competitor_one['addressCountry'],
        competitor_one['name'],
        Team(1)
    ), Competitor(
        competitor_two['abbreviatedName'],
        competitor_two['addressCountry'],
        competitor_two['name'],
        Team(2)
    )


def display_map(game):
    map = Map(
        key=game['attributes']['map'],
        name=game['attributes']['mapName'],
        score=game['attributes']['map']
    )
    score = MapScore(
        competitor_one_score=game['attributes']['mapScore']['team1'],
        competitor_two_score=game['attributes']['mapScore']['team2'],
    )
    return MapResult(
        map=map,
        score=score
    )


def display_game(match, competitor_one: Competitor,
                 competitor_two: Competitor):
    games = []
    for raw_game in match['games']:
        game = display_map(raw_game)
        games.append([game.map.name, game.score.competitor_one_score,
                      game.score.competitor_two_score])
    return games


def display_match(match):
    competitor_one, competitor_two = get_competitors(match)
    tp.banner(f'{competitor_one.name} VS {competitor_two.name}')
    games = display_game(match, competitor_one, competitor_two)

    headers = ['Map ', f'{competitor_one.name}', f'{competitor_two.name}']

    tp.table(games, headers, width=17)


def display_bracket(bracket: t.Dict):
    for match in bracket.get('matches', {})[:1]:
        display_match(match)

