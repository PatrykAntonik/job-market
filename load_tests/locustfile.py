from __future__ import annotations

from config import CONFIG
from journeys.candidate import run_candidate_journey
from journeys.employer import run_employer_journey
from locust import task
from users.base import BaseJobMarketUser


class CandidateUser(BaseJobMarketUser):
    persona = "candidate"
    account_pool_path = CONFIG.candidate_accounts_path
    weight = CONFIG.candidate_weight

    @task
    def journey(self):
        run_candidate_journey(self)


class EmployerUser(BaseJobMarketUser):
    persona = "employer"
    account_pool_path = CONFIG.employer_accounts_path
    weight = CONFIG.employer_weight

    @task
    def journey(self):
        run_employer_journey(self)
