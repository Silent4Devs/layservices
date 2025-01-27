import requests
from config.settings import LOGRHYTHM_API

class LogRhythmAPI:
    def __init__(self):
        self.base_url = LOGRHYTHM_API["base_url"]
        self.api_key = LOGRHYTHM_API["api_key"]
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def get_logs(self, params=None):
        url = f"{self.base_url}/logs"
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()
