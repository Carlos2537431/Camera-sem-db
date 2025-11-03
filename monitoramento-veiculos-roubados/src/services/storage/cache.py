from datetime import datetime, timedelta
import json
import os

class Cache:
    def __init__(self, expiration_minutes=10):
        self.expiration_minutes = expiration_minutes
        self.cache_data = {}
        self.cache_time = {}

    def set(self, key, value):
        self.cache_data[key] = value
        self.cache_time[key] = datetime.now()

    def get(self, key):
        if key in self.cache_data:
            if self.is_expired(key):
                self.remove(key)
                return None
            return self.cache_data[key]
        return None

    def is_expired(self, key):
        if key in self.cache_time:
            return datetime.now() > self.cache_time[key] + timedelta(minutes=self.expiration_minutes)
        return True

    def remove(self, key):
        if key in self.cache_data:
            del self.cache_data[key]
            del self.cache_time[key]

    def clear(self):
        self.cache_data.clear()
        self.cache_time.clear()

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.cache_data, f)

    def load_from_file(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.cache_data = json.load(f)
                self.cache_time = {key: datetime.now() for key in self.cache_data.keys()}