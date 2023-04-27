"""
This script sill get the Scoring and Assist Data for each league
"""

import logging
import os
from typing import Any, Union

import pandas as pd
import requests
from dagster import AssetIn, asset, OpExecutionContext

from footbal_dagster.utils.tables_schema import score_assists_data_json


@asset(
    ins={
        "league_data": AssetIn("get_country_leagues"),
    },
    required_resource_keys={"credentials"},
    group_name="Statistics_table",
)
def get_league_statistics(
    context: OpExecutionContext,
    league_data: pd.DataFrame,
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
            os.environ["SCORING_URL"],
            headers=context.resources.credentials,
            params=params,
            timeout=5,
        )

        response_assist = requests.get(
            os.environ["ASSIST_URL"],
            headers=context.resources.credentials,
            params=params,
            timeout=5,
        )

        if response_score.status_code == 200 and response_assist.status_code == 200:
            logging.info("Successfully extracted data for league statistics")
        else:
            raise AssertionError("Data failed to extracted")

        score_content = response_score.json()["response"]
        assist_content = response_assist.json()["response"]

        score_dataset = parse_score_assist_data(
            stats_data=score_content, final_dataset=score_dataset
        )
        assist_dataset = parse_score_assist_data(
            stats_data=assist_content, final_dataset=assist_dataset
        )

    score_dataframe = pd.DataFrame(score_dataset)
    assist_dataframe = pd.DataFrame(assist_dataset)

    pd.DataFrame(score_dataframe).to_csv(
        f"{os.getcwd()}/footbal_dagster/results_data/score_data.csv", index=False
    )
    pd.DataFrame(assist_dataframe).to_csv(
        f"{os.getcwd()}/footbal_dagster/results_data/assist_data.csv", index=False
    )

    return score_dataframe, assist_dataframe


def parse_score_assist_data(
    stats_data: list[dict[str, Any]],
    final_dataset: dict[str, list[Union[str, int, bool, float]]],
) -> dict[str, list[Union[str, int, bool, float]]]:
    """
    Function to parse the response that gets assists and score data
    Args:
        stats_data (dict[str, Union[str, int, Iterable]]): Dictionary containing all scraped info
        final_dataset (pd.DataFrame): Final DataFrame
    """

    for data in stats_data:
        player_data = data["player"]
        player_stats = data["statistics"][0]

        final_dataset["player_id"].append(player_data["id"])
        final_dataset["club_id"].append(player_stats["team"]["id"])
        final_dataset["league_id"].append(player_stats["league"]["id"])
        final_dataset["player_name"].append(player_data["name"])
        final_dataset["player_position"].append(player_stats["games"]["position"])
        final_dataset["player_rating"].append(player_stats["games"]["rating"])
        final_dataset["player_age"].append(player_data["age"])
        final_dataset["player_nationality"].append(player_data["nationality"])
        final_dataset["player_height"].append(
            str(player_data["height"]).replace(" cm", "")
        )
        final_dataset["player_weight"].append(
            str(player_data["weight"]).replace(" kg", "")
        )
        final_dataset["player_photo"].append(player_data["photo"])
        final_dataset["injured"].append(player_data["injured"])
        final_dataset["appearences"].append(player_stats["games"]["appearences"])
        final_dataset["minutes"].append(player_stats["games"]["minutes"])
        final_dataset["shots_total"].append(int(player_stats["shots"]["total"] or 0))
        final_dataset["shots_on_goal"].append(int(player_stats["shots"]["on"] or 0))
        final_dataset["goals"].append(int(player_stats["goals"]["total"] or 0))
        final_dataset["assists"].append(int(player_stats["goals"]["assists"] or 0))
        final_dataset["passes"].append(int(player_stats["passes"]["total"] or 0))
        final_dataset["key_passes"].append(int(player_stats["passes"]["key"] or 0))
        final_dataset["passes_accuracy"].append(player_stats["passes"]["accuracy"])
        final_dataset["penalties_scored"].append(player_stats["penalty"]["scored"])
        final_dataset["penalties_missed"].append(player_stats["penalty"]["missed"])

    return final_dataset
