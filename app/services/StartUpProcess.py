from app.database.Qdrant import QdrantManager


def starting():

    qdrant = QdrantManager()
    qdrant.migrate('file_server_documents', 1024)