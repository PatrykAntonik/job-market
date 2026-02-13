from __future__ import annotations

import random
from typing import List

from load_tests.config import CONFIG
from load_tests.http_utils import coerce_list_payload
from load_tests.journeys.common import tolerant_post
from load_tests.reference_data import (
    get_contract_type_choices,
    get_industries,
    get_remoteness_choices,
    get_seniority_choices,
)


def _get_job_ids(user, *, limit: int) -> List[int]:
    ids: List[int] = []
    for page in (1, 2, 3):
        res = user.api_get(
            "/api/jobs/",
            name="jobs.list",
            params={"page": page},
        )
        if res.status_code != 200:
            break
        items = coerce_list_payload(user.api_json(res))
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
    # Reference data fetched per-user for realistic traffic
    get_contract_type_choices(user, name=user._name("jobs.contract_types"))
    get_industries(user, name=user._name("jobs.industries"))
    get_remoteness_choices(user, name=user._name("jobs.remoteness_levels"))
    get_seniority_choices(user, name=user._name("jobs.seniority"))

    target = random.randint(CONFIG.candidate_apply_min, CONFIG.candidate_apply_max)
    candidate_ids = _get_job_ids(user, limit=max(target * 3, target))
    if not candidate_ids:
        return

    applied = 0
    for job_id in candidate_ids:
        if applied >= target:
            break
        detail_res = user.api_get(
            f"/api/jobs/{job_id}/",
            name="jobs.detail",
        )
        if detail_res.status_code != 200:
            continue
        apply_res = tolerant_post(
            user,
            f"/api/jobs/{job_id}/apply/",
            name="jobs.apply",
            tolerated={400},
        )
        if apply_res.status_code == 201:
            applied += 1
        # 400 = duplicate apply, marked as success by tolerant_post, try next job
