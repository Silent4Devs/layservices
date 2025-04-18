from qdrant_client import QdrantClient
from config import settings  
from .ConnectionManager import ConnectionManager
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.http.exceptions import UnexpectedResponse
from typing import List, Dict
import uuid

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

    def migrate(self, collection_name: str, vector_size : int):
        """
        Migrate or create a collection in Qdrant if it doesn't exist.
        
        Args:
            collection_name (str): Name of the collection to be checked or created.
            embedding_size (int): The size of the embedding vectors to be used in the collection.
            distance (str): The distance metric to be used. Default is 'Cosine'.
        """
        try:
            collections = self.client.get_collections()
            collection_names = [collection[0] for collection in collections]

            if collection_name not in collection_names:
                
                print(f"Collection '{collection_name}' not found. Creating it...")

                self.client.create_collection(
                    collection_name="file_server_documents",
                    vectors_config=VectorParams(size=vector_size, distance=Distance.DOT),
                )
                print(f"Collection '{collection_name}' created successfully.")
            else:
                print(f"Collection '{collection_name}' already exists.")

        except Exception as e:
            print(f"An error occurred during migration: {e}")

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
                vectors = embedding.get("embeddings")    
                payload = embedding.get("payload", {})
                    
                for vector in vectors:
                    if not isinstance(vector, list) or not vector:
                        raise ValueError(f"Embedding inválido en posición {idx}: {vector}")
                    
                    points.append(PointStruct(id=str(uuid.uuid4()), vector=vector, payload=payload))

            operation_info = self.client.upsert(
                collection_name=collection,
                wait=True,
                points=points,
            )

            print(f"Operation Qdrant Info: {operation_info}")
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