from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from load_tests.http_utils import coerce_list_payload, request


_OPTIONAL_MISSING_STATUSES = {404, 405, 501}


def _optional_request(
    user,
    method: str,
    path: str,
    *,
    name: str,
    auth: bool = True,
    params: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
    ok_statuses: Sequence[int] = (200,),
):
    """
    Execute a request that may not exist in some environments.

    Missing endpoints (404/405/501) are treated as *success* in Locust stats.
    """

    headers: Dict[str, str] = {}
    if auth:
        headers.update(user._auth_headers())

    # Use catch_response so we can treat "missing optional endpoints" as success.
    with user.client.request(
        method,
        path,
        name=user._name(name),
        headers=headers,
        params=params,
        json=json,
        catch_response=True,
    ) as res:
        if res.status_code in _OPTIONAL_MISSING_STATUSES:
            res.success()
            return None
        if res.status_code in ok_statuses:
            res.success()
        return res


def optional_get(
    user,
    path: str,
    *,
    name: str,
    auth: bool = True,
    params: Optional[Dict[str, Any]] = None,
    ok_statuses: Sequence[int] = (200,),
):
    """
    Execute a GET that may not exist in some environments.

    Returns:
    - response when endpoint exists (any status)
    - None when endpoint is missing (404/405/501)
    """
    return _optional_request(
        user,
        "GET",
        path,
        name=name,
        auth=auth,
        params=params,
        ok_statuses=ok_statuses,
    )


def optional_list(
    user,
    path: str,
    *,
    name: str,
    auth: bool = True,
    params: Optional[Dict[str, Any]] = None,
) -> Optional[List[Dict[str, Any]]]:
    res = optional_get(user, path, name=name, auth=auth, params=params)
    if res is None:
        return None
    if res.status_code != 200:
        # Non-200 means we do not know if the list is empty or the request failed;
        # returning None prevents write-actions from being attempted based on missing data.
        return None
    return coerce_list_payload(user.api_json(res))


def optional_post(
    user,
    path: str,
    *,
    name: str,
    auth: bool = True,
    json: Optional[Dict[str, Any]] = None,
    ok_statuses: Sequence[int] = (200, 201),
):
    return _optional_request(
        user,
        "POST",
        path,
        name=name,
        auth=auth,
        json=json,
        ok_statuses=ok_statuses,
    )
