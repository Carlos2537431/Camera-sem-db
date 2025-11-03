from src.services.notifications.police_notifier import PoliceNotifier
from src.services.integracoes.detecta_client import DetectaClient
from src.services.integracoes.alerta_brasil_client import AlertaBrasilClient

class NotificationDispatcher:
    def __init__(self):
        self.police_notifier = PoliceNotifier()
        self.detecta_client = DetectaClient()
        self.alerta_brasil_client = AlertaBrasilClient()

    def dispatch_notification(self, vehicle_info):
        if vehicle_info['status'] == 'roubado':
            self.notify_police(vehicle_info)
            self.notify_integrations(vehicle_info)

    def notify_police(self, vehicle_info):
        self.police_notifier.notify(vehicle_info)

    def notify_integrations(self, vehicle_info):
        self.detecta_client.send_alert(vehicle_info)
        self.alerta_brasil_client.send_alert(vehicle_info)