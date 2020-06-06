

import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.types import Decimal

import credentials

from dynamo_database import *
from models import *
from player import Player
import json

import time

''' Use this file to run sample queries against db '''


session = boto3.Session(
    aws_access_key_id=credentials.DYNAMO_IAM_ACCESS_KEY_ID,
    aws_secret_access_key=credentials.DYNAMO_IAM_SECRET_KEY,
    region_name=credentials.REGION_NAME
)

db = session.resource('dynamodb')


#create_basketball_archive_database(db)

table = db.Table(TABLE_NAME)

#update_player_info_by_letters(table, ('a',))

update_players_seasons_by_year(table, 2020)


#table.delete()