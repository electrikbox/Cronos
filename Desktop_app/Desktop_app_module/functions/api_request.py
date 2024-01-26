""" Scrapper to get user's crons list """

import sys
import requests


class CronScraper:
    LOGIN_URL = "http://localhost:8000/api/login/"
    CRONS_URL = "http://localhost:8000/api/crons/"

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        self.authenticated = False
        self.token = None

    # Function to log in and get the token
    # =========================================================================

    def user_auth(self):
        login_headers = {"Content-Type": "application/json"}
        login_data = {"username": self.username, "password": self.password}

        login_response = requests.post(
            self.LOGIN_URL, headers=login_headers, json=login_data
        )

        if login_response.status_code == 200:
            self.token = login_response.json().get("token", "")
            self.authenticated = True
            return self.token
        else:
            print(
                f"Connection failed. Status code: {login_response.status_code}"
            )
            self.authenticated = False
            return None

    # Get user crons list
    # =========================================================================

    def get_remote_crons(self, token):
        self.token = token

        crons_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {self.token}",
        }

        response = requests.get(self.CRONS_URL, headers=crons_headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(
                f"Unable to obtain list of crons. Status code: {response.status_code}"
            )
            return None


# =================================================================

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Please provide a username and password in argument"
        )
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]

    cron_scraper = CronScraper(username, password)
    cron_scraper.user_auth()

    if cron_scraper.authenticated:
        print("Successful authentication")
        crons_list = cron_scraper.get_remote_crons()

        if crons_list:
            print(crons_list)
    else:
        print("Authentication failed")
