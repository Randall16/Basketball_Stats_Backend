import mysql.connector

from db_config import *
from models import *


mydb = mysql.connector.connect (
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)

cursor = mydb.cursor()

SQL_INSERT_PLAYER_TABLE = '''INSERT INTO player_table (player_id, name,
    year_from, year_to, position, height, weight, birthdate, colleges, hall_of_fame) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

SQL_INSERT_SEASON_TABLE = '''INSERT INTO season_table (player_id, year, 
    playoffs, team, age, games_played, games_started, minutes, field_goals_made,
    field_goals_attempted, threes_made, threes_attempted, twos_made,
    twos_attempted, free_throws_made, free_throws_attempted, offensive_rebounds,
    defensive_rebounds, total_rebounds, assists, steals, blocks, turnovers,
    personal_fouls, points)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s)'''