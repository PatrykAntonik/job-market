# Load Tests (Locust)

This folder contains Locust load tests that simulate realistic multi-step journeys for four personas:

- Candidate 1 (with registration)
- Candidate 2 (without registration; seeded login)
- Employer 1 (with registration)
- Employer 2 (without registration; seeded login)

The suite is designed for repeatable performance comparisons by keeping the scenario mix and
randomness controlled via configuration.

## Run (Docker only)

### 1) Create `load_tests/.env`

`load_tests/config.py` auto-loads `load_tests/.env` when present.

Minimum:

```bash
LOCUST_HOST=http://127.0.0.1:8080
```

For “without registration” personas (recommended):

```bash
C2_ACCOUNTS_PATH=load_tests/data/c2_accounts.json
E2_ACCOUNTS_PATH=load_tests/data/e2_accounts.json
PERSONA_WEIGHTS=80/10/8/2
```

### 2) Build the Locust image

The image installs dependencies using the Poetry `load-testing` dependency group from the repo root,
but you do not need Poetry installed locally to run the load test.

```bash
docker build -f load_tests/Dockerfile-locust -t jobmarket-locust .
```

### 3) Run Locust (web UI)

```bash
docker run --rm -p 8089:8089 \
  --env-file load_tests/.env \
  -v "$PWD/load_tests/data":/app/load_tests/data:ro \
  jobmarket-locust
```

Then open `http://localhost:8089`.

### 4) Minikube / Docker networking “gotchas”

If your target API is in Minikube (especially `minikube start --driver=docker`) and you see:

- users spawn, but **Stats stay at 0**, or
- many request failures with **status code `0`** (timeouts / connection errors),

it usually means the Locust container cannot route to the Minikube Node IP/NodePort (e.g. `192.168.49.2:31048`).

**Recommended (Linux):** run Locust with host networking:

```bash
docker run --rm --network=host \
  --env-file load_tests/.env \
  -v "$PWD/load_tests/data":/app/load_tests/data:ro \
  jobmarket-locust
```

**Alternative (Linux):** route through the host gateway and use `host.docker.internal`:

```bash
docker run --rm -p 8089:8089 \
  --add-host=host.docker.internal:host-gateway \
  --env-file load_tests/.env \
  -v "$PWD/load_tests/data":/app/load_tests/data:ro \
  jobmarket-locust
```

Then set `LOCUST_HOST` to something reachable from your host, for example via port-forward:

```bash
kubectl -n jobmarket port-forward svc/job-market-service-lb 8080:8080
# LOCUST_HOST=http://host.docker.internal:8080
```

### 5) Headless example

```bash
docker run --rm \
  --env-file load_tests/.env \
  -v "$PWD/load_tests/data":/app/load_tests/data:ro \
  jobmarket-locust \
  --headless -u 50 -r 5 -t 10m
```

## Required Configuration (env vars)

- `LOCUST_HOST`: Base URL of the API under test (e.g., `http://localhost:8080`)

Persona weights (default mix matches `C2/C1/E2/E1=80/10/8/2`):

- `PERSONA_WEIGHTS`: Optional single value in canonical order `C2/C1/E2/E1` (e.g., `80/10/8/2`). If set, overrides the per-persona `*_WEIGHT` vars below.
- `C1_WEIGHT`: Candidate 1 (with registration)
- `C2_WEIGHT`: Candidate 2 (seeded login)
- `E1_WEIGHT`: Employer 1 (with registration)
- `E2_WEIGHT`: Employer 2 (seeded login)

Seeded account pools (for “without registration” personas):

- `C2_ACCOUNTS_PATH`: Path to JSON/CSV account pool for Candidate 2 (e.g., `load_tests/data/c2_accounts.json`)
- `E2_ACCOUNTS_PATH`: Path to JSON/CSV account pool for Employer 2 (e.g., `load_tests/data/e2_accounts.json`)

Optional:

- `LOADTEST_SEED`: Integer seed for repeatable randomness
- `WAIT_MIN_SECONDS` / `WAIT_MAX_SECONDS`: Think time bounds
- `LOADTEST_WORKER_INDEX` / `LOADTEST_WORKER_COUNT`: Deterministic sharding for seeded accounts in multi-worker runs
- `DEFAULT_CITY_ID`: City id to use during registration if city lists are empty/slow
- `DEFAULT_INDUSTRY_ID`: Industry id to use during employer registration if industry lists are empty/slow
- `HTTP_RETRY_MAX`: Retry count for selected transient statuses (default: `1`)
- `HTTP_RETRY_BACKOFF_MS`: Backoff between retries
- `HTTP_RETRY_STATUSES`: Comma-separated HTTP statuses to retry (default: `0,429,500,502,503,504`; note `0` is a request exception/timeout)
- `CANDIDATE_APPLY_MIN` / `CANDIDATE_APPLY_MAX`: How many jobs a candidate tries to apply to per journey (default: `3..5`)
- `EMPLOYER_OFFERS_PER_JOURNEY`: How many offers an employer creates per journey (default: `1`)
- `CANDIDATE_RESUME_UPLOAD_ENABLED`: If `true`, candidate registration flow may attempt a resume upload (default: `false`)

Behavior notes:

- Job browsing uses *paginated* `/api/jobs/` requests (page 1–3) to avoid expensive “fetch everything” patterns.
- Some endpoints (e.g. applicants) are treated as optional: if they return 404/405/501 they are counted as success and skipped.

## Account Pool File Format

JSON example:

```json
[
  {"email": "candidate1@example.com", "password": "password123"},
  {"email": "candidate2@example.com", "password": "password123"}
]
```

CSV example:

```csv
email,password
candidate1@example.com,password123
candidate2@example.com,password123
```

## Notes

- Do not commit secrets/passwords; provide them via env vars or mounted files.
- Token refresh is not supported by this API; users re-login on 401/403.
- Weights are **relative Locust weights**; using values that sum to `100` is recommended when you want to reason in percentages.

## Validation (quality gates)

Commands (run from repo root):

```bash
# DB config is required for pytest in this repo:
export DATABASE_URL="sqlite:////tmp/jobmarket_test.sqlite3"

poetry run black JobMarket2 JobApp --check
poetry run isort -c JobApp JobMarket2
poetry run pylint --fail-under=8.0 JobApp JobMarket2
poetry run pytest -n auto
```

Latest run (2026-02-07):

- `poetry run black JobMarket2 JobApp --check` ✅ (verified via per-file `black --check` across 52 files)
- `poetry run isort -c JobApp JobMarket2` ✅
- `poetry run pylint --fail-under=8.0 JobApp JobMarket2` ✅
- `poetry run pytest -n auto` ✅ (79 passed)

## Smoke runs (manual)

Docker (headless, 10 minutes):

```bash
docker build -f load_tests/Dockerfile-locust -t jobmarket-locust .

docker run --rm -p 8089:8089 \
  --env-file load_tests/.env \
  -v "$PWD/load_tests/data":/app/load_tests/data:ro \
  jobmarket-locust \
  --headless \
  -u 50 -r 5 -t 10m
```

## Seed Data (required for C2/E2)

“Without registration” personas (Candidate 2 / Employer 2) require pre-seeded login accounts, and
candidate apply flows are most realistic when baseline job offers exist.

This repo provides an additive, idempotent Django management command:

```bash
poetry run python manage.py seed_loadtest_data \
  --total-users 50 \
  --weights 80/10/8/2 \
  --pool-buffer 2 \
  --jobs-target 120 \
  --output-dir load_tests/data \
  --format json
```

Outputs (untracked by default):

- `load_tests/data/c2_accounts.json`
- `load_tests/data/e2_accounts.json`

Then configure Locust to use those pools, for example:

```bash
export C2_ACCOUNTS_PATH="load_tests/data/c2_accounts.json"
export E2_ACCOUNTS_PATH="load_tests/data/e2_accounts.json"
```

Notes:

- The command is **additive-only** (no deletes) and safe to rerun; reruns should mostly reuse data.
- Pool sizing defaults to `pool = expected_users_per_persona × pool_buffer`.
  - `expected_users_per_persona` is derived from `--total-users` and `--weights` (canonical `C2/C1/E2/E1`).
  - Use `--c2-pool-size/--e2-pool-size` to override exact pool sizes when needed.
