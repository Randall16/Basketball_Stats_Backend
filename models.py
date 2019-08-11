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


class PlayerSeasonPerGame(typing.NamedTuple):

    year: str
    playoffs: bool
    team: str
    age: int
    games_played: int
    games_started: int
    minutes: float
    field_goal_percentage: float
    three_percentage: float
    free_throw_percentage: float
    offensive_rebounds: float
    defensive_rebounds: float
    total_rebounds: float
    assists: float
    steals: float
    blocks: float
    turnovers: float
    personal_fouls: float
    points: float

    @classmethod
    def from_season_totals(cls, season_totals: PlayerSeasonTotals):
        year = season_totals.year
        playoffs = season_totals.playoffs
        team = season_totals.team
        age = season_totals.age
        games_played = season_totals.games_played
        games_started = season_totals.games_started
        minutes = None
        field_goal_percentage = None
        three_percentage = None
        free_throw_percentage = None
        offensive_rebounds = None
        defensive_rebounds = None
        total_rebounds = None
        assists = None
        steals = None
        blocks = None
        turnovers = None
        personal_fouls = None
        points = None

        # validate input    
        if season_totals == None or season_totals.games_played == None or season_totals.games_played <= 0:
            return cls(year, playoffs, team, age, games_played, games_started,
                minutes, field_goal_percentage, three_percentage, free_throw_percentage,
                offensive_rebounds, defensive_rebounds, total_rebounds, assists,
                steals, blocks, turnovers, personal_fouls, points)

        if season_totals.minutes != None:
            minutes = season_totals.minutes / season_totals.games_played
            minutes = round(minutes, 1)

        if season_totals.field_goals_attempted != None and season_totals.field_goals_made != None:
            if season_totals.field_goals_attempted <= 0:
                field_goal_percentage = 0
            else:
                field_goal_percentage = season_totals.field_goals_made / season_totals.field_goals_attempted
                field_goal_percentage = round(field_goal_percentage, 3)

        if season_totals.threes_attempted != None and season_totals.threes_made != None:
            if season_totals.threes_attempted <= 0:
                three_percentage = 0
            else:
                three_percentage = season_totals.threes_made / season_totals.threes_attempted
                three_percentage = round(three_percentage, 3)

        if season_totals.free_throws_attempted != None and season_totals.free_throws_made != None:
            if season_totals.free_throws_attempted <= 0:
                free_throw_percentage = 0
            else:
                free_throw_percentage = season_totals.free_throws_made / season_totals.free_throws_attempted
                free_throw_percentage = round(free_throw_percentage, 3)

        if season_totals.offensive_rebounds != None:
            offensive_rebounds = season_totals.offensive_rebounds / season_totals.games_played
            offensive_rebounds = round(offensive_rebounds, 1)

        if season_totals.defensive_rebounds != None:
            defensive_rebounds = season_totals.defensive_rebounds / season_totals.games_played
            defensive_rebounds = round(defensive_rebounds, 1)

        if season_totals.total_rebounds != None:
            total_rebounds = season_totals.total_rebounds / season_totals.games_played
            total_rebounds = round(total_rebounds, 1)

        if season_totals.assists != None:
            assists = season_totals.assists / season_totals.games_played
            assists = round(assists, 1)

        if season_totals.assists != None:
            assists = season_totals.assists / season_totals.games_played
            assists = round(assists, 1)

        if season_totals.steals != None:
            steals = season_totals.steals / season_totals.games_played
            steals = round(steals, 1)

        if season_totals.blocks != None:
            blocks = season_totals.blocks / season_totals.games_played
            blocks = round(blocks, 1)

        if season_totals.turnovers != None:
            turnovers = season_totals.turnovers / season_totals.games_played
            turnovers = round(turnovers, 1)

        if season_totals.personal_fouls != None:
            personal_fouls = season_totals.personal_fouls / season_totals.games_played
            personal_fouls = round(personal_fouls, 1)

        if season_totals.points != None:
            points = season_totals.points / season_totals.games_played
            points = round(points, 1)

        return cls(year, playoffs, team, age, games_played, games_started,
                minutes, field_goal_percentage, three_percentage, free_throw_percentage,
                offensive_rebounds, defensive_rebounds, total_rebounds, assists,
                steals, blocks, turnovers, personal_fouls, points)