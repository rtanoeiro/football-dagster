""""
This module will contains all assets for this Dagster project
"""
import os

import pandas as pd
import requests
from dagster import asset, OpExecutionContext

from football_dagster.utils.tables_schema import league_data_json, leagues

# TODO: Check how we can improve logging into Dagster assets
# TODO: Check how to create separate workflows so even though assets
# are dependent on each other, they have a different pipeline
# TODO: Check how we can integrate a SQL Export


@asset(
    required_resource_keys={"credentials"},
    group_name="update_country_data",
)
def get_country_leagues(context: OpExecutionContext):
    """Gathering leagues data available on API

    Args:
        credentials (Dictionary): Asset to load credentials.

    Raises:
        AssertionError: In case the extraction fails, an error is raised
    """

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
            headers=context.resources.credentials,
            params=params,
            timeout=5,
        )
        if response.status_code == 200:
            # context.log.info("Successfully extracted data for country and league")
            pass

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

    league_dataframe = pd.DataFrame(league_dataset)

    pd.DataFrame(league_dataset).to_csv(
        f"{os.getcwd()}/football_dagster/results_data/league_data.csv", index=False
    )

    return league_dataframe
