"""
Initialize all usable assets/resources/sensors that are defined within the project
"""

from dagster import Definitions

from football_dagster.assets import ASSETS
from football_dagster.resources import RESOURCES


all_assets = [*ASSETS]
all_resources = RESOURCES

defs = Definitions(assets=all_assets, resources=all_resources)
