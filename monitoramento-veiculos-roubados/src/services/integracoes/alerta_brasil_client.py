import requests

class AlertaBrasilClient:
    def __init__(self, api_key, base_url="https://api.alertabrasil.com"):
        self.api_key = api_key
        self.base_url = base_url

    def report_vehicle_stolen(self, license_plate, description):
        url = f"{self.base_url}/report"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "license_plate": license_plate,
            "description": description
        }
        response = requests.post(url, json=data, headers=headers)
        return response.json()

    def check_vehicle_status(self, license_plate):
        url = f"{self.base_url}/status/{license_plate}"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(url, headers=headers)
        return response.json()