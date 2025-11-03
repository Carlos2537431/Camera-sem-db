import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = os.getenv("DEBUG", "False") == "True"
    DATABASE_URL = os.getenv("DATABASE_URL")
    FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")
    MONUV_API_KEY = os.getenv("MONUV_API_KEY")
    DETECTA_API_KEY = os.getenv("DETECTA_API_KEY")
    ALERTA_BRASIL_API_KEY = os.getenv("ALERTA_BRASIL_API_KEY")
    NOTIFICATION_CHANNEL = os.getenv("NOTIFICATION_CHANNEL", "default_channel")