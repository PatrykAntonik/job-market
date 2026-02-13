from __future__ import annotations

from load_tests.journeys.employer_jobs import run_employer_jobs
from load_tests.journeys.employer_profile import run_employer_profile


def run_employer_with_registration(user) -> None:
    # Phase 1: Profile setup (returns location_id or None)
    location_id = run_employer_profile(user)
    # Phase 2: Job offer creation (skips offer creation if location_id is None)
    run_employer_jobs(user, location_id=location_id)
