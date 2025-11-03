import schedule
import time
from services.monuv.client import MonuvClient
from services.integracoes.detecta_client import DetectaClient
from services.integracoes.alerta_brasil_client import AlertaBrasilClient
from services.notifications.dispatcher import NotificationDispatcher

monuv_client = MonuvClient()
detecta_client = DetectaClient()
alerta_brasil_client = AlertaBrasilClient()
notification_dispatcher = NotificationDispatcher()

def verificar_veiculos_roubados():
    veiculos_roubados = detecta_client.obter_veiculos_roubados()
    for veiculo in veiculos_roubados:
        if monuv_client.verificar_veiculo(veiculo['placa']):
            notification_dispatcher.notificar_policia(veiculo)
            notification_dispatcher.enviar_alerta(veiculo)

schedule.every(1).minutes.do(verificar_veiculos_roubados)

while True:
    schedule.run_pending()
    time.sleep(1)