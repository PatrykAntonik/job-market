from __future__ import annotations

from load_tests.http_utils import coerce_list_payload, pick_first_int_id
from load_tests.journeys.employer_jobs import run_employer_jobs


def run_employer_without_registration(user) -> None:
    # Phase 1: Profile + location fetch (read-only, no creation)
    user.api_get("/api/employers/profile/", name="employers.profile.get")

    loc_res = user.api_get(
        "/api/employers/profile/locations/",
        name="employers.locations.list",
        params={"no_pagination": "true"},
    )
    if loc_res.status_code == 200:
        locations = coerce_list_payload(user.api_json(loc_res))
        location_id = pick_first_int_id(locations)
    else:
        location_id = None

    # Phase 2: Job offer creation (skips offer creation if location_id is None)
    run_employer_jobs(user, location_id=location_id)
