from app.services.DocumentsLoader import DocumentsLoader
from prefect import flow, task, get_run_logger
from prefect.client.schemas.schedules import CronSchedule
from prefect import Flow
import traceback
import asyncio
from app.database.Qdrant import QdrantManager
from app.services.Embeddings import Embeddings

@task(retries=2, retry_delay_seconds=30)
async def load_documents(document_type: str):
    logger = get_run_logger()
    try:
        logger.info(f"Iniciando carga de documentos del folder {document_type}...")
        loader = DocumentsLoader(document_type)
        results = loader.load()
        logger.info(f"Carga de {document_type} completada")
        return results
    except Exception as e:
        logger.error(f"Error en {document_type}: {str(e)}")
        logger.error(traceback.format_exc())
        raise

@task(retries=2, retry_delay_seconds=30)
async def save_embeddings(embeddings_with_payload : list):
    
    qdrant_client = QdrantManager()
    get_run_logger().info(f"Guardando embeddings")
    qdrant_client.save_embeddings(embeddings_with_payload, "file_server_documents")
    get_run_logger().info("Embeddings guardados.")
    

@task()
async def save_files_in_database(embeddings_with_payload : str):
    pass

@flow(
    name="document_loading_flow",
    timeout_seconds=3600,
    retries=1,
    retry_delay_seconds=300
)
async def document_loading_flow():

    get_run_logger().info("Iniciando carga de documentos...")
    
    sla_docs = await load_documents("SLA")
    await save_embeddings(sla_docs)
    bd_docs = await load_documents("BD")  
    await save_embeddings(bd_docs)  
    mt_docs = await load_documents("MT")
    await save_embeddings(mt_docs)
        
    await save_embeddings(sla_docs+bd_docs+mt_docs)