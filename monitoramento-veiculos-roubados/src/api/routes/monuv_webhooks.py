from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.monuv.client import MonuvClient
from services.notifications.police_notifier import PoliceNotifier

router = APIRouter()
monuv_client = MonuvClient()
police_notifier = PoliceNotifier()

class VehicleReport(BaseModel):
    license_plate: str
    status: str

@router.post("/webhook/monuv")
async def receive_monuv_webhook(report: VehicleReport):
    if report.status == "stolen":
        try:
            # Notify the police about the stolen vehicle
            police_notifier.notify(report.license_plate)
            return {"message": "Police notified about the stolen vehicle."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Webhook received, no action taken."}