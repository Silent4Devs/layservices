import requests
from config.settings import REMEDY_API

class RemedyAPI:
    def __init__(self):
        self.base_url = REMEDY_API["base_url"]
        self.auth = (REMEDY_API["username"], REMEDY_API["password"])

    def create_ticket(self, ticket_data):
        url = f"{self.base_url}/tickets"
        response = requests.post(url, auth=self.auth, json=ticket_data)
        return response.json()
