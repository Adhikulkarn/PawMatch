# PawMatch Backend — Infrastructure & Deployment Guide

This directory contains the production-grade, cloud-agnostic containerized setup for the **PawMatch** Django REST API backend.

---

## 1. Environment Architecture & Database Setup

The backend uses dynamic environment resolution (`django-environ`) configured in `config/settings/base.py`:

- **Development**: Reads `.env.development` when `DJANGO_SETTINGS_MODULE=config.settings.development` (Development Neon PostgreSQL / local SQLite).
- **Staging**: Reads `.env.staging` when `DJANGO_SETTINGS_MODULE=config.settings.staging`.
- **Production**: Reads `.env.production` or Render environment vault when `DJANGO_SETTINGS_MODULE=config.settings.production`.

### Local Execution Commands

```bash
# Run Django Development System Checks
python manage.py check --settings=config.settings.development

# Run Development Migrations
python manage.py migrate --settings=config.settings.development

# Run Development Server
python manage.py runserver --settings=config.settings.development
```

---

## 2. Local Containerization & Docker Setup

### Build Docker Image
```bash
docker build -t pawmatch-backend:latest .
```

### Run Multi-Service Compose Stack
```bash
# Start backend container
docker compose up -d

# View container telemetry logs
docker compose logs -f backend

# Stop container stack
docker compose down
```

The containerized API will be accessible at `http://localhost:8000`.  
Health check probe: `http://localhost:8000/health/`

---

## 3. Render Cloud Deployment (Docker Runtime)

PawMatch is configured for zero-friction deployment on **Render** using Docker runtime.

### Step-by-Step Deployment Instructions
1. **Push Repository**: Ensure latest code is pushed to GitHub.
2. **Connect Render Blueprint**:
   - Log in to the [Render Dashboard](https://dashboard.render.com/).
   - Click **New +** ➔ **Blueprint**.
   - Connect your `PawMatch` GitHub repository.
   - Render automatically detects `render.yaml` and executes `build.sh`.

### Render Environment Variables

| Variable | Required | Value / Sample | Description |
| :--- | :---: | :--- | :--- |
| `DJANGO_SETTINGS_MODULE` | Yes | `config.settings.production` | Django settings entry point |
| `SECRET_KEY` | Yes | *[Auto-Generated Secret]* | Cryptographic key |
| `DATABASE_URL` | Yes | `postgres://user:pass@ep-neon.cloud/pawmatch` | Production Neon PostgreSQL URI |
| `REDIS_URL` | Optional | `redis://:pass@redis-host:6379/0` | Cache and Celery message broker |
| `ALLOWED_HOSTS` | Yes | `.onrender.com,api.pawmatch.com` | Allowed host origins |
| `CORS_ALLOWED_ORIGINS` | Yes | `https://pawmatch.com` | Allowed CORS origins for frontend |
| `SECURE_SSL_REDIRECT` | Yes | `true` | Forces HTTPS redirection |
| `LOG_LEVEL` | No | `INFO` | Logging severity threshold |
| `LOG_FORMAT` | No | `json` | Structured JSON log output |

---

## 4. Telemetry, Tracing & Health Probes

- **Health Probe**: `GET /health/`
  ```json
  {
      "status": "healthy",
      "service": "pawmatch-backend",
      "version": "1.0.0",
      "environment": "development",
      "timestamp": "2026-07-30T07:06:05.016125+00:00"
  }
  ```
  - **Latency:** Sub-millisecond execution time (`0.328 ms`), zero database queries.
- **Distributed Tracing**: `RequestIDMiddleware` injects a unique UUIDv4 into `X-Request-ID` HTTP response headers and trace logs.
- **Structured JSON Logging**: Outputs ISO 8601 UTC JSON payloads formatted for Render, CloudWatch, Loki, and ELK Stack.

---

## 5. Automated CI/CD Pipeline

The GitHub Actions workflow [`.github/workflows/backend.yml`](file:///home/spidy/Desktop/projects/PawMatch/.github/workflows/backend.yml) automatically runs on push/PR to `main`, `staging`, or `develop`:

1. **Formatting**: `isort --profile black --check .` and `black --check .`
2. **Linting**: `flake8 .`
3. **Django Checks**: `manage.py check` (Dev & Prod mode)
4. **Unit Tests**: `pytest`
5. **Docker Container Build**: Builds multi-stage Docker image (no registry push).
