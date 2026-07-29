# AGENTS.md — PawMatch

This is a **pre-code project** — no source files, package managers, build scripts, or tests exist yet. Everything lives in `docs/` and is currently in "Approved Blueprint" / placeholder status.

## Mandatory reading order

Before writing any code, read these in order (per `docs/README.md:200`):

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
| Database | PostgreSQL 17 |
| Cache/Queue | Redis / Celery |
| Media | Cloudinary |
| Auth | DRF Simple JWT (access + refresh tokens) |
| API docs | drf-spectacular (OpenAPI 3) |
| Backend deploy | Render (PaaS web + worker) |
| Frontend deploy | Vercel (edge SPA) |

## Current state

- **No code scaffolded** — no `requirements.txt`, `package.json`, `manage.py`, or `src/`.
- All `docs/` files are **blueprint templates** (generic boilerplate). Real content must be written.
- 8 initial ADRs exist (`ADR-001` through `ADR-008`). ~32 more are backlogged.
- V1.0 target is the "Foundation" release (auth, RBAC, shelter management, pet listings, search, adoption workflow, notifications, admin panel).

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
