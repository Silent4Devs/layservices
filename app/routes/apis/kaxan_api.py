import requests
import json
from config.settings import BASE_URL, HEADERS

def send_request(endpoint, data):
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.post(url, headers=HEADERS, data=json.dumps(data), verify=False)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}