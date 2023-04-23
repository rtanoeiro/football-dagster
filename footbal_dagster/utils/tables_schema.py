"""
This module will contain schema for the scrapped data
"""

from typing import Union, TypedDict

club_data_json: dict[str, list[Union[str, int]]] = {
    "club_id": [],
    "club_name": [],
    "club_flag": [],
    "club_country": [],
}

league_data_json: dict[str, list[Union[str, int]]] = {
    "id": [],
    "name": [],
    "logo": [],
    "country": [],
    "flag": [],
    "current_season": [],
    "start_date": [],
    "end_date": [],
}

score_assists_data_json: dict[str, list[Union[str, int, bool, float]]] = {
    "player_id": [],
    "club_id": [],
    "league_id": [],
    "player_name": [],
    "player_position": [],
    "player_rating": [],
    "player_age": [],
    "player_nationality": [],
    "player_height": [],
    "player_weight": [],
    "player_photo": [],
    "injured": [],
    "appearences": [],
    "minutes": [],
    "shots_total": [],
    "shots_on_goal": [],
    "goals": [],
    "assists": [],
    "passes": [],
    "key_passes": [],
    "passes_accuracy": [],
    "penalties_scored": [],
    "penalties_missed": [],
}

standings_data: dict[str, list[Union[str, int]]] = {
    "league_id": [],
    "club_id": [],
    "club_name": [],
    "club_form": [],
    "league_rank": [],
    "description": [],
    "points": [],
    "goalsDiff": [],
    "status": [],
    "last_updated": [],
    "home_played": [],
    "home_win": [],
    "home_draw": [],
    "home_losses": [],
    "home_goals": [],
    "home_conceded": [],
    "away_played": [],
    "away_win": [],
    "away_draw": [],
    "away_losses": [],
    "away_goals": [],
    "away_conceded": [],
}


class ScoreAssistMetada(TypedDict):
    """
    Class to hold the Metadata for the Score and Assist Tables

    Args:
        TypedDict (TypedDict): TypedDict introduced on Python 3.8+
        https://peps.python.org/pep-0589/
    """

    player_id: int
    club_id: int
    league_id: int
    player_name: str
    player_position: str
    player_rating: float
    player_age: int
    player_nationality: str
    player_height: int
    player_weight: int
    player_photo: str
    injured: bool
    appearences: int
    minutes: int
    shots_total: int
    shots_on_goal: int
    goals: int
    assists: int
    passes: int
    key_passes: int
    passes_accuracy: int
    penalties_scored: int
    penalties_missed: int
