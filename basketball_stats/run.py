import mysql.connector
import json
import time
from parse_player_season import get_player_seasons
from parse_players import get_players

from models import *
from database import *
from player import Player

''' Use this file to run sample queries against db '''


db = get_local_database()

update_database_by_season(db, 2019)