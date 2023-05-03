"""
Asset to get the credentials to scrape data
"""

import os
from dagster import resource


@resource
def get_credentials():
    """
    This function will be user to get the credentials to make API Requests
    """
    return {
        "X-RapidAPI-Key": os.environ["X-RAPIDAPI-KEY"],
        "X-RapidAPI-Host": os.environ["X-RAPIDAPI-HOST"],
    }
