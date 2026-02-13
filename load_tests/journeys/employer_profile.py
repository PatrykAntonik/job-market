from __future__ import annotations

from typing import Optional

from load_tests.http_utils import coerce_list_payload, pick_first_int_id
from load_tests.reference_data import (
    get_benefits,
    get_cities,
    random_int_id,
)


def get_or_create_location_id(user) -> Optional[int]:
    loc_res = user.api_get(
        "/api/employers/profile/locations/",
        name="employers.locations.list",
        params={"no_pagination": "true"},
    )
    if loc_res.status_code != 200:
        return None

    locations = coerce_list_payload(user.api_json(loc_res))
    existing_id = pick_first_int_id(locations)
    if existing_id:
        return existing_id

    # Create a location using a randomly discovered city.
    cities = get_cities(user, name=user._name("ref.cities"))
    city_id = random_int_id(cities)
    if city_id is None:
        return None
    create_res = user.api_post(
        "/api/employers/profile/locations/",
        name="employers.locations.create",
        json={"city": city_id},
    )
    if create_res.status_code not in (200, 201):
        return None
    created = user.api_json(create_res) or {}
    return created.get("id") if isinstance(created, dict) else None


def ensure_benefit(user) -> None:
    ben_res = user.api_get(
        "/api/employers/profile/benefits/",
        name="employers.benefits.list",
        params={"no_pagination": "true"},
    )
    if ben_res.status_code != 200:
        return
    current = coerce_list_payload(user.api_json(ben_res))
    if current:
        return

    benefits = get_benefits(user, name=user._name("ref.benefits"))
    benefit_id = random_int_id(benefits)
    if benefit_id is None:
        return
    user.api_post(
        "/api/employers/profile/benefits/",
        name="employers.benefits.create",
        json={"benefit": benefit_id},
    )


def run_employer_profile(user) -> Optional[int]:
    user.api_get("/api/employers/profile/", name="employers.profile.get")
    ensure_benefit(user)
    return get_or_create_location_id(user)
