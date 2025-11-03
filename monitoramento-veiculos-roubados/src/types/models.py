from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Vehicle(BaseModel):
    license_plate: str
    make: str
    model: str
    year: int
    color: str
    status: str  # e.g., 'stolen', 'recovered', 'active'
    last_seen: Optional[datetime] = None

class Alert(BaseModel):
    vehicle: Vehicle
    alert_time: datetime
    location: str
    description: Optional[str] = None

class PoliceNotification(BaseModel):
    vehicle: Vehicle
    notification_time: datetime
    police_station_id: str
    status: str  # e.g., 'notified', 'resolved'