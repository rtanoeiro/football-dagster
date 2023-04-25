"""
Initialize all usable assets/resources/sensors that are defined within the project
"""

from dagster import Definitions, load_assets_from_modules

from footbal_dagster.assets.footbal_api import (
    league_standings,
    league_statistics,
    leagues_countries,
)
from footbal_dagster.resources.credentials import get_credentials

footbal_api_asset = load_assets_from_modules(
    [leagues_countries, league_standings, league_statistics]
)

all_assets = [*footbal_api_asset]
all_resources = {"credentials": get_credentials()}

defs = Definitions(assets=all_assets, resources=all_resources)
