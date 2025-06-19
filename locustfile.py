from locust import HttpUser, task, between
import random

class GatewayLoadTest(HttpUser):
    wait_time = between(0.5, 0.7)  # avg ~1.6 requests per second

    @task
    def send_data(self):
        payload = {
            # "value": random.randint(1, 100)  # simulate sensor data
            "value": random.randint(1, 100)  # simulate sensor data
        }
        self.client.post("/ingest", json=payload)