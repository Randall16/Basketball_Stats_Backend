import mysql.connector
import json
from parse_player_season import get_player_seasons
from parse_players import get_players

from models import *
from database import *

import time

""" for i in range(2010, 2000, -1):
    time.sleep(26)
    seasons = get_player_seasons(i, False)
    cursor.executemany(SQL_INSERT_SEASON_TABLE, seasons)

mydb.commit()

mydb.close() """

s = '''player_id, year, 
    playoffs, team, age, games_played, games_started, minutes, field_goals_made,
    field_goals_attempted, threes_made, threes_attempted, twos_made,
    twos_attempted, free_throws_made, free_throws_attempted, offensive_rebounds,
    defensive_rebounds, total_rebounds, assists, steals, blocks, turnovers,
    personal_fouls, points'''

cursor.execute('select %s from season_table where player_id = \'jamesle01\'' % s)
seasons = [ PlayerSeasonTotals(*i) for i in cursor.fetchall() ]

for i in seasons:
    dc = i._asdict()
    del dc['player_id']
    dc['tes'] = None
    js = json.dumps(dc, default=str)
    print(js)