
import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.types import Decimal

import credentials
from parse_players_infos import get_players_infos
from parse_players_seasons import get_players_seasons
from player import Player
from models import PlayerInfo, PlayerSeasonTotals


PRIMARY_KEY = 'player_id'
SORT_KEY = 'player_data_type'

SORT_KEY_INFO_INDICATOR = 'INFO'
SORT_KEY_SEASON_INDICATOR = 'SEASON'

PLAYER_INFO_ENTITY_ATTRIBUTES = (PRIMARY_KEY, SORT_KEY, 'name', 'year_from',
    'year_to', 'position', 'height', 'weight', 'birthdate', 'colleges', 'hall_of_fame')

PLAYER_SEASON_ENTITY_ATTRIBUTES = (PRIMARY_KEY, SORT_KEY, 'year', 'playoffs',
    'team', 'age', 'games_played', 'games_started', 'minutes', 'field_goals_made',
    'field_goals_attempted', 'threes_made', 'threes_attempted', 'twos_made', 
    'twos_attempted', 'free_throws_made', 'free_throws_attempted',
    'offensive_rebounds', 'defensive_rebounds', 'total_rebounds', 'assists',
    'steals', 'blocks', 'turnovers', 'personal_fouls', 'points' )


def create_basketball_archive_database(db_resource):
    """ Creates the DynamoDB table from AWS Dynamo Resource """
    db_resource.create_table(
        TableName='basketball_archive',
        KeySchema=[
            {
                'AttributeName': PRIMARY_KEY,
                'KeyType': 'HASH'
            },
            {
                'AttributeName': SORT_KEY,
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': PRIMARY_KEY,
                'AttributeType': 'S'
            },
            {
                'AttributeName': SORT_KEY,
                'AttributeType': 'S'
            },
        ],
        BillingMode='PAY_PER_REQUEST'
    )


def update_player_info_by_letter(table, letter: chr):
    player_infos = get_players_infos((letter,))

    with table.batch_writer() as batch: 
        for player_info in player_infos:
            """ table.put_item(
                Item={
                    PRIMARY_KEY: player_info.player_id,
                    SORT_KEY: 'info',
                    'name': player_info.name,
                    'year_from': player_info.year_from,
                    'year_to': player_info.year_to,
                    'position': player_info.position,
                    'height': player_info.height,
                    'weight': player_info.weight,
                    'birthdate': player_info.birthdate,
                    'colleges': player_info.colleges,
                    'hall_of_fame': player_info.hall_of_fame
                }
            ) """

            # Preparing to insert player_info into Dynamo table
            # Inserting into dynamo table takes a dictionary, player_info_values
            # will be the values portion of that dictionary
            player_info_values = list(player_info)
            # Need to add the SORT_KEY_INFO_INDICATOR because that is not part
            # of the player info object
            player_info_values.insert(1, SORT_KEY_INFO_INDICATOR)

            # Now create the dictionary by zipping the PLAYER_INFO_ENTITY_ATTRIBUTES
            # as the keys with the values created above
            item = dict(zip(PLAYER_INFO_ENTITY_ATTRIBUTES, player_info_values))
            
            # Finally insert into the table
            batch.put_item(Item=item)


def update_players_seasons_by_year(table, year: int, playoffs: bool=False):

    players_seasons = get_players_seasons(year, playoffs)

    with table.batch_writer() as batch: 
        for player_season in players_seasons:
            # Preparing to insert player_season into Dynamo table
            # Inserting into dynamo table takes a dictionary, player_season_values 
            # will be the values portion of that dictionary
            player_season_values = list(player_season)


            sort_key_value = generate_player_season_sort_key(player_season.year, 
                player_season.team, player_season.playoffs)

            # Add the sort_key_value to the values list created above
            player_season_values.insert(1, sort_key_value)

            # Now create the dictionary by zipping the 
            # PLAYER_SEASON_ENTITY_ATTRIBUTES as the keys with the values created above
            item = dict(zip(PLAYER_SEASON_ENTITY_ATTRIBUTES, player_season_values))

            batch.put_item(Item=item)


def generate_player_season_sort_key(year: int, team: str, playoffs: bool) -> str:
    season_type = 'REGULAR'
    if playoffs:
        season_type = 'PLAYOFF'

    return SORT_KEY_SEASON_INDICATOR + '#' + season_type + str(year) + '#' + team

def get_player_info_by_id(table, player_id: str) -> PlayerInfo:

    player_info = table.get_item(
        Key={
            PRIMARY_KEY: player_id,
            SORT_KEY: SORT_KEY_INFO_INDICATOR
        }
    )

    player_info = player_info['Item']

    # Deleting sort key because we want to convert this into our Python 
    # PlayerInfo object
    del player_info[SORT_KEY]

    return PlayerInfo(**player_info)

def get_player_seasons_by_id(table, player_id: str) -> []:

    seasons = table.query(
        KeyConditionExpression=Key(PRIMARY_KEY).eq(player_id)
            & Key(SORT_KEY).begins_with(SORT_KEY_SEASON_INDICATOR)
    )

    seasons = seasons['Items']
    
    season_objects = []
    for season in seasons:

        # Deleting sort key because we want to convert this into our Python 
        # PlayerSeasonTotals object
        del season[SORT_KEY]

        # DynamoDB has some obscure custom object for storing any numerical
        # value. The for loop below converts that type into standard python ints.
        for k, v in season.items():
            if isinstance(v, Decimal):
                season[k] = int(v)

        season_objects.append(PlayerSeasonTotals(**season))

    return season_objects

def get_player_by_id(table, player_id: str) -> Player:
    player_info = get_player_info_by_id(table, player_id)
    seasons = get_player_seasons_by_id(table, player_id)

    return Player(player_info, seasons)
        