from __future__ import annotations

from load_tests.journeys.candidate_jobs import run_candidate_jobs
from load_tests.journeys.candidate_profile import run_candidate_profile


def run_candidate_with_registration(user) -> None:
    # Phase 1: Profile setup (failures don't block Phase 2)
    run_candidate_profile(user)
    # Phase 2: Job browsing and applying
    run_candidate_jobs(user)
