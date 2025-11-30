import random

from faker import Faker
from locust import HttpUser, between, task
import requests


fake = Faker()


class CandidateUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        city_list = self.client.get("/api/users/cities/?no_pagination=true").json()
        job_offer_list = self.client.get("/api/jobs/?no_pagination=true").json()
        self.city = random.choice(city_list)
        self.job_offer = random.choice(job_offer_list)

    @task
    def standard_route(self):
        self.client.get("/")
        payload = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.unique.email(),
            "password": fake.password(),
            "phone_number": fake.unique.phone_number(),
            "city": self.city["id"],
        }
        print(payload)
        self.client.post("/api/candidates/register/", json=payload)
