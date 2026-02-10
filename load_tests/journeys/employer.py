from __future__ import annotations

import random
from typing import Any, Dict, List, Optional

from faker import Faker

from load_tests.config import FAKER
from load_tests.reference_data import (
    get_cities,
    get_contract_type_choices,
    get_remoteness_choices,
    get_seniority_choices,
    get_skills,
    pick_choice_value,
)


def fetch_profile(user) -> Optional[Dict[str, Any]]:
    res = user.api_get("/api/employers/profile/", name="employer.profile.get")
    if res.status_code != 200:
        return None
    data = user.api_json(res)
    return data if isinstance(data, dict) else None


def update_profile(user, *, faker: Faker = FAKER) -> None:
    payload = {"description": faker.sentence(nb_words=18)}
    user.api_patch(
        "/api/employers/profile/", name="employer.profile.patch", json=payload
    )


def ensure_location(user) -> Optional[int]:
    res = user.api_get(
        "/api/employers/profile/locations/", name="employer.locations.list"
    )
    payload = user.api_json(res)
    locations: List[Dict[str, Any]] = []
    if isinstance(payload, dict) and isinstance(payload.get("results"), list):
        locations = payload["results"]
    elif isinstance(payload, list):
        locations = payload

    for loc in locations:
        if isinstance(loc, dict) and isinstance(loc.get("id"), int):
            return loc["id"]

    # No locations: attempt to create one using city id from profile->user->city, or fallback 1.
    profile = fetch_profile(user) or {}
    city_id = None
    if isinstance(profile.get("user"), dict):
        city_id = profile["user"].get("city")
    if not isinstance(city_id, int):
        cities = get_cities(user.client)
        city_id = cities[0]["id"] if cities else None
    if city_id is None:
        return None
    create = user.api_post(
        "/api/employers/profile/locations/",
        name="employer.locations.create",
        json={"city": city_id},
    )
    created = user.api_json(create)
    if isinstance(created, dict) and isinstance(created.get("id"), int):
        return created["id"]
    return None


def create_offer(user, *, faker: Faker = FAKER) -> Optional[int]:
    location_id = ensure_location(user)
    if not location_id:
        return None

    skills = get_skills(user.client)
    skill_ids = [
        s["id"] for s in skills if isinstance(s, dict) and isinstance(s.get("id"), int)
    ]
    if not skill_ids:
        return None
    random.shuffle(skill_ids)

    seniority = pick_choice_value(get_seniority_choices(user.client))
    contract = pick_choice_value(get_contract_type_choices(user.client))
    remoteness = pick_choice_value(get_remoteness_choices(user.client))

    payload: Dict[str, Any] = {
        "description": faker.paragraph(nb_sentences=3),
        "location": location_id,
        "remoteness": remoteness or "onsite",
        "contract": contract or "employment_contract",
        "seniority": seniority or "JUNIOR",
        "position": f"{faker.job()}",
        "wage": random.randint(5000, 25000),
        "currency": "PLN",
        "skills": skill_ids[: min(3, len(skill_ids))],
    }

    res = user.api_post(
        "/api/jobs/profile/", name="employer.offer.create", json=payload
    )
    if res.status_code not in (200, 201):
        return None
    created = user.api_json(res)
    if isinstance(created, dict) and isinstance(created.get("id"), int):
        return created["id"]
    return None


def update_offer(user, offer_id: int, *, faker: Faker = FAKER) -> None:
    payload = {"position": f"{faker.job()} (updated)"}
    user.api_patch(
        f"/api/jobs/profile/{offer_id}/", name="employer.offer.patch", json=payload
    )


def list_own_offers(user) -> None:
    user.api_get("/api/jobs/profile/", name="employer.offer.list")


def run_employer_journey(user) -> None:
    fetch_profile(user)
    update_profile(user)
    offer_id = create_offer(user)
    if offer_id:
        update_offer(user, offer_id)
    list_own_offers(user)
    # Optional actions like viewing applicants/closing offers are not implemented in this API; no-op.
