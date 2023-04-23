""""
This module will contains all assets for this Dagster project
"""
import logging
import os

import pandas as pd
import requests
from dagster import asset, AssetIn
from typing import Union

from footbal_dagster.utils.tables_schema import (
    club_data_json,
    league_data_json,
    score_assists_data_json,
    standings_data,
)


@asset
def get_credentials() -> dict[str, list[Union[str, int]]]:
    """
    This function will be user to get the credentials to make API Requests
    """
    api_key = os.environ["X-RAPIDAPI-KEY"]
    api_host = os.environ["X-RAPIDAPI-HOST"]

    api_credentials = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": api_host}

    return api_credentials


@asset(ins={"credentials": AssetIn("get_credentials")})
def get_countries_leagues(credentials):
    """Gathering leagues data available on API

    Args:
        credentials (Dictionary): Asset to load credentials.
        #TODO: Perhaps convert it to a resource?

    Raises:
        AssertionError: In case the extraction fails, an error is raised
    """

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s:  %(levelname)s MESSAGE: %(message)s",
        filename="logs/league_data.txt",
    )

    leagues = {
        "England": "Premier League",
        # "Germany": "Bundesliga",
        # "Italy": "Serie A",
        # "France": "Ligue 1",
        # "Spain": "La Liga",
    }

    league_dataset = league_data_json

    for current_country, curent_league in leagues.items():
        params = {
            "country": current_country,
            "name": curent_league,
            "current": "true",
            "type": "league",
        }

        response = requests.request(
            "GET",
            url=os.environ["LEAGUES_URL"],
            headers=credentials,
            params=params,
            timeout=5,
        )
        if response.status_code == 200:
            logging.info("Successfully extracted data for country and league")
        else:
            raise AssertionError("Data failed to extracted")

        content = response.json()["response"]

        for data in content:
            league_dataset["id"].append(data["league"]["id"])
            league_dataset["name"].append(data["league"]["name"])
            league_dataset["logo"].append(data["league"]["logo"])
            league_dataset["country"].append(data["country"]["name"])
            league_dataset["flag"].append(data["country"]["flag"])
            league_dataset["current_season"].append(data["seasons"][0]["year"])
            league_dataset["start_date"].append(data["seasons"][0]["start"])
            league_dataset["end_date"].append(data["seasons"][0]["end"])

    pd.DataFrame(league_dataset).to_csv("data/league_data.csv", index=False)
