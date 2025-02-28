<<<<<<< HEAD
from apis.logrhythm_api import LogRhythmAPI
from apis.remedy_api import RemedyAPI
from apis.prtg_api import PRTGAPI
from apis.defender_api import DefenderAPI

def main():
    logrhythm = LogRhythmAPI()
    remedy = RemedyAPI()
    prtg = PRTGAPI()
    defender = DefenderAPI()

    # Ejemplo: Obtener logs de LogRhythm y crear tickets en Remedy
    logs = logrhythm.get_logs()
    for log in logs:
        ticket_data = {
            "title": f"Alert: {log['title']}",
            "description": log['description']
        }
        remedy.create_ticket(ticket_data)

    # Obtener sensores de PRTG
    sensors = prtg.get_sensors()
    print("Sensores PRTG:", sensors)

    # Obtener alertas de Microsoft Defender
    alerts = defender.get_alerts()
    print("Alertas Defender:", alerts)

if __name__ == "__main__":
    main()
=======
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
>>>>>>> 2b4c3697a7f18893b1b6e0fc4bcb1e1690a714a0
