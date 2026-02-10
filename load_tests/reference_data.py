from __future__ import annotations

from typing import Any, Dict, List

from load_tests.config import CONFIG
from load_tests.http_utils import coerce_list_payload, request


_CACHE: Dict[str, List[Dict[str, Any]]] = {}


def _get_cached(client, key: str, path: str, *, name: str) -> List[Dict[str, Any]]:
    if key in _CACHE:
        return _CACHE[key]
    res = request(client, "GET", path, name=name)
    if res.status_code != 200:
        # Fall back to configured seeded defaults when available.
        if key == "cities" and CONFIG.default_city_id is not None:
            _CACHE[key] = [{"id": CONFIG.default_city_id}]
            return _CACHE[key]
        if key == "industries" and CONFIG.default_industry_id is not None:
            _CACHE[key] = [{"id": CONFIG.default_industry_id}]
            return _CACHE[key]
        # Do not cache transient failures (prevents "sticky" empty lists after one timeout).
        return []
    data = coerce_list_payload(res.json())
    _CACHE[key] = data
    return data


def get_cities(client, *, name: str) -> List[Dict[str, Any]]:
    return _get_cached(
        client, "cities", "/api/users/cities/?no_pagination=true", name=name
    )


def get_countries(client, *, name: str) -> List[Dict[str, Any]]:
    return _get_cached(
        client, "countries", "/api/users/countries/?no_pagination=true", name=name
    )


def get_skills(client, *, name: str) -> List[Dict[str, Any]]:
    return _get_cached(
        client, "skills", "/api/jobs/skills/?no_pagination=true", name=name
    )


def get_industries(client, *, name: str) -> List[Dict[str, Any]]:
    return _get_cached(
        client, "industries", "/api/jobs/industries/?no_pagination=true", name=name
    )


def get_seniority_choices(client, *, name: str) -> List[Dict[str, Any]]:
    return _get_cached(
        client, "seniority", "/api/jobs/seniority/?no_pagination=true", name=name
    )


def get_contract_type_choices(client, *, name: str) -> List[Dict[str, Any]]:
    return _get_cached(
        client,
        "contract_types",
        "/api/jobs/contract-types/?no_pagination=true",
        name=name,
    )


def get_remoteness_choices(client, *, name: str) -> List[Dict[str, Any]]:
    return _get_cached(
        client,
        "remoteness_levels",
        "/api/jobs/remoteness-levels/?no_pagination=true",
        name=name,
    )


def get_benefits(client, *, name: str) -> List[Dict[str, Any]]:
    return _get_cached(
        client, "benefits", "/api/employers/benefits/?no_pagination=true", name=name
    )


def pick_choice_value(items: List[Dict[str, Any]]) -> str:
    # Items are ChoiceSerializer output: {"value": "...", "display": "..."}
    for item in items:
        val = item.get("value")
        if isinstance(val, str) and val:
            return val
    return ""


def pick_first_int_id(items: List[Dict[str, Any]]) -> int:
    for item in items:
        val = item.get("id")
        if isinstance(val, int):
            return val
    return 0
