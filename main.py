from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer
import torch

app = FastAPI(
    title="SOCfusion",
    description="AI Agent for Automating Tasks and Decision-Making in SOC",
    version="0.1.0"
)

model_name = "distilgpt2"  
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

text_generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0 if torch.cuda.is_available() else -1)

class QueryRequest(BaseModel):
    query: str


@app.post("/query")
async def query_agent(request: QueryRequest):
    try:
        response = text_generator(request.query, max_length=50, num_return_sequences=1)
        return {"response": response[0]["generated_text"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Ejecutar la aplicación
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)