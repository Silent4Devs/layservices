from prefect import flow, get_run_logger
from prefect.events import Event
from app.services.apis.LogRhythmProcessor import LogrhythmProcessor
from app.services.apis.PRTGProcessor import PRTGProcessor

@flow(name="Handler: Procesamiento de Alarmas de Logrhythm")
async def alert_handler_logrhythm(event: Event):
    alarm_data = event.payload

    print(f"Alarma {alarm_data['alarmId']} procesada")
    

@flow(name="Handler: Procesamiento de Alarmas de PRTG")
async def alert_handler_prtg(event: Event):
    alarm_data = event.payload

    print(f"Alarma {alarm_data['alarmId']} procesada")
    