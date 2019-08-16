import mysql.connector

from db_config import *


def get_local_database() -> mysql.connector.connection.MySQLConnection:
    return mysql.connector.connect (
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )