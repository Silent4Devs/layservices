from qdrant_client import QdrantClient
from config import settings  # Importar settings desde config.py
from .ConnectionManager import ConnectionManager

class QdrantManager(ConnectionManager):
    def __init__(self):
        """
        Open a Qdrant connection and initialize a client.
        """
        qdrant_host = settings.QDRANT_HOST
        qdrant_port = settings.QDRANT_PORT

        self.client = QdrantClient(host=qdrant_host, port=qdrant_port)

    def get_client(self):
        """
        Returns the Qdrant client.

        :return: QdrantClient instance.
        """
        return self.client

    def close_connection(self):
        """
        Close the Qdrant connection.
        """
        print("Qdrant connection closed.")