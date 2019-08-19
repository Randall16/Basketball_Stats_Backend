#  File contains SQL statements to be used in conjunction with the
#  mysql connector library.

SQL_INSERT_PLAYER_TABLE = '''INSERT INTO player_table (player_id, name,
    year_from, year_to, position, height, weight, birthdate, colleges, hall_of_fame) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    year_from = VALUES(year_from),
    year_to = VALUES(year_to),
    position = VALUES(position),
    height = VALUES(height),
    weight = VALUES(weight),
    birthdate = VALUES(birthdate),
    colleges = VALUES(colleges),
    hall_of_fame = VALUES(hall_of_fame)'''


SQL_INSERT_SEASON_TABLE = '''INSERT INTO season_table (player_id, year, 
    playoffs, team, age, games_played, games_started, minutes, field_goals_made,
    field_goals_attempted, threes_made, threes_attempted, twos_made,
    twos_attempted, free_throws_made, free_throws_attempted, offensive_rebounds,
    defensive_rebounds, total_rebounds, assists, steals, blocks, turnovers,
    personal_fouls, points)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    team = VALUES(team),
    age = VALUES(age),
    games_played = VALUES(games_played),
    games_started = VALUES(games_started),
    minutes = VALUES(minutes),
    field_goals_made = VALUES(field_goals_made),
    field_goals_attempted = VALUES(field_goals_attempted),
    threes_made = VALUES(threes_made),
    threes_attempted = VALUES(threes_attempted),
    twos_made = VALUES(twos_made),
    twos_attempted = VALUES(twos_attempted),
    free_throws_made = VALUES(free_throws_attempted),
    offensive_rebounds = VALUES(offensive_rebounds),
    defensive_rebounds = VALUES(defensive_rebounds),
    total_rebounds = VALUES(total_rebounds),
    assists = VALUES(assists),
    steals = VALUES(steals),
    blocks = VALUES(blocks),
    turnovers = VALUES(turnovers),
    personal_fouls = VALUES(personal_fouls),
    points = VALUES(points)'''

SQL_QUERY_GET_PLAYER_INFO_BY_ID = '''SELECT *
    FROM player_table
    WHERE player_id = \"%s\" '''

SQL_QUERY_GET_PLAYER_SEASONS_BY_ID = '''SELECT *
    FROM season_table
    WHERE player_id = \"%s\"
    ORDER BY playoffs, year'''

SQL_QUERY_GET_ALL_PLAYER_IDS = 'SELECT player_id FROM player_table'

SQL_SEASON_TABLE_COLUMNS = '''season_table.player_id, year, 
    playoffs, team, age, games_played, games_started, minutes, field_goals_made,
    field_goals_attempted, threes_made, threes_attempted, twos_made,
    twos_attempted, free_throws_made, free_throws_attempted, offensive_rebounds,
    defensive_rebounds, total_rebounds, assists, steals, blocks, turnovers,
    personal_fouls, points'''

SQL_QUERY_GET_PLAYER_SEASONS_BY_NAME = 'SELECT ' + SQL_SEASON_TABLE_COLUMNS + '''
    FROM season_table
    INNER JOIN player_table 
    ON season_table.player_id = player_table.player_id
    WHERE player_table.name = \'%s\'
    ORDER BY year'''