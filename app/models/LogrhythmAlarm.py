from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from .base import Base
from sqlalchemy.sql import func

class LogRhythmAlarm(Base):
    __tablename__ = 'logrhythm_alarms'

    id = Column(Integer, primary_key=True)
    alert_data_id = Column(String(36), nullable=True)
    alarm_rule_id = Column(String(36), nullable=True)
    alarm_id = Column(String(36), nullable=True)
    person_id = Column(String(36), nullable=True)
    alarm_date = Column(DateTime, nullable=True)
    alarm_status_name = Column(String(50), nullable=True)
    entity_id = Column(String(36), nullable=True)
    entity_name = Column(String(255), nullable=True)
    alarm_rule_name = Column(String(255), nullable=True)
    last_updated_id = Column(String(36), nullable=True)
    last_updated_name = Column(String(255), nullable=True)
    date_inserted = Column(DateTime, server_default=func.now(), nullable=True)
    date_updated = Column(DateTime, onupdate=func.now(), nullable=True)
    associated_cases = Column(JSON, nullable=True)
    last_person_id = Column(String(36), nullable=True)
    event_count = Column(Integer, nullable=True)
    event_date_first = Column(DateTime, nullable=True)
    event_date_last = Column(DateTime, nullable=True)
    rbp_max = Column(Float, nullable=True)
    rbp_avg = Column(Float, nullable=True)
    smart_response_actions = Column(JSON, nullable=True)
    alarm_data_cached = Column(Boolean, nullable=True)

    classification_id = Column(Integer, nullable=True)
    classification_name = Column(String(100), nullable=True)
    classification_type_name = Column(String(100), nullable=True)
    command = Column(String(500), nullable=True)
    common_event_id = Column(Integer, nullable=True)
    common_event_name = Column(String(255), nullable=True)
    impacted_entity_id = Column(Integer, nullable=True)
    impacted_entity_name = Column(String(255), nullable=True)
    impacted_host_name = Column(String(255), nullable=True)
    impacted_ip = Column(String(50), nullable=True)
    impacted_zone = Column(String(100), nullable=True)
    impacted_port = Column(Integer, nullable=True)
    log_date = Column(DateTime, nullable=True)
    log_source_host_name = Column(String(255), nullable=True)
    log_source_name = Column(String(255), nullable=True)
    log_source_type_name = Column(String(255), nullable=True)
    message_id = Column(Integer, nullable=True)
    process = Column(String(255), nullable=True)
    process_id = Column(Integer, nullable=True)
    priority = Column(Integer, nullable=True)
    severity = Column(String(50), nullable=True)
    status = Column(String(50), nullable=True)

    def __repr__(self):
        return f"<LogRhythmAlarm(id={self.id}, alarm_id='{self.alarm_id}', status='{self.alarm_status_name}')>"