from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import random
import re
from typing import FrozenSet, Optional, Tuple

from dotenv import load_dotenv
from faker import Faker


def _load_dotenv_if_present() -> None:
    dotenv_path_raw = os.getenv("LOADTEST_ENV_FILE")
    if dotenv_path_raw:
        dotenv_path = Path(dotenv_path_raw)
        if dotenv_path.exists():
            load_dotenv(dotenv_path=dotenv_path, override=False)
        return

    default_path = Path(__file__).resolve().parent / ".env"
    if default_path.exists():
        load_dotenv(dotenv_path=default_path, override=False)


_load_dotenv_if_present()


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    return int(raw)


def _env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    return float(raw)


def _env_str(name: str, default: str) -> str:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw


def _env_optional_str(name: str) -> Optional[str]:
    raw = os.getenv(name)
    if raw is None or raw == "":
        return None
    return raw


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None or raw == "":
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


def _env_csv_ints(name: str, default: FrozenSet[int]) -> FrozenSet[int]:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return frozenset(int(x.strip()) for x in raw.split(",") if x.strip())


def _parse_persona_weights(raw: str) -> Tuple[int, int, int, int]:
    """
    Parse weights in canonical order: C2/C1/E2/E1.

    Accepts separators: '/', ',', whitespace.
    Example: "80/10/8/2" or "80,10,8,2".
    """

    parts = [p for p in re.split(r"[/,\\s]+", raw.strip()) if p]
    if len(parts) != 4:
        raise ValueError(
            "Invalid PERSONA_WEIGHTS; expected 4 integers in order C2/C1/E2/E1 "
            '(e.g., "80/10/8/2").'
        )
    c2, c1, e2, e1 = (int(p) for p in parts)
    return c1, c2, e1, e2


@dataclass(frozen=True)
class LoadTestConfig:
    host: str

    # Personas (weights)
    c1_weight: int  # Candidate 1 (with registration)
    c2_weight: int  # Candidate 2 (seeded login)
    e1_weight: int  # Employer 1 (with registration)
    e2_weight: int  # Employer 2 (seeded login)

    # Seeded pools (used by "without registration" personas)
    c2_accounts_path: Optional[str]
    e2_accounts_path: Optional[str]
    worker_index: int
    worker_count: int

    default_city_id: Optional[int]
    default_industry_id: Optional[int]

    wait_min_seconds: float
    wait_max_seconds: float

    loadtest_seed: Optional[int]

    http_retry_max: int
    http_retry_backoff_ms: int
    http_retry_statuses: FrozenSet[int]

    candidate_resume_upload_enabled: bool
    candidate_apply_min: int
    candidate_apply_max: int
    employer_offers_per_journey: int


def _validate_config(cfg: LoadTestConfig) -> None:
    for name, value in (
        ("C1_WEIGHT", cfg.c1_weight),
        ("C2_WEIGHT", cfg.c2_weight),
        ("E1_WEIGHT", cfg.e1_weight),
        ("E2_WEIGHT", cfg.e2_weight),
    ):
        if value <= 0:
            raise ValueError(f"{name} must be a positive integer (got {value}).")

    if cfg.worker_count < 1:
        raise ValueError(
            f"LOADTEST_WORKER_COUNT must be >= 1 (got {cfg.worker_count})."
        )
    if cfg.worker_index < 0 or cfg.worker_index >= cfg.worker_count:
        raise ValueError(
            "LOADTEST_WORKER_INDEX must be in range "
            f"[0, LOADTEST_WORKER_COUNT) (got {cfg.worker_index}/{cfg.worker_count})."
        )

    if cfg.wait_min_seconds < 0 or cfg.wait_max_seconds < 0:
        raise ValueError("WAIT_MIN_SECONDS/WAIT_MAX_SECONDS must be >= 0.")
    if cfg.wait_min_seconds > cfg.wait_max_seconds:
        raise ValueError("WAIT_MIN_SECONDS must be <= WAIT_MAX_SECONDS.")

    if cfg.candidate_apply_min < 0 or cfg.candidate_apply_max < 0:
        raise ValueError("CANDIDATE_APPLY_MIN/CANDIDATE_APPLY_MAX must be >= 0.")
    if cfg.candidate_apply_min > cfg.candidate_apply_max:
        raise ValueError("CANDIDATE_APPLY_MIN must be <= CANDIDATE_APPLY_MAX.")

    if cfg.employer_offers_per_journey < 0:
        raise ValueError("EMPLOYER_OFFERS_PER_JOURNEY must be >= 0.")

    if not (cfg.host or os.getenv("LOCUST_HOST")):
        # Locust also supports --host; keep config validation focused on env inputs only.
        pass


def load_config() -> LoadTestConfig:
    seed_raw = _env_optional_str("LOADTEST_SEED")
    seed = int(seed_raw) if seed_raw is not None else None

    city_raw = _env_optional_str("DEFAULT_CITY_ID")
    default_city_id = int(city_raw) if city_raw is not None else None

    industry_raw = _env_optional_str("DEFAULT_INDUSTRY_ID")
    default_industry_id = int(industry_raw) if industry_raw is not None else None

    weights_raw = _env_optional_str("PERSONA_WEIGHTS")
    if weights_raw:
        c1_weight, c2_weight, e1_weight, e2_weight = _parse_persona_weights(weights_raw)
    else:
        c1_weight = _env_int("C1_WEIGHT", 10)
        c2_weight = _env_int("C2_WEIGHT", 80)
        e1_weight = _env_int("E1_WEIGHT", 2)
        e2_weight = _env_int("E2_WEIGHT", 8)

    cfg = LoadTestConfig(
        host=_env_str("LOCUST_HOST", ""),
        c1_weight=c1_weight,
        c2_weight=c2_weight,
        e1_weight=e1_weight,
        e2_weight=e2_weight,
        c2_accounts_path=_env_optional_str("C2_ACCOUNTS_PATH"),
        e2_accounts_path=_env_optional_str("E2_ACCOUNTS_PATH"),
        worker_index=_env_int("LOADTEST_WORKER_INDEX", 0),
        worker_count=_env_int("LOADTEST_WORKER_COUNT", 1),
        default_city_id=default_city_id,
        default_industry_id=default_industry_id,
        wait_min_seconds=_env_float("WAIT_MIN_SECONDS", 1.0),
        wait_max_seconds=_env_float("WAIT_MAX_SECONDS", 3.0),
        loadtest_seed=seed,
        http_retry_max=_env_int("HTTP_RETRY_MAX", 1),
        http_retry_backoff_ms=_env_int("HTTP_RETRY_BACKOFF_MS", 250),
        http_retry_statuses=_env_csv_ints(
            "HTTP_RETRY_STATUSES", frozenset({0, 429, 500, 502, 503, 504})
        ),
        candidate_resume_upload_enabled=_env_bool(
            "CANDIDATE_RESUME_UPLOAD_ENABLED", False
        ),
        candidate_apply_min=_env_int("CANDIDATE_APPLY_MIN", 3),
        candidate_apply_max=_env_int("CANDIDATE_APPLY_MAX", 5),
        employer_offers_per_journey=_env_int("EMPLOYER_OFFERS_PER_JOURNEY", 1),
    )
    _validate_config(cfg)
    return cfg


CONFIG = load_config()


def seed_everything() -> Faker:
    faker = Faker()
    if CONFIG.loadtest_seed is None:
        return faker
    random.seed(CONFIG.loadtest_seed)
    Faker.seed(CONFIG.loadtest_seed)
    faker.seed_instance(CONFIG.loadtest_seed)
    return faker


FAKER = seed_everything()
