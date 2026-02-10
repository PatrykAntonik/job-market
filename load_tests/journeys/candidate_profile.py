from __future__ import annotations

import datetime as dt
from typing import Any, Dict, List

from load_tests.config import FAKER
from load_tests.journeys.common import optional_list, optional_post
from load_tests.reference_data import get_skills, pick_first_int_id


def _iso(d: dt.date) -> str:
    return d.isoformat()


def run_candidate_profile(user) -> None:
    # Profile (self)
    user.api_get("/api/candidates/profile/", name="candidates.profile.get")

    # Experience
    existing_experience = optional_list(
        user,
        "/api/candidates/profile/experience/",
        name="candidates.experience.list",
        params={"no_pagination": "true"},
    )
    if existing_experience is not None and len(existing_experience) < 1:
        started = FAKER.date_between(start_date="-6y", end_date="-2y")
        ended = FAKER.date_between(start_date="-2y", end_date="-30d")
        payload = {
            "company_name": f"{FAKER.company()}",
            "date_from": _iso(started),
            "date_to": _iso(ended),
            "is_current": False,
            "job_position": FAKER.job(),
            "description": FAKER.sentence(nb_words=16),
        }
        optional_post(
            user,
            "/api/candidates/profile/experience/",
            name="candidates.experience.create",
            json=payload,
        )

    # Education
    existing_education = optional_list(
        user,
        "/api/candidates/profile/education/",
        name="candidates.education.list",
        params={"no_pagination": "true"},
    )
    if existing_education is not None and len(existing_education) < 1:
        started = FAKER.date_between(start_date="-10y", end_date="-6y")
        ended = FAKER.date_between(start_date="-6y", end_date="-3y")
        payload = {
            "school_name": f"{FAKER.company()} University",
            "field_of_study": FAKER.job(),
            "degree": FAKER.random_element(
                elements=("BSc", "MSc", "Engineer", "BA", "MA", "PhD")
            ),
            "date_from": _iso(started),
            "date_to": _iso(ended),
            "is_current": False,
        }
        optional_post(
            user,
            "/api/candidates/profile/education/",
            name="candidates.education.create",
            json=payload,
        )

    # Skills
    existing_skills = optional_list(
        user,
        "/api/candidates/profile/skills/",
        name="candidates.skills.list",
        params={"no_pagination": "true"},
    )
    if existing_skills is not None and len(existing_skills) < 1:
        skills = get_skills(user.client, name=user._name("jobs.skills"))
        skill_id = pick_first_int_id(skills)
        if skill_id:
            optional_post(
                user,
                "/api/candidates/profile/skills/",
                name="candidates.skills.create",
                json={"skill": skill_id},
            )
