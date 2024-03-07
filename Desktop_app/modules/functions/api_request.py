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

    def user_auth(self) -> str | None:
        """ Authenticate user and get token """
        login_headers = {"Content-Type": "application/json"}
        login_data = {"username": self.username, "password": self.password}

        login_response = requests.post(
            self.LOGIN_URL, headers=login_headers, json=login_data
        )

        if login_response.status_code == 200:
            self.token = login_response.headers.get("Authorization", "").split(" ")[1]
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
        """ Get list of crons from the server """
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

    # Send cron validation
    # =========================================================================

    def send_cron_validation(self, cron_id):
        """ Send cron validation to the server """
        self.user_auth()

        cron_data = {"validated": True}
        crons_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {self.token}",
        }

        validation_url = f"{self.CRONS_URL}{cron_id}/update/"
        response = requests.put(
            validation_url, headers=crons_headers, json=cron_data
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(
                f"Failed to send validation for cron {cron_id}. Status code: {response.status_code}"
            )
            return None

    # Delete unvalideted cron
    # =========================================================================

    def unvalidated_cron_delete(self, cron_id) -> str | None:
        """ Delete unvalidated cron """
        self.user_auth()

        crons_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {self.token}",
        }

        validation_url = f"{self.CRONS_URL}{cron_id}/delete/"
        response = requests.delete(validation_url, headers=crons_headers)

        if response.status_code == 204:
            print(f"{cron_id} deleted : not executable on this computer")
            return f"{cron_id} deleted : not executable on this computer"
        else:
            print(f"Failed to delete {cron_id}. {response.status_code}")
            return None
