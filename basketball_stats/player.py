import json
from models import *

class Player:

    def __init__(self, player_info: PlayerInfo, all_seasons_totals: []):

        self.player_info = player_info

        # Divide the seasons into regular seasons and playoffs
        self.regular_season_stats = list(filter(
            lambda season: season.playoffs == False, all_seasons_totals
        ))
        self.playoff_stats = list(filter(
            lambda season: season.playoffs == True, all_seasons_totals
        ))

        # Calculate career averages
        regular_career = self._calculate_career(self.regular_season_stats)
        playoff_career = self._calculate_career(self.playoff_stats)
           

        # Convert SeasonTotals into full PlayerSeason objects
        self.regular_season_stats = list(map(
            lambda season: PlayerSeason(season), self.regular_season_stats
        ))  
        self.playoff_stats = list(map(
            lambda season: PlayerSeason(season), self.playoff_stats
        ))  

        # Sort season by year then by total_games_played
        self.regular_season_stats.sort(key=lambda season: (season.year, season.total_games_played))
        self.playoff_stats.sort(key=lambda season: (season.year, season.total_games_played))

        # Add career into season lists 
        if regular_career != None:
            self.regular_season_stats.append(PlayerSeason(regular_career))
        if playoff_career != None:
            self.playoff_stats.append(PlayerSeason(playoff_career))


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

    def _calculate_career(self, season_totals: []) -> PlayerSeasonTotals:

        if season_totals == None or len(season_totals) == 0:
            return None

        # Declare all variables of a PlayerSeasonTotals
        games_played = games_started = minutes = field_goals_made = field_goals_attempted = 0
        threes_made = threes_attempted = twos_made = twos_attempted = 0
        free_throws_made = free_throws_attempted = offensive_rebounds = defensive_rebounds = 0
        total_rebounds = assists = steals = blocks = turnovers = 0
        personal_fouls = points = 0

        # Sum up the totals
        for season in season_totals:
            games_played += season.games_played or 0
            games_started += season.games_started or 0
            minutes += season.minutes or 0
            field_goals_made += season.field_goals_made or 0
            field_goals_attempted += season.field_goals_attempted or 0
            threes_made += season.threes_made or 0
            threes_attempted += season.threes_attempted or 0
            twos_made += season.twos_made or 0
            twos_attempted += season.twos_attempted or 0
            free_throws_made += season.free_throws_made or 0
            free_throws_attempted += season.free_throws_attempted or 0
            offensive_rebounds += season.offensive_rebounds or 0
            defensive_rebounds += season.defensive_rebounds or 0
            total_rebounds += season.total_rebounds or 0
            assists += season.assists or 0
            steals += season.steals or 0
            blocks += season.blocks or 0
            turnovers += season.turnovers or 0
            personal_fouls += season.personal_fouls or 0
            points += season.points or 0
        
        return PlayerSeasonTotals(self.player_info.player_id, None, None,
            'Career', None, games_played, games_started, minutes, field_goals_made,
            field_goals_attempted, threes_made, threes_attempted, twos_made,
            twos_attempted, free_throws_made, free_throws_attempted, offensive_rebounds,
            defensive_rebounds, total_rebounds, assists, steals, blocks, turnovers,
            personal_fouls, points)