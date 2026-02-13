# Load Tests (Locust)

Locust load tests simulating realistic multi-step journeys for four personas:

| Persona | Key | Auth | Description |
|---------|-----|------|-------------|
| Candidate 1 | c1 | Registration | Registers, builds profile, browses and applies to jobs |
| Candidate 2 | c2 | Seeded login | Logs in, browses and applies to jobs (no profile setup) |
| Employer 1 | e1 | Registration | Registers, sets up profile/locations, creates job offers |
| Employer 2 | e2 | Seeded login | Logs in, fetches pre-seeded locations, creates job offers |

## Prerequisites

- Docker (for containerized runs)
- Poetry (for local runs or seeding)
- Running API instance with seeded data

## 1. Seed Test Data

```bash
poetry install
poetry run python manage.py migrate
poetry run python manage.py seed_loadtest_data \
  --total-users 50 \
  --weights 80/10/8/2 \
  --pool-buffer 2 \
  --jobs-target 120 \
  --output-dir load_tests/data \
  --format json
```

Creates:
- `load_tests/data/c2_accounts.json` — Candidate account pool
- `load_tests/data/e2_accounts.json` — Employer account pool (with pre-seeded locations)
- Reference data and 120 baseline job offers

The command is idempotent — safe to rerun.

## 2. Configure Environment

```bash
cp load_tests/.env.example load_tests/.env
```

Edit `load_tests/.env`:
```bash
LOCUST_HOST=http://localhost:8000
C2_ACCOUNTS_PATH=load_tests/data/c2_accounts.json
E2_ACCOUNTS_PATH=load_tests/data/e2_accounts.json
PERSONA_WEIGHTS=80/10/8/2
LOADTEST_SEED=12345
```

## 3. Run via Docker (Recommended)

```bash
# Build
docker build -f load_tests/Dockerfile-locust -t jobmarket-locust .

# Web UI (http://localhost:8089)
docker run --rm -p 8089:8089 \
  --env-file load_tests/.env \
  -v "$PWD/load_tests/data":/app/load_tests/data:ro \
  jobmarket-locust

# Headless
docker run --rm \
  --env-file load_tests/.env \
  -v "$PWD/load_tests/data":/app/load_tests/data:ro \
  jobmarket-locust \
  --headless -u 50 -r 5 -t 10m
```

If the API runs on the host, use `--network=host` instead of `-p 8089:8089`.

## 4. Run via Poetry (Local)

```bash
poetry install --with load-testing

# Web UI
poetry run locust -f load_tests/locustfile.py

# Headless
poetry run locust -f load_tests/locustfile.py --headless -u 50 -r 5 -t 10m
```

## Metric Naming Convention

Each request is labeled `{persona}: {action}`:
- `c1: candidates.register` — C1 registration
- `c2: jobs.apply` — C2 applying to a job
- `e1: jobs.profile.create` — E1 creating a job offer
- `e2: employers.locations.list` — E2 fetching locations

Duplicate job applications (HTTP 400) are marked as success in Locust — this is expected behavior during concurrent runs.

## Configuration Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `LOCUST_HOST` | (required) | API base URL |
| `PERSONA_WEIGHTS` | `80/10/8/2` | Traffic weights (C2/C1/E2/E1) |
| `C2_ACCOUNTS_PATH` | — | Candidate account pool JSON path |
| `E2_ACCOUNTS_PATH` | — | Employer account pool JSON path |
| `LOADTEST_SEED` | — | Seed for reproducible randomness |
| `WAIT_MIN_SECONDS` / `WAIT_MAX_SECONDS` | `1.0` / `3.0` | Think time bounds (seconds) |
| `CANDIDATE_APPLY_MIN` / `CANDIDATE_APPLY_MAX` | `3` / `5` | Jobs to apply per candidate |
| `EMPLOYER_OFFERS_PER_JOURNEY` | `1` | Offers created per employer |
| `DEFAULT_CITY_ID` / `DEFAULT_INDUSTRY_ID` | — | Fallback IDs if reference data is empty |
| `HTTP_RETRY_MAX` | `1` | Retry count for transient failures |
| `HTTP_RETRY_STATUSES` | `0,429,500,502,503,504` | Statuses to retry |
| `LOADTEST_WORKER_INDEX` / `LOADTEST_WORKER_COUNT` | `0` / `1` | Multi-worker account sharding |

## Account Pool Format

```json
[
  {"email": "user@example.com", "password": "password123"}
]
```

CSV format (with `email,password` header) is also supported.

## Notes

- Token refresh is not supported; users re-login on 401/403.
- Weights are relative Locust weights; sum-to-100 recommended for percentage reasoning.
- Do not commit secrets; provide via env vars or mounted files.
