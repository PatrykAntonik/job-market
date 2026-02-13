from __future__ import annotations

import csv
from dataclasses import dataclass
import json
from pathlib import Path
from threading import Lock
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class Account:
    email: str
    password: str


_CACHE: Dict[str, Tuple[Account, ...]] = {}
_ALLOC_LOCK = Lock()
_ALLOC_COUNTERS: Dict[int, int] = {}


def load_account_pool(path: Optional[str]) -> Tuple[Account, ...]:
    if not path:
        return tuple()
    if path in _CACHE:
        return _CACHE[path]

    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Account pool file not found: {path}")

    if p.suffix.lower() == ".json":
        data = json.loads(p.read_text(encoding="utf-8"))
        accounts = tuple(
            Account(email=x["email"], password=x["password"]) for x in data
        )
        _CACHE[path] = accounts
        return accounts

    if p.suffix.lower() in {".csv", ".txt"}:
        rows: List[Account] = []
        with p.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                email = (row.get("email") or "").strip()
                password = (row.get("password") or "").strip()
                if email and password:
                    rows.append(Account(email=email, password=password))
        accounts = tuple(rows)
        _CACHE[path] = accounts
        return accounts

    raise ValueError(f"Unsupported account pool format for {path}. Use .json or .csv")


def allocate_account(
    pool: Tuple[Account, ...], *, worker_index: int = 0, worker_count: int = 1
) -> Account:
    """
    Deterministically allocate a unique account for the life of a simulated user.

    This is intentionally *not* random to reduce collisions and improve run repeatability.
    For distributed runs, set LOADTEST_WORKER_INDEX/LOADTEST_WORKER_COUNT so workers pick
    disjoint indices.
    """

    if worker_count < 1:
        raise ValueError("worker_count must be >= 1")
    if worker_index < 0 or worker_index >= worker_count:
        raise ValueError("worker_index must be in range [0, worker_count)")
    if not pool:
        raise RuntimeError("Account pool is empty")

    with _ALLOC_LOCK:
        pool_key = id(pool)
        local_index = _ALLOC_COUNTERS.get(pool_key, 0)
        _ALLOC_COUNTERS[pool_key] = local_index + 1

    pool_index = local_index * worker_count + worker_index
    if pool_index >= len(pool):
        raise RuntimeError(
            f"Account pool exhausted (need index {pool_index}, pool size {len(pool)}). "
            "Seed more accounts or reduce users/weights."
        )

    return pool[pool_index]
