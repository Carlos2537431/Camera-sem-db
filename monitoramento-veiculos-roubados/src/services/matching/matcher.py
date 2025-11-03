import requests

class Matcher:
    def __init__(self, plates_repository, monuv_client, police_notifier):
        self.plates_repository = plates_repository
        self.monuv_client = monuv_client
        self.police_notifier = police_notifier

    def match_plate(self, recognized_plate):
        stolen_plates = self.plates_repository.get_stolen_plates()
        for stolen_plate in stolen_plates:
            if self.is_similar(recognized_plate, stolen_plate):
                self.notify_police(recognized_plate, stolen_plate)
                self.send_alert_to_monuv(recognized_plate)
                return True
        return False

    def is_similar(self, plate1, plate2):
        return plate1 == plate2  # Implementar lógica de similaridade se necessário

    def notify_police(self, recognized_plate, stolen_plate):
        self.police_notifier.notify(recognized_plate, stolen_plate)

    def send_alert_to_monuv(self, recognized_plate):
        self.monuv_client.send_alert(recognized_plate)