from fastapi import APIRouter, HTTPException
from app.database.Postgres import PostgreSQLManager
from app.database.Redis import RedisManager
from app.database.Qdrant import QdrantManager
from sqlalchemy.sql import text
from app.database.FileServer import SMBClient


router = APIRouter()

@router.get("/postgresql", response_model=dict)
async def test_postgresql():
    """
    Test PostgreSQL connection.
    """
    postgres_manager = PostgreSQLManager()
    try:
        session = postgres_manager.get_client()
       
        result = session.execute(text("SELECT 1"))
        return {"status": "green", "message": "PostgreSQL is working :)"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PostgreSQL error: {str(e)}")
    finally:
        # Close the connection
        postgres_manager.close_connection()

@router.get("/redis", response_model=dict)
async def test_redis():
    """
    Test Redis connection.
    """
    redis_manager = RedisManager()
    try:
        client = redis_manager.get_client()
        if client.ping():
            return {"status": "green", "message": "Redis is working:)"}
        else:
            raise HTTPException(status_code=500, detail="Redis is not responding")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")
    finally:
        redis_manager.close_connection()

@router.get("/qdrant", response_model=dict)
async def test_qdrant():
    """
    Test Qdrant connection.
    """
    qdrant_manager = QdrantManager()
    try:
        client = qdrant_manager.get_client()
        collections = client.get_collections()
        return {"status": "green", "message": "Qdrant is working :)", "collections": collections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Qdrant error: {str(e)}")
    finally:
        qdrant_manager.close_connection()

@router.get("/file-server", response_model=dict)
async def test_smb():
    """
    Test SMB connection.
    """
    smb_client = SMBClient()
    try:

        files = smb_client.list_files()
        return {"status": "green", "message": "SMB connection working:)", "folders": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SMB error: {str(e)}")
    finally:
 
        smb_client.close_connection()