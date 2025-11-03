from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.notifications.police_notifier import PoliceNotifier

router = APIRouter()

class Alert(BaseModel):
    license_plate: str
    description: str

@router.post("/alerts/")
async def create_alert(alert: Alert):
    try:
        notifier = PoliceNotifier()
        await notifier.notify_police(alert.license_plate, alert.description)
        return {"message": "Alert sent to police successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/alerts/{license_plate}")
async def get_alert(license_plate: str):
    # Placeholder for retrieving alert information
    return {"message": f"Alert information for {license_plate}."}