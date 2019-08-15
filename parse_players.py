import requests
import unidecode
from datetime import datetime
from bs4 import BeautifulSoup

from models import PlayerInfo

import time

_URL = 'https://www.basketball-reference.com/players/%c/'
_ALPHABET = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
    'q','r','s','t','u','v','w','x','y','z')

def get_players(letters: ()=_ALPHABET, sleep_time: int=0) -> ():
    players = []  
    for letter in letters:
        time.sleep(sleep_time)
        html = get_players_html(letter.lower())
        parsed_players = parse_player_table_html(html)

        if parsed_players != None:
            players.extend(parsed_players)
    
    return tuple(players)

def get_players_html(letter: str) -> BeautifulSoup:
    req = requests.get(_URL % letter)

    if req.status_code != 200:
        return None

    all_html = BeautifulSoup(req.text, features='html.parser')

    table = all_html.find('table', id='players')
    table_body = table.find('tbody')
    return table_body

def parse_player_table_html(table: BeautifulSoup) -> []:

    if table == None:
        return None
    
    players_list = []

    rows = table.find_all('tr')

    for row in rows:
        # name and playerID are stored in each rows table header
        name = row.find("th").text
        link = row.select_one('a').attrs['href']

        # need to format name and player id
        name = unidecode.unidecode(name)    # convert to ascii
        hall_of_fame = False
        if name[-1] == '*':
            name = name[0:-1]
            hall_of_fame = True
        player_id = link.split('/')[3]      # extract playerID.html
        player_id = player_id.split('.')[0] # remove the '.html'

        # grab all table data for the row
        cols = row.find_all('td')

        # extract remaining data
        year_from = cols[0].text
        year_to = cols[1].text
        position = cols[2].text
        height = _convert_to_inches(cols[3].text)
        weight = None
        if cols[4].text != None and cols[4].text != '':
            weight = int(cols[4].text)
        birthdate = _reformat_birthdate(cols[5].text)
        colleges = cols[6].text

        # nullify empty strings
        if position == '':
            position = None
        if birthdate == '':
            birthdate = None
        if colleges == '':
            colleges = None

        # construct playerinfo object
        player = PlayerInfo(player_id, name, year_from, year_to, position,
            height, weight, birthdate, colleges, hall_of_fame)
        
        # add to the list
        players_list.append(player)
    
    return players_list

def _convert_to_inches(height_str: str) -> int:
    """ Utility function to convert feet-inches to inches """
    if height_str == None or height_str == '':
        return None
    else:
        feet = int(height_str.split('-')[0])
        inches = int(height_str.split('-')[1])
        return (feet * 12) + inches

def _reformat_birthdate(birthdate: str) -> str:
    if birthdate == None or birthdate == '':
        return None
    else:
        return datetime.strptime(birthdate, '%B %d, %Y').strftime('%Y-%m-%d')