"""This module will contain all jobs for this Dagster project"""

from dagster import AssetSelection, define_asset_job


JOB_LEAGUES = "update_country_data"
JOB_STANDINGS_STATISTICS = "updated_league_data"

update_country_data_job = define_asset_job(
    name=JOB_LEAGUES,
    selection=AssetSelection.groups("update_country_data"),
    tags={"job": JOB_LEAGUES},
)
updated_league_data_job = define_asset_job(
    name=JOB_STANDINGS_STATISTICS,
    selection=AssetSelection.groups("updated_league_data"),
    tags={"job": JOB_LEAGUES},
)

JOBS = [update_country_data_job, updated_league_data_job]
