# python3 -m unittest tests/test_modules/test_functions/test_api_request.py
# python3 -m unittest discover tests
# coverage run -m unittest discover
# coverage run --source=modules,modules/functions -m unittest discover --omit='**/__init__.py'
# coverage report
# coverage html

import unittest
from unittest.mock import patch
from io import StringIO
from modules.functions.api_request import CronScraper


class MockResponse:
    """ Mock response object """
    def __init__(self, status_code, json_data=None, cookies_data=None):
        self.status_code = status_code
        self._json_data = json_data
        self._cookies_data = cookies_data

    def json(self):
        return self._json_data

    @property
    def cookies(self):
        return self._cookies_data


class TestCronScraper(unittest.TestCase):
    """ Test CronScraper class """
    def setUp(self):
        """ Create a new instance of CronScraper """
        self.scraper = CronScraper("username", "password")

    def test_user_auth_success(self):
        """ Test user_auth method """
        mock_cookies = {
            "access_token": "token",
            "refresh_token": "refresh_token",
        }
        mock_response = MockResponse(
            200,
            json_data={
                "access_token": "token",
                "refresh_token": "refresh_token",
            },
            cookies_data=mock_cookies,
        )

        with patch("requests.post") as mock_post:
            mock_post.return_value = mock_response
            token = self.scraper.user_auth()
            self.assertEqual(token, "token")
            self.assertTrue(self.scraper.authenticated)

    def test_user_auth_failure(self):
        """ Test user_auth method """
        mock_response = MockResponse(401)

        with patch("requests.post") as mock_post:
            mock_post.return_value = mock_response
            with patch("sys.stdout", new=StringIO()) as fake_out:
                token = self.scraper.user_auth()
                self.assertIsNone(token)
                self.assertFalse(self.scraper.authenticated)
                printed_output = fake_out.getvalue().strip()

        self.assertEqual(
            printed_output,
            "Connection failed. Status code: 401"
        )

    def test_get_remote_crons_success(self):
        """ Test get_remote_crons method """
        mock_response = MockResponse(
            200,
            json_data=[
                {"id": 1, "name": "cron1"},
                {"id": 2, "name": "cron2"}
            ])

        with patch("requests.get") as mock_get:
            mock_get.return_value = mock_response
            crons = self.scraper.get_remote_crons("token")
            self.assertIsNotNone(crons)
            self.assertEqual(len(crons), 2)
            self.assertEqual(crons[0]["name"], "cron1")
            self.assertEqual(crons[1]["name"], "cron2")

    def test_get_remote_crons_failure(self):
        """ Test get_remote_crons method """
        mock_response = MockResponse(401)

        with patch("requests.get") as mock_get:
            mock_get.return_value = mock_response
            with patch("sys.stdout", new=StringIO()) as fake_out:
                crons = self.scraper.get_remote_crons("token")
                self.assertIsNone(crons)
                printed_output = fake_out.getvalue().strip()

        self.assertEqual(
            printed_output,
            "Unable to obtain list of crons. Status code: 401"
        )
