from AlarmFetcher import AlarmFetcher
import aiohttp
import asyncio
from dotenv import load_dotenv
import os
import ssl


class PRTGAlarmFetcher(AlarmFetcher):

    def __init__(self, url: str, api_key: str):
        super().__init__(url, api_key)
        self.seen_alerts = set()

    async def fetchAlarms(self):

        params = {
                "content": "messages",
                "columns": "group,group_raw,device,device_raw,sensor,sensor_raw,status,status_raw",
                "apitoken": self.api_key
            }

        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False  
        ssl_context.verify_mode = ssl.CERT_NONE 

        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    async with session.get(self.url, params=params, ssl=ssl_context) as response:
                        if response.status == 200:
                            data = await response.json()
                            alerts = data.get("alerts", [])
                            for alert in alerts:
                                alert_id = alert.get("id")
                                if alert_id and alert_id not in self.seen_alerts:
                                    self.seen_alerts.add(alert_id)
                                    print(f"Nueva alerta: {alert}")
                        else:
                            print(f"Error {response.status}: {await response.text()}")
                except Exception as e:
                    print(f"Error de conexión: {e}")
                
                await asyncio.sleep(0.3)  
async def main():
    load_dotenv()
    url = os.getenv("PRTG_API_URL")
    api_key = os.getenv("PRTG_API_TOKEN")
    if not api_key:
        print("API_KEY no encontrada en .env")
        return
    fetcher = PRTGAlarmFetcher(url, api_key)
    await fetcher.fetchAlarms()

if __name__ == "__main__":
    asyncio.run(main())