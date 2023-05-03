"""
Initialize all usable assets/resources/sensors that are defined within the project
"""

from dagster import load_assets_from_modules

from footbal_dagster.assets.footbal_api import (
    league_standings,
    league_statistics,
    leagues_countries,
)

footbal_api_asset = load_assets_from_modules(
    [leagues_countries, league_standings, league_statistics], group_name="footbal_api"
)

ASSETS = footbal_api_asset
