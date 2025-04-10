from qdrant_client import QdrantClient
from config import settings  
from .ConnectionManager import ConnectionManager
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.http.exceptions import UnexpectedResponse
from typing import List, Dict

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

    def migrate(self):

        self.client.create_collection(
            collection_name="file_server_documents",
            vectors_config=VectorParams(size=4, distance=Distance.DOT),
        )

    def reset(self):
        pass

    def save_embeddings(self, embeddings: List[Dict], collection: str):

        """
        Function to load embedding into a given collection of Qdrant
        
        """
        try:
            if not embeddings:
                raise ValueError("La lista de embeddings está vacía.")
            
            if not isinstance(collection, str) or not collection:
                raise ValueError("El nombre de la colección no es válido.")

            points = []
            for idx, embedding in enumerate(embeddings):
                vector = embedding.get('embedding')
                payload = embedding.get('payload', {})

                if not isinstance(vector, list) or not vector:
                    raise ValueError(f"Embedding inválido en posición {idx}: {vector}")
                
                points.append(PointStruct(vector=vector, payload=payload))

            operation_info = self.client.upsert(
                collection_name=collection,
                wait=True,
                points=points,
            )

            return operation_info

        except ValueError as ve:
            print(f"[VALIDATION ERROR] {ve}")
            return None

        except UnexpectedResponse as e:
            print(f"[QDRANT ERROR] Error en la respuesta del servidor Qdrant: {e}")
            return None

        except Exception as ex:
            print(f"[UNKNOWN ERROR] Error inesperado al guardar embeddings: {ex}")
            return None