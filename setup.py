"""
Script containing dependencies of dagster module 
"""

from setuptools import find_packages, setup

setup(
    name="football_dagster",
    packages=find_packages(exclude=["football_dagster_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "pandas",
        "requests",
        "stubs",
        "types-requests",
        "pyodbc",
    ],
    extras_require={"dev": ["dagit", "pytest", "black", "pylint", "mypy", "bandit"]},
)
