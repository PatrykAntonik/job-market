from __future__ import annotations

from locust import task

from load_tests.config import CONFIG
from load_tests.journeys.candidate_with_registration import (
    run_candidate_with_registration,
)
from load_tests.journeys.candidate_without_registration import (
    run_candidate_without_registration,
)
from load_tests.journeys.employer_with_registration import (
    run_employer_with_registration,
)
from load_tests.journeys.employer_without_registration import (
    run_employer_without_registration,
)
from load_tests.users.base import BaseJobMarketUser


class Candidate2SeededUser(BaseJobMarketUser):
    persona_key = "c2"
    role = "candidate"
    auth_mode = "seeded"
    account_pool_path = CONFIG.c2_accounts_path
    weight = CONFIG.c2_weight

    @task
    def journey(self):
        run_candidate_without_registration(self)


class Candidate1RegisterUser(BaseJobMarketUser):
    persona_key = "c1"
    role = "candidate"
    auth_mode = "register"
    weight = CONFIG.c1_weight

    @task
    def journey(self):
        run_candidate_with_registration(self)


class Employer2SeededUser(BaseJobMarketUser):
    persona_key = "e2"
    role = "employer"
    auth_mode = "seeded"
    account_pool_path = CONFIG.e2_accounts_path
    weight = CONFIG.e2_weight

    @task
    def journey(self):
        run_employer_without_registration(self)


class Employer1RegisterUser(BaseJobMarketUser):
    persona_key = "e1"
    role = "employer"
    auth_mode = "register"
    weight = CONFIG.e1_weight

    @task
    def journey(self):
        run_employer_with_registration(self)
