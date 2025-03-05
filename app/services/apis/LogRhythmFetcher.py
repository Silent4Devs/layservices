import aiohttp
import asyncio
import os
from dotenv import load_dotenv
from .AlarmFetcher import AlarmFetcher

class LoghRhythmAlarmFetcher(AlarmFetcher):

    def __init__(self, url: str, api_key: str):
        super().__init__(url, api_key)
        self.seen_alerts = set()
        self.headers = {"Authorization": f"Bearer {self.api_key}", "accept" : "application/json"}

    async def fetchAlarms(self):

        async with aiohttp.ClientSession() as session:
            while True:
                async with session.get(url=self.url, headers=self.headers, ssl=False) as response:
                    print("Consultando...")
                    if response.status == 200:                     
                        data = await response.json()
                    
                        data = data.get("alarmsSearchDetails")
                                          
                        for alarma in data:                         
                     
                            alarm_id = alarma.get("alarmId") 
                            if alarm_id not in self.seen_alerts:                             
                                self.seen_alerts.add(alarm_id)                            
                                print(f"Nueva alarma: {alarma}") 
                    await asyncio.sleep(0.3)
        return response.text

async def main():
    load_dotenv()
    url = os.getenv("LOGRHYTHM_API_TOKEN") + "lr-alarm-api/alarms"
    api_key = os.getenv("LOGRHYTHM_API_TOKEN")
    if not api_key:
        print("API_KEY no encontrada en .env")
        return
    fetcher = LoghRhythmAlarmFetcher(url, api_key)
    await fetcher.fetchAlarms()

if __name__ == "__main__":
    asyncio.run(main())
