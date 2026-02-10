from __future__ import annotations

from load_tests.journeys.employer_jobs import run_employer_jobs
from load_tests.journeys.employer_profile import run_employer_profile


def run_employer_without_registration(user) -> None:
    location_id = run_employer_profile(user)
    run_employer_jobs(user, location_id=location_id)
