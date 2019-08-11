import mysql.connector
import json
from parse_player_season import get_player_seasons
from parse_players import get_players

from models import *
from database import *

''' Use this file to run sample queries against db '''

cols = '''season_table.player_id, year, 
    playoffs, team, age, games_played, games_started, minutes, field_goals_made,
    field_goals_attempted, threes_made, threes_attempted, twos_made,
    twos_attempted, free_throws_made, free_throws_attempted, offensive_rebounds,
    defensive_rebounds, total_rebounds, assists, steals, blocks, turnovers,
    personal_fouls, points'''

sql_query = ''' SELECT %s
                FROM season_table
                INNER JOIN player_table 
                ON season_table.player_id = player_table.player_id
                WHERE player_table.name = \'%s\' '''

#print(sql_query % (cols, 'Larry Bird'))
cursor.execute(sql_query % (cols, 'Michael Jordan'))
seasons = [ PlayerSeasonTotals(*i) for i in cursor.fetchall() ]

for i in seasons:
    dc = i._asdict()
    del dc['player_id']
    dc['tes'] = None
    js = json.dumps(dc, default=str)
    print(js)