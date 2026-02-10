from __future__ import annotations

import random
from typing import Any, Dict, List, Optional

from load_tests.config import CONFIG, FAKER
from load_tests.http_utils import coerce_list_payload
from load_tests.journeys.common import optional_get
from load_tests.reference_data import (
    get_contract_type_choices,
    get_remoteness_choices,
    get_seniority_choices,
    get_skills,
    pick_choice_value,
    pick_first_int_id,
)


def _pick_skill_ids(user, *, max_count: int = 3) -> List[int]:
    skills = get_skills(user.client, name=user._name("jobs.skills"))
    ids: List[int] = []
    for item in skills:
        val = item.get("id")
        if isinstance(val, int):
            ids.append(val)
    if not ids:
        return []
    count = min(max_count, len(ids))
    if count <= 0:
        return []
    return random.sample(ids, k=count)


def _create_offer(user, *, location_id: int) -> Optional[int]:
    remoteness = pick_choice_value(
        get_remoteness_choices(user.client, name=user._name("jobs.remoteness_levels"))
    )
    seniority = pick_choice_value(
        get_seniority_choices(user.client, name=user._name("jobs.seniority"))
    )
    contract = pick_choice_value(
        get_contract_type_choices(user.client, name=user._name("jobs.contract_types"))
    )
    skill_ids = _pick_skill_ids(user, max_count=3)

    if not (remoteness and seniority and contract and skill_ids):
        return None

    payload: Dict[str, Any] = {
        "description": FAKER.paragraph(nb_sentences=3),
        "location": location_id,
        "remoteness": remoteness,
        "contract": contract,
        "seniority": seniority,
        "position": f"{FAKER.job()} ({FAKER.word().title()})",
        "wage": random.randint(4000, 25000),
        "currency": "PLN",
        "skills": skill_ids,
    }
    res = user.api_post("/api/jobs/profile/", name="jobs.profile.create", json=payload)
    if res.status_code not in (200, 201):
        return None
    created = user.api_json(res)
    if not isinstance(created, dict):
        return None
    offer_id = created.get("id")
    return offer_id if isinstance(offer_id, int) else None


def run_employer_jobs(user, *, location_id: Optional[int]) -> None:
    # Own offers list (profile)
    offers_res = optional_get(
        user,
        "/api/jobs/profile/",
        name="jobs.profile.list",
        params={"page": 1},
    )
    if offers_res is None:
        offers = []
    else:
        offers = (
            coerce_list_payload(user.api_json(offers_res))
            if offers_res.status_code == 200
            else []
        )
    existing_offer_id = pick_first_int_id(offers) or None

    # Create offers if possible
    if location_id:
        for _ in range(max(0, CONFIG.employer_offers_per_journey)):
            created_id = _create_offer(user, location_id=location_id)
            if created_id:
                existing_offer_id = created_id

    # Applicants view (still valid even if empty)
    if existing_offer_id:
        optional_get(
            user,
            f"/api/jobs/profile/{existing_offer_id}/applicants/",
            name="jobs.profile.applicants",
            params={"page": 1},
        )
