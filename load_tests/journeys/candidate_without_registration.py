from __future__ import annotations

from load_tests.journeys.candidate_jobs import run_candidate_jobs


def run_candidate_without_registration(user) -> None:
    # Phase 1: Profile check (read-only, no creation)
    user.api_get("/api/candidates/profile/", name="candidates.profile.get")
    # Phase 2: Job browsing and applying
    run_candidate_jobs(user)
