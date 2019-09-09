import mysql.connector
import json
from parse_player_season import get_player_seasons
from parse_players import get_players

from models import *
from database import *
from player import Player

''' Use this file to run sample queries against db '''


db = get_local_database()
player = get_player_by_id(db, 'westje01')


print(player.to_json())