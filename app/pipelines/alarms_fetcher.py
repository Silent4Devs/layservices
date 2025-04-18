from prefect import flow, task, get_run_logger
from app.services.apis.LogRhythmFetcher import LoghRhythmAlarmFetcher
from app.services.apis.PRTGFetcher import PRTGAlarmFetcher
from config import settings

@task
async def fetch_alarms_logrhythm(url: str, api_key: str):
    
    fetcher = LoghRhythmAlarmFetcher(url, api_key)
    await fetcher.fetchAlarms()

@flow
async def alarm_monitoring_logrythm():
    """Prefect Flow to fetch alarms in real time from Logrhythm."""

    logger = get_run_logger()
    logger.info("Escuchando alarmas de logrhythm")

    url = settings.LOGRHYTHM_API_URL + "lr-alarm-api/alarms"
    api_key = settings.LOGRHYTHM_API_TOKEN

    if not api_key:

        print("There is no api key in your .env")

    await fetch_alarms_logrhythm(url, api_key)

@task 
async def fetch_alarms_prtg(url : str, api_key : str):
    
    fetcher = PRTGAlarmFetcher(url, api_key)
    await fetcher.fetchAlarms()

@flow
async def alarm_monitoring_prtg():
    """Prefect Flow to fetch alarms in real time from PRTG."""

    logger = get_run_logger()
    logger.info("Escuchando alarmas de prtg...")

    url = settings.PRTG_API_URL
    api_key =   settings.PRTG_API_TOKEN
    if not api_key:
        print("API_KEY no encontrada en .env")
        return
    await fetch_alarms_prtg(url, api_key)