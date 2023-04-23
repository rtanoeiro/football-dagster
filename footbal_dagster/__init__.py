"""
Initialize all usable assets/resources/sensors that are defined within the project
"""

from dagster import Definitions, load_assets_from_modules

from footbal_dagster.assets.footbal_api import (
    country_leagues,
    league_standings,
    league_statistics,
)
from footbal_dagster.assets.credentials import credentials

footbal_api_asset = load_assets_from_modules(
    [country_leagues, league_standings, league_statistics]
)
credentials_asset = load_assets_from_modules([credentials])

all_assets = [*footbal_api_asset, *credentials_asset]

defs = Definitions(
    assets=all_assets,
)
