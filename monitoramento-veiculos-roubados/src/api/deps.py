from fastapi import Depends
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.services.notifications.dispatcher import NotificationDispatcher
from src.services.integracoes.detecta_client import DetectaClient
from src.services.integracoes.alerta_brasil_client import AlertaBrasilClient

def get_db_session() -> Session:
    db = get_db()
    try:
        yield db
    finally:
        db.close()

def get_notification_dispatcher() -> NotificationDispatcher:
    return NotificationDispatcher()

def get_detecta_client() -> DetectaClient:
    return DetectaClient()

def get_alerta_brasil_client() -> AlertaBrasilClient:
    return AlertaBrasilClient()