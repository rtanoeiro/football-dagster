"""Initialize all usable assets/resources/sensors that are defined within the project"""

from dagster import Definitions

from football_dagster.assets import ASSETS
from football_dagster.resources import RESOURCES
from .jobs import JOBS

defs = Definitions(assets=[*ASSETS], resources=RESOURCES, jobs=[*JOBS])
