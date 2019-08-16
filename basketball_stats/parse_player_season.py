import requests
from bs4 import BeautifulSoup

from models import *

_URL = 'https://www.basketball-reference.com/leagues/NBA_%d_totals.html'
_PLAYOFF_URL = 'https://www.basketball-reference.com/playoffs/NBA_%d_totals.html'

def get_player_seasons(year: int, playoffs: bool=False) -> ():
    html = get_player_seasons_html(year, playoffs)
    season_list = parse_player_season_html(html, year, playoffs)
    return tuple(season_list)


def get_player_seasons_html(year: int, playoffs: bool) -> BeautifulSoup:
    """ Fetches player season totals html table from Basketball Reference """
    url = _PLAYOFF_URL if playoffs else _URL

    req = requests.get(url % year)

    if req.status_code != 200:
        return None

    all_html = BeautifulSoup(req.text, features='html.parser')

    table = all_html.find('table', id='totals_stats')
    table_body = table.find('tbody')
    return table_body

def parse_player_season_html(table: BeautifulSoup, year: int, playoffs: bool=False) -> []:

    if table == None:
        return None
    
    seasons_list = []

    rows = table.find_all('tr', {'class': ['full_table', 'italic_text partial_table']})

    for row in rows:

        link = row.select_one('a').attrs['href']

        # extract player_id from link in href
        player_id = link.split('/')[3]
        player_id = player_id.split('.')[0]

        # grab all table data for the row
        cols = row.find_all('td')

        age = _to_int(cols[2].text)
        team = cols[3].text
        games_played = _to_int(cols[4].text)
        games_started = _to_int(cols[5].text)
        minutes = _to_int(cols[6].text)
        field_goals_made = _to_int(cols[7].text)
        field_goals_attempted = _to_int(cols[8].text)
        threes_made = _to_int(cols[10].text)
        threes_attempted = _to_int(cols[11].text)
        twos_made = _to_int(cols[13].text)
        twos_attempted = _to_int(cols[14].text)
        free_throws_made = _to_int(cols[17].text)
        free_throws_attempted = _to_int(cols[18].text)
        offensive_rebounds = _to_int(cols[20].text)
        defensive_rebounds = _to_int(cols[21].text)
        total_rebounds = _to_int(cols[22].text)
        assists = _to_int(cols[23].text)
        steals = _to_int(cols[24].text)
        blocks = _to_int(cols[25].text)
        turnovers = _to_int(cols[26].text)
        personal_fouls = _to_int(cols[27].text)
        points = _to_int(cols[28].text)

        player_season = PlayerSeasonTotals(player_id, year, playoffs, team, age,
            games_played, games_started, minutes, field_goals_made,
            field_goals_attempted, threes_made, threes_attempted, twos_made,
            twos_attempted, free_throws_made, free_throws_attempted,
            offensive_rebounds, defensive_rebounds, total_rebounds, assists,
            steals, blocks, turnovers, personal_fouls, points)

        seasons_list.append(player_season)


    return seasons_list

def _to_int(text: str) -> int:
    """ Utility function to convert strings to ints while handling null/empty strings """
    if text != None and text != '':
        return int(text)
    else:
        return None