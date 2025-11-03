from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests

router = APIRouter()

class WebhookPayload(BaseModel):
    license_plate: str
    status: str
    timestamp: str

@router.post("/monuv/webhook")
async def handle_monuv_webhook(payload: WebhookPayload):
    if payload.status == "stolen":
        # Aqui você pode integrar com a API Detecta e Alerta Brasil
        notify_police(payload.license_plate)
        return {"message": "Notification sent to police for stolen vehicle."}
    return {"message": "No action needed."}

def notify_police(license_plate: str):
    # Lógica para notificar a polícia através da API
    police_api_url = "https://api.police.gov/notify"
    data = {"license_plate": license_plate}
    response = requests.post(police_api_url, json=data)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to notify police")