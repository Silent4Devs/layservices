from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer
from app.routes import health_databases
from app.routes import documents
import torch

app = FastAPI(
    title="SOCfusion",
    description="AI Agent for Automating Tasks and Decision-Making in SOC",
    version="0.1.0"
)

app.include_router(health_databases.router, prefix="/health")
app.include_router(documents.router, prefix="/documents")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
