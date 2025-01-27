from apis.logrhythm_api import LogRhythmAPI
from apis.remedy_api import RemedyAPI
from apis.prtg_api import PRTGAPI
from apis.defender_api import DefenderAPI

def main():
    logrhythm = LogRhythmAPI()
    remedy = RemedyAPI()
    prtg = PRTGAPI()
    defender = DefenderAPI()

    # Ejemplo: Obtener logs de LogRhythm y crear tickets en Remedy
    logs = logrhythm.get_logs()
    for log in logs:
        ticket_data = {
            "title": f"Alert: {log['title']}",
            "description": log['description']
        }
        remedy.create_ticket(ticket_data)

    # Obtener sensores de PRTG
    sensors = prtg.get_sensors()
    print("Sensores PRTG:", sensors)

    # Obtener alertas de Microsoft Defender
    alerts = defender.get_alerts()
    print("Alertas Defender:", alerts)

if __name__ == "__main__":
    main()
