import uvicorn
from fastapi import FastAPI
from src.api.routes import health, alerts, monuv_webhooks
from src.core.config import settings

app = FastAPI(title="Monitoramento de Veículos Roubados")

app.include_router(health.router)
app.include_router(alerts.router)
app.include_router(monuv_webhooks.router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)