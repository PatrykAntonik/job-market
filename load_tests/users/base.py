from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

from locust import HttpUser, between

from load_tests.accounts import Account, allocate_account, load_account_pool
from load_tests.auth import Tokens, login, register_candidate, register_employer
from load_tests.config import CONFIG
from load_tests.http_utils import format_action_name, request, safe_json


@dataclass
class SessionAuth:
    email: str
    password: str
    tokens: Tokens


class BaseJobMarketUser(HttpUser):
    abstract = True

    wait_time = between(CONFIG.wait_min_seconds, CONFIG.wait_max_seconds)

    persona_key: str  # "c1" | "c2" | "e1" | "e2"
    role: Literal["candidate", "employer"]
    auth_mode: Literal["register", "seeded"]
    account_pool_path: Optional[str] = None

    _auth: Optional[SessionAuth] = None

    def on_start(self):
        self._ref_cache = {}

        # Host can be provided via LOCUST_HOST or via CLI; enforce at least one.
        if not (self.host or CONFIG.host):
            raise RuntimeError("Missing LOCUST_HOST (or --host)")
        if not self.host and CONFIG.host:
            self.host = CONFIG.host

        self._authenticate()

    def _authenticate(self) -> None:
        if self.auth_mode == "register":
            self._auth = self._register()
            return
        if self.auth_mode == "seeded":
            self._auth = self._login_seeded()
            return
        raise RuntimeError(f"Unknown auth_mode: {self.auth_mode}")

    def _name(self, action: str) -> str:
        return format_action_name(self.persona_key, action)

    def _register(self) -> SessionAuth:
        if self.role == "candidate":
            email, password, tokens = register_candidate(
                self,
                request_name=self._name("candidates.register"),
            )
        elif self.role == "employer":
            email, password, tokens = register_employer(
                self,
                request_name=self._name("employers.register"),
            )
        else:
            raise RuntimeError(f"Unknown role: {self.role}")
        return SessionAuth(email=email, password=password, tokens=tokens)

    def _login_seeded(self) -> SessionAuth:
        pool = load_account_pool(self.account_pool_path)
        account: Account = allocate_account(
            pool,
            worker_index=CONFIG.worker_index,
            worker_count=CONFIG.worker_count,
        )
        tokens = login(
            self.client,
            email=account.email,
            password=account.password,
            request_name=self._name("users.login"),
        )
        return SessionAuth(
            email=account.email, password=account.password, tokens=tokens
        )

    @property
    def access_token(self) -> str:
        if not self._auth:
            raise RuntimeError("User is not authenticated")
        return self._auth.tokens.access

    def _auth_headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}

    def api_request(self, method: str, path: str, *, name: str, **kwargs):
        headers = dict(kwargs.pop("headers", {}) or {})
        headers.update(self._auth_headers())

        res = request(
            self.client, method, path, name=self._name(name), headers=headers, **kwargs
        )
        if res.status_code in (401, 403):
            # Re-login and retry once (no refresh endpoint exists).
            if self._auth:
                self._auth = SessionAuth(
                    email=self._auth.email,
                    password=self._auth.password,
                    tokens=login(
                        self.client,
                        email=self._auth.email,
                        password=self._auth.password,
                        request_name=self._name("users.login"),
                    ),
                )
                headers = dict(kwargs.get("headers") or {})
                headers.update(self._auth_headers())
                res = request(
                    self.client,
                    method,
                    path,
                    name=self._name(name),
                    headers=headers,
                    **kwargs,
                )
        return res

    def api_get(self, path: str, *, name: str, params=None):
        return self.api_request("GET", path, name=name, params=params)

    def api_post(self, path: str, *, name: str, json=None, data=None, files=None):
        return self.api_request(
            "POST", path, name=name, json=json, data=data, files=files
        )

    def api_patch(self, path: str, *, name: str, json=None, data=None, files=None):
        return self.api_request(
            "PATCH", path, name=name, json=json, data=data, files=files
        )

    def api_json(self, response):
        return safe_json(response)
