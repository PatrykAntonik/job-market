# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the repo's Specify scripts (see `.specify/scripts/`).

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]
**Primary Dependencies**: [e.g., Django, Django REST Framework, Poetry or NEEDS CLARIFICATION]
**Storage**: [e.g., PostgreSQL via DATABASE_URL or NEEDS CLARIFICATION]
**Testing**: [e.g., pytest or NEEDS CLARIFICATION]
**Target Platform**: [e.g., Linux server (Kubernetes) or NEEDS CLARIFICATION]
**Project Type**: [single/web/mobile - determines source structure]
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [ ] No file deletions are required; if deletion is needed, pause and request explicit approval
      as a standalone request (Constitution Principle I).
- [ ] Runtime plan is Kubernetes-first (Minikube) and references `k8s/` manifests; Docker Compose is
      only a secondary option (Constitution Principle II).
- [ ] Project structure changes respect Django layout: `JobMarket2/` (project) and `JobApp/` (app),
      tests in `tests/` (Constitution Principle III).
- [ ] Quality gates defined for this feature: formatting/linting/tests/migrations (Principle IV).
- [ ] Security/config impacts called out (env vars, secrets, auth/CORS/JWT) (Principle V).

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
JobMarket2/            # Django project (settings/urls/asgi/wsgi)
JobApp/                # Django app (views/serializers/permissions/migrations)
tests/                 # pytest tests (mirror app modules)
docs/                  # API docs/supporting docs
k8s/                   # Kubernetes manifests (Minikube-first runtime)
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
