import aiohttp
import asyncio

class AlertFetcher:
    def __init__(self, url: str):
        self.url = url
        self.seen_alerts = set()

    async def fetch_alerts(self):
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    async with session.get(self.url) as response:
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
    url = "https://10.249.249.3:8501/lr-alarm-api/alarms"
    fetcher = AlertFetcher(url)
    await fetcher.fetch_alerts()

if __name__ == "__main__":
    asyncio.run(main())
