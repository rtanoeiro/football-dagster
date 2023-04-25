"""
Initialize all usable assets/resources/sensors that are defined within the project
"""

from dagster import Definitions, load_assets_from_modules, ResourceDefinition, String

from footbal_dagster.assets.footbal_api import (
    league_standings,
    league_statistics,
    leagues_countries,
)
from footbal_dagster.resources.credentials import get_credentials

footbal_api_asset = load_assets_from_modules(
    [leagues_countries, league_standings, league_statistics]
)

api_credentials = ResourceDefinition(
    resource_fn=get_credentials,
    config_schema={
        "X-RapidAPI-Key": String,
        "X-RapidAPI-Host": String,
    },
)

all_assets = [*footbal_api_asset]
all_resources = {"credentials": api_credentials}

defs = Definitions(assets=all_assets, resources=all_resources)
