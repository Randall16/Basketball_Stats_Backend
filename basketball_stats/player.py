import json
from models import *

class Player:

    def __init__(self, player_info: PlayerInfo, all_seasons_totals: []):

        self.player_info = player_info

        self.regular_season_stats = []
        self.playoff_stats = []

        # divide the seasons into regular seasons and playoffs
        for season in all_seasons_totals:
            all_stats = PlayerSeason(season)
            if season.playoffs == 0:
                self.regular_season_stats.append(all_stats)
            elif season.playoffs == 1:
                self.playoff_stats.append(all_stats)

        # sort season by year then by total_games_played
        self.regular_season_stats.sort(key=lambda season: (season.year, season.total_games_played))
        self.playoff_stats.sort(key=lambda season: (season.year, season.total_games_played))


    def to_json(self, print_pretty: bool=False):
        json_data = {}

        json_data = self.player_info._asdict()

        # convert to boolean
        json_data['hall_of_fame'] = bool(json_data['hall_of_fame'])

        json_data['regular_season_stats'] = [season.__dict__ for season in self.regular_season_stats]
        json_data['playoff_stats'] = [season.__dict__ for season in self.playoff_stats]

        for i in json_data['regular_season_stats']:
            del i['player_id']
            del i['playoffs']

        for i in json_data['playoff_stats']:
            del i['player_id']
            del i['playoffs']

        if print_pretty:
            return json.dumps(json_data, default=str, indent=4)
        else:
            return json.dumps(json_data, default=str)