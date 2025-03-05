import aiohttp
import asyncio
import os
from dotenv import load_dotenv

class AlertFetcher:

    def __init__(self, url: str, api_key: str):
        self.url = url
        self.api_key = api_key
        self.seen_alerts = set()

    async def fetch_alerts(self):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    async with session.get(self.url, headers=headers) as response:
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
    url = "https://10.249.249.3:8501/lr-alarm-api/alarms"
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("API_KEY no encontrada en .env")
        return
    fetcher = AlertFetcher(url, api_key)
    await fetcher.fetch_alerts()

if __name__ == "__main__":
    asyncio.run(main())
