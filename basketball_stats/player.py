import json
from models import *

class Player:

    def __init__(self, player_info: PlayerInfo, all_seasons_totals: []):
        #playoff_totals: PlayerSeasonTotals ):

        self.player_info = player_info

        # Filter all seasons into regular season and playoffs
        self.season_totals = list(filter(lambda season: season.playoffs == 0, all_seasons_totals))
        self.playoff_totals = list(filter(lambda season: season.playoffs == 1, all_seasons_totals))
        
        # Create a list containing all seasons averages
        all_averages = [PlayerSeasonPerGame.from_season_totals(season) for season in all_seasons_totals]

        # Filter all_averages into regular season and playoffs
        self.season_averages = list(filter(lambda season: season.playoffs == 0, all_averages))
        self.playoff_averages = list(filter(lambda season: season.playoffs == 1, all_averages))
    
    def to_json(self, print_pretty: bool=False):
        json_data = {}
        
        json_data = self.player_info._asdict()

        # Convert hall_of_fame key to a boolean value
        json_data['hall_of_fame'] = bool(self.player_info.hall_of_fame)

        # Make an entry for each type of season
        # each season is a NamedTuple so convert by calling _asdict() function
        json_data['regular_season_averages'] = [season._asdict() for season in self.season_averages]
        json_data['regular_season_totals'] = [season._asdict() for season in self.season_totals]
        json_data['playoff_averages'] = [season._asdict() for season in self.playoff_averages]
        json_data['playoff_totals'] = [season._asdict() for season in self.playoff_totals]
        
        
        # Delete 'player_id' and 'playoffs' key from each season
        for i in json_data['regular_season_totals']: del i['player_id']; del i['playoffs']
        for i in json_data['regular_season_averages']: del i['player_id']; del i['playoffs']
        for i in json_data['playoff_totals']: del i['player_id']; del i['playoffs']
        for i in json_data['playoff_averages']: del i['player_id']; del i['playoffs']
        
        if(print_pretty):
            return json.dumps(json_data, default=str, indent=4)
        else:
            return json.dumps(json_data, default=str)