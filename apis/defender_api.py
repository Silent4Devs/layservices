import requests
from config.settings import DEFENDER_API
from utils.auth_manager import get_defender_token

class DefenderAPI:
    def __init__(self):
        self.base_url = DEFENDER_API["base_url_def"]
        self.token = get_defender_token()

    def get_alerts(self):
        url = f"{self.base_url}/alerts"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        return response.json()
