from abc import ABC, abstractmethod
from prefect import flow

class AlarmProcessor(ABC):
    @abstractmethod
    def save(self, alarm_data: dict):
        """Save the alarm on the database"""
        pass

    @abstractmethod
    def process(self, alarm_data: dict):
        """Process the alarm"""
        pass