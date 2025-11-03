import json
import pika
from services.monuv.client import MonuvClient
from services.integracoes.detecta_client import DetectaClient
from services.integracoes.alerta_brasil_client import AlertaBrasilClient
from services.notifications.dispatcher import NotificationDispatcher

class Consumer:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.monuv_client = MonuvClient()
        self.detecta_client = DetectaClient()
        self.alerta_brasil_client = AlertaBrasilClient()
        self.notification_dispatcher = NotificationDispatcher()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

    def callback(self, ch, method, properties, body):
        message = json.loads(body)
        self.process_message(message)

    def process_message(self, message):
        vehicle_plate = message.get("plate")
        if vehicle_plate:
            self.check_vehicle_status(vehicle_plate)

    def check_vehicle_status(self, plate):
        if self.monuv_client.is_vehicle_stolen(plate):
            self.notify_police(plate)
            self.detecta_client.report_stolen_vehicle(plate)
            self.alerta_brasil_client.report_stolen_vehicle(plate)

    def notify_police(self, plate):
        self.notification_dispatcher.notify_police(plate)

    def start_consuming(self):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
        print(f"[*] Waiting for messages in {self.queue_name}. To exit press CTRL+C")
        self.channel.start_consuming()

if __name__ == "__main__":
    consumer = Consumer(queue_name='vehicle_alerts')
    consumer.start_consuming()