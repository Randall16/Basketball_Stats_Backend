import typing

class PlayerInfo(typing.NamedTuple):

    player_id: str
    name: str
    year_from: str
    year_to: str
    position: str
    height: int
    weight: int
    birthdate: str
    colleges: str
    hall_of_fame: bool


class PlayerSeasonTotals(typing.NamedTuple):

    player_id: str
    year: str
    playoffs: bool
    team: str
    age: int
    games_played: int
    games_started: int
    minutes: int
    field_goals_made: int
    field_goals_attempted: int
    threes_made: int
    threes_attempted: int
    twos_made: int
    twos_attempted: int
    free_throws_made: int
    free_throws_attempted: int
    offensive_rebounds: int
    defensive_rebounds: int
    total_rebounds: int
    assists: int
    steals: int
    blocks: int
    turnovers: int
    personal_fouls: int
    points: int


class PlayerSeason():
    
    # info
    player_id: str
    year: str
    playoffs: bool
    team: str
    age: int

    # totals
    total_games_played: int
    total_games_started: int
    total_minutes: int
    total_field_goals_made: int
    total_field_goals_attempted: int
    total_threes_made: int
    total_threes_attempted: int
    total_twos_made: int
    total_twos_attempted: int
    total_free_throws_made: int
    total_free_throws_attempted: int
    total_offensive_rebounds: int
    total_defensive_rebounds: int
    total_rebounds: int
    total_assists: int
    total_steals: int
    total_blocks: int
    total_turnovers: int
    total_personal_fouls: int
    total_points: int

    # shooting percentages
    field_goal_percentage: float
    three_percentage: float
    twos_percentage: float
    free_throw_percentage: float
    effective_field_goal_percentage: float
    true_shooting_percentage: float

    # per game
    minutes_per_game: float
    offensive_rebounds_per_game: float
    defensive_rebounds_per_game: float
    total_rebounds_per_game: float
    assists_per_game: float
    steals_per_game: float
    blocks_per_game: float
    turnovers_per_game: float
    personal_fouls_per_game: float
    points_per_game: float


    def __init__(self, season_totals: PlayerSeasonTotals):

        self.player_id = season_totals.player_id
        self.year = season_totals.year
        self.playoffs = season_totals.playoffs
        self.team = season_totals.team
        self.age = season_totals.age

        self.total_games_played = season_totals.games_played
        self.total_games_started = season_totals.games_started
        self.total_minutes = season_totals.minutes
        self.total_field_goals_made = season_totals.field_goals_made
        self.total_field_goals_attempted = season_totals.field_goals_attempted
        self.total_threes_made = season_totals.threes_made
        self.total_threes_attempted = season_totals.threes_attempted
        self.total_twos_made = season_totals.twos_made
        self.total_twos_attempted = season_totals.twos_attempted
        self.total_free_throws_made = season_totals.free_throws_made
        self.total_free_throws_attempted = season_totals.free_throws_attempted
        self.total_offensive_rebounds = season_totals.offensive_rebounds
        self.total_defensive_rebounds = season_totals.defensive_rebounds
        self.total_rebounds = season_totals.total_rebounds
        self.total_assists = season_totals.assists
        self.total_steals = season_totals.steals
        self.total_blocks = season_totals.blocks
        self.total_turnovers = season_totals.turnovers
        self.total_personal_fouls = season_totals.personal_fouls
        self.total_points = season_totals.points

        self.field_goal_percentage = None
        self.three_percentage = None
        self.two_percentage = None
        self.free_throw_percentage = None
        self.effective_field_goal_percentage = None
        self.true_shooting_percentage = None

        self.minutes_per_game = None
        self.offensive_rebounds_per_game = None
        self.defensive_rebounds_per_game = None
        self.total_rebounds_per_game = None
        self.assists_per_game = None
        self.steals_per_game = None
        self.blocks_per_game = None
        self.turnovers_per_game = None
        self.personal_fouls_per_game = None
        self.points_per_game = None

        self._calculate_per_game(season_totals)
    
    def _calculate_per_game(self, season_totals: PlayerSeasonTotals):
        """ calculate all per game stats """

        # validate input    
        if season_totals == None or season_totals.games_played == None or season_totals.games_played <= 0:
            return

        if season_totals.minutes != None:
            self.minutes_per_game = season_totals.minutes / season_totals.games_played
            self.minutes_per_game = round(self.minutes_per_game, 1)

        if season_totals.field_goals_attempted != None and season_totals.field_goals_made != None:
            if season_totals.field_goals_attempted <= 0:
                self.field_goal_percentage = 0
            else:
                self.field_goal_percentage = season_totals.field_goals_made / season_totals.field_goals_attempted
                self.field_goal_percentage = round(self.field_goal_percentage, 3)

        if season_totals.threes_attempted != None and season_totals.threes_made != None:
            if season_totals.threes_attempted <= 0:
                self.three_percentage = 0
            else:
                self.three_percentage = season_totals.threes_made / season_totals.threes_attempted
                self.three_percentage = round(self.three_percentage, 3)

        if season_totals.twos_attempted != None and season_totals.twos_attempted != None:
            if season_totals.twos_attempted <= 0:
                self.three_percentage = 0
            else:
                self.two_percentage = season_totals.twos_made / season_totals.twos_attempted
                self.two_percentage = round(self.two_percentage, 3)

        if season_totals.free_throws_attempted != None and season_totals.free_throws_made != None:
            if season_totals.free_throws_attempted <= 0:
                self.free_throw_percentage = 0
            else:
                self.free_throw_percentage = season_totals.free_throws_made / season_totals.free_throws_attempted
                self.free_throw_percentage = round(self.free_throw_percentage, 3)

        if (season_totals.field_goals_attempted != None and season_totals.field_goals_made != None
            and season_totals.threes_made != None and season_totals.field_goals_attempted != 0):
            # using eFG% formula
            self.effective_field_goal_percentage = ((season_totals.field_goals_made
                + 0.5 * season_totals.threes_made) / season_totals.field_goals_attempted)
            self.effective_field_goal_percentage = round(self.effective_field_goal_percentage, 3)

        if (season_totals.points != None and season_totals.free_throws_attempted != None
            and season_totals.field_goals_attempted != None and season_totals.free_throws_attempted != 0):
            # using true shooting formula
            self.true_shooting_percentage = (season_totals.points / (2 * (
                season_totals.field_goals_attempted + 0.44 * season_totals.free_throws_attempted)))
            self.true_shooting_percentage = round(self.true_shooting_percentage, 3)

        if season_totals.offensive_rebounds != None:
            self.offensive_rebounds_per_game = season_totals.offensive_rebounds / season_totals.games_played
            self.offensive_rebounds_per_game = round(self.offensive_rebounds_per_game, 1)

        if season_totals.defensive_rebounds != None:
            self.defensive_rebounds_per_game = season_totals.defensive_rebounds / season_totals.games_played
            self.defensive_rebounds_per_game = round(self.defensive_rebounds_per_game, 1)

        if season_totals.total_rebounds != None:
            self.total_rebounds_per_game = season_totals.total_rebounds / season_totals.games_played
            self.total_rebounds_per_game = round(self.total_rebounds_per_game, 1)

        if season_totals.assists != None:
            self.assists_per_game = season_totals.assists / season_totals.games_played
            self.assists_per_game = round(self.assists_per_game, 1)

        if season_totals.steals != None:
            self.steals_per_game = season_totals.steals / season_totals.games_played
            self.steals_per_game = round(self.steals_per_game, 1)

        if season_totals.blocks != None:
            self.blocks_per_game = season_totals.blocks / season_totals.games_played
            self.blocks_per_game = round(self.blocks_per_game, 1)

        if season_totals.turnovers != None:
            self.turnovers_per_game = season_totals.turnovers / season_totals.games_played
            self.turnovers_per_game = round(self.turnovers_per_game, 1)

        if season_totals.personal_fouls != None:
            self.personal_fouls_per_game = season_totals.personal_fouls / season_totals.games_played
            self.personal_fouls_per_game = round(self.personal_fouls_per_game, 1)

        if season_totals.points != None:
            self.points_per_game = season_totals.points / season_totals.games_played
            self.points_per_game = round(self.points_per_game, 1)