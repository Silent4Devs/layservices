import requests
from config.settings import PRTG_API

class PRTGAPI:
    def __init__(self):
        self.base_url = PRTG_API["base_url"]
        self.auth_params = {
            "username": PRTG_API["username"],
            "password": PRTG_API["password"]
        }

    def get_sensors(self):
        url = f"{self.base_url}/table.json"
        response = requests.get(url, params=self.auth_params)
        return response.json()
