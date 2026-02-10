from __future__ import annotations

from dataclasses import dataclass
import io
from typing import Any, Dict, Optional, Tuple
import uuid

from faker import Faker

from load_tests.config import CONFIG, FAKER
from load_tests.http_utils import request
from load_tests.reference_data import get_cities, get_countries, get_industries


@dataclass(frozen=True)
class Tokens:
    access: str
    refresh: Optional[str] = None


def _parse_tokens(data: Any) -> Tokens:
    if not isinstance(data, dict):
        raise ValueError(f"Unexpected token response shape: {type(data)}")
    access = data.get("access") or data.get("token") or data.get("access_token")
    refresh = data.get("refresh") or data.get("refresh_token")
    if not access:
        raise ValueError("Token response missing access token")
    return Tokens(access=str(access), refresh=str(refresh) if refresh else None)


def login(
    client, *, email: str, password: str, request_name: str = "auth.login"
) -> Tokens:
    res = request(
        client,
        "POST",
        "/api/users/login/",
        json={"email": email, "password": password},
        name=request_name,
    )
    if res.status_code != 200:
        raise RuntimeError(f"Login failed ({res.status_code}): {res.text}")
    return _parse_tokens(res.json())


def _persona_prefix_from_request_name(request_name: str) -> Optional[str]:
    # Convention used across the suite: "{persona}: {action}"
    if ": " in request_name:
        return request_name.split(": ", 1)[0].strip() or None
    return None


def register_candidate(
    client, *, faker: Faker = FAKER, request_name: str = "candidate.register"
) -> Tuple[str, str, Tokens]:
    persona_prefix = _persona_prefix_from_request_name(request_name)
    cities_ref_name = (
        f"{persona_prefix}: ref.cities" if persona_prefix else "ref.cities"
    )
    countries_ref_name = (
        f"{persona_prefix}: ref.countries" if persona_prefix else "ref.countries"
    )

    # Discovery (often done on onboarding forms)
    get_countries(client, name=countries_ref_name)

    if CONFIG.default_city_id is not None:
        city_id = CONFIG.default_city_id
    else:
        cities = get_cities(client, name=cities_ref_name)
        city_id = cities[0]["id"] if cities else None
    if city_id is None:
        raise RuntimeError(
            "No cities available for candidate registration. Seed cities or set DEFAULT_CITY_ID."
        )

    email = f"loadtest+candidate-{uuid.uuid4().hex}@example.com"
    password = f"LoadTest-{uuid.uuid4().hex[:12]}!"

    payload: Dict[str, Any] = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": email,
        "password": password,
        "phone_number": f"{uuid.uuid4().int % 10**12:012d}",
    }
    payload["city"] = city_id

    res = request(
        client,
        "POST",
        "/api/candidates/register/",
        json=payload,
        name=request_name,
    )
    if res.status_code not in (200, 201):
        raise RuntimeError(f"Candidate register failed ({res.status_code}): {res.text}")

    tokens = _parse_tokens(res.json())
    return email, password, tokens


def register_employer(
    client, *, faker: Faker = FAKER, request_name: str = "employer.register"
) -> Tuple[str, str, Tokens]:
    persona_prefix = _persona_prefix_from_request_name(request_name)
    cities_ref_name = (
        f"{persona_prefix}: ref.cities" if persona_prefix else "ref.cities"
    )
    countries_ref_name = (
        f"{persona_prefix}: ref.countries" if persona_prefix else "ref.countries"
    )
    industries_ref_name = (
        f"{persona_prefix}: ref.industries" if persona_prefix else "ref.industries"
    )

    # Discovery (often done on onboarding forms)
    get_countries(client, name=countries_ref_name)

    if CONFIG.default_city_id is not None:
        city_id = CONFIG.default_city_id
    else:
        cities = get_cities(client, name=cities_ref_name)
        city_id = cities[0]["id"] if cities else None
    if city_id is None:
        raise RuntimeError(
            "No cities available for employer registration. Seed cities or set DEFAULT_CITY_ID."
        )

    if CONFIG.default_industry_id is not None:
        industry_id = CONFIG.default_industry_id
    else:
        industries = get_industries(client, name=industries_ref_name)
        industry_id = industries[0]["id"] if industries else None
    if industry_id is None:
        raise RuntimeError(
            "No industries available for employer registration. Seed industries or set DEFAULT_INDUSTRY_ID."
        )

    email = f"loadtest+employer-{uuid.uuid4().hex}@example.com"
    password = f"LoadTest-{uuid.uuid4().hex[:12]}!"

    payload: Dict[str, Any] = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": email,
        "password": password,
        "phone_number": f"{uuid.uuid4().int % 10**12:012d}",
        "company_name": f"{faker.company()} {uuid.uuid4().hex[:6]}",
        "description": faker.sentence(nb_words=12),
        "website_url": f"https://{uuid.uuid4().hex[:10]}.example.com",
        "city": city_id,
        "industry": industry_id,
    }

    res = request(
        client,
        "POST",
        "/api/employers/register/",
        json=payload,
        name=request_name,
    )
    if res.status_code not in (200, 201):
        raise RuntimeError(f"Employer register failed ({res.status_code}): {res.text}")

    tokens = _parse_tokens(res.json())
    return email, password, tokens


def build_dummy_pdf_bytes() -> bytes:
    # Minimal PDF header/footer; good enough for upload validation that checks extension only.
    buf = io.BytesIO()
    buf.write(b"%PDF-1.4\n")
    buf.write(b"1 0 obj<<>>endobj\n")
    buf.write(b"trailer<<>>\n%%EOF\n")
    return buf.getvalue()


def maybe_upload_candidate_resume(
    client, *, access_token: str, filename: str = "resume.pdf"
) -> bool:
    if not CONFIG.candidate_resume_upload_enabled:
        return False
    pdf_bytes = build_dummy_pdf_bytes()
    headers = {"Authorization": f"Bearer {access_token}"}
    files = {"resume": (filename, pdf_bytes, "application/pdf")}
    res = request(
        client,
        "PATCH",
        "/api/candidates/profile/",
        files=files,
        headers=headers,
        name="candidate.profile.resume_upload",
    )
    # If API doesn't accept multipart on this endpoint or rejects, treat as unsupported for now.
    return res.status_code in (200, 202)
