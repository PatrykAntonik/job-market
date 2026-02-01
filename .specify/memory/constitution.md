<!--
Sync Impact Report
- Version change: N/A (template) -> 1.0.0
- Modified principles (template placeholders -> concrete principles):
  - Principle 1 -> I. Safety: No File Deletions Without Explicit Approval
  - Principle 2 -> II. Kubernetes-First Runtime (Minikube)
  - Principle 3 -> III. Django/DRF Conventions and Project Layout
  - Principle 4 -> IV. Quality Gates: Format, Lint, Tests, Migrations
  - Principle 5 -> V. Security and Configuration Hygiene
- Added sections:
  - Runtime & Deployment
  - Development Workflow & Review
- Removed sections: N/A
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md
  - ✅ .specify/templates/tasks-template.md
  - ⚠ .specify/templates/commands/*.md (directory not present in this repo; references removed/avoided)
- Runtime guidance docs:
  - ✅ GEMINI.md
  - ⚠ AGENTS.md (file is not present in repo right now; decide whether to recreate/update it)
- Follow-up TODOs:
  - TODO(SECRET_ROTATION): .env contains secrets (DJANGO_SECRET_KEY, DATABASE_URL, API keys). Ensure it
    remains untracked and rotate credentials if they were ever exposed.
  - TODO(SECRET_SANITIZE_K8S): k8s/Secret.yaml contains a DATABASE_URL. Ensure it remains untracked and
    prefer a safer secret workflow (e.g., created out-of-band) for shared environments.
-->

# Job Market API Constitution

## Core Principles

### I. Safety: No File Deletions Without Explicit Approval
- We MUST NOT delete any files without explicit confirmation from the user.
- If deletion is necessary, we MUST ask first, and that request MUST be a dedicated, standalone ask
  (do not combine it with other work).
- If a delete is approved, we MUST state exactly which paths will be deleted before doing it.
Rationale: Prevent accidental data loss and keep destructive actions deliberate and auditable.

### II. Kubernetes-First Runtime (Minikube)
- Local/runtime deployment MUST target Kubernetes first, using Minikube, based on manifests in `k8s/`.
- Docker Compose MAY be used only as a second option when Kubernetes/Minikube is not suitable.
- Kubernetes resources MUST remain deployable and consistent (namespace, ports, probes, env wiring).
Rationale: Keep the primary runtime path aligned with production-like orchestration and current repo
configuration.

### III. Django/DRF Conventions and Project Layout
- The Django project MUST remain in `JobMarket2/` (settings/urls/asgi/wsgi).
- Application code MUST live in `JobApp/` (views/serializers/permissions/migrations).
- Tests MUST live in `tests/` and mirror app modules; add new suites beside related feature dirs.
- Follow naming conventions: snake_case for modules/functions, PascalCase for classes; DRF serializer
  names MUST align with model/use-case (e.g., `JobSerializer`, `JobCreateSerializer`).
Rationale: Consistent structure reduces onboarding time and keeps changes easy to locate/review.

### IV. Quality Gates: Format, Lint, Tests, Migrations
- Code MUST target Python 3.12 and follow 4-space indentation.
- Before merging, changes MUST pass formatting and linting (`poetry run ruff format`, `make lint`).
- Behavioral changes MUST include tests (pytest) and MUST pass (`make test` in container, or pytest
  locally when appropriate).
- Any schema change MUST include committed Django migrations and MUST be applied in dev/test.
Rationale: Quality gates prevent regressions and keep codebase health predictable over time.

### V. Security and Configuration Hygiene
- Secrets MUST NOT be committed to version control (including passwords, tokens, DATABASE_URLs).
- Local config MUST be provided via `.env` (untracked) and Kubernetes secrets/configmaps at runtime.
- Changes affecting auth, CORS, JWT, or permissions MUST be documented and include tests/verification
  steps.
Rationale: Prevent credential leakage and make security-relevant changes reviewable and testable.

## Runtime & Deployment

- **Primary**: Kubernetes on Minikube using `k8s/` manifests.
  - Keep health checks aligned with the application health endpoint (`/health/`).
  - Prefer explicit namespaces (current manifests use `jobmarket`).
  - Document any required cluster prerequisites (ingress, image registry access, DB connectivity).
- **Secondary**: Docker Compose via `docker-compose.yml` (use only when Minikube is not suitable).
- **Images**: If a deployment changes runtime behavior, update the Kubernetes manifests accordingly
  (image tag, env vars, ports, probes).

## Development Workflow & Review

- **Dependencies**: Use Poetry (`poetry install`) as the authoritative dependency manager.
- **Local dev**: `poetry run python manage.py migrate` then `poetry run python manage.py runserver`.
- **Docker-based dev (secondary)**: `make build-start`, `make restart`, `make logs`.
- **Reviews**: PRs MUST describe intent, testing performed, and any contract/config changes. If new
  env vars are introduced, they MUST be documented.

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

- This Constitution supersedes other local conventions when they conflict.
- Compliance is checked in planning (feature plan “Constitution Check”) and in review (PR checklist).
- Amendments MUST:
  - describe what changed and why,
  - update dependent templates/docs as needed,
  - follow semantic versioning for the Constitution:
    - MAJOR: incompatible governance/principle changes,
    - MINOR: new principle/section or materially expanded guidance,
    - PATCH: clarifications/typos/non-semantic refinements.
- Destructive actions policy: file deletions require explicit, separate approval (see Principle I).

**Version**: 1.0.0 | **Ratified**: 2026-01-30 | **Last Amended**: 2026-01-30
