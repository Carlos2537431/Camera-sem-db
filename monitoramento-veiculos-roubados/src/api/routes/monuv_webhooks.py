from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.monuv.client import MonuvClient
from src.services.notifications.police_notifier import PoliceNotifier
from src.core.config import settings

router = APIRouter()

class VehicleReport(BaseModel):
    license_plate: str
    status: str

@router.post("/webhook/monuv")
async def receive_monuv_webhook(report: VehicleReport):
    if report.status == "stolen":
        try:
            # Instancia clientes sob demanda com base nas configurações
            notifier = PoliceNotifier()
            # MonuvClient exige api_key; cria apenas se configurado (não é usado neste stub)
            api_key = getattr(settings, "MONUV_API_KEY", None)
            if api_key:
                _monuv = MonuvClient(api_key)

            # Exemplo de chamada segura (não quebra se sem config)
            _ = notifier.notify_police({
                "license_plate": report.license_plate,
                "model": "",
                "color": "",
                "location": "",
                "timestamp": ""
            })
            return {"message": "Police notify attempted."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Webhook received, no action taken."}