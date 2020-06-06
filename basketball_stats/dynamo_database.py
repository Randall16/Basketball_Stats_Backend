
import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.types import Decimal

import credentials
from parse_players_infos import get_players_infos
from parse_players_seasons import get_players_seasons
from player import Player
from models import PlayerInfo, PlayerSeasonTotals


TABLE_NAME = 'basketball_archive2'
PRIMARY_KEY = 'data_type'
SORT_KEY = 'id'

DATA_TYPE_INDICATOR_INFO = 'INFO'
DATA_TYPE_INDICATOR_SEASON = 'SEASON'

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
        TableName=TABLE_NAME,
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


def update_player_info_by_letters(table, letters: tuple):
    player_infos = get_players_infos(letters, 2)

    with table.batch_writer() as batch: 
        for player_info in player_infos:
            # Preparing to insert player_info into Dynamo table
            # Inserting into dynamo table takes a dictionary, player_info_values
            # will be the values portion of that dictionary
            player_info_values = list(player_info)
            # Need to add the DATA_TYPE_INDICATOR_INFO because that is not part
            # of the PlayerInfo object
            player_info_values.insert(0, DATA_TYPE_INDICATOR_INFO)

            # Now create the dictionary by zipping the PLAYER_INFO_ENTITY_ATTRIBUTES
            # as the keys with the values created above
            item = dict(zip(PLAYER_INFO_ENTITY_ATTRIBUTES, player_info_values))
            
            # Finally insert into the table
            batch.put_item(Item=item)


def update_players_seasons_by_year(table, year: int, playoffs: bool=False):

    players_seasons = get_players_seasons(year, playoffs)

    #known_player_ids = get_all_player_ids_that_have_info(table)
    #letters_to_update = set()

    with table.batch_writer() as batch: 
        for player_season in players_seasons:
            # Preparing to insert player_season into Dynamo table
            # Inserting into dynamo table takes a dictionary, player_season_values 
            # will be the values portion of that dictionary
            player_season_values = list(player_season)


            # Add the DATA_TYPE_INDICATOR_SEASON to the values list created above
            player_season_values.insert(0, DATA_TYPE_INDICATOR_SEASON)

            # Now create the dictionary by zipping the 
            # PLAYER_SEASON_ENTITY_ATTRIBUTES as the keys with the values created above
            item = dict(zip(PLAYER_SEASON_ENTITY_ATTRIBUTES, player_season_values))

            batch.put_item(Item=item)

    """ if player_season.player_id not in known_player_ids:
                letters_to_update.add(player_season.player_id[0])
    
    update_player_info_by_letters(table, tuple(letters_to_update)) """


""" def generate_player_season_sort_key(year: int, team: str, playoffs: bool) -> str:
    season_type = 'REGULAR'
    if playoffs:
        season_type = 'PLAYOFF'

    key = (SORT_KEY_SEASON_INDICATOR + '_' + season_type + '_' + str(year)
        +  '_' + team)

    return key """


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
    player_info = _convert_to_ints(player_info)

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

        season = _convert_to_ints(season)

        season_objects.append(PlayerSeasonTotals(**season))

    return season_objects


def get_player_by_id(table, player_id: str) -> Player:
    player_info = get_player_info_by_id(table, player_id)
    seasons = get_player_seasons_by_id(table, player_id)

    return Player(player_info, seasons)


def get_all_player_infos(table) -> []:
    
    player_infos = table.scan(
        FilterExpression=Key(SORT_KEY).eq(SORT_KEY_INFO_INDICATOR)
    )

    player_infos = player_infos['Items']


    player_info_objects = []
    for player_info in player_infos:

        del player_info[SORT_KEY]
        player_info = _convert_to_ints(player_info)


        player_info_objects.append( PlayerInfo(**player_info) )

    return player_info_objects


def _convert_to_ints(dictionary: {}) -> {}:
    # DynamoDB has some obscure custom object for storing any numerical
    # value. The for loop below converts that type into standard python ints.
    for k, v in dictionary.items():
        if isinstance(v, Decimal):
            dictionary[k] = int(v)

    return dictionary




def get_all_player_ids_that_have_info(table):
    
    player_ids = set()

    response = table.scan(
        ProjectionExpression=PRIMARY_KEY,
        FilterExpression=Key(SORT_KEY).eq(SORT_KEY_INFO_INDICATOR),
    ) 

    for pair in response.get('Items', []):
        player_ids.add(pair[PRIMARY_KEY])


    while 'LastEvaluatedKey' in response:
        response = table.scan(
            ProjectionExpression=PRIMARY_KEY,
            FilterExpression=Key(SORT_KEY).eq(SORT_KEY_INFO_INDICATOR),
            ExclusiveStartKey=response['LastEvaluatedKey']
        )

        for pair in response.get('Items', []):
            player_ids.add(pair[PRIMARY_KEY])
            
     

    return player_ids