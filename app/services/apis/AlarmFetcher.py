from abc import ABC, abstractmethod

class AlarmFetcher(ABC):

    def __init__(self, url: str, api_key: str):
        self.url = url
        self.api_key = api_key

    @abstractmethod
    async def fetchAlarms(self):
        raise NotImplementedError

