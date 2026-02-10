from __future__ import annotations

from typing import Any, Dict, List, Optional

from load_tests.http_utils import pick_first_int_id
from load_tests.journeys.common import optional_list, optional_post
from load_tests.reference_data import (
    get_benefits,
    get_cities,
    pick_first_int_id as pick_first_ref_id,
)


def get_or_create_location_id(user) -> Optional[int]:
    locations = optional_list(
        user,
        "/api/employers/profile/locations/",
        name="employers.locations.list",
        params={"no_pagination": "true"},
    )
    if locations is None:
        return None

    existing_id = pick_first_int_id(locations)
    if existing_id:
        return existing_id

    # Create a location using a discovered city.
    cities = get_cities(user.client, name=user._name("users.cities"))
    city_id = pick_first_ref_id(cities) or 0
    if not city_id:
        return None
    res = optional_post(
        user,
        "/api/employers/profile/locations/",
        name="employers.locations.create",
        json={"city": city_id},
    )
    if res is None:
        return None
    if res.status_code not in (200, 201):
        return None
    created = user.api_json(res) or {}
    return created.get("id") if isinstance(created, dict) else None


def ensure_benefit(user) -> None:
    current = optional_list(
        user,
        "/api/employers/profile/benefits/",
        name="employers.benefits.list",
        params={"no_pagination": "true"},
    )
    if current is None:
        return
    if current:
        return

    benefits = get_benefits(user.client, name=user._name("employers.benefits.ref_list"))
    benefit_id = pick_first_ref_id(benefits) or 0
    if not benefit_id:
        return
    optional_post(
        user,
        "/api/employers/profile/benefits/",
        name="employers.benefits.create",
        json={"benefit": benefit_id},
    )


def run_employer_profile(user) -> Optional[int]:
    user.api_get("/api/employers/profile/", name="employers.profile.get")
    ensure_benefit(user)
    return get_or_create_location_id(user)
