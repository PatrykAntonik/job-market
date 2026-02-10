from __future__ import annotations

import json
from pathlib import Path

from django.core.management import call_command
import pytest

from JobApp.models import (
    Benefit,
    Candidate,
    City,
    Country,
    Employer,
    Industry,
    JobOffer,
    Skill,
    User,
)


@pytest.mark.django_db
def test_seed_loadtest_data_idempotent(tmp_path: Path) -> None:
    args = [
        "--seed",
        "123",
        "--total-users",
        "10",
        "--pool-buffer",
        "2",
        "--jobs-target",
        "20",
        "--output-dir",
        str(tmp_path),
        "--format",
        "json",
        "--countries",
        "2",
        "--cities",
        "5",
        "--industries",
        "3",
        "--skills",
        "5",
        "--benefits",
        "3",
    ]

    call_command("seed_loadtest_data", *args)
    snapshot = {
        "countries": Country.objects.count(),
        "cities": City.objects.count(),
        "industries": Industry.objects.count(),
        "skills": Skill.objects.count(),
        "benefits": Benefit.objects.count(),
        "users": User.objects.count(),
        "candidates": Candidate.objects.count(),
        "employers": Employer.objects.count(),
        "offers": JobOffer.objects.count(),
    }

    call_command("seed_loadtest_data", *args)
    assert snapshot == {
        "countries": Country.objects.count(),
        "cities": City.objects.count(),
        "industries": Industry.objects.count(),
        "skills": Skill.objects.count(),
        "benefits": Benefit.objects.count(),
        "users": User.objects.count(),
        "candidates": Candidate.objects.count(),
        "employers": Employer.objects.count(),
        "offers": JobOffer.objects.count(),
    }


@pytest.mark.django_db
def test_seed_loadtest_data_account_pool_output_format(tmp_path: Path) -> None:
    call_command(
        "seed_loadtest_data",
        "--seed",
        "123",
        "--c2-pool-size",
        "3",
        "--e2-pool-size",
        "2",
        "--jobs-target",
        "0",
        "--output-dir",
        str(tmp_path),
        "--format",
        "json",
        "--countries",
        "1",
        "--cities",
        "2",
        "--industries",
        "2",
        "--skills",
        "2",
        "--benefits",
        "2",
    )

    c2_path = tmp_path / "c2_accounts.json"
    e2_path = tmp_path / "e2_accounts.json"
    assert c2_path.exists()
    assert e2_path.exists()

    c2 = json.loads(c2_path.read_text(encoding="utf-8"))
    e2 = json.loads(e2_path.read_text(encoding="utf-8"))
    assert isinstance(c2, list) and len(c2) == 3
    assert isinstance(e2, list) and len(e2) == 2

    for row in c2 + e2:
        assert set(row.keys()) == {"email", "password"}
        assert isinstance(row["email"], str) and row["email"]
        assert isinstance(row["password"], str) and row["password"]
