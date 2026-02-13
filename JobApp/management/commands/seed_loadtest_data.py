from __future__ import annotations

import csv
from dataclasses import dataclass
import json
import math
from pathlib import Path
import random
from typing import List, Sequence, Tuple

from django.core.management.base import BaseCommand
from faker import Faker

from JobApp.models import (
    Benefit,
    Candidate,
    City,
    Country,
    Employer,
    EmployerBenefit,
    EmployerLocation,
    Industry,
    JobOffer,
    JobOfferSkill,
    Skill,
    User,
)


@dataclass(frozen=True)
class SeedCounts:
    created: int = 0
    reused: int = 0

    def add_created(self, n: int = 1) -> "SeedCounts":
        return SeedCounts(created=self.created + n, reused=self.reused)

    def add_reused(self, n: int = 1) -> "SeedCounts":
        return SeedCounts(created=self.created, reused=self.reused + n)


def _parse_weights(raw: str) -> Tuple[int, int, int, int]:
    """
    Canonical order: C2/C1/E2/E1.
    Example: "80/10/8/2".
    """

    parts = [p for p in raw.replace(",", "/").split("/") if p.strip()]
    if len(parts) != 4:
        raise ValueError('Expected 4 weights in order C2/C1/E2/E1 (e.g., "80/10/8/2").')
    c2, c1, e2, e1 = (int(p.strip()) for p in parts)
    for v in (c2, c1, e2, e1):
        if v <= 0:
            raise ValueError("Weights must be positive integers.")
    return c2, c1, e2, e1


def _expected_users(total: int, *, weight: int, weight_sum: int) -> int:
    if total <= 0:
        return 0
    return int(math.ceil(total * (weight / weight_sum)))


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _seed_unique_by_name(model, names: Sequence[str]) -> SeedCounts:
    counts = SeedCounts()
    for name in names:
        _, created = model.objects.get_or_create(name=name)
        counts = counts.add_created() if created else counts.add_reused()
    return counts


def _seed_countries(*, count: int) -> List[Country]:
    # Use deterministic, namespaced country names so reruns are idempotent.
    names = [f"LoadTest Country {i:02d}" for i in range(1, count + 1)]
    _seed_unique_by_name(Country, names)
    return list(Country.objects.filter(name__in=names).order_by("name"))


def _seed_cities(*, countries: Sequence[Country], count: int) -> List[City]:
    cities: List[City] = []
    for i in range(1, count + 1):
        country = countries[(i - 1) % len(countries)]
        name = f"LoadTest City {i:04d}"
        province = f"LoadTest Province {(i - 1) % 10:02d}"
        zip_code = f"{(i - 1) % 100:02d}-{(i * 37) % 1000:03d}"
        city, _ = City.objects.get_or_create(
            name=name,
            province=province,
            zip_code=zip_code,
            country=country,
        )
        cities.append(city)
    return cities


def _phone(prefix: str, idx: int) -> str:
    # Keep it simple and unique; PhoneField accepts string-like values.
    return f"+{prefix}{idx:08d}"


def _get_or_create_user(
    *,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    phone_number: str,
    city: City,
) -> Tuple[User, bool]:
    existing = User.objects.filter(email=email).first()
    if existing:
        return existing, False
    user = User.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        city=city,
    )
    return user, True


def _seed_candidate_pool(
    *,
    fake: Faker,
    cities: Sequence[City],
    pool_size: int,
    password: str,
) -> Tuple[List[Tuple[str, str]], SeedCounts]:
    counts = SeedCounts()
    accounts: List[Tuple[str, str]] = []
    for i in range(pool_size):
        email = f"loadtest+c2-{i:05d}@example.com"
        user, created = _get_or_create_user(
            email=email,
            password=password,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            phone_number=_phone("1001", i),
            city=cities[i % len(cities)],
        )
        counts = counts.add_created() if created else counts.add_reused()

        Candidate.objects.get_or_create(
            user=user,
            defaults={"about": "Seeded load test candidate account."},
        )
        accounts.append((email, password))
    return accounts, counts


def _seed_employer_pool(
    *,
    fake: Faker,
    cities: Sequence[City],
    industries: Sequence[Industry],
    benefits: Sequence[Benefit],
    pool_size: int,
    password: str,
) -> Tuple[List[Tuple[str, str]], List[Employer], SeedCounts]:
    counts = SeedCounts()
    accounts: List[Tuple[str, str]] = []
    employers: List[Employer] = []

    for i in range(pool_size):
        email = f"loadtest+e2-{i:05d}@example.com"
        user, created = _get_or_create_user(
            email=email,
            password=password,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            phone_number=_phone("2001", i),
            city=cities[i % len(cities)],
        )
        counts = counts.add_created() if created else counts.add_reused()

        employer, _ = Employer.objects.get_or_create(
            user=user,
            defaults={
                "company_name": f"LoadTest Employer {i:05d}",
                "website_url": f"https://loadtest-e2-{i:05d}.example.com",
                "description": "Seeded load test employer account.",
                "industry": industries[i % len(industries)],
            },
        )
        employers.append(employer)

        # Ensure at least one location/benefit so employer journeys can create offers quickly.
        city = cities[(i * 7) % len(cities)]
        EmployerLocation.objects.get_or_create(employer=employer, city=city)
        if benefits:
            benefit = benefits[i % len(benefits)]
            EmployerBenefit.objects.get_or_create(employer=employer, benefit=benefit)

        accounts.append((email, password))
    return accounts, employers, counts


def _seed_job_offers(
    *,
    fake: Faker,
    employers: Sequence[Employer],
    skills: Sequence[Skill],
    target_count: int,
) -> SeedCounts:
    prefix = "LT Seed Offer"
    existing = JobOffer.objects.filter(position__startswith=prefix).count()
    counts = SeedCounts(reused=existing)
    if existing >= target_count:
        return counts

    if not employers:
        return counts

    for i in range(existing, target_count):
        employer = employers[i % len(employers)]
        location = (
            EmployerLocation.objects.filter(employer=employer).order_by("id").first()
        )
        if location is None:
            # Should not happen if pools were created via this command, but keep it additive-safe.
            continue

        offer = JobOffer.objects.create(
            employer=employer,
            description=fake.paragraph(nb_sentences=3),
            location=location,
            remoteness=random.choice(JobOffer.RemotenessLevel.values),
            contract=random.choice(JobOffer.ContractType.values),
            seniority=random.choice(JobOffer.Seniority.values),
            position=f"{prefix} {i:05d}",
            wage=random.randint(4000, 25000),
            currency="PLN",
        )

        # Attach a small set of skills to keep offers realistic.
        if skills:
            picked = random.sample(list(skills), k=min(3, len(skills)))
            for skill in picked:
                JobOfferSkill.objects.get_or_create(offer=offer, skill=skill)

        counts = counts.add_created()
    return counts


def _write_accounts_json(path: Path, accounts: Sequence[Tuple[str, str]]) -> None:
    path.write_text(
        json.dumps([{"email": e, "password": p} for e, p in accounts], indent=2) + "\n",
        encoding="utf-8",
    )


def _write_accounts_csv(path: Path, accounts: Sequence[Tuple[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["email", "password"])
        writer.writeheader()
        for email, password in accounts:
            writer.writerow({"email": email, "password": password})


class Command(BaseCommand):
    help = (
        "Seed additive, idempotent data for load tests (accounts + reference + offers)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--seed", type=int, default=12345, help="Random seed for stable seeding."
        )

        parser.add_argument(
            "--total-users",
            type=int,
            default=50,
            help="Expected total concurrent users for the run.",
        )
        parser.add_argument(
            "--weights",
            type=str,
            default="80/10/8/2",
            help='Persona weights in canonical order C2/C1/E2/E1 (default: "80/10/8/2").',
        )
        parser.add_argument(
            "--pool-buffer",
            type=int,
            default=2,
            help="Pool sizing buffer multiplier (default: 2).",
        )
        parser.add_argument(
            "--c2-users",
            type=int,
            default=None,
            help="Override expected C2 user count.",
        )
        parser.add_argument(
            "--e2-users",
            type=int,
            default=None,
            help="Override expected E2 user count.",
        )
        parser.add_argument(
            "--c2-pool-size",
            type=int,
            default=None,
            help="Override C2 account pool size.",
        )
        parser.add_argument(
            "--e2-pool-size",
            type=int,
            default=None,
            help="Override E2 account pool size.",
        )

        parser.add_argument(
            "--default-password",
            type=str,
            default="LoadTestPassword123!",
            help="Password to set for newly created seeded accounts (printed to pool outputs).",
        )

        parser.add_argument("--countries", type=int, default=5)
        parser.add_argument("--cities", type=int, default=25)
        parser.add_argument("--industries", type=int, default=15)
        parser.add_argument("--skills", type=int, default=40)
        parser.add_argument("--benefits", type=int, default=15)

        parser.add_argument(
            "--jobs-target",
            type=int,
            default=120,
            help="Target count of baseline seeded job offers.",
        )

        parser.add_argument(
            "--output-dir",
            type=str,
            default="load_tests/data",
            help="Directory for writing account pool files (should be untracked).",
        )
        parser.add_argument(
            "--format",
            choices=("json", "csv", "both"),
            default="json",
            help="Account pool output format.",
        )
        parser.add_argument(
            "--json-summary",
            action="store_true",
            help="Print a JSON summary (no secrets).",
        )

    def handle(self, *args, **options):
        seed: int = options["seed"]
        random.seed(seed)
        fake = Faker()
        Faker.seed(seed)
        fake.seed_instance(seed)

        total_users: int = options["total_users"]
        pool_buffer: int = options["pool_buffer"]
        if pool_buffer < 1:
            raise ValueError("--pool-buffer must be >= 1")

        c2_weight, c1_weight, e2_weight, e1_weight = _parse_weights(options["weights"])
        weight_sum = c2_weight + c1_weight + e2_weight + e1_weight

        expected_c2 = options["c2_users"]
        if expected_c2 is None:
            expected_c2 = _expected_users(
                total_users, weight=c2_weight, weight_sum=weight_sum
            )
        expected_e2 = options["e2_users"]
        if expected_e2 is None:
            expected_e2 = _expected_users(
                total_users, weight=e2_weight, weight_sum=weight_sum
            )

        c2_pool_size = options["c2_pool_size"] or max(1, expected_c2 * pool_buffer)
        e2_pool_size = options["e2_pool_size"] or max(1, expected_e2 * pool_buffer)

        self.stdout.write(
            self.style.MIGRATE_HEADING("Seeding reference data (additive)...")
        )
        countries = _seed_countries(count=options["countries"])
        cities = _seed_cities(countries=countries, count=options["cities"])
        industries_names = [
            f"LoadTest Industry {i:03d}" for i in range(1, options["industries"] + 1)
        ]
        skills_names = [
            f"LoadTest Skill {i:03d}" for i in range(1, options["skills"] + 1)
        ]
        benefits_names = [
            f"LoadTest Benefit {i:03d}" for i in range(1, options["benefits"] + 1)
        ]

        _seed_unique_by_name(Industry, industries_names)
        _seed_unique_by_name(Skill, skills_names)
        _seed_unique_by_name(Benefit, benefits_names)

        industries = list(
            Industry.objects.filter(name__in=industries_names).order_by("name")
        )
        skills = list(Skill.objects.filter(name__in=skills_names).order_by("name"))
        benefits = list(
            Benefit.objects.filter(name__in=benefits_names).order_by("name")
        )

        self.stdout.write(
            self.style.MIGRATE_HEADING("Seeding seeded-account pools (C2/E2)...")
        )
        password: str = options["default_password"]
        c2_accounts, c2_counts = _seed_candidate_pool(
            fake=fake,
            cities=cities,
            pool_size=c2_pool_size,
            password=password,
        )
        e2_accounts, e2_employers, e2_counts = _seed_employer_pool(
            fake=fake,
            cities=cities,
            industries=industries,
            benefits=benefits,
            pool_size=e2_pool_size,
            password=password,
        )

        self.stdout.write(self.style.MIGRATE_HEADING("Seeding baseline job offers..."))
        offers_counts = _seed_job_offers(
            fake=fake,
            employers=e2_employers,
            skills=skills,
            target_count=options["jobs_target"],
        )

        output_dir = Path(options["output_dir"]).resolve()
        _ensure_dir(output_dir)
        fmt = options["format"]
        if fmt in ("json", "both"):
            _write_accounts_json(output_dir / "c2_accounts.json", c2_accounts)
            _write_accounts_json(output_dir / "e2_accounts.json", e2_accounts)
        if fmt in ("csv", "both"):
            _write_accounts_csv(output_dir / "c2_accounts.csv", c2_accounts)
            _write_accounts_csv(output_dir / "e2_accounts.csv", e2_accounts)

        self.stdout.write(self.style.SUCCESS("Seeding complete."))
        self.stdout.write(
            f"Output dir: {output_dir} (files: c2_accounts.*, e2_accounts.*)"
        )
        self.stdout.write(
            f"Pools: C2={c2_pool_size} (expected users {expected_c2}, buffer {pool_buffer}x), "
            f"E2={e2_pool_size} (expected users {expected_e2}, buffer {pool_buffer}x)"
        )
        self.stdout.write(
            f"Accounts: C2 created={c2_counts.created} reused={c2_counts.reused}; "
            f"E2 created={e2_counts.created} reused={e2_counts.reused}"
        )
        self.stdout.write(
            f"Offers: created={offers_counts.created} existing={offers_counts.reused} (target {options['jobs_target']})"
        )

        if options["json_summary"]:
            self.stdout.write(
                json.dumps(
                    {
                        "output_dir": str(output_dir),
                        "c2_pool_size": c2_pool_size,
                        "e2_pool_size": e2_pool_size,
                        "c2_created": c2_counts.created,
                        "c2_reused": c2_counts.reused,
                        "e2_created": e2_counts.created,
                        "e2_reused": e2_counts.reused,
                        "offers_created": offers_counts.created,
                        "offers_existing": offers_counts.reused,
                    }
                )
            )
