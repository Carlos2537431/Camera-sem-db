import pytest
from src.services.integracoes.detecta_client import DetectaClient
from src.services.integracoes.alerta_brasil_client import AlertaBrasilClient
from src.services.monuv.client import MonuvClient

@pytest.fixture
def detecta_client():
    return DetectaClient()

@pytest.fixture
def alerta_brasil_client():
    return AlertaBrasilClient()

@pytest.fixture
def monuv_client():
    return MonuvClient()

def test_detecta_client_integration(detecta_client):
    response = detecta_client.check_vehicle("ABC1234")
    assert response is not None
    assert response['status'] in ['found', 'not_found']

def test_alerta_brasil_client_integration(alerta_brasil_client):
    response = alerta_brasil_client.report_vehicle("ABC1234")
    assert response is not None
    assert response['success'] is True

def test_monuv_client_integration(monuv_client):
    response = monuv_client.receive_webhook({"license_plate": "ABC1234", "status": "stolen"})
    assert response is not None
    assert response['acknowledged'] is True