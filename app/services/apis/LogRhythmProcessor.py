from app.services.apis.AlarmProcessor import AlarmProcessor
from config import settings
from app.database.Postgres import PostgreSQLManager
from app.models.LogrhythmAlarm import LogRhythmAlarm
from datetime import datetime
from app.services.KaxanScanner import IpScanner, DomainScanner
from app.services.SendRequest import RequestClient
from prefect import get_run_logger
from app.agents.AlertClassifier import AlertClassifier

class LogrhythmProcessor(AlarmProcessor):
    
    def __init__(self):
        self.session = PostgreSQLManager().get_client()
        self.client = RequestClient('https://192.168.9.123/')
        self.logger = get_run_logger()
        self.classifier = AlertClassifier()

    def save(self, alarm: dict, response : str):
        """Guarda la información del alarm en la base de datos."""

        details = alarm.get("details", {})
        event = alarm.get("event", {})
        
        log_alarm = LogRhythmAlarm(
            alarm_rule_id=details.get("alarmRuleID"),
            alarm_id=details.get("alarmId"),
            person_id=details.get("personId"),
            alarm_date=self.parse_datetime(details.get("alarmDate")),
            alarm_status=details.get("alarmStatus"),
            alarm_status_name=details.get("alarmStatusName"),
            entity_id=details.get("entityId"),
            entity_name=details.get("entityName"),
            alarm_rule_name=details.get("alarmRuleName"),
            last_updated_id=details.get("last_updated_id"),
            last_updated_name=details.get("last_updated_name"),
            last_person_id=details.get("last_person_id"),
            event_count=details.get("eventCount"),
            event_date_first=self.parse_datetime(details.get("eventDateFirst")),
            event_date_last=self.parse_datetime(details.get("eventDateLast")),
            rbp_max=details.get("rbp_max"),
            rbp_avg=details.get("rbp_avg"),
            smart_response_actions=", ".join(details.get("smart_response_actions", [])),  
            
            classification_id=event.get("classification_id"),
            classification_name=event.get("classification_name"),
            classification_type_name=event.get("classificationTypeName"),
            command=event.get("command"),
            common_event_id=event.get("commonEventId"),
            common_event_name=event.get("commonEventName"),
            impacted_entity_id=event.get("impactedEntityId"),
            impacted_entity_name=event.get("impactedEntityName"),
            impacted_host_name=event.get("impactedHost"),
            impacted_ip=event.get("impactedIp"),
            impacted_zone=event.get("impactedZone"),
            impacted_port=event.get("impactedPort"),
            log_date=self.parse_datetime(event.get("logDate")),
            log_source_host_name=event.get("logSourceHostName"),
            log_source_name=event.get("log_source_name"),
            log_source_type_name=event.get("logSourceTypeName"),
            message_id=event.get("messageId"),
            process=event.get("process"),
            process_id=event.get("processId"),
            priority=event.get("priority"),
            severity=event.get("severity"),
            status=event.get("status"),

            model_classification=response
        )

        self.session.add(log_alarm)
        self.session.commit()

    async def process(self, alarm: dict):
        """Process the information and stores it in the db"""
        try:
            
            prompt = str(alarm)
            response = self.classifier.classify(prompt)
            self.logger.info(f"Response: {response}")
            self.save(alarm, response)
            

            details = alarm.get("details", {})

            event = alarm.get("event", {})
            alarmId = details.get("alarmId", {})
            
            impacted_ip = event.get("impacted_ip", None)
            impacted_hostname = event.get("impacted_host_name", None)

            origin_ip = event.get("originHostName")
            origin_hostname = event.get("originIP")

            # domain_scanner = DomainScanner(self.client)
            # ip_scanner = IpScanner(self.client)

            # if origin_ip:
                
            #     results_origin_ip_ = await ip_scanner.scan(origin_ip)

            # if origin_hostname:
            
            #     results_origin_hostname = await domain_scanner.scan(origin_hostname)

            # if impacted_ip:

            #     results_impacted_ip = await ip_scanner.scan(impacted_ip)

            # if impacted_hostname:
                
            #     results_impacted_ip = await domain_scanner.scan(impacted_hostname)

            self.logger.info(f"Alarma {alarmId} procesada correctamente.")

            
        except Exception as e:
            self.session.rollback()
            self.logger.info(f"Error saving the alarm: {e}")

    @staticmethod
    def parse_datetime(date_str):
        """Turns a string into a datetime obj"""
        if date_str:
            try:
                return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                return None
        return None