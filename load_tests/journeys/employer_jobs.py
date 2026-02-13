from __future__ import annotations

import logging
import random
from typing import Any, Dict, List, Optional

from load_tests.config import CONFIG, FAKER
from load_tests.http_utils import coerce_list_payload, pick_first_int_id
from load_tests.reference_data import (
    get_contract_type_choices,
    get_remoteness_choices,
    get_seniority_choices,
    get_skills,
    random_choice_value,
    random_int_id,
)


logger = logging.getLogger(__name__)


def _pick_skill_ids(user, *, max_count: int = 3) -> List[int]:
    skills = get_skills(user, name=user._name("ref.skills"))
    ids: List[int] = []
    for item in skills:
        val = item.get("id")
        if isinstance(val, int):
            ids.append(val)
    if not ids:
        return []
    count = min(max_count, len(ids))
    return random.sample(ids, k=count)


def _create_offer(user, *, location_id: int) -> Optional[int]:
    remoteness = random_choice_value(
        get_remoteness_choices(user, name=user._name("jobs.remoteness_levels"))
    )
    seniority = random_choice_value(
        get_seniority_choices(user, name=user._name("jobs.seniority"))
    )
    contract = random_choice_value(
        get_contract_type_choices(user, name=user._name("jobs.contract_types"))
    )
    skill_ids = _pick_skill_ids(user, max_count=3)

    if not (remoteness and seniority and contract and skill_ids):
        logger.warning(
            "Skipping offer creation: missing reference data "
            "(remoteness=%s, seniority=%s, contract=%s, skills=%d)",
            remoteness,
            seniority,
            contract,
            len(skill_ids),
        )
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
    # Own offers list
    offers_res = user.api_get(
        "/api/jobs/profile/",
        name="jobs.profile.list",
        params={"page": 1},
    )
    if offers_res.status_code == 200:
        offers = coerce_list_payload(user.api_json(offers_res))
    else:
        offers = []
    existing_offer_id = pick_first_int_id(offers)

    # Create offers if location is available
    if location_id is not None:
        for _ in range(max(0, CONFIG.employer_offers_per_journey)):
            created_id = _create_offer(user, location_id=location_id)
            if created_id:
                existing_offer_id = created_id
    else:
        logger.warning(
            "Skipping offer creation: location_id is None (location fetch/create failed)"
        )

    # Applicants view
    if existing_offer_id:
        user.api_get(
            f"/api/jobs/profile/{existing_offer_id}/applicants/",
            name="jobs.profile.applicants",
            params={"page": 1},
        )
