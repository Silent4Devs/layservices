import os
import requests

params = {
    "content": "messages",
    "columns": "group,group_raw,device,device_raw,sensor,sensor_raw,status,status_raw",
    "apitoken": os.getenv("PRTG_API_TOKEN")
}

try:
    response = os.getenv("PRTG_API_URL", params=params)
    response.raise_for_status()  # Lanza una excepción si hay un error HTTP
    data = response.json()
    print("Datos obtenidos:", data)
except requests.exceptions.RequestException as e:
    print(f"Error al realizar la solicitud: {e}")
    data = None