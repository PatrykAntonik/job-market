from __future__ import annotations

import random
from typing import Any, Dict, List

from load_tests.config import CONFIG
from load_tests.http_utils import coerce_list_payload, request
from load_tests.reference_data import (
    get_contract_type_choices,
    get_industries,
    get_remoteness_choices,
    get_seniority_choices,
)


def _get_job_ids(user, *, limit: int) -> List[int]:
    ids: List[int] = []
    # Prefer paginated listing to avoid heavy "no_pagination" responses under load.
    for page in (1, 2, 3):
        res = request(
            user.client,
            "GET",
            "/api/jobs/",
            params={"page": page},
            name=user._name("jobs.list"),
        )
        if res.status_code != 200:
            break
        items = coerce_list_payload(res.json())
        for item in items:
            val = item.get("id")
            if isinstance(val, int):
                ids.append(val)
        if len(ids) >= limit:
            break

    if not ids:
        return []
    if len(ids) <= limit:
        return ids
    return random.sample(ids, k=limit)


def run_candidate_jobs(user) -> None:
    # Reference lists commonly used by filter UIs (fetched for realism / stable metrics).
    get_contract_type_choices(user.client, name=user._name("jobs.contract_types"))
    get_industries(user.client, name=user._name("jobs.industries"))
    get_remoteness_choices(user.client, name=user._name("jobs.remoteness_levels"))
    get_seniority_choices(user.client, name=user._name("jobs.seniority"))

    target = random.randint(CONFIG.candidate_apply_min, CONFIG.candidate_apply_max)
    # Over-fetch so we can skip duplicates/failed applies.
    candidate_ids = _get_job_ids(user, limit=max(target * 3, target))
    if not candidate_ids:
        return

    applied = 0
    for job_id in candidate_ids:
        if applied >= target:
            break
        res = request(
            user.client,
            "GET",
            f"/api/jobs/{job_id}/",
            name=user._name("jobs.detail"),
        )
        if res.status_code != 200:
            continue
        apply_res = user.api_post(
            f"/api/jobs/{job_id}/apply/",
            name="jobs.apply",
        )
        if apply_res.status_code == 201:
            applied += 1
            continue
        # 400 is common for duplicate apply; try another job id.
