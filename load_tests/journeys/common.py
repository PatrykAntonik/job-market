from __future__ import annotations

from typing import Any, Dict, Optional, Set


def tolerant_post(
    user,
    path: str,
    *,
    name: str,
    json: Optional[Dict[str, Any]] = None,
    tolerated: Optional[Set[int]] = None,
):
    """
    POST with catch_response handling for expected non-2xx statuses.

    Tolerated statuses (e.g., {400} for duplicate apply) are marked as
    Locust successes. 2xx responses are auto-success. All other non-2xx
    responses are reported as Locust failures.
    """
    if tolerated is None:
        tolerated = set()

    with user.client.request(
        "POST",
        path,
        name=user._name(name),
        headers=user._auth_headers(),
        json=json,
        catch_response=True,
    ) as res:
        if res.status_code in tolerated:
            res.success()
        return res
