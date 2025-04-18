from abc import ABC, abstractmethod

class ConnectionManager(ABC):
    """
    Abstract base class (interface) for managing connections to different services.
    """

    @abstractmethod
    def get_client(self):
        """
        Returns the client to interact with the database
        """
        pass

    @abstractmethod
    def close_connection(self):
        """
        Close the connection
        """
        pass