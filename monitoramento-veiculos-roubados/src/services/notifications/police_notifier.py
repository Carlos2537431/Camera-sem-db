import requests
import json
from core.config import settings

class PoliceNotifier:
    def __init__(self):
        self.api_url = settings.POLICE_API_URL
        self.api_key = settings.POLICE_API_KEY

    def notify_police(self, vehicle_info):
        payload = {
            "license_plate": vehicle_info['license_plate'],
            "model": vehicle_info['model'],
            "color": vehicle_info['color'],
            "location": vehicle_info['location'],
            "timestamp": vehicle_info['timestamp']
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            response = requests.post(self.api_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error notifying police: {e}")
            return None

# Usage example (to be called from another part of the application):
# notifier = PoliceNotifier()
# notifier.notify_police({
#     "license_plate": "ABC1234",
#     "model": "Fusca",
#     "color": "Blue",
#     "location": "Rua das Flores, 123",
#     "timestamp": "2023-10-01T12:00:00Z"
# })