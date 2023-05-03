"""
Initialize all usable assets/resources/sensors that are defined within the project
"""

from dagster import load_assets_from_modules

from football_dagster.assets.football_api import (
    league_standings,
    league_statistics,
    leagues_countries,
)

FOOTBALL_API = "football_api"
football_api_asset = load_assets_from_modules(
    [leagues_countries, league_standings, league_statistics], group_name="football_api"
)

ASSETS = football_api_asset
