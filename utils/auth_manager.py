import requests
from config.settings import DEFENDER_API

def get_defender_token():
    url = f"https://login.microsoftonline.com/{DEFENDER_API['tenant_id']}/oauth2/v2.0/token"
    data = {
        "client_id": DEFENDER_API["client_id"],
        "client_secret": DEFENDER_API["client_secret"],
        "grant_type": "client_credentials",
        "scope": "https://graph.microsoft.com/.default"
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json().get("access_token")
