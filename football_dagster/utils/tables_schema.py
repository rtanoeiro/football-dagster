"""
This module will contain schema for the scrapped data
"""

from typing import Union

leagues = {
    "England": "Premier League",
    # "Germany": "Bundesliga",
    # "Italy": "Serie A",
    # "France": "Ligue 1",
    # "Spain": "La Liga",
}

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
