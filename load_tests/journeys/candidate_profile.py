from __future__ import annotations

import datetime as dt

from load_tests.config import FAKER
from load_tests.http_utils import coerce_list_payload
from load_tests.reference_data import get_skills, random_int_id


def _iso(d: dt.date) -> str:
    return d.isoformat()


def run_candidate_profile(user) -> None:
    # Profile (self)
    user.api_get("/api/candidates/profile/", name="candidates.profile.get")

    # Experience: list then create if empty
    exp_res = user.api_get(
        "/api/candidates/profile/experience/",
        name="candidates.experience.list",
        params={"no_pagination": "true"},
    )
    if exp_res.status_code == 200:
        existing_experience = coerce_list_payload(user.api_json(exp_res))
        if len(existing_experience) < 1:
            started = FAKER.date_between(start_date="-6y", end_date="-2y")
            ended = FAKER.date_between(start_date="-2y", end_date="-30d")
            user.api_post(
                "/api/candidates/profile/experience/",
                name="candidates.experience.create",
                json={
                    "company_name": f"{FAKER.company()}",
                    "date_from": _iso(started),
                    "date_to": _iso(ended),
                    "is_current": False,
                    "job_position": FAKER.job(),
                    "description": FAKER.sentence(nb_words=16),
                },
            )

    # Education: list then create if empty
    edu_res = user.api_get(
        "/api/candidates/profile/education/",
        name="candidates.education.list",
        params={"no_pagination": "true"},
    )
    if edu_res.status_code == 200:
        existing_education = coerce_list_payload(user.api_json(edu_res))
        if len(existing_education) < 1:
            started = FAKER.date_between(start_date="-10y", end_date="-6y")
            ended = FAKER.date_between(start_date="-6y", end_date="-3y")
            user.api_post(
                "/api/candidates/profile/education/",
                name="candidates.education.create",
                json={
                    "school_name": f"{FAKER.company()} University",
                    "field_of_study": FAKER.job(),
                    "degree": FAKER.random_element(
                        elements=("BSc", "MSc", "Engineer", "BA", "MA", "PhD")
                    ),
                    "date_from": _iso(started),
                    "date_to": _iso(ended),
                    "is_current": False,
                },
            )

    # Skills: list then add one if empty
    skills_res = user.api_get(
        "/api/candidates/profile/skills/",
        name="candidates.skills.list",
        params={"no_pagination": "true"},
    )
    if skills_res.status_code == 200:
        existing_skills = coerce_list_payload(user.api_json(skills_res))
        if len(existing_skills) < 1:
            skills = get_skills(user, name=user._name("ref.skills"))
            skill_id = random_int_id(skills)
            if skill_id is not None:
                user.api_post(
                    "/api/candidates/profile/skills/",
                    name="candidates.skills.create",
                    json={"skill": skill_id},
                )
