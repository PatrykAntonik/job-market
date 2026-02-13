from __future__ import annotations

import logging
import random
from typing import Any, Dict, List, Optional

from load_tests.config import CONFIG
from load_tests.http_utils import coerce_list_payload, request


logger = logging.getLogger(__name__)


def _get_cached(user, key: str, path: str, *, name: str) -> List[Dict[str, Any]]:
    """Fetch reference data with per-user caching.

    Each virtual user fetches once per journey and stores in user._ref_cache.
    """
    cache = user._ref_cache
    if key in cache:
        return cache[key]
    res = request(user.client, "GET", path, name=name)
    if res.status_code != 200:
        # Fall back to configured seeded defaults when available.
        if key == "cities" and CONFIG.default_city_id is not None:
            cache[key] = [{"id": CONFIG.default_city_id}]
            return cache[key]
        if key == "industries" and CONFIG.default_industry_id is not None:
            cache[key] = [{"id": CONFIG.default_industry_id}]
            return cache[key]
        # Do not cache transient failures (prevents "sticky" empty lists after one timeout).
        return []
    data = coerce_list_payload(res.json())
    cache[key] = data
    return data


def get_cities(user, *, name: str) -> List[Dict[str, Any]]:
    return _get_cached(
        user, "cities", "/api/users/cities/?no_pagination=true", name=name
    )


def get_countries(user, *, name: str) -> List[Dict[str, Any]]:
    return _get_cached(
        user, "countries", "/api/users/countries/?no_pagination=true", name=name
    )


def get_skills(user, *, name: str) -> List[Dict[str, Any]]:
    return _get_cached(
        user, "skills", "/api/jobs/skills/?no_pagination=true", name=name
    )


def get_industries(user, *, name: str) -> List[Dict[str, Any]]:
    return _get_cached(
        user, "industries", "/api/jobs/industries/?no_pagination=true", name=name
    )


def get_seniority_choices(user, *, name: str) -> List[Dict[str, Any]]:
    return _get_cached(
        user, "seniority", "/api/jobs/seniority/?no_pagination=true", name=name
    )


def get_contract_type_choices(user, *, name: str) -> List[Dict[str, Any]]:
    return _get_cached(
        user,
        "contract_types",
        "/api/jobs/contract-types/?no_pagination=true",
        name=name,
    )


def get_remoteness_choices(user, *, name: str) -> List[Dict[str, Any]]:
    return _get_cached(
        user,
        "remoteness_levels",
        "/api/jobs/remoteness-levels/?no_pagination=true",
        name=name,
    )


def get_benefits(user, *, name: str) -> List[Dict[str, Any]]:
    return _get_cached(
        user, "benefits", "/api/employers/benefits/?no_pagination=true", name=name
    )


def pick_choice_value(items: List[Dict[str, Any]]) -> str:
    """Pick the first valid choice value. Used in auth.py registration for determinism."""
    for item in items:
        val = item.get("value")
        if isinstance(val, str) and val:
            return val
    return ""


def pick_first_int_id(items: List[Dict[str, Any]]) -> int:
    """Pick the first valid int ID. Used in auth.py registration for determinism."""
    for item in items:
        val = item.get("id")
        if isinstance(val, int):
            return val
    return 0


def random_choice_value(items: List[Dict[str, Any]]) -> Optional[str]:
    """Pick a random 'value' string from choice-serializer items."""
    valid = [
        item["value"]
        for item in items
        if isinstance(item.get("value"), str) and item["value"]
    ]
    if not valid:
        logger.warning("random_choice_value: no valid choices available")
        return None
    return random.choice(valid)


def random_int_id(items: List[Dict[str, Any]]) -> Optional[int]:
    """Pick a random integer 'id' from items."""
    valid = [item["id"] for item in items if isinstance(item.get("id"), int)]
    if not valid:
        logger.warning("random_int_id: no valid IDs available")
        return None
    return random.choice(valid)
