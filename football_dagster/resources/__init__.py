"""
Initialize all usable assets/resources/sensors that are defined within the project
"""

from football_dagster.resources.credentials import get_credentials


RESOURCES = {"credentials": get_credentials}
