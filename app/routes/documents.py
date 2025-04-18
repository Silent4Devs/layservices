from fastapi import APIRouter, UploadFile, File, HTTPException, Header
from app.database.FileServer import SMBClient
from fastapi.responses import StreamingResponse
from io import BytesIO
from typing import List
from app.services.Docling import DocumentProcessor
import os
import tempfile

router = APIRouter()

@router.get("/file/")
def get_file(file_name: str = Header(..., convert_underscores=False)):
    file_content = SMBClient().get_file(file_name)
    if file_content is None:
        raise HTTPException(status_code=404, detail="File not found or cannot be read.")

    if file_name.lower().endswith(".docx"):
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    elif file_name.lower().endswith(".pdf"):
        media_type = "application/pdf"
    else:
        raise HTTPException(status_code=400, detail="Only .docx and .pdf files are supported.")

    return StreamingResponse(BytesIO(file_content), media_type=media_type, headers={
        "Content-Disposition": f'attachment; filename="{file_name.split("/")[-1]}"'
    })

@router.get("/files", response_model=List[str])
def get_files():
    try:
        files = SMBClient().list_files()
        if not files:
            raise HTTPException(status_code=404, detail="No files found.")
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving file list: {str(e)}")
    
@router.post("/get-markdown")
async def convert_document_to_markdown(file: UploadFile = File(...)):
    if not file.filename.endswith((".pdf", ".docx")):
        return {"error": "Only .pdf and .docx files are supported."}

    try:
        file_bytes = await file.read()
        print("Conviertiendo a bytes...")
        byte_stream = BytesIO(file_bytes)

        processor = DocumentProcessor()
        print("Procesando...")
        markdown = processor.getMarkdown(byte_stream)
        print("Finalizando...")
        return {
            "filename": file.filename,
            "markdown": markdown,
        }

    except Exception as e:
        return {"error": str(e)}