from app.services.Embeddings import Embeddings
from fastapi import APIRouter, UploadFile, File, HTTPException, Body
from typing import List 
from pydantic import BaseModel

router = APIRouter()

class TextsPayload(BaseModel):
    texts: List[str]

@router.post("/file/embeddings/")
async def get_embeddings(payload: TextsPayload = Body(...)):
    """
    Body:
    {
      "texts": ["texto1", "texto2", ...]
    }
    Returns:
    {
      "vectors": [[...], [...], ...]
    }
    """
    try:
        model = Embeddings()
        vectors = model.generateEmbeddings(payload.texts)

        return {"vectors": vectors}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando embeddings: {e}")