from __future__ import annotations

import random
from typing import Any, Dict, List, Optional

from faker import Faker

from load_tests.auth import maybe_upload_candidate_resume
from load_tests.config import FAKER
from load_tests.reference_data import get_cities


def fetch_profile(user) -> Optional[Dict[str, Any]]:
    res = user.api_get("/api/candidates/profile/", name="candidate.profile.get")
    if res.status_code != 200:
        return None
    data = user.api_json(res)
    return data if isinstance(data, dict) else None


def update_profile(user, *, faker: Faker = FAKER) -> None:
    payload = {"about": faker.sentence(nb_words=18)}
    user.api_patch(
        "/api/candidates/profile/", name="candidate.profile.patch", json=payload
    )


def maybe_upload_resume(user) -> None:
    maybe_upload_candidate_resume(user.client, access_token=user.access_token)


def browse_jobs(user, *, faker: Faker = FAKER) -> List[int]:
    # A small set of browse requests to mimic pagination + search/filter.
    job_ids: List[int] = []
    for i in range(2):
        params: Dict[str, Any] = {"page": i + 1}
        if random.random() < 0.5:
            params["search"] = faker.word()
        res = user.client.get("/api/jobs/", params=params, name="jobs.list")
        if res.status_code != 200:
            continue
        payload = user.api_json(res)
        items = []
        if isinstance(payload, dict) and isinstance(payload.get("results"), list):
            items = payload["results"]
        elif isinstance(payload, list):
            items = payload
        for it in items:
            if isinstance(it, dict) and isinstance(it.get("id"), int):
                job_ids.append(it["id"])
        if job_ids:
            break
    return job_ids


def open_job_details(user, job_ids: List[int]) -> None:
    for job_id in job_ids[:3]:
        user.client.get(f"/api/jobs/{job_id}/", name="jobs.detail")


def run_candidate_journey(user) -> None:
    # Auth is handled by BaseJobMarketUser.on_start.
    fetch_profile(user)
    update_profile(user)
    maybe_upload_resume(user)
    job_ids = browse_jobs(user)
    open_job_details(user, job_ids)
    # Optional actions like bookmark/apply are not implemented in this API; keep as explicit no-op.
