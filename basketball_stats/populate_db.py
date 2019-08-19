import time

from parse_player_season import get_player_seasons
from parse_players import get_players
from models import *
from database import get_local_database
from sql_statements import *


mydb = get_local_database()
cursor = mydb.cursor()

for i in range(1960, 1949, -1):
    seasons = get_player_seasons(i, True)
    cursor.executemany(SQL_INSERT_SEASON_TABLE, seasons)
    mydb.commit()
    print('%d year playoffs successfully inserted' % i)
    time.sleep(35)

mydb.close()