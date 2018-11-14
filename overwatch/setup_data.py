import json
import logging
import typing as t

# from prettytable import PrettyTable
# import enum

logger = logging.getLogger('overwatch-stats')
logger.setLevel(logging.DEBUG)


class Competitor(t.NamedTuple):
    abbreviated_name: str
    address_country: str
    name: str


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
    with open('../data_files/results.json', 'r') as json_file:
        match_data_json = json_file.read()

    return json.loads(match_data_json)


def get_competitors(match):
    competitor_one = match['competitors'][0]
    competitor_two = match['competitors'][1]
    return Competitor(
        competitor_one['abbreviatedName'],
        competitor_one['addressCountry'],
        competitor_one['name'],
    ), Competitor(
        competitor_two['abbreviatedName'],
        competitor_two['addressCountry'],
        competitor_two['name'],
    )


def display_map(game):
    try:
        map = Map(
            key=game['attributes']['map'],
            name=game['attributes']['mapName'],
            score=game['attributes']['map']
        )
    except KeyError as exception:
        logging.error('Failed to build map', game)
        return
    score = MapScore(
        competitor_one_score=game['attributes']['mapScore']['team1'],
        competitor_two_score=game['attributes']['mapScore']['team2'],
    )
    result = MapResult(
        map=map,
        score=score
    )
    print(result)


def display_game(match, competitor_one, competitor_two):
    for game in match['games']:
        display_map(game)


def display_match(match):
    competitor_one, competitor_two = get_competitors(match)
    print(f'{competitor_one.name} VS {competitor_two.name}')
    display_game(match, competitor_one, competitor_two)


def display_bracket(bracket: t.Dict):
    for match in bracket.get('matches', {}):
        display_match(match)


if __name__ == '__main__':
    match_data = convert_json()
    print('loaded')
    display_bracket(bracket=match_data['brackets'][0])
