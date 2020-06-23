

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

ayton_id = 'aytonde01'
bam_id = 'adebaba01'
giannis_id = 'antetgi01'
west_id = 'westje01'
beal_id = 'bealbr01'


""" player = get_player_by_id(table, ayton_id)

d = { 'body': player.to_json(False) }
print(d) """
print(get_all_player_infos(table))

#print(len(get_all_player_infos(table)))
#print(len(get_all_player_ids_that_have_info(table)))

#table.delete()