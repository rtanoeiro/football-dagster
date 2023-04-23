from dagster import Definitions, load_assets_from_modules

from footbal_dagster.assets import country_leagues_asset

all_assets = load_assets_from_modules([country_leagues_asset])

defs = Definitions(
    assets=all_assets,
)
