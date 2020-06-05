

import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.types import Decimal

import credentials

from dynamo_database import *
from models import *
from player import Player
import json

''' Use this file to run sample queries against db '''


session = boto3.Session(
    aws_access_key_id=credentials.DYNAMO_IAM_ACCESS_KEY_ID,
    aws_secret_access_key=credentials.DYNAMO_IAM_SECRET_KEY,
    region_name=credentials.REGION_NAME
)

db = session.resource('dynamodb')


#create_basketball_archive_database(db)

table = db.Table('basketball_archive')



ayton = get_player_by_id(table, 'aytonde01')
print(ayton.to_json(True))


table.delete()