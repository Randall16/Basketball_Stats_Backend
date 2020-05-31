
import boto3

import credentials
from parse_players import get_players


PRIMARY_KEY = 'player_id'
SORT_KEY = 'player_data_type'

PLAYER_INFO_ENTITY_ATTRIBUTES = (PRIMARY_KEY, SORT_KEY, 'name', 'year_from',
    'year_to', 'position', 'height', 'weight', 'birthdate', 'colleges', 'hall_of_fame')


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


def update_player_info_by_letter(letter: chr, table):
    player_infos = get_players((letter,))


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

        li = list(player_info)
        li.insert(1, 'info')
        item = dict(zip(PLAYER_INFO_ENTITY_ATTRIBUTES, li))
        table.put_item(
            Item=item
        )

