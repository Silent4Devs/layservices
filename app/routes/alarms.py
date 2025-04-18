from fastapi import APIRouter, UploadFile, File, HTTPException, Header, Depends
from app.database.FileServer import SMBClient
from fastapi.responses import StreamingResponse
from io import BytesIO
from typing import List
from app.database.Postgres import PostgreSQLManager
from app.models.LogrhythmAlarm import LogRhythmAlarm
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = PostgreSQLManager().get_client()
    try:
        yield db
    finally:
        db.close()

@router.get("/logrhythm/")
def get_all_alarms(db: Session = Depends(get_db)):
    alarms = db.query(LogRhythmAlarm).order_by(LogRhythmAlarm.date_inserted).all()
    return jsonable_encoder(alarms)

@router.post("/classify")
def classifyAlarm(db: Session = Depends(get_db)):

    pass
    
    