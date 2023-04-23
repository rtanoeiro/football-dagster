"""
This script sill get the Scoring and Assist Data for each league
"""

import logging
import os

import pandas as pd
import requests
from dagster import AssetIn, asset

from footbal_dagster.utils.tables_schema import score_assists_data_json


@asset(
    ins={
        "credentials": AssetIn("get_credentials"),
        "league_data": AssetIn("get_countries_leagues"),
    }
)
def get_league_statistics(
    credentials: dict[str, str], league_data: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    From each country gathered on the league_data asset,  this asset will
    gather statistics (scoring, assisting, player grades) from each country league

    Args:
        credentials (Dictionary): Asset to load credentials.
        league_data(Asset): Asset that will hold which leagues will have their tables
            scraped

    Raises:
        AssertionError: In case the extraction fails, an error is raised
    """

    score_dataset, assist_dataset = score_assists_data_json, score_assists_data_json

    ids = league_data["id"].tolist()
    seasons = league_data["current_season"].tolist()

    for current_id, current_season in zip(ids, seasons):
        params = {"league": current_id, "season": current_season}
        response_score = requests.get(
            os.environ["SCORING_URL"], headers=credentials, params=params, timeout=5
        )

        response_assist = requests.get(
            os.environ["ASSIST_URL"], headers=credentials, params=params, timeout=5
        )
        if response_score.status_code == 200 and response_assist.status_code == 200:
            logging.info("Successfully extracted data for league statistics")
        else:
            raise AssertionError("Data failed to extracted")

        data_score = response_score.json()["response"]
        data_assist = response_assist.json()["response"]

        for data in data_score:
            player_data = data["player"]
            player_stats = data["statistics"][0]

            score_dataset["player_id"].append(player_data["id"])
            score_dataset["club_id"].append(player_stats["team"]["id"])
            score_dataset["league_id"].append(player_stats["league"]["id"])
            score_dataset["player_name"].append(player_data["name"])
            score_dataset["player_position"].append(player_stats["games"]["position"])
            score_dataset["player_rating"].append(player_stats["games"]["rating"])
            score_dataset["player_age"].append(player_data["age"])
            score_dataset["player_nationality"].append(player_data["nationality"])
            score_dataset["player_height"].append(
                str(player_data["height"]).replace(" cm", "")
            )
            score_dataset["player_weight"].append(
                str(player_data["weight"]).replace(" kg", "")
            )
            score_dataset["player_photo"].append(player_data["photo"])
            score_dataset["injured"].append(player_data["injured"])
            score_dataset["appearences"].append(player_stats["games"]["appearences"])
            score_dataset["minutes"].append(player_stats["games"]["minutes"])
            score_dataset["shots_total"].append(
                int(player_stats["shots"]["total"] or 0)
            )
            score_dataset["shots_on_goal"].append(int(player_stats["shots"]["on"] or 0))
            score_dataset["goals"].append(int(player_stats["goals"]["total"] or 0))
            score_dataset["assists"].append(int(player_stats["goals"]["assists"] or 0))
            score_dataset["passes"].append(int(player_stats["passes"]["total"] or 0))
            score_dataset["key_passes"].append(int(player_stats["passes"]["key"] or 0))
            score_dataset["passes_accuracy"].append(player_stats["passes"]["accuracy"])
            score_dataset["penalties_scored"].append(player_stats["penalty"]["scored"])
            score_dataset["penalties_missed"].append(player_stats["penalty"]["missed"])

        for data in data_assist:
            player_data = data["player"]
            player_stats = data["statistics"][0]

            assist_dataset["player_id"].append(player_data["id"])
            assist_dataset["club_id"].append(player_stats["team"]["id"])
            assist_dataset["league_id"].append(player_stats["league"]["id"])
            assist_dataset["player_name"].append(player_data["name"])
            assist_dataset["player_position"].append(player_stats["games"]["position"])
            assist_dataset["player_rating"].append(player_stats["games"]["rating"])
            assist_dataset["player_age"].append(player_data["age"])
            assist_dataset["player_nationality"].append(player_data["nationality"])
            assist_dataset["player_height"].append(
                str(player_data["height"]).replace(" cm", "")
            )
            assist_dataset["player_weight"].append(
                str(player_data["weight"]).replace(" kg", "")
            )
            assist_dataset["player_photo"].append(player_data["photo"])
            assist_dataset["injured"].append(player_data["injured"])
            assist_dataset["appearences"].append(player_stats["games"]["appearences"])
            assist_dataset["minutes"].append(player_stats["games"]["minutes"])
            assist_dataset["shots_total"].append(
                int(player_stats["shots"]["total"] or 0)
            )
            assist_dataset["shots_on_goal"].append(
                int(player_stats["shots"]["on"] or 0)
            )
            assist_dataset["goals"].append(int(player_stats["goals"]["total"] or 0))
            assist_dataset["assists"].append(int(player_stats["goals"]["assists"] or 0))
            assist_dataset["passes"].append(int(player_stats["passes"]["total"] or 0))
            assist_dataset["key_passes"].append(int(player_stats["passes"]["key"] or 0))
            assist_dataset["passes_accuracy"].append(player_stats["passes"]["accuracy"])
            assist_dataset["penalties_scored"].append(player_stats["penalty"]["scored"])
            assist_dataset["penalties_missed"].append(player_stats["penalty"]["missed"])

    score_dataframe = pd.DataFrame(score_dataset)
    assist_dataframe = pd.DataFrame(assist_dataset)

    pd.DataFrame(score_dataframe).to_csv(
        f"{os.getcwd()}/footbal_dagster/results_data/score_data.csv", index=False
    )
    pd.DataFrame(assist_dataframe).to_csv(
        f"{os.getcwd()}/footbal_dagster/results_data/assist_data.csv", index=False
    )

    return score_dataframe, assist_dataframe
