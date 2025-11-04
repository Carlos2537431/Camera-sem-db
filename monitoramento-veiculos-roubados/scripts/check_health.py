import os
import sys
import asyncio
import httpx
from httpx import ASGITransport

# Garante que a raiz do projeto esteja no PYTHONPATH quando executado a partir de scripts/
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.main import app

async def main():
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/health")
        print(resp.status_code, resp.json())

if __name__ == "__main__":
    asyncio.run(main())
