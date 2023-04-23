"""
Gathering leagues data available on API
"""

import logging
import os

import pandas as pd
import requests
from dagster import AssetIn, asset

from footbal_dagster.utils.tables_schema import club_data_json, standings_data


@asset(
    ins={
        "credentials": AssetIn("get_credentials"),
        "league_data": AssetIn("get_countries_leagues"),
    }
)
def league_standings(
    credentials: dict[str, str], league_data: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """From each country gathered on the league_data asset,
    This asset will gather standings (league table) and data for each club on the league

    Args:
        credentials (Dictionary): Asset to load credentials.
        #TODO: Perhaps convert it to a resource?
        league_data(Asset): Asset that will hold which leagues will have their tables
            scraped

    Raises:
        AssertionError: In case the extraction fails, an error is raised
    """

    club_dataset = club_data_json
    standings_dataset = standings_data

    ids = league_data["id"].tolist()
    seasons = league_data["current_season"].tolist()

    for current_id, current_season in zip(ids, seasons):
        params = {
            "season": current_season,
            "league": current_id,
        }

        response = requests.get(
            url=os.environ["STANDINGS_URL"],
            headers=credentials,
            params=params,
            timeout=5,
        )

        if response.status_code == 200:
            logging.info("Successfully extracted data for league standings")
        else:
            raise AssertionError("Data failed to extracted")

        content = response.json()["response"]

        league_data = content[0]["league"]
        standings = content[0]["league"]["standings"][0]

        for standing in standings:
            club_dataset["club_id"].append(standing["team"]["id"])
            club_dataset["club_name"].append(standing["team"]["name"])
            club_dataset["club_flag"].append(standing["team"]["logo"])
            club_dataset["club_country"].append(league_data["country"])

            standings_dataset["league_id"].append(league_data["id"])
            standings_dataset["club_id"].append(standing["team"]["id"])
            standings_dataset["club_name"].append(standing["team"]["name"])
            standings_dataset["club_form"].append(standing["form"])
            standings_dataset["league_rank"].append(standing["rank"])
            standings_dataset["description"].append(standing["description"])
            standings_dataset["points"].append(standing["points"])
            standings_dataset["goalsDiff"].append(standing["goalsDiff"])
            standings_dataset["status"].append(standing["status"])
            standings_dataset["last_updated"].append(standing["update"])
            standings_dataset["home_played"].append(standing["home"]["played"])
            standings_dataset["home_win"].append(standing["home"]["win"])
            standings_dataset["home_draw"].append(standing["home"]["draw"])
            standings_dataset["home_losses"].append(standing["home"]["lose"])
            standings_dataset["home_goals"].append(standing["home"]["goals"]["for"])
            standings_dataset["home_conceded"].append(
                standing["home"]["goals"]["against"]
            )
            standings_dataset["away_played"].append(standing["away"]["played"])
            standings_dataset["away_win"].append(standing["away"]["win"])
            standings_dataset["away_draw"].append(standing["away"]["draw"])
            standings_dataset["away_losses"].append(standing["away"]["lose"])
            standings_dataset["away_goals"].append(standing["away"]["goals"]["for"])
            standings_dataset["away_conceded"].append(
                standing["away"]["goals"]["against"]
            )

    standings_dataframe = pd.DataFrame(standings_dataset)
    club_dataframe = pd.DataFrame(club_dataset)

    pd.DataFrame(standings_dataset).to_csv(
        f"{os.getcwd()}/footbal_dagster/results_data/standings_data.csv", index=False
    )
    pd.DataFrame(club_dataset).to_csv(
        f"{os.getcwd()}/footbal_dagster/results_data/club_data.csv", index=False
    )

    return standings_dataframe, club_dataframe
