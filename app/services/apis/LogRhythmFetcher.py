import aiohttp
import asyncio
import os
from dotenv import load_dotenv
from app.services.apis.AlarmFetcher import AlarmFetcher
from app.services.apis.LogRhythmProcessor import LogrhythmProcessor
from config import settings
from prefect import get_run_logger
from app.database.Postgres import PostgreSQLManager
from app.models.LogrhythmAlarm import LogRhythmAlarm
from sqlalchemy.sql import exists

class LoghRhythmAlarmFetcher(AlarmFetcher):

    def __init__(self, url: str, api_key: str):
        super().__init__(url, api_key)
        self.seen_alerts = set()
        self.headers = {"Authorization": f"Bearer {self.api_key}", "accept" : "application/json"}
        self.processor = LogrhythmProcessor()
        self.logger = get_run_logger()
        self.session = PostgreSQLManager().get_client()

    async def fetchAlarms(self):

        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    async with session.get(url=self.url, headers=self.headers, ssl=False) as response:
                        self.logger.info("Consultando...")

                        if response.status == 200:
                            data = await response.json()
                            data = data.get("alarmsSearchDetails", [])

                            for alarma in data:
                                alarm_id = alarma.get("alarmId")
                                if alarm_id not in self.seen_alerts:
                                    self.seen_alerts.add(alarm_id)

                                    try:
                                        detail = await self.getAlarmInformationById(alarm_id)
                                        event = await self.getAlarmEventInformationById(alarm_id)
                                        self.processor.process({'data': data, 'detail': detail, 'event' : event})
                                    except Exception as e:
                                        print(f"Error procesando alarma {alarm_id}: {e}")

                        else:
                            print(f"Error HTTP: {response.status}")

                except aiohttp.ClientError as e:
                    print(f"Error de conexión: {e}")

                except Exception as e:
                    print(f"Error inesperado: {e}")

                await asyncio.sleep(0.3) 
                   
        return response.text
    
    async def getAlarmInformationById(self, alarm_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.url + f"/{alarm_id}", headers=self.headers, ssl=False) as response:
                
                if response.status == 200:
                    
                    data = await response.json()
                    return data
                
                return
    
    async def getAlarmEventInformationById(self, alarm_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.url + f"/{alarm_id}/events", headers=self.headers, ssl=False) as response:
                
                if response.status == 200:
                    
                    data = await response.json()
                    return data
                
                return
            
    def isNewAlarm(self, alarm_id):
        """ Verifies if the alarms is already in the database"""
        try:
          
            exists_query = self.session.query(
                exists().where(LogRhythmAlarm.alarm_id == alarm_id)
            ).scalar()
            
            return not exists_query

        except Exception as e:
            self.logger.error(f"Error verificando alarma: {str(e)}")
            raise