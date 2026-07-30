# AGENTS.md — PawMatch

PawMatch backend infrastructure and deployment setup is **production-ready**. Core infrastructure, settings modules, containerization, Render deployment blueprints, security audit parameters, CI/CD pipelines, and health endpoints are fully implemented.

## Mandatory reading order

Before writing any feature code, read these in order:

1. `docs/PRODUCT_ROADMAP.md` — version scope
2. `docs/TECHNOLOGY_STACK.md` — approved dependencies (SSOT — no unapproved packages)
3. `docs/architecture/SYSTEM_ARCHITECTURE.md`
4. `docs/architecture/DATABASE_SCHEMA.md`
5. `docs/architecture/AUTHENTICATION.md` + `docs/architecture/RBAC.md`
6. `docs/architecture/API_SPECIFICATION_V1.md`
7. `docs/backend/DJANGO_GUIDELINES.md`
8. `docs/frontend/COMPONENT_GUIDELINES.md`
9. `docs/deployment/ENVIRONMENT_VARIABLES.md`

## ADR system (governance)

All architectural decisions require an ADR. Existing ADRs live under `docs/adr/ADR-XXX-*.md`.

- **Read all Accepted ADRs before coding. Never violate them.**
- Propose a new ADR when introducing any new technology, framework, or pattern.
- ADRs are immutable once accepted — supersede rather than edit.
- `docs/adr/README.md` documents the ADR workflow, template, and lifecycle.

## Tech stack (from TECHNOLOGY_STACK.md)

| Layer | Choice |
|---|---|
| Backend | Python 3.13+ / Django 5.x / DRF / Gunicorn / WhiteNoise |
| Frontend | React 19 / Vite / Tailwind CSS / React Router / TanStack Query / Axios / React Hook Form / Zod / Framer Motion |
| Database | PostgreSQL 17 (Neon) |
| Cache/Queue | Redis / Celery |
| Media | Cloudinary |
| Auth | DRF Simple JWT (access + refresh tokens) |
| API docs | drf-spectacular (OpenAPI 3) |
| Backend deploy | Render (Docker Runtime) |
| Frontend deploy | Vercel (Edge SPA) |

## Current State & Completed Infrastructure

- **Backend Architecture**: Scaffolded under `backend/` using domain-driven layout (`apps/`, `config/`, `requirements/`, `manage.py`).
- **Multi-Environment Settings**: Modularized into `base.py`, `development.py`, `staging.py`, `production.py`, `logging.py`.
- **Environment Resolution**: Dynamic `.env.<environment>` resolution based on `DJANGO_SETTINGS_MODULE`.
- **Containerization**: Multi-stage OCI `Dockerfile`, `.dockerignore`, `docker-compose.yml`, `gunicorn.conf.py`.
- **Render Deployment**: Render blueprint `render.yaml` and hardened build script `build.sh`.
- **Telemetry & Logging**: Sub-millisecond `/health/` probe (0.328 ms), `RequestIDMiddleware` distributed tracing, and ISO 8601 UTC JSON structured logging.
- **CI/CD Pipeline**: GitHub Actions workflow `.github/workflows/backend.yml` validating Black, isort, Flake8, Django checks, pytest, and Docker builds.
- **Git Security**: Strictly ignored `.env`, `.env.*` files (only `.env.example` tracked).
- **Target Next Phase**: Authentication & User Accounts implementation (V1.0 Foundation release).

## Git conventions

- Branch: `feature/*` → `develop` → `staging` → `main`
- Commits: [Conventional Commits](https://www.conventionalcommits.org/) format
- All doc/code changes via PR. Architectural changes require an ADR first.

## AI agent rules

- **Never** import or install packages not listed in `TECHNOLOGY_STACK.md` without an approved ADR.
- Enforce UUID primary keys, DRF permission classes from RBAC.md, and environment-isolated configs.
- Never hardcode production secrets or shared resources in dev config.
- See `docs/ai/` for additional agent guidance (AI_DEVELOPMENT_RULES.md, AI_WORKFLOW.md, AI_LIMITATIONS.md, CODING_CONVENTIONS.md).

## Project lifecycle

| Phase | Version | Scope |
|---|---|---|
| Foundation | V1.0 | Auth, RBAC, shelters, pet listings, search, adoption workflow, notifications, admin |
| Smart Adoption | V1.5 | AI matching, lifestyle scoring |
| Pet Care | V2.0 | Medical records, telehealth |
| Future | V3.0–V7.0 | Vet platform, marketplace, enterprise, IoT |

## Key docs structure

| Path | Purpose |
|---|---|
| `docs/adr/` | Architecture Decision Records |
| `docs/architecture/` | System blueprints (schema, API spec, RBAC, deployment arch) |
| `docs/backend/` | Django/DRF/service-layer conventions |
| `docs/frontend/` | React component/routing/state conventions |
| `docs/deployment/` | Render, Vercel, env vars, backup, DR |
| `docs/security/` | JWT, RBAC, data protection, audit logs |
| `docs/development/` | Git workflow, coding standards, code review, branching |
| `docs/testing/` | Test pyramid, unit/integration/E2E strategy |
