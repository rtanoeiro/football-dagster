"""
Asset to get the credentials to scrape data
"""

import os
from dagster import asset


@asset
def get_credentials() -> dict[str, str]:
    """
    This function will be user to get the credentials to make API Requests
    """
    api_key = os.environ["X-RAPIDAPI-KEY"]
    api_host = os.environ["X-RAPIDAPI-HOST"]

    api_credentials = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": api_host}

    return api_credentials