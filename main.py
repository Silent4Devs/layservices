from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer
from app.routes import health_databases
from app.routes import documents
import torch
from contextlib import asynccontextmanager
from app.services.StartUpProcess import starting

@asynccontextmanager
async def lifespan(app: FastAPI):
    starting()  
    yield  
    print("Cerrando aplicación...")  

app = FastAPI(
    title="SOCfusion",
    description="AI Agent for Automating Tasks and Decision-Making in SOC",
    version="0.1.0", 
    lifespan=lifespan
)

app.include_router(health_databases.router, prefix="/health")
app.include_router(documents.router, prefix="/documents")

# Use this route to test code and functions
@app.get("/test")
def test_route():
    print("Hola mundo")
    return {"message": "Test endpoint activo"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
