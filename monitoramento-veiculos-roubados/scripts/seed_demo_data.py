import os
import json
from src.services.storage.firebase import FirebaseStorage

def seed_demo_data():
    firebase_storage = FirebaseStorage()

    demo_data = {
        "vehicles": [
            {
                "license_plate": "ABC1D23",
                "status": "stolen",
                "reported_at": "2023-10-01T12:00:00Z",
                "owner": {
                    "name": "John Doe",
                    "contact": "john.doe@example.com"
                }
            },
            {
                "license_plate": "XYZ4W56",
                "status": "stolen",
                "reported_at": "2023-10-02T14:30:00Z",
                "owner": {
                    "name": "Jane Smith",
                    "contact": "jane.smith@example.com"
                }
            }
        ]
    }

    # Save demo data to Firebase
    for vehicle in demo_data["vehicles"]:
        firebase_storage.save_vehicle_data(vehicle)

    print("Demo data seeded successfully.")

if __name__ == "__main__":
    seed_demo_data()