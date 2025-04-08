from app.services.DocumentsLoader import DocumentsLoader
from prefect import flow, task, get_run_logger
from prefect.client.schemas.schedules import CronSchedule
from prefect import Flow
import traceback
import asyncio

@task(retries=2, retry_delay_seconds=30)
async def load_documents(document_type: str):
    logger = get_run_logger()
    try:
        logger.info(f"Iniciando carga de documentos del folder {document_type}...")
        loader = DocumentsLoader(document_type)
        loader.load()
        logger.info(f"Carga de {document_type} completada")
        return True
    except Exception as e:
        logger.error(f"Error en {document_type}: {str(e)}")
        logger.error(traceback.format_exc())
        raise

@flow(
    name="document_loading_flow",
    timeout_seconds=3600,
    retries=1,
    retry_delay_seconds=300
)
async def document_loading_flow():

    get_run_logger().info("Iniciando carga de documentos...")
    await asyncio.gather(
        load_documents("SLA"),
        load_documents("BD"),
        load_documents("MT")
    )
