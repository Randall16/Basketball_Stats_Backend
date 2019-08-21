import mysql.connector
import json
from parse_player_season import get_player_seasons
from parse_players import get_players

from models import *
from database import *
from player import Player

''' Use this file to run sample queries against db '''


db = get_aws_database()


info_list = get_all_players_info(db)

li = [i._asdict() for i in info_list]

print(json.dumps(li, default=str))