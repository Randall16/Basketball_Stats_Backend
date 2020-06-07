import mysql.connector
import time

from parse_player_season import get_player_seasons
from parse_players import get_players
from player import Player
from models import *
from sql_statements import *
from db_config import *


def get_local_database() -> mysql.connector.connection.MySQLConnection:
    return mysql.connector.connect (
        host=LOCAL_HOST,
        user=LOCAL_USER,
        password=LOCAL_PASSWORD,
        database=LOCAL_DATABASE
    )

def get_aws_database() -> mysql.connector.connection.MySQLConnection:
    return mysql.connector.connect (
        host=AWS_HOST,
        user=AWS_USER,
        password=AWS_PASSWORD,
        database=AWS_DATABASE
    )

def get_all_players_info(database: mysql.connector.connection.MySQLConnection) -> []:

    cursor = database.cursor()

    cursor.execute(SQL_QUERY_GET_ALL_PLAYERS_INFO)
    db_response = cursor.fetchall()

    if db_response == None:
        return None
    
    players_info = [PlayerInfo(*info) for info in db_response]
    return players_info

def get_all_player_ids(database: mysql.connector.connection.MySQLConnection) -> []:

    cursor = database.cursor()

    cursor.execute(SQL_QUERY_GET_ALL_PLAYER_IDS)

    db_response = [i[0] for i in cursor.fetchall()]
    
    return db_response

def get_player_info_by_id(database: mysql.connector.connection.MySQLConnection,
    player_id: str) -> PlayerInfo:

    cursor = database.cursor()

    # Interpolate sql query with the player_id
    SQL_QUERY_WITH_ID = SQL_QUERY_GET_PLAYER_INFO_BY_ID % player_id

    # pull data from the database
    cursor.execute(SQL_QUERY_WITH_ID)
    db_response = cursor.fetchone() # Should only be one player so use fetchone()

    if db_response == None:
        return None

    # Create PlayerInfo with the database response
    player_info = PlayerInfo(*db_response)
    return player_info

def get_player_season_totals_by_id(database: mysql.connector.connection.MySQLConnection,
    player_id: str) -> []:

    cursor = database.cursor()

    # Interpolate sql query with the player_id
    SQL_QUERY_WITH_ID = SQL_QUERY_GET_PLAYER_SEASONS_BY_ID % player_id

    # pull data from the database
    cursor.execute(SQL_QUERY_WITH_ID)
    db_response = cursor.fetchall() # Multiple seasons so use fetchall()

    if db_response == None:
        return None

    # create a PlayerSeasonTotal object for every row in the database response
    season_totals = [PlayerSeasonTotals(*season) for season in db_response]
    return season_totals

def get_player_by_id(database: mysql.connector.connection.MySQLConnection,
    player_id: str) -> Player:

    player_info = get_player_info_by_id(database, player_id)

    if player_info == None:
        return None

    player_seasons = get_player_season_totals_by_id(database, player_id)

    if player_seasons == None:
        return None

    return Player(player_info, player_seasons)

def update_database_by_season(database: mysql.connector.connection.MySQLConnection,
    year: int, sleep_interval: int=0):

    cursor = database.cursor()
    player_ids = get_all_player_ids(database)
    known_ids = set()

    for i in player_ids:
        known_ids.add(i)

    seasons = get_player_seasons(year)

    # add any unknown players into the players table
    for season in seasons:
        if season.player_id not in known_ids:
            player_infos = get_players(season.player_id[0])

            cursor.executemany(SQL_INSERT_PLAYER_TABLE, player_infos)
            database.commit()

            for player in player_infos:
                known_ids.add(player.player_id)

            time.sleep(2)

    # add seasons
    for season in seasons:
        if season.player_id in known_ids:
            cursor.execute(SQL_INSERT_SEASON_TABLE, season)
        else:
            print('Unable to add player %s does not exist in players table' % season.player_id)

    database.commit()
    