"""
Module that will contains all tests for this Dagster project
"""
import unittest


class TestCounties(unittest.TestCase):
    def setUp(self) -> None:
        ## TODO: SETUP LEAGUES TO SCRAPE DATA
        return super().setUp()

    def test_counties(self):
        self.assertEqual(1, 1)
