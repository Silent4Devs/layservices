import requests
from requests.exceptions import RequestException
from config.settings import LOGRHYTHM_API
import aiohttp
import asyncio
import os


class LogRhythmAPI:
    def __init__(self):
        self.base_url = os.getenv("LOGRHYTHM_API_URL")
        self.api_key = os.getenv("LOGRHYTHM_API_TOKEN")
        self.headers = {"Authorization": f"Bearer {self.api_key}", "accept" : "application/json"}

    async def get_logs(self, params=None):
        url = f"{self.base_url}lr-alarm-api/alarms"
        alarmas_vistas = set()
        async with aiohttp.ClientSession() as session:
            while True:
                async with session.get(url=url, headers=self.headers, ssl=False) as response:
                    print("Consultando...")
                    if response.status == 200:                     
                        data = await response.json()
                    
                        data = data.get("alarmsSearchDetails")
                                          
                        for alarma in data:                         
                     
                            alarm_id = alarma.get("alarmId") 
                            if alarm_id not in alarmas_vistas:                             
                                alarmas_vistas.add(alarm_id)                            
                                print(f"Nueva alarma: {alarma}") 
                    await asyncio.sleep(0.5)
        return response.text
