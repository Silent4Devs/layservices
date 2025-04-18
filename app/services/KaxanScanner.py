from abc import ABC, abstractmethod
from app.services.SendRequest import RequestClient

class BaseScanner(ABC):
    """
    Abstract base class for scanning requests.
    It defines the structure for scanning hashes, ips, domains and url via kaxan.
    """

    def __init__(self, api_client: RequestClient, endpoint: str):
        self.api_client = api_client
        self.endpoint = endpoint
    
    @abstractmethod
    async def scan(self, data):
        pass

    async def _send_request(self, data):
        if not data:
            return {"error": f"{self.__class__.__name__} no puede estar vacío"}
        return await self.request_client.send_request(self.endpoint, data)


class IpScanner(BaseScanner):
    ENDPOINT = "/api/scan-ip/"
    
    def __init__(self, request_client: RequestClient):
        super().__init__(request_client, self.ENDPOINT)

    async def scan(self, data):
        return await self._send_request(data)


class DomainScanner(BaseScanner):
    ENDPOINT = "/api/scan-domain/"
    
    def __init__(self, request_client: RequestClient):
        super().__init__(request_client, self.ENDPOINT)

    async def scan(self, data):
        return await self._send_request(data)


class HashScanner(BaseScanner):
    ENDPOINT = "/api/scan-hash/"
    
    def __init__(self, request_client: RequestClient):
        super().__init__(request_client, self.ENDPOINT)

    async def scan(self, data):
        return await self._send_request(data)


class UrlScanner(BaseScanner):
    ENDPOINT = "/api/scan-url/"
    
    def __init__(self, request_client: RequestClient):
        super().__init__(request_client, self.ENDPOINT)

    async def scan(self, data):
        return await self._send_request(data)
