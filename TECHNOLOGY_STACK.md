# PawMatch Technology Stack Specification

```text
Project:         PawMatch
Document:        Official Technology Stack Specification
Version:         1.0
Status:          Approved / Single Source of Truth
Document Owner:  PawMatch Technical Architecture Board
Last Updated:    July 29, 2026
```

---

## Table of Contents

- [1. Introduction](#1-introduction)
- [2. Approved Technology Policy](#2-approved-technology-policy)
- [3. System Overview](#3-system-overview)
- [4. Technology Stack Summary](#4-technology-stack-summary)
- [5. Frontend Technologies](#5-frontend-technologies)
  - [5.1 Core Framework: React 19](#51-core-framework-react-19)
  - [5.2 Build Tool: Vite](#52-build-tool-vite)
  - [5.3 Styling: Tailwind CSS](#53-styling-tailwind-css)
  - [5.4 Routing: React Router](#54-routing-react-router)
  - [5.5 HTTP Client: Axios](#55-http-client-axios)
  - [5.6 Forms: React Hook Form](#56-forms-react-hook-form)
  - [5.7 Validation: Zod](#57-validation-zod)
  - [5.8 Server State: TanStack Query](#58-server-state-tanstack-query)
  - [5.9 Animations: Framer Motion](#59-animations-framer-motion)
- [6. Backend Technologies](#6-backend-technologies)
  - [6.1 Programming Language: Python 3.13+](#61-programming-language-python-313)
  - [6.2 Backend Framework: Django 5.x](#62-backend-framework-django-5x)
  - [6.3 API Framework: Django REST Framework (DRF)](#63-api-framework-django-rest-framework-drf)
  - [6.4 Authentication: DRF Simple JWT](#64-authentication-drf-simple-jwt)
  - [6.5 Background Processing: Celery](#65-background-processing-celery)
  - [6.6 Task Broker: Redis](#66-task-broker-redis)
  - [6.7 API Documentation: drf-spectacular](#67-api-documentation-drf-spectacular)
  - [6.8 Filtering: django-filter](#68-filtering-django-filter)
  - [6.9 CORS Management: django-cors-headers](#69-cors-management-django-cors-headers)
  - [6.10 Environment Variables: python-decouple](#610-environment-variables-python-decouple)
  - [6.11 Image Processing: Pillow](#611-image-processing-pillow)
  - [6.12 Production WSGI Server: Gunicorn](#612-production-wsgi-server-gunicorn)
  - [6.13 Static File Serving: WhiteNoise](#613-static-file-serving-whitenoise)
- [7. Database](#7-database)
- [8. Media Storage](#8-media-storage)
- [9. Deployment Stack](#9-deployment-stack)
- [10. Development Tools](#10-development-tools)
- [11. API Standards](#11-api-standards)
- [12. Security Stack](#12-security-stack)
- [13. Background Processing Architecture](#13-background-processing-architecture)
- [14. Folder Structure](#14-folder-structure)
- [15. Environment Strategy](#15-environment-strategy)
- [16. Coding Standards](#16-coding-standards)
- [17. Scalability Strategy](#17-scalability-strategy)
- [18. Future Technologies](#18-future-technologies)
- [19. Technology Decision Records](#19-technology-decision-records)
- [20. Version Compatibility](#20-version-compatibility)
- [21. Documentation Structure](#21-documentation-structure)
- [22. Conclusion](#22-conclusion)

---

## 1. Introduction

This document establishes the **official, authoritative technology stack specification** for the **PawMatch** pet adoption and health ecosystem.

The primary purpose of this specification is to provide a single, immutable source of truth for software engineers, platform architects, open-source contributors, and AI coding agents. It governs technical choices, architectural patterns, toolchains, deployment strategies, and engineering standards across all PawMatch repositories.

All present and future software development within the PawMatch ecosystem must strictly adhere to the guidelines set forth in this document unless explicitly superseded by an approved Architecture Decision Record (ADR).

---

## 2. Approved Technology Policy

To maintain long-term system maintainability, strict security posture, high performance, and cohesive developer productivity, **PawMatch enforces a strict Approved Technology Policy**:

1. **Strict Inclusion Rule**: Only technologies, libraries, frameworks, services, and languages explicitly documented within this specification are approved for production use.
2. **Prohibition of Unapproved Dependendies**: Developers and AI coding agents are strictly prohibited from introducing unvetted frameworks, third-party libraries, databases, ORMs, state management tools, or cloud micro-services without prior review.
3. **Architecture Decision Record (ADR) Requirement**: If a new feature requires a tool or technology not covered by this specification, an Architecture Decision Record (ADR) must be drafted, submitted to the Architecture Board, and formally approved before any code integration.
4. **Agent Compliance**: AI coding agents operating within PawMatch codebases must cross-reference this document prior to proposing dependencies, scaffolding projects, or refactoring existing modules.

---

## 3. System Overview

The PawMatch architecture follows a modern, decoupled client-server pattern. The client tier is powered by a high-performance Single Page Application (SPA) built with React 19 and Vite. The backend tier utilizes a Django 5.x REST framework API backed by PostgreSQL 17 for relational storage, Cloudinary for optimized media management, Redis as a memory broker/cache, and Celery for asynchronous background processing.

```text
React (Vite)
      │
      ▼
 REST API
      │
      ▼
 Django + DRF
      │
 ┌────┼───────────────┐
 │    │               │
 ▼    ▼               ▼
PostgreSQL      Cloudinary
 │
 ▼
Redis
 │
 ▼
Celery Workers
```

### Component Inter-Communication Flow

1. **Client to API Tier**: The React SPA communicates asynchronously with the Django REST Framework (DRF) backend via secure HTTPS using JSON-encoded REST endpoints authenticated with JWT bearer tokens.
2. **Backend to Database Tier**: Django's Object-Relational Mapper (ORM) interacts directly with PostgreSQL 17 over an encrypted connection pooling layer to manage relational state, transactional boundaries, and structured complex queries.
3. **Backend to Media Cloud**: When users or shelters upload media (e.g., pet photos, medical PDFs), Django delegates storage, compression, thumbnail generation, and CDN delivery to Cloudinary via the Cloudinary Python SDK.
4. **Backend to Task Broker**: For long-running operations (email dispatches, push notifications, image re-encoding, AI model invocations), DRF endpoints push JSON task payloads directly into Redis queues.
5. **Task Broker to Worker Tier**: Asynchronous Celery Worker processes pull queued tasks from Redis, execute background routines out-of-band, update database models, or interface with external APIs without blocking the HTTP request-response cycle.

---

## 4. Technology Stack Summary

| Layer | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Frontend Framework** | React | 19.x | Declarative component UI rendering |
| **Frontend Build Tool** | Vite | 6.x / Latest | Next-gen fast HMR & optimized production bundling |
| **Frontend Styling** | Tailwind CSS | 3.4 / 4.x | Utility-first responsive styling engine |
| **Frontend Router** | React Router | 7.x / Latest | Client-side routing & deep linking |
| **HTTP Client** | Axios | 1.x | Promise-based HTTP client for API requests |
| **Form Handling** | React Hook Form | 7.x | High-performance, un-controlled form state management |
| **Schema Validation** | Zod | 3.x | TypeScript-first runtime schema validation |
| **Server State Management** | TanStack Query | 5.x | Server-state caching, synchronization & optimistic UI |
| **UI Animations** | Framer Motion | 11.x | Fluid micro-interactions and layout transitions |
| **Language (Backend)** | Python | 3.13+ | Core backend runtime environment |
| **Backend Framework** | Django | 5.1+ | Robust web framework (ORM, Security, Admin) |
| **REST API Engine** | Django REST Framework | 3.15+ | RESTful API serialization, viewsets, and permissions |
| **Authentication** | DRF Simple JWT | 5.3+ | OAuth2/JWT access & refresh token lifecycle |
| **Task Queue / Workers** | Celery | 5.4+ | Asynchronous job execution and cron schedules |
| **Message Broker / Cache** | Redis | 7.4 / Latest | In-memory message broker for Celery & future cache |
| **API Documentation** | drf-spectacular | 0.28+ | OpenAPI 3.0 schema generator & Swagger/ReDoc UI |
| **Database Filtering** | django-filter | 24.x | Dynamic URL query string filtering for DRF viewsets |
| **CORS Middleware** | django-cors-headers | 4.x | Cross-Origin Resource Sharing control |
| **Environment Management** | python-decouple | 3.8+ | Strict separation of settings and secrets |
| **Image Processing** | Pillow | 10.x+ | Python Imaging Library for server-side manipulation |
| **WSGI Server** | Gunicorn | 23.x+ | Production HTTP WSGI server for UNIX |
| **Static Files** | WhiteNoise | 6.x | Direct static file serving for Python web apps |
| **Relational Database** | PostgreSQL | 17.x | Primary ACID-compliant relational data store |
| **Media Storage / CDN** | Cloudinary | Cloud SDK | Cloud media hosting, auto-compression, and global CDN |
| **Frontend Hosting** | Vercel | Cloud | Edge hosting & continuous integration deployment |
| **Backend Hosting** | Render | Cloud | Managed PaaS web services for Django & Celery |

---

## 5. Frontend Technologies

---

### 5.1 Core Framework: React 19

- **Purpose**: Powering the user-facing SPA, interactive shelter portals, and adoption management interfaces.
- **Advantages**:
  - Declarative component-based architecture fostering reusability across complex views.
  - React 19 Concurrent Rendering features, Server Actions integration capability, and improved hook ergonomics (`use()`, `useActionState()`).
  - Massive ecosystem of accessible UI primitives and developer tools.
- **Selection Rationale**: Industry standard for enterprise SPAs, ensuring high developer availability, top-tier performance, and long-term ecosystem stability.
- **Best Practices**:
  - Functional components with strict TypeScript/ESLint typing.
  - Component decoupling: keep presentational components stateless and extract complex domain logic into custom hooks.
  - Avoid unnecessary re-renders through memoization (`useMemo`, `useCallback`) where empirically needed.

---

### 5.2 Build Tool: Vite

- **Purpose**: Next-generation development server and production bundler for the React frontend application.
- **Key Features & Benefits**:
  - **Lightning-Fast HMR**: Native ES Modules (ESM) serving provides instantaneous Hot Module Replacement regardless of application size.
  - **Optimized Production Bundling**: Uses Rollup under the hood with automatic code splitting, tree shaking, and asset preloading.
  - **Instant Server Cold Starts**: Zero-bundling dev server initialization.

---

### 5.3 Styling: Tailwind CSS

- **Purpose**: Provides atomic, utility-first CSS for constructing responsive, highly custom, modern user interfaces.
- **Selection Rationale**: Eliminates stylesheet bloat, avoids specificity wars, enforces visual consistency via design tokens, and integrates seamlessly with component frameworks.

---

### 5.4 Routing: React Router

- **Purpose**: Client-side routing, route guard enforcement (RBAC route protection), and dynamic parameter handling.
- **Implementation Rules**:
  - Protected route wrappers verifying JWT presence and user role claims before mounting view components.
  - Lazy loading of route components using `React.lazy()` for code splitting.

---

### 5.5 HTTP Client: Axios

- **Purpose**: Formulating promise-based HTTP network requests from the browser to backend REST APIs.
- **Key Capabilities Utilized**:
  - Centralized instance configuration (`baseURL`, default timeout headers).
  - Request Interceptors: Automatically attaching JWT Authorization bearer tokens (`Bearer <access_token>`).
  - Response Interceptors: Intercepting `401 Unauthorized` responses to seamlessly execute token refresh calls via `DRF Simple JWT` before retrying failed requests.

---

### 5.6 Forms: React Hook Form

- **Purpose**: Handling complex form state (adoption applications, pet listing creators, shelter registration forms).
- **Advantages**: Minimal re-renders (uncontrolled inputs), tiny bundle footprint, intuitive validation integration with schema builders.

---

### 5.7 Validation: Zod

- **Purpose**: TypeScript-first runtime schema validation for forms, environment variables, and API responses.
- **Integration**: Works directly with React Hook Form via `@hookform/resolvers/zod` to enforce validation rules on client forms prior to network dispatch.

---

### 5.8 Server State: TanStack Query

- **Purpose**: Managing server state, asynchronous API data fetching, caching, deduplication, background re-fetching, and optimistic UI updates.
- **Selection Rationale**: Separates client state from server state, eliminating complex Redux boilerplate while providing robust cache invalidation strategies out of the box.

---

### 5.9 Animations: Framer Motion

- **Purpose**: Delivering fluid, accessible micro-animations, page transitions, modal overlays, and interactive card swipes (for pet matching).

---

## 6. Backend Technologies

---

### 6.1 Programming Language: Python 3.13+

- **Selection Rationale**: Python is the global benchmark for web API development, artificial intelligence, data science, and asynchronous task execution. Python 3.13 provides notable performance enhancements, improved error tracebacks, and enhanced memory efficiency.

---

### 6.2 Backend Framework: Django 5.x

- **Purpose**: Core application engine handling HTTP request routing, ORM abstractions, security middleware, database migrations, and administrative capabilities.
- **Core Pillars**:
  - **Model-Template-View (MTV) / Clean Separation**: Leveraged primarily as a headless backend service engine.
  - **Enterprise Security**: Built-in protection against SQL Injection, CSRF, Clickjacking, and XSS.
  - **Robust ORM**: Expressive database model definitions, automated schema migration management, and transaction management.
  - **Built-in Admin Panel**: Powerful operational interface for internal platform staff to manage models directly.

---

### 6.3 API Framework: Django REST Framework (DRF)

- **Purpose**: Toolkit layered on top of Django to construct powerful, standardized REST APIs.
- **Key Modules Utilized**:
  - **Serializers**: Data parsing, strict payload validation, and JSON serialization.
  - **ModelViewSets & Generic Views**: Reducing CRUD boilerplate while preserving custom override hooks.
  - **Permission Classes**: Fine-grained RBAC enforcement (`IsAuthenticated`, `IsShelterManager`, `IsAdminUser`).
  - **Pagination**: Standardized limit/offset and cursor-based JSON response pagination.

---

### 6.4 Authentication: DRF Simple JWT

- **Purpose**: JSON Web Token (JWT) authentication plugin for DRF.
- **Token Architecture**:
  - **Access Token**: Short-lived (e.g., 15 minutes) bearer token sent in HTTP `Authorization` headers.
  - **Refresh Token**: Long-lived (e.g., 7 days) token used exclusively to acquire new access tokens.
  - **Token Rotation & Blacklisting**: Enforces single-use refresh tokens with automatic blacklisting upon rotation to prevent replay attacks.

---

### 6.5 Background Processing: Celery

- **Purpose**: Asynchronous task queue and job scheduler executing CPU-intensive or latency-heavy operations off the main HTTP thread.
- **Architecture**:
  - Celery Client (Django) enqueues tasks into Redis.
  - Celery Worker processes pull tasks asynchronously and execute routines.
  - Celery Beat acts as a cron-like scheduler for periodic background jobs.
- **Primary Use Cases**:
  - **Email Dispatch**: Welcome emails, application status alerts, password reset links.
  - **Notification Delivery**: Multi-channel push and in-app message broadcasting.
  - **Media Processing**: High-resolution image re-encoding and Cloudinary sync.
  - **AI Task Dispatch**: Asynchronous callouts to ML scoring pipelines.
  - **Scheduled Cleanup**: Expired session purging and stale application auto-archiving.

---

### 6.6 Task Broker: Redis

- **Purpose**: High-performance in-memory key-value store acting as the primary message broker for Celery task queues and future application caching.
- **Selection Rationale**: Sub-millisecond latency, extreme throughput, native pub/sub support, and seamless integration with Celery and Django cache backends.

---

### 6.7 API Documentation: drf-spectacular

- **Purpose**: Automated OpenAPI 3.0 schema generation for Django REST Framework.
- **Developer Interfaces Provided**:
  - **Swagger UI**: Interactive browser sandbox for testing API endpoints (`/api/schema/swagger-ui/`).
  - **ReDoc**: Clean, production-grade documentation viewer (`/api/schema/redoc/`).

---

### 6.8 Filtering: django-filter

- **Purpose**: Provides declarative URL query parameter filtering for DRF querysets (e.g., `/api/v1/pets/?species=Dog&age_category=Young&gender=Female`).

---

### 6.9 CORS Management: django-cors-headers

- **Purpose**: Handles Cross-Origin Resource Sharing (CORS) headers to allow secure requests from the Vercel-hosted React client to the Render-hosted Django backend.

---

### 6.10 Environment Variables: python-decouple

- **Purpose**: Strictly separates configuration settings and sensitive credentials (API keys, database URLs) from source code following 12-Factor App methodology.

---

### 6.11 Image Processing: Pillow

- **Purpose**: Python Imaging Library used server-side for image verification, dimension checking, and preliminary format transformation prior to cloud storage upload.

---

### 6.12 Production Server: Gunicorn

- **Purpose**: Production-grade Green Unicorn WSGI HTTP server running Django application processes behind cloud reverse proxies.

---

### 6.13 Static File Serving: WhiteNoise

- **Purpose**: Serves Django static files (Admin UI CSS/JS, Swagger UI assets) directly from the Python web application without requiring a dedicated Nginx server for static asset hosting.

---

## 7. Database

### PostgreSQL 17

PawMatch relies on **PostgreSQL 17** as its primary, single-source-of-truth relational database management system.

#### Key Architectural Highlights

- **ACID Compliance**: Strict transactional safety guarantees for adoption workflows, financial transactions, and user identity changes.
- **JSONB Document Support**: Efficient storage and indexing of semi-structured document payloads (e.g., dynamic shelter questionnaire templates, AI compatibility vector logs).
- **UUID Primary Keys**: All primary entities use Universally Unique Identifiers (UUIDv4) instead of sequential integers to prevent enumeration attacks and simplify future database sharding.
- **Relational Integrity**: Strict foreign key constraints (`ON DELETE RESTRICT` / `ON DELETE CASCADE`), unique constraints, and check constraints enforced at the database tier.
- **Performance Indexing**: B-Tree, GIN (for JSONB), and Partial Indexes applied strategically to high-frequency query paths (e.g., `shelter_id`, `status`, `species`).
- **Soft Deletes**: Critical domain models (User profiles, Pet Listings) implement soft-deletion fields (`is_deleted`, `deleted_at`) to preserve historical audit logs and application records.

#### Rationale Over Alternative Databases
PostgreSQL was selected over MySQL/MongoDB due to its unmatched stability, native JSONB index performance, rich extension ecosystem (PostGIS for future geographic search), and industry-wide compliance standards.

---

## 8. Media Storage

### Cloudinary

All user-generated assets—including pet photos, shelter logos, medical records, and verification documents—are managed via **Cloudinary**.

#### Features & Usage Breakdown

- **Direct Cloud Uploads**: Client-side or backend-delegated secure media uploads.
- **Automated Compression & Optimization**: Automatic conversion to next-gen image formats (WebP/AVIF) with quality optimization based on client screen DPI.
- **Dynamic On-The-Fly Transformations**: Dynamic image resizing, cropping (e.g., square pet card thumbnails), and watermarking via URL parameters.
- **Global CDN Delivery**: Low-latency content delivery worldwide via Cloudinary's multi-CDN architecture.
- **Secure File Storage**: Access-restricted private cloud storage for sensitive PDFs (shelter legal licenses, veterinary medical records).

---

## 9. Deployment Stack

```text
┌────────────────────────────────────────────────────────┐
│                   Vercel Global CDN                    │
│                 (React 19 Frontend SPA)                │
└───────────────────────────┬────────────────────────────┘
                            │ HTTPS / REST
                            ▼
┌────────────────────────────────────────────────────────┐
│                   Render PaaS Cloud                    │
│  ┌──────────────────────┐    ┌──────────────────────┐  │
│  │ Django Gunicorn Web  │    │ Celery Worker Engine │  │
│  └──────────┬───────────┘    └──────────▲───────────┘  │
└─────────────┼───────────────────────────┼──────────────┘
              │                           │
      ┌───────┴──────────┐        ┌───────┴──────────┐
      ▼                  ▼        ▼                  ▼
┌───────────┐      ┌───────────┐┌───────────┐      ┌───────────┐
│ Managed   │      │ Cloudinary││ Managed   │      │ Email/Push│
│ PostgreSQL│      │ Media CDN ││ Redis     │      │ Gateways  │
└───────────┘      └───────────┘└───────────┘      └───────────┘
```

- **Frontend Hosting (Vercel)**: Global Edge Network hosting for the React SPA. Provides continuous deployment git triggers, automated preview deployments for pull requests, and global SSL termination.
- **Backend Hosting (Render)**: Fully managed PaaS hosting for Django web services and dedicated background worker instances. Automatically runs Gunicorn WSGI processes and Celery background workers.
- **Managed PostgreSQL (Render/Neon/AWS RDS)**: Dedicated managed PostgreSQL database instance featuring automated automated daily backups, storage auto-scaling, and failover support.
- **Managed Redis (Render/Upstash/Redis Cloud)**: High-availability managed Redis cluster providing low-latency caching and message brokerage.
- **Cloudinary**: Cloud-native media asset storage and CDN delivery.

---

## 10. Development Tools

| Tool | Category | Purpose & Utilization |
| :--- | :--- | :--- |
| **Git** | Distributed Version Control | Source code versioning, branching strategy enforcement, and history tracking. |
| **GitHub** | Code Hosting & Collaboration | Centralized code repository, Pull Request reviews, Issue tracking, and Project boards. |
| **VS Code** | IDE / Editor | Standardized development environment with recommended extensions (Python, Pylance, Tailwind CSS, ESLint). |
| **Postman** | API Testing | Manual API endpoint testing, environment variable collection sharing, and integration testing. |
| **Bruno** | Offline API Client | Git-friendly, open-source API client storing test collections as plain files directly within code repos. |
| **Docker (Future)** | Containerization | Future containerized local development environment (`docker-compose`) for orchestrating Postgres, Redis, Celery, and Django. |
| **GitHub Actions (Future)** | CI/CD Automation | Automated testing pipelines running pytest, ESLint, Black, and automated deployment triggers on main branch merges. |

---

## 11. API Standards

PawMatch enforces strict RESTful API design conventions:

1. **Protocol**: HTTP/2 over TLS 1.3 (HTTPS) mandatory across all environments.
2. **Data Format**: Standardized JSON payloads (`Content-Type: application/json`).
3. **URL Naming Conventions**: Resource-oriented, lowercase, plural nouns (e.g., `/api/v1/shelters/`, `/api/v1/pets/{id}/applications/`).
4. **HTTP Status Codes**:
   - `200 OK`: Successful read or update operation.
   - `201 Created`: Successful resource creation.
   - `204 No Content`: Successful deletion.
   - `400 Bad Request`: Validation failure or malformed JSON payload.
   - `401 Unauthorized`: Missing or invalid JWT authentication token.
   - `403 Forbidden`: Authenticated user lacks required RBAC role permissions.
   - `404 Not Found`: Target resource does not exist.
   - `429 Too Many Requests`: Rate limit exceeded.
   - `500 Internal Server Error`: Unhandled server exception.
5. **API Versioning**: Enforced via URL routing prefix (`/api/v1/`). Major breaking changes will be introduced cleanly under `/api/v2/`.
6. **Documentation Contract**: All DRF viewsets must be annotated with `drf-spectacular` decorators to auto-generate OpenAPI 3.0 specs.

---

## 12. Security Stack

- **JWT Authentication**: Short-lived access tokens paired with rotate-on-use refresh tokens stored securely.
- **HTTPS Enforcement**: Strict Transport Security (HSTS) headers enabled on production.
- **Password Hashing**: Django's default `PBKDF2PasswordHasher` or `bcrypt` with work factor 12.
- **Security Middleware**: Django Security Middleware enforcing X-Content-Type-Options, X-Frame-Options (`DENY`), and Content Security Policy (CSP).
- **CSRF Protection**: CSRF tokens enforced on state-changing session calls.
- **CORS Control**: Explicit origin whitelisting avoiding wildcard (`*`) access in production.
- **Verification Systems**: Time-bound, cryptographically signed tokens for email verification and password resets.
- **Role-Based Access Control (RBAC)**: Fine-grained permission guards on every API endpoint.
- **Audit Logging**: Structured database logging of administrative overrides, shelter verification status changes, and sensitive profile edits.
- **Future Security Roadmap**: HTTP-only Secure Cookies for token storage, Rate Limiting via Redis (`django-ratelimit`).

---

## 13. Background Processing Architecture

```text
Client Application
       │
       │ (1) HTTP POST /api/v1/applications/
       ▼
Django REST API Service
       │
       ├─► (2) Synchronously commits application to PostgreSQL
       │
       │ (3) Enqueues async task: send_application_notice.delay(app_id)
       ▼
Redis Message Broker Queue
       │
       │ (4) Worker polls queued task payload
       ▼
Celery Worker Process
       │
       ├────────────► (5A) Email Gateway (Sends transactional email to Shelter)
       ├────────────► (5B) Cloudinary SDK (Processes & verifies attached PDF docs)
       ├────────────► (5C) Push Notification Service (Dispatches push to mobile/web)
       └────────────► (5D) Future AI Pipeline (Calculates initial compatibility vector)
```

### Workflow Execution Sequence

1. **Client Action**: User submits an adoption application via React client UI.
2. **Synchronous Handling**: Django REST API receives payload, validates fields, writes record to PostgreSQL, and immediately returns a `201 Created` HTTP response to the client (sub-100ms response time).
3. **Task Enqueueing**: Before returning HTTP response, Django pushes a lightweight Celery task message into Redis containing target IDs.
4. **Broker Queue Management**: Redis holds task messages in dedicated queues (`emails`, `media`, `default`).
5. **Worker Execution**: An idle Celery worker process dequeues the task, retrieves context, and handles third-party API integration (email dispatch, media compression, notification fanout) out-of-band without blocking user experience.

---

## 14. Folder Structure

The PawMatch backend codebase follows a modular Django app architecture:

```text
backend/
├── apps/                        # Pluggable Django Application Modules
│   ├── authentication/          # User auth, JWT token rotation, password resets
│   ├── users/                   # User profiles, RBAC roles, preferences
│   ├── shelters/                # Shelter registration, verification, profiles
│   ├── pets/                    # Pet catalog, listings, media models
│   ├── applications/            # Adoption application workflow state machine
│   ├── notifications/           # In-app notification center & email templates
│   └── analytics/               # System metrics, shelter reporting aggregations
│
├── config/                      # Project Configuration Root
│   ├── settings/                # Environment-specific settings modules
│   │   ├── __init__.py
│   │   ├── base.py              # Shared base configurations
│   │   ├── local.py             # Local development settings
│   │   └── production.py        # Production hardening settings
│   ├── asgi.py                  # ASGI entry point for async protocols
│   ├── celery.py                # Celery app initialization & configuration
│   ├── urls.py                  # Master URL routing table & OpenAPI mounts
│   └── wsgi.py                  # WSGI entry point for Gunicorn
│
├── common/                      # Shared Cross-Cutting Utilities
│   ├── constants.py             # Enums, status codes, global constants
│   ├── exceptions.py            # Custom DRF exception handler
│   ├── mixins.py                # Reusable model & viewset mixins (TimestampMixin)
│   ├── permissions.py           # Shared RBAC permission classes
│   └── utils.py                 # Helper functions (crypto, formatting)
│
├── media/                       # Local media development fallback directory
├── static/                      # Static assets gathered by collectstatic
├── templates/                   # HTML templates for transactional emails
├── requirements/                # Python Dependency Files
│   ├── base.txt                 # Core production dependencies
│   ├── local.txt                # Development dependencies (pytest, black, flake8)
│   └── production.txt           # Production server dependencies (gunicorn, gevent)
│
├── docs/                        # Project technical documentation
├── manage.py                    # Django CLI management entry point
└── README.md                    # Backend developer onboarding guide
```

---

## 15. Environment Strategy

PawMatch is designed using a strict **multi-environment architecture**. The project maintains three completely independent environments:

- **Development** (`dev`)
- **Staging** (`staging`)
- **Production** (`production`)

Each environment operates as an isolated execution domain with dedicated infrastructure, data stores, API keys, and credential vaults.

---

### 15.1 Environment Profiles

#### Development Environment
- **Purpose**: Local feature implementation, bug fixing, and rapid iteration by software engineers.
- **Characteristics**:
  - `DEBUG = True`
  - Local PostgreSQL instance (`localhost:5432/pawmatch_dev`)
  - Local Redis instance (`localhost:6379/0`)
  - Local Celery Worker process (`celery -A config worker --loglevel=debug`)
  - Isolated Development Cloudinary folder path (`/pawmatch/dev/`)
  - Local email backend (`django.core.mail.backends.console.EmailBackend`) or Mailtrap sandbox
  - Verbose logging (`DEBUG` log level enabled across all app loggers)
  - Dedicated local development secret keys (`SECRET_KEY = "dev-insecure-secret-key"`)
  - Instant Hot Reloading (Vite HMR on frontend, Django auto-reloader on backend)
  - Local interactive API documentation enabled (`/api/schema/swagger-ui/`)
- **Deployment Target**: Developer Local Machines.

---

#### Staging Environment
- **Purpose**: Quality Assurance (QA), User Acceptance Testing (UAT), feature validation, client demonstrations, and pre-production release candidate testing.
- **Characteristics**:
  - `DEBUG = False`
  - Independent Managed PostgreSQL database instance (`pawmatch_staging_db`)
  - Independent Managed Redis cluster (`pawmatch_staging_redis`)
  - Dedicated Staging Celery Worker service on Render
  - Isolated Staging Cloudinary folder path (`/pawmatch/staging/`)
  - Dedicated Staging Email SMTP Gateway (SendGrid / Mailgun test sandbox)
  - Full HTTPS/TLS encryption enabled
  - Production-equivalent configuration parameters (security middleware, CORS origin whitelisting)
  - Completely independent secrets vault
  - Test payment keys (Stripe test mode keys) and sandbox third-party API keys
- **Deployment Target**: Render Staging Cloud Web Services (`staging-api.pawmatch.com`).

---

#### Production Environment
- **Purpose**: Live platform supporting active pet adopters, animal shelters, veterinarians, and system administrators.
- **Characteristics**:
  - `DEBUG = False`
  - High-availability Production PostgreSQL database with automated continuous backups
  - High-availability Production Redis cluster
  - Dedicated Production Celery Worker and Celery Beat scheduler instances on Render
  - Isolated Production Cloudinary folder path (`/pawmatch/prod/`)
  - Enterprise Production Email Provider (SendGrid / AWS SES with dedicated IP warming)
  - Forced HTTPS Only (`SECURE_SSL_REDIRECT = True`, HSTS enabled)
  - Strict production security headers (X-Frame-Options `DENY`, CSP, X-Content-Type-Options)
  - Optimized structured JSON logging (`INFO` / `ERROR` levels)
  - Active application monitoring, performance telemetry, and automated error tracking
  - Automated continuous database backups with point-in-time recovery (PITR)
  - Production-grade cryptographically secure secrets
- **Deployment Target**: Render Production Cloud Services (`api.pawmatch.com`).

---

### 15.2 Environment Isolation Policy

To guarantee security compliance, eliminate cross-environment contamination, and prevent catastrophic accidental data loss, **every environment maintains 100% resource isolation**.

| Resource Component | Development Environment | Staging Environment | Production Environment |
| :--- | :--- | :--- | :--- |
| **Relational Database** | Local PostgreSQL (`pawmatch_dev`) | Render Staging PostgreSQL | Render Production PostgreSQL |
| **Message Broker / Cache** | Local Redis (`localhost:6379`) | Render Staging Redis | Render Production Redis |
| **Media Cloud Path** | Cloudinary `/pawmatch/dev/` | Cloudinary `/pawmatch/staging/` | Cloudinary `/pawmatch/prod/` |
| **Email Gateway** | Console / Mailtrap Sandbox | Test SMTP Sandbox Credentials | Production SMTP Provider |
| **API Keys & Secrets** | Development Secrets | Independent Staging Secrets | Production Vault Secrets |

#### Mandatory Isolation Principles
1. **Zero Resource Sharing**: No environment shall ever share a database, Redis cache instance, Cloudinary bucket folder, API key, or secret key with another environment under any circumstance.
2. **Data Leakage Prevention**: Production credentials must never exist on developer local machines or in staging environment definitions.
3. **Storage Namespace Isolation**: Cloudinary upload presets and folder paths are explicitly segmented per environment (`/dev/`, `/staging/`, `/prod/`).

---

### 15.3 Categorized Environment Variables

Environment variables are parsed via `python-decouple` and structured into standardized categories:

#### Django Framework Core
- `SECRET_KEY`: Cryptographic signing key.
- `DEBUG`: Boolean flag (`True` in Dev, `False` in Staging/Prod).
- `ALLOWED_HOSTS`: Comma-separated list of valid HTTP Host headers.

#### Database Settings
- `DATABASE_URL`: PostgreSQL connection string (`postgres://user:pass@host:5432/dbname`).

#### Redis Broker
- `REDIS_URL`: Redis connection URL (`redis://:password@host:6379/0`).

#### Celery Asynchronous Queue
- `CELERY_BROKER_URL`: Celery broker URI (typically matches `REDIS_URL`).
- `CELERY_RESULT_BACKEND`: Celery task result store URI.

#### Cloudinary Asset Management
- `CLOUDINARY_CLOUD_NAME`: Cloudinary cloud identifier.
- `CLOUDINARY_API_KEY`: API access key.
- `CLOUDINARY_API_SECRET`: Secret key for signing uploads.

#### Authentication & JWT
- `ACCESS_TOKEN_LIFETIME`: Access token expiry duration in minutes.
- `REFRESH_TOKEN_LIFETIME`: Refresh token expiry duration in days.
- `JWT_SIGNING_KEY`: Secret key used for signing JWT tokens.

#### Email Gateway
- `EMAIL_HOST`: SMTP server hostname.
- `EMAIL_PORT`: SMTP server port (587 for TLS).
- `EMAIL_HOST_USER`: SMTP account username / API key ID.
- `EMAIL_HOST_PASSWORD`: SMTP account password / API secret.
- `DEFAULT_FROM_EMAIL`: Sender address (`PawMatch <noreply@pawmatch.com>`).

#### Security & Headers
- `CSRF_TRUSTED_ORIGINS`: Comma-separated trusted origins for CSRF validation.
- `CORS_ALLOWED_ORIGINS`: Comma-separated allowed origins for cross-site requests.
- `SECURE_SSL_REDIRECT`: Boolean forcing HTTP to HTTPS redirect (`True` in Staging/Prod).

#### Monitoring & Observability
- `SENTRY_DSN`: Error tracking DSN URI (Future).
- `LOG_LEVEL`: Active logging threshold (`DEBUG`, `INFO`, `WARNING`, `ERROR`).

---

### 15.4 Configuration File Architecture

Django project settings are structured into modular configuration files within `config/settings/`:

```text
config/settings/
├── __init__.py          # Settings module entry point
├── base.py              # Shared base configurations (Apps, Middleware, DRF, Celery base)
├── development.py       # Development overrides (DEBUG=True, local DB/Redis, console email)
├── staging.py           # Staging overrides (DEBUG=False, test keys, staging cloud services)
└── production.py        # Production hardening (DEBUG=False, HSTS, secure headers, prod DB)
```

#### Settings File Responsibilities

- **`base.py`**: Defines core application modules (`INSTALLED_APPS`), shared middleware stacks, password validators, static file paths, DRF default settings, and JWT configurations common to all environments.
- **`development.py`**: Inherits from `base.py`. Enables `DEBUG=True`, configures local database/Redis connections, enables Django Debug Toolbar (optional), and sets email backend to console output.
- **`staging.py`**: Inherits from `base.py`. Enforces `DEBUG=False`, configures Staging database connection string from environment, sets up Staging Cloudinary folders, enables test SMTP credentials, and enforces SSL checks.
- **`production.py`**: Inherits from `base.py`. Enforces `DEBUG=False`, configures Production database pooling, enables WhiteNoise static file caching, configures production email providers, enforces strict HSTS / CSRF / CORS security headers, and configures production logging handlers.

---

### 15.5 Deployment Architecture

#### Development Infrastructure
```text
Developer Local Machine
       │
       ├─► Local Django Dev Server (http://127.0.0.1:8000)
       ├─► Local PostgreSQL Instance (localhost:5432/pawmatch_dev)
       ├─► Local Redis Instance (localhost:6379/0)
       ├─► Local Celery Worker Process
       └─► Cloudinary Development Folder (/pawmatch/dev/)
```

#### Staging Infrastructure
```text
Render Staging Web Service (staging-api.pawmatch.com)
       │
       ├─► Managed Render Staging PostgreSQL (pawmatch_staging_db)
       ├─► Managed Render Staging Redis (pawmatch_staging_redis)
       ├─► Render Staging Celery Worker Service
       └─► Cloudinary Staging Folder (/pawmatch/staging/)
```

#### Production Infrastructure
```text
Render Production Web Service (api.pawmatch.com)
       │
       ├─► High-Availability Managed Production PostgreSQL (pawmatch_prod_db)
       ├─► High-Availability Managed Production Redis (pawmatch_prod_redis)
       ├─► Dedicated Render Production Celery Worker & Beat Scheduler
       └─► Cloudinary Production Folder (/pawmatch/prod/)
```

---

### 15.6 Deployment Strategy & Git Workflow

PawMatch employs an automated, Git-branch-triggered continuous delivery workflow:

```text
feature/* branch  ──►  Pull Request  ──►  develop branch  ──►  Auto-Deploy ──► Development / Local QA
                                               │
                                               ▼
release/* branch  ──►  Pull Request  ──►  staging branch  ──►  Auto-Deploy ──► Staging Environment
                                               │
                                               ▼
                       Merge PR      ──►  main branch     ──►  Auto-Deploy ──► Production Environment
```

#### Git Branch & Environment Responsibilities

| Git Branch | Target Environment | Deployment Trigger | Primary Purpose |
| :--- | :--- | :--- | :--- |
| `feature/*` | Local Development | Manual local run | Feature development and unit testing by engineers. |
| `develop` | Development / QA | Automatic on push | Integration testing of merged features. |
| `staging` | Staging (UAT) | Automatic on push | Pre-release validation, UAT, client demo, and regression testing. |
| `main` | Production | Automatic on release merge | Customer-facing live application deployment. |

---

### 15.7 Data Protection & Security Policy

1. **Production Data Confidentiality**: Production database dumps, real user records, adoption application files, and real pet documents must **NEVER** be downloaded, copied, or stored on local Development machines.
2. **Staging Data Anonymization**: Production data must never be restored into Staging environments unless all Personally Identifiable Information (PII)—including names, emails, phone numbers, and physical addresses—is completely anonymized via automated sanitization scripts.
3. **Independent Secrets Management**: Every environment must utilize distinct, non-overlapping secret keys, JWT signing keys, and database passwords.
4. **Database & Cache Independence**: Every environment must connect to an independent relational database and Redis instance.
5. **Storage Path Isolation**: Every environment must store uploaded media in dedicated, isolated Cloudinary folders (`/dev/`, `/staging/`, `/prod/`).
6. **Backup Policy**: Automated daily backups and Point-In-Time Recovery (PITR) are mandatory for **Staging** and **Production** databases. Backups are disabled for local Development instances.

---

## 16. Coding Standards

### Python & Backend Standards
- **PEP 8 Compliance**: Code must strictly conform to PEP 8 formatting guidelines.
- **Code Formatter (Black)**: Automated formatting with standard 88-character line length limit.
- **Import Sorting (isort)**: Standardized import grouping (Standard Library ➔ Third-Party ➔ Local Django Apps).
- **Linter (flake8)**: Static analysis enforcing zero unused imports, undefined variables, or syntax issues.
- **Type Hints**: Mandatory Python type annotations on service layer functions, domain helpers, and utility methods.
- **Docstrings**: Google-style docstrings for non-trivial functions, classes, and DRF viewsets.
- **UUID Primary Keys**: Mandatory UUIDv4 primary key default for all new models.
- **Service Layer Pattern**: Heavy business logic extracted out of DRF Views and Django Models into dedicated service modules (`services.py`).

---

## 17. Scalability Strategy

The PawMatch technology stack is purposefully engineered to scale seamlessly across upcoming roadmap releases (V1.0 through V7.0):

- **Horizontal API Scaling**: Stateless Django REST API containers hosted on Render can scale horizontally behind load balancers to accommodate traffic surges.
- **Decoupled Background Queue**: Offloading notifications, email dispatches, and image transformations to Celery workers ensures API response latency remains sub-150ms regardless of platform load.
- **Read-Replica Database Scaling**: PostgreSQL supports read-replicas for handling heavy catalog search traffic as adoption volume scales.
- **Global CDN Caching**: Cloudinary CDN and Vercel Edge caching offload 95%+ of static media and frontend asset bandwidth away from core app servers.
- **Future Microservices Migration Path**: Clear app boundary separation (`apps/authentication`, `apps/pets`, `apps/applications`) enables individual modules to be split into independent microservices if traffic demands warrant in future enterprise phases.

---

## 18. Future Technologies

The following technologies are intentionally **deferred** to maintain focus during early product phases. They may be introduced in future enterprise versions via formal ADR approval:

- **Docker & Kubernetes**: Container orchestration deferred until multi-node deployment complexity requires container mesh management.
- **Terraform / Infrastructure-as-Code**: Deferred until multi-cloud infrastructure requirements emerge.
- **Apache Kafka / RabbitMQ**: Deferred in favor of Redis for Celery broker management due to Redis's simplicity and lower operational overhead.
- **GraphQL**: Deferred in favor of RESTful APIs + OpenAPI documentation to keep client integration simple and predictable.
- **WebSockets / Django Channels**: Deferred until real-time instant chat features are introduced in Community V5.0.
- **Sentry / Prometheus / Grafana / OpenTelemetry**: Enterprise monitoring suite deferred to V6.0 Enterprise milestone.

---

## 19. Technology Decision Records

| Technology | Decision | Primary Reason for Selection |
| :--- | :--- | :--- |
| **React 19** | **Chosen** | Global industry standard, component reusability, concurrent rendering capabilities. |
| **Vite** | **Chosen** | Instant HMR dev server and optimized Rollup build bundler replacing slow legacy build tools. |
| **Tailwind CSS** | **Chosen** | Rapid UI development, responsive utilities, and enforced visual design consistency. |
| **Python 3.13+** | **Chosen** | High developer productivity, top-tier AI/ML library support, excellent asynchronous engine. |
| **Django 5.x + DRF** | **Chosen** | Battery-included framework providing robust ORM, security middleware, and rapid REST API generation. |
| **PostgreSQL 17** | **Chosen** | Unmatched relational reliability, strict ACID compliance, and rich JSONB document support. |
| **Cloudinary** | **Chosen** | Automated image compression, dynamic thumbnail transformations, and integrated global CDN. |
| **Redis** | **Chosen** | Ultra-fast in-memory performance for Celery message brokerage and caching capabilities. |
| **Celery** | **Chosen** | Robust, scalable asynchronous background task execution and job scheduling. |
| **Render** | **Chosen** | Frictionless PaaS deployment for Django web services, background workers, and managed databases. |
| **Vercel** | **Chosen** | Industry-leading edge hosting platform optimized for React Single Page Applications. |

---

## 20. Version Compatibility

| Technology / Library | Minimum Supported Version | Recommended Version |
| :--- | :--- | :--- |
| **Python** | `3.13.0` | `3.13.x` |
| **Django** | `5.1.0` | `5.1.x` |
| **Django REST Framework** | `3.15.0` | `3.15.x` |
| **DRF Simple JWT** | `5.3.0` | `5.3.x` |
| **drf-spectacular** | `0.28.0` | `0.28.x` |
| **PostgreSQL** | `17.0` | `17.x` |
| **Redis** | `7.2.0` | `7.4.x` |
| **Celery** | `5.4.0` | `5.4.x` |
| **React** | `19.0.0` | `19.x` |
| **Vite** | `6.0.0` | `6.x` |
| **Tailwind CSS** | `3.4.0` | `3.4.x / 4.x` |
| **Cloudinary Python SDK** | `1.41.0` | `1.41.x` |

---

## 21. Documentation Hierarchy & Structure

To maintain clean documentation architecture across the PawMatch ecosystem, all project documentation must be organized according to the following official directory structure:

```text
docs/
│
├── architecture/                 # System Architecture & Technical Specifications
│   ├── PRODUCT_ROADMAP.md        # Product release roadmap (V1.0 - V7.0)
│   ├── TECHNOLOGY_STACK.md       # Official approved technology stack specification
│   ├── SYSTEM_ARCHITECTURE.md    # High-level architecture & component interaction diagrams
│   ├── DATABASE_SCHEMA.md        # Relational schema ERDs, table dictionaries & indexes
│   ├── API_SPECIFICATION_V1.md   # OpenAPI / REST endpoint specifications
│   ├── AUTHENTICATION.md         # JWT authentication flow & token lifecycle
│   ├── RBAC.md                   # Role-Based Access Control matrix & permissions
│   ├── ERROR_CODES.md            # Standardized API error code dictionary
│   ├── VERSIONING.md             # API & semantic versioning policy
│   └── DEPLOYMENT.md             # Infrastructure & deployment setup guide
│
├── adr/                          # Architectural Decision Records (ADRs)
│   ├── ADR-001-Choose-Django.md
│   ├── ADR-002-Use-UUIDs.md
│   ├── ADR-003-Cloudinary.md
│   ├── ADR-004-Celery-and-Redis.md
│   ├── ADR-005-Render-Deployment.md
│   └── ADR-006-PostgreSQL.md
│
├── development/                  # Developer Onboarding & Engineering Standards
│   ├── BACKEND_GUIDELINES.md     # Django & Python best practices
│   ├── FRONTEND_GUIDELINES.md    # React & Tailwind engineering guidelines
│   ├── CODING_STANDARDS.md       # PEP 8, Black, ESLint, type hint rules
│   ├── GIT_WORKFLOW.md           # Git branching policy, commit naming & PR template
│   └── CONTRIBUTING.md           # Contributor code of conduct & setup guide
│
├── ai/                           # AI Coding Agent Rules & Context Specifications
│   ├── AI_DEVELOPMENT_RULES.md   # Guardrails & rules for AI coding agents
│   ├── PROMPT_GUIDELINES.md      # Recommended prompts & context instructions
│   ├── CONTEXT.md                # System context map for LLM workspace injection
│   └── AI_WORKFLOW.md            # Workflow instructions for autonomous coding tasks
│
├── api/                          # Executable API Collections & OpenAPI Specs
│   ├── POSTMAN_COLLECTION.json   # Postman collection for manual API testing
│   ├── BRUNO_COLLECTION/         # Bruno API test collection directory
│   ├── OPENAPI.yaml              # Exported OpenAPI 3.0 YAML specification
│   └── API_CHANGELOG.md          # History of API route changes and deprecations
│
├── deployment/                   # Cloud Provider Setup & Configuration Guides
│   ├── RENDER.md                 # Render backend & worker configuration instructions
│   ├── VERCEL.md                 # Vercel frontend deployment settings
│   ├── CLOUDINARY.md             # Cloudinary account & upload preset setup
│   ├── REDIS.md                  # Managed Redis instance configuration
│   ├── CELERY.md                 # Celery worker process daemon setup
│   └── ENVIRONMENT_VARIABLES.md  # Master list of required environment variables
│
├── testing/                      # QA & Automated Testing Specifications
│   ├── TESTING_STRATEGY.md       # Overall testing methodology (Unit, Integration, E2E)
│   ├── UNIT_TESTS.md             # Backend pytest & React Vitest unit guidelines
│   ├── INTEGRATION_TESTS.md      # API integration test suite specifications
│   ├── API_TESTING.md            # Automated Postman / Newman test collections
│   └── PERFORMANCE_TESTING.md    # Locust load testing specifications
│
└── assets/                       # Diagram Sources & Visual Media
    ├── diagrams/                 # Editable Mermaid, Draw.io & PlantUML diagram sources
    ├── images/                   # Screenshots & architectural flowcharts
    └── screenshots/              # Application UI walkthrough screenshots
```

### Documentation Directory Management Protocol

- **`architecture/`**: Maintained by Lead Architects. Contains high-level blueprints. AI agents must consult these files before implementing new modules.
- **`adr/`**: Maintained by Core Engineering Team. Captures historical context behind architectural decisions. Every tech stack change requires a new numbered ADR file.
- **`development/`**: Maintained by Engineering Leads. Onboarding guides and code formatting rules for human developers and AI assistants.
- **`ai/`**: Maintained by AI Operations Team. Defines boundaries, context maps, and execution rules specifically tailored for AI coding agents.
- **`api/`**: Maintained by API Developers. Contains executable Postman/Bruno test suites and OpenAPI definitions synced with backend releases.
- **`deployment/`**: Maintained by DevOps Engineers. Step-by-step infrastructure provisioning instructions.
- **`testing/`**: Maintained by QA Team. Testing standards and coverage thresholds.

---

## 22. Conclusion

The **PawMatch Technology Stack Specification** serves as the definitive technical contract governing all software development within the PawMatch ecosystem.

By adhering to this specification:
- **Developers** maintain high velocity, clean architecture, and seamless code reviews.
- **AI Coding Agents** operate within strict architectural guardrails, preventing unintended dependency sprawl or technical debt.
- **PawMatch Ecosystem** achieves high performance, robust security, strict reliability, and effortless scalability from V1.0 Foundation through V7.0 Future AI releases.

This document is the official technology reference for PawMatch. All contributors must adhere to these specifications unless superseded by a formally approved Architectural Decision Record (ADR).
