"""Initialize all usable assets/resources/sensors that are defined within the project"""

from dagster import load_assets_from_package_module

from football_dagster.assets import football_api

football_api_asset = load_assets_from_package_module(football_api)

ASSETS = football_api_asset
