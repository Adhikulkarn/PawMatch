# PawMatch — Pet Adoption & Health Ecosystem

[![Backend CI](https://github.com/Adhikulkarn/PawMatch/actions/workflows/backend.yml/badge.svg)](https://github.com/Adhikulkarn/PawMatch/actions/workflows/backend.yml)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Django 5.x](https://img.shields.io/badge/django-5.x-green.svg)](https://www.djangoproject.com/)
[![Docker OCI](https://img.shields.io/badge/docker-multi--stage-blue.svg)](https://www.docker.com/)
[![Render Deployment](https://img.shields.io/badge/deployment-render-purple.svg)](https://render.com/)

PawMatch is an enterprise-grade pet adoption, shelter management, and animal healthcare platform built on Python 3.13+, Django 5.x REST Framework, PostgreSQL 17 (Neon), Redis, and React 19.

---

## 🌟 Key Architecture & Completed Infrastructure

- **Domain-Driven Modular Structure**: Decoupled Django apps (`apps/core/`, `accounts/`, `shelters/`, `pets/`, `adoptions/`, `notifications/`, `administration/`, `audit_logs/`).
- **Multi-Environment Settings**: Dynamic `.env.<environment>` resolution for Development, Staging, and Production (`config/settings/`).
- **Production Dockerization**: Multi-stage OCI `Dockerfile`, non-root execution (`USER 10001:10001`), layer caching.
- **Render PaaS Deployment**: Infrastructure-as-Code blueprint (`render.yaml`) & hardened deployment script (`build.sh`).
- **Telemetry & Tracing**: Sub-millisecond `/health/` endpoint (`0.328 ms`), `X-Request-ID` distributed tracing middleware, ISO 8601 UTC JSON structured logging.
- **CI/CD Pipeline**: GitHub Actions workflow (`.github/workflows/backend.yml`) enforcing Black, isort, Flake8, Django checks, pytest, and Docker builds.

---

## 🚀 Quick Start (Development & Local Docker)

### 1. Local Python Virtual Environment Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/development.txt
python manage.py migrate --settings=config.settings.development
python manage.py runserver --settings=config.settings.development
```

### 2. Local Docker Compose Stack

```bash
docker compose up -d --build
```
Access the health check endpoint at `http://localhost:8000/health/`.

---

## 📚 Technical Documentation & Knowledge Base

- **Master Knowledge Base**: [`docs/README.md`](file:///home/spidy/Desktop/projects/PawMatch/docs/README.md)
- **Backend Architecture & Guidelines**: [`backend/README.md`](file:///home/spidy/Desktop/projects/PawMatch/backend/README.md)
- **Directory Tree & File Map**: [`backend/filestructure.md`](file:///home/spidy/Desktop/projects/PawMatch/backend/filestructure.md)
- **Environment Variables Catalog**: [`docs/deployment/ENVIRONMENT_VARIABLES.md`](file:///home/spidy/Desktop/projects/PawMatch/docs/deployment/ENVIRONMENT_VARIABLES.md)
- **Render Deployment Blueprint**: [`docs/deployment/RENDER.md`](file:///home/spidy/Desktop/projects/PawMatch/docs/deployment/RENDER.md)
