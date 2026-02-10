from __future__ import annotations

from load_tests.journeys.candidate_jobs import run_candidate_jobs
from load_tests.journeys.candidate_profile import run_candidate_profile


def run_candidate_without_registration(user) -> None:
    run_candidate_profile(user)
    run_candidate_jobs(user)
