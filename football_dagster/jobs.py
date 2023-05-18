"""This module will contain all jobs for this Dagster project"""

from dagster import AssetSelection, define_asset_job

# Jobs in data-dagster are used with Ops and are defined in a different way
# Show Data-Dagster op/job usage

# A job does one of two things:
# 
# Materializes a selection of Software-defined Assets
# Executes a graph of ops, which are not tied to software-defined assets
# Jobs can be launched in a few different ways:
# 
# Manually from the UI
# At fixed intervals, by schedules
# When external changes occur, using sensors

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
