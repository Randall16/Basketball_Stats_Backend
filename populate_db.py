import mysql.connector
import time

from parse_player_season import get_player_seasons
from parse_players import get_players
from models import *
from database import *


for i in range(1980, 1979, -1):
    time.sleep(2)
    seasons = get_player_seasons(i, False)
    cursor.executemany(SQL_INSERT_SEASON_TABLE, seasons)
    mydb.commit()
    print('%d year successfully inserted' % i)

mydb.close()