from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from load_tests.config import CONFIG


def _sleep_ms(ms: int) -> None:
    time.sleep(ms / 1000.0)


def request(
    client,
    method: str,
    path: str,
    *,
    name: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    files: Optional[Dict[str, Any]] = None,
):
    attempt = 0
    last = None
    while True:
        attempt += 1
        last = client.request(
            method,
            path,
            name=name,
            headers=headers,
            params=params,
            json=json,
            data=data,
            files=files,
        )
        if CONFIG.http_retry_max <= 0:
            return last
        if last.status_code not in CONFIG.http_retry_statuses:
            return last
        if attempt > CONFIG.http_retry_max:
            return last
        _sleep_ms(CONFIG.http_retry_backoff_ms)


def safe_json(response) -> Any:
    try:
        return response.json()
    except Exception:
        return None


def format_action_name(persona_key: str, action: str) -> str:
    return f"{persona_key}: {action}"


def coerce_list_payload(payload: Any) -> List[Dict[str, Any]]:
    """
    Tolerate common DRF response shapes:
    - list of objects (no pagination)
    - {"results": [...]} (paginated)
    - {"data": [...]} (non-DRF wrapper sometimes used)
    """

    if payload is None:
        return []
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if isinstance(payload, dict):
        for key in ("results", "data", "items"):
            val = payload.get(key)
            if isinstance(val, list):
                return [x for x in val if isinstance(x, dict)]
    return []


def pick_first_int_id(items: List[Dict[str, Any]]) -> Optional[int]:
    for item in items:
        val = item.get("id")
        if isinstance(val, int):
            return val
    return None
