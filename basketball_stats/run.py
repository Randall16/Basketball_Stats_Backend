import mysql.connector
import json
from parse_player_season import get_player_seasons
from parse_players import get_players

from models import *
from database import *
from player import Player

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
                WHERE player_table.name = \'%s\'
                ORDER BY year'''

db = get_local_database()


player = get_player_by_id(db, 'simmojo02')
print(player.to_json())