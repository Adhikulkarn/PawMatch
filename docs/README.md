# PawMatch Master Engineering Documentation

```text
Project:         PawMatch
Document:        Master Knowledge Base & Documentation Directory Index
Status:          Approved / Single Source of Truth
Version:         1.0
Document Owner:  PawMatch Engineering Architecture Board
Last Updated:    July 29, 2026
```

---

## Table of Contents

- [1. Introduction](#1-introduction)
- [2. Documentation Hierarchy](#2-documentation-hierarchy)
- [3. Documentation Relationships & Dependency Flow](#3-documentation-relationships--dependency-flow)
- [4. Implementation & Reading Priority](#4-implementation--reading-priority)
- [5. AI Coding Agent Guidelines](#5-ai-coding-agent-guidelines)
- [6. Maintenance & Contribution Rules](#6-maintenance--contribution-rules)

---

## 1. Introduction

Welcome to the official **PawMatch Engineering Knowledge Base**. This repository directory serves as the **Single Source of Truth (SSOT)** for all architectural, operational, API, backend, frontend, security, deployment, and testing specifications.

PawMatch is designed as a production-grade, AI-powered pet adoption and healthcare ecosystem. This documentation is structured to support human developers, DevOps engineers, QA teams, product managers, and autonomous AI coding agents throughout the platform lifecycle.

---

## 2. Documentation Hierarchy

```text
docs/
│
├── README.md                      # Master Documentation Guide (This File)
│
├── architecture/                  # Platform Architecture & Core Blueprints
│   ├── PRODUCT_ROADMAP.md         # V1.0 to V7.0 release strategy and milestones
│   ├── TECHNOLOGY_STACK.md        # Approved frameworks, libraries, and runtime policy
│   ├── SYSTEM_ARCHITECTURE.md     # High-level component interactions & data flow
│   ├── DATABASE_SCHEMA.md         # Relational schema ERDs, indexing, and data models
│   ├── API_SPECIFICATION_V1.md    # RESTful API route contracts and payload definitions
│   ├── AUTHENTICATION.md          # JWT auth architecture, session control, and refresh
│   ├── RBAC.md                    # Role-Based Access Control matrix and permissions
│   ├── ERROR_CODES.md             # Standardized application error codes dictionary
│   ├── VERSIONING.md              # Semantic versioning & API deprecation policies
│   ├── DEPLOYMENT_ARCHITECTURE.md # Cloud infrastructure topology (Render + Vercel)
│   ├── MEDIA_STORAGE.md           # Cloudinary media transformation & upload pipelines
│   └── SECURITY_ARCHITECTURE.md   # Threat modeling, encryption, and protection policy
│
├── adr/                           # Architecture Decision Records (ADRs)
│   ├── README.md                  # ADR index & submission guidelines
│   ├── ADR-001-Choose-Django.md   # Selection of Python 3.13 / Django 5.x REST backend
│   ├── ADR-002-Use-UUIDs.md       # Primary key policy (UUIDv4 over auto-increment)
│   ├── ADR-003-Choose-PostgreSQL.md # RDBMS selection (PostgreSQL 17)
│   ├── ADR-004-Cloudinary.md      # Media asset management solution selection
│   ├── ADR-005-Celery-Redis.md    # Asynchronous task queue and message broker selection
│   ├── ADR-006-Render.md          # Backend PaaS web service deployment selection
│   ├── ADR-007-Vercel.md          # Frontend SPA edge network deployment selection
│   └── ADR-008-JWT.md             # Bearer token authentication choice
│
├── api/                           # Executable API Specifications & Tooling
│   ├── README.md                  # API documentation overview & Swagger link
│   ├── API_CHANGELOG.md           # Historical route changes and deprecation logs
│   ├── OPENAPI.md                 # OpenAPI 3.0 specification export guide
│   ├── POSTMAN.md                 # Postman integration & collection import
│   ├── BRUNO.md                   # Bruno offline API collection workflow
│   ├── REQUEST_RESPONSE_STANDARDS.md # Payload envelope & JSON standards
│   ├── PAGINATION.md              # Limit/offset & cursor pagination standards
│   ├── FILTERING.md               # `django-filter` query string criteria
│   └── RATE_LIMITING.md           # Redis rate limiting thresholds
│
├── backend/                       # Backend Engineering Standards & Design Patterns
│   ├── README.md                  # Backend index & service layer architecture
│   ├── PROJECT_STRUCTURE.md       # Modular Django app layout (`apps/`, `config/`)
│   ├── DJANGO_GUIDELINES.md       # Core Django conventions & settings policies
│   ├── MODEL_GUIDELINES.md        # ORM model design, migrations, and indexing
│   ├── SERIALIZER_GUIDELINES.md   # DRF Serializer validation patterns
│   ├── VIEWSET_GUIDELINES.md      # ModelViewSet overrides and generic views
│   ├── SERVICE_LAYER.md           # Decoupled business logic services (`services.py`)
│   ├── SIGNALS.md                 # Django signals policy & event handlers
│   ├── CELERY.md                  # Celery worker process & task definition rules
│   ├── REDIS.md                   # Redis caching keyspace & pub/sub setup
│   ├── CLOUDINARY.md              # Cloudinary SDK usage in Django models
│   ├── LOGGING.md                 # Structured JSON logging guidelines
│   └── TESTING.md                 # Pytest & Django test runner setup
│
├── frontend/                      # Frontend Engineering Standards & UI Architecture
│   ├── README.md                  # Frontend index & React 19 architecture
│   ├── PROJECT_STRUCTURE.md       # Feature-driven React folder structure
│   ├── COMPONENT_GUIDELINES.md    # UI component design, props, and accessibility
│   ├── ROUTING.md                 # React Router setup & protected route guards
│   ├── STATE_MANAGEMENT.md        # TanStack Query & local state guidelines
│   ├── API_INTEGRATION.md         # Axios interceptors, JWT refresh, API hooks
│   ├── FORM_GUIDELINES.md         # React Hook Form + Zod schema validation
│   └── UI_STANDARDS.md            # Tailwind CSS design tokens & animations
│
├── deployment/                    # Multi-Environment Infrastructure & DevOps
│   ├── README.md                  # Deployment overview & environment matrix
│   ├── DEVELOPMENT.md             # Local environment setup guide
│   ├── STAGING.md                 # Render Staging environment specification
│   ├── PRODUCTION.md              # Render Production hardening specification
│   ├── RENDER.md                  # Render web service & worker provisioning
│   ├── VERCEL.md                  # Vercel deployment pipeline setup
│   ├── REDIS.md                   # Managed Redis cluster setup
│   ├── CLOUDINARY.md              # Cloudinary environment folder isolation (`/dev/`, `/staging/`, `/prod/`)
│   ├── POSTGRESQL.md              # Database connection pooling & SSL settings
│   ├── ENVIRONMENT_VARIABLES.md   # Master environment variable catalog
│   ├── BACKUP_STRATEGY.md         # Automated backup & Point-In-Time Recovery (PITR)
│   └── DISASTER_RECOVERY.md       # Incident recovery & failover runbooks
│
├── security/                      # Platform Security & Regulatory Compliance
│   ├── README.md                  # Security posture & vulnerability disclosure
│   ├── AUTHENTICATION.md          # Multi-factor & JWT security policies
│   ├── AUTHORIZATION.md           # Permission checking & RBAC guards
│   ├── DATA_PROTECTION.md         # Data encryption at rest & in transit
│   ├── PASSWORD_POLICY.md         # Hashing work factors & complexity rules
│   ├── SECURITY_HEADERS.md        # HSTS, CSP, X-Frame-Options configurations
│   ├── JWT_POLICY.md              # Token rotation, lifetime & blacklisting
│   └── AUDIT_LOGS.md              # Security audit logging specification
│
├── development/                   # Software Engineering Workflow & Governance
│   ├── README.md                  # Contributor workflow index
│   ├── CONTRIBUTING.md            # Code of conduct & contribution guide
│   ├── GIT_WORKFLOW.md            # Git branch policy & Pull Request workflow
│   ├── CODING_STANDARDS.md        # PEP 8, Black, ESLint, TypeScript standards
│   ├── CODE_REVIEW.md             # Reviewer checklists & PR approval criteria
│   ├── BRANCHING_STRATEGY.md      # `feature/*` -> `develop` -> `staging` -> `main`
│   ├── COMMIT_CONVENTION.md       # Conventional Commits format
│   └── RELEASE_PROCESS.md         # Version tagging & release checklist
│
├── testing/                       # Quality Assurance & Automated Testing
│   ├── README.md                  # Testing philosophy & coverage thresholds
│   ├── TESTING_STRATEGY.md        # Test pyramid (Unit, Integration, E2E)
│   ├── UNIT_TESTS.md              # Pytest & Vitest unit testing guidelines
│   ├── INTEGRATION_TESTS.md       # API endpoint integration test suite
│   ├── API_TESTING.md             # Newman & Bruno automated API testing
│   ├── SECURITY_TESTING.md        # Static (SAST) and dynamic (DAST) analysis
│   └── PERFORMANCE_TESTING.md     # Locust load testing & latency SLAs
│
├── ai/                            # AI Coding Agent Instructions & Guardrails
│   ├── README.md                  # AI agent onboarding & workspace rules
│   ├── AI_CONTEXT.md              # Context injection map for LLMs
│   ├── AI_DEVELOPMENT_RULES.md    # Strict constraints for AI code generation
│   ├── PROMPT_GUIDELINES.md       # Recommended prompt templates for tasks
│   ├── CODING_CONVENTIONS.md      # Machine-readable coding rules
│   ├── AI_WORKFLOW.md             # Step-by-step task execution protocol
│   └── AI_LIMITATIONS.md          # Prohibited operations for AI agents
│
└── assets/                        # Diagrams, Screenshots & Visual Assets
    ├── diagrams/                  # Editable Mermaid / PlantUML diagram files
    ├── images/                    # System architecture flowcharts
    └── screenshots/               # Application UI walkthroughs
```

---

## 3. Documentation Relationships & Dependency Flow

The PawMatch documentation is designed as a directed acyclic graph (DAG) of technical dependencies. Every document references foundational blueprints to ensure complete consistency across the codebase:

```text
[ PRODUCT_ROADMAP.md ]  ──►  [ TECHNOLOGY_STACK.md ]
                                      │
                                      ▼
                        [ SYSTEM_ARCHITECTURE.md ]
                                      │
           ┌──────────────────────────┼──────────────────────────┐
           ▼                          ▼                          ▼
[ DATABASE_SCHEMA.md ]          [ RBAC.md ]           [ AUTHENTICATION.md ]
           │                          │                          │
           └──────────────────────────┼──────────────────────────┘
                                      │
                                      ▼
                        [ API_SPECIFICATION_V1.md ]
                                      │
           ┌──────────────────────────┴──────────────────────────┐
           ▼                                                     ▼
[ backend/SERVICE_LAYER.md ]                       [ frontend/API_INTEGRATION.md ]
```

### Key Dependency Rules
1. **`PRODUCT_ROADMAP.md`** drives release scope.
2. **`TECHNOLOGY_STACK.md`** defines allowed dependencies; no tool may be used if absent from this file.
3. **`SYSTEM_ARCHITECTURE.md`** establishes component boundaries before code scaffolding.
4. **`DATABASE_SCHEMA.md`** and **`RBAC.md`** define entities and permissions prior to writing Django models or API views.
5. **`API_SPECIFICATION_V1.md`** acts as the single contract between backend DRF developers and frontend React developers.

---

## 4. Implementation & Reading Priority

To minimize redesign, technical debt, and code rework, human developers and AI agents must read and implement documentation in the following strict sequential priority:

| Priority Order | Document | Purpose & Rationale |
| :---: | :--- | :--- |
| **1** | [PRODUCT_ROADMAP.md](file:///home/spidy/Desktop/projects/PawMatch/PRODUCT_ROADMAP.md) | Understand version goals, features, and target milestones. |
| **2** | [TECHNOLOGY_STACK.md](file:///home/spidy/Desktop/projects/PawMatch/TECHNOLOGY_STACK.md) | Verify approved libraries, Python/Node versions, and frameworks. |
| **3** | [SYSTEM_ARCHITECTURE.md](file:///home/spidy/Desktop/projects/PawMatch/docs/architecture/SYSTEM_ARCHITECTURE.md) | Grasp high-level data flow, services, and asynchronous worker queues. |
| **4** | [DATABASE_SCHEMA.md](file:///home/spidy/Desktop/projects/PawMatch/docs/architecture/DATABASE_SCHEMA.md) | Understand relational entities, fields, foreign keys, and indexes. |
| **5** | [AUTHENTICATION.md](file:///home/spidy/Desktop/projects/PawMatch/docs/architecture/AUTHENTICATION.md) & [RBAC.md](file:///home/spidy/Desktop/projects/PawMatch/docs/architecture/RBAC.md) | Master JWT lifecycle, user roles, and access control matrices. |
| **6** | [API_SPECIFICATION_V1.md](file:///home/spidy/Desktop/projects/PawMatch/docs/architecture/API_SPECIFICATION_V1.md) | Review endpoint contracts, query filters, and response schemas. |
| **7** | [backend/DJANGO_GUIDELINES.md](file:///home/spidy/Desktop/projects/PawMatch/docs/backend/DJANGO_GUIDELINES.md) | Follow backend Django app conventions and service layer patterns. |
| **8** | [frontend/COMPONENT_GUIDELINES.md](file:///home/spidy/Desktop/projects/PawMatch/docs/frontend/COMPONENT_GUIDELINES.md) | Follow React 19 UI component conventions and state management rules. |
| **9** | [deployment/ENVIRONMENT_VARIABLES.md](file:///home/spidy/Desktop/projects/PawMatch/docs/deployment/ENVIRONMENT_VARIABLES.md) | Configure environment secrets across Dev, Staging, and Prod. |

---

## 5. AI Coding Agent Guidelines

Autonomous AI agents (including Claude Code, Cursor, ChatGPT, Gemini CLI, Copilot, Windsurf) working on PawMatch must adhere to the following mandatory execution rules:

1. **Prerequisite Reading**: Prior to modifying or generating code, AI agents MUST inspect [TECHNOLOGY_STACK.md](file:///home/spidy/Desktop/projects/PawMatch/TECHNOLOGY_STACK.md) and [SYSTEM_ARCHITECTURE.md](file:///home/spidy/Desktop/projects/PawMatch/docs/architecture/SYSTEM_ARCHITECTURE.md).
2. **Zero Unapproved Dependencies**: AI agents must **NEVER** install or import third-party packages, ORMs, or utility libraries not listed in [TECHNOLOGY_STACK.md](file:///home/spidy/Desktop/projects/PawMatch/TECHNOLOGY_STACK.md) without an approved ADR.
3. **Database Schema Compliance**: AI agents creating or modifying Django models must reference [DATABASE_SCHEMA.md](file:///home/spidy/Desktop/projects/PawMatch/docs/architecture/DATABASE_SCHEMA.md) and enforce UUID primary keys.
4. **RBAC & Security Enforcement**: AI agents writing DRF API views must apply explicit permission classes as defined in [RBAC.md](file:///home/spidy/Desktop/projects/PawMatch/docs/architecture/RBAC.md).
5. **Environment Isolation**: AI agents must respect environment isolation parameters and never hardcode production keys or shared resources in development configurations.

---

## 6. Maintenance & Contribution Rules

- All documentation changes must be submitted via Pull Request.
- Any architectural change requires drafting a new Architectural Decision Record in `docs/adr/`.
- Keep Markdown clean, well-formatted, and compliant with GitHub-Flavored Markdown (GFM).
