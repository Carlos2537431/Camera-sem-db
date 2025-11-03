import requests

class DetectaClient:
    def __init__(self, api_key, base_url="https://api.detecta.com"):
        self.api_key = api_key
        self.base_url = base_url

    def report_stolen_vehicle(self, plate_number, additional_info=None):
        url = f"{self.base_url}/report"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "plate": plate_number,
            "info": additional_info
        }
        response = requests.post(url, json=data, headers=headers)
        return response.json()

    def check_vehicle_status(self, plate_number):
        url = f"{self.base_url}/status/{plate_number}"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(url, headers=headers)
        return response.json()