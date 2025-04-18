from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer
from app.routes import health_databases
from app.routes import documents
from app.routes import alarms
from contextlib import asynccontextmanager
from app.services.StartUpProcess import starting
from app.services.Embeddings import Embeddings
from app.pipelines.file_server import document_loading_flow
import asyncio
import uvicorn
from app.agents.AlertClassifier import AlertClassifier

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
app.include_router(alarms.router, prefix="/alarms")

# Use this route to test code and functions
@app.get("/test")
def test_route():

    result = AlertClassifier().get_prompt_template()
    print(result)
    return {"message": "Finished"}


if __name__ == "__main__":
 
    uvicorn.run(app, host="0.0.0.0", port=8000)
