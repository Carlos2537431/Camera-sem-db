from firebase_admin import credentials, firestore

class FirebaseStorage:
    def __init__(self, cred_file, db_url):
        self.cred = credentials.Certificate(cred_file)
        self.app = firebase_admin.initialize_app(self.cred, {
            'databaseURL': db_url
        })
        self.db = firestore.client()

    def add_vehicle_report(self, vehicle_data):
        reports_ref = self.db.collection('vehicle_reports')
        reports_ref.add(vehicle_data)

    def get_vehicle_reports(self):
        reports_ref = self.db.collection('vehicle_reports')
        return [doc.to_dict() for doc in reports_ref.stream()]

    def update_vehicle_report(self, report_id, updated_data):
        reports_ref = self.db.collection('vehicle_reports').document(report_id)
        reports_ref.update(updated_data)

    def delete_vehicle_report(self, report_id):
        reports_ref = self.db.collection('vehicle_reports').document(report_id)
        reports_ref.delete()