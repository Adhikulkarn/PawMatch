# Render Deployment Specification

```text
Document ID:     DEPLOYMENT-RENDER
Status:          Approved Specification
Version:         1.1
Document Owner:  PawMatch Architecture & Engineering Team
Last Updated:    July 30, 2026
```

---

## 1. Overview & Architecture

PawMatch backend is deployed on **Render** using the **Docker Runtime**. Render hosts the Gunicorn WSGI application service, connects to a managed Neon PostgreSQL database cluster, and processes background jobs.

---

## 2. Infrastructure-as-Code (`render.yaml`)

Render deployments are driven by the repository Blueprint specification:

```yaml
services:
  - type: web
    name: pawmatch-backend
    runtime: docker
    dockerfilePath: backend/Dockerfile
    dockerContext: backend
    plan: starter
    region: oregon
    branch: main
    autoDeploy: true
    healthCheckPath: /health/
    envVars:
      - key: DJANGO_SETTINGS_MODULE
        value: config.settings.production
      - key: PYTHONUNBUFFERED
        value: "1"
      - key: PYTHONDONTWRITEBYTECODE
        value: "1"
      - key: PYTHONFAULTHANDLER
        value: "1"
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        sync: false
      - key: REDIS_URL
        sync: false
      - key: ALLOWED_HOSTS
        value: ".onrender.com"
      - key: CORS_ALLOWED_ORIGINS
        sync: false
      - key: CSRF_TRUSTED_ORIGINS
        sync: false
      - key: SECURE_SSL_REDIRECT
        value: "true"
      - key: GUNICORN_WORKERS
        value: "2"
      - key: GUNICORN_THREADS
        value: "4"
      - key: GUNICORN_TIMEOUT
        value: "60"
      - key: GUNICORN_GRACEFUL_TIMEOUT
        value: "30"
      - key: LOG_LEVEL
        value: "INFO"
      - key: LOG_FORMAT
        value: "json"
```

---

## 3. Hardened Build Script (`build.sh`)

Render build execution uses a hardened Bash script:

- **Strict Flags**: Enforces `set -o errexit`, `set -o pipefail`, `set -o nounset`.
- **Error Trapping**: Traps failure events (`trap ... ERR`) with line numbers for Render log telemetry.
- **Pipeline Execution**:
  1. Upgrades `pip`.
  2. Installs production dependencies (`requirements/production.txt`).
  3. Executes `python manage.py check --deploy`.
  4. Collects static assets (`python manage.py collectstatic --noinput --clear`).
  5. Executes database migrations (`python manage.py migrate --noinput`).

---

## 4. Health Probes & Zero-Downtime Deploys

- **Health Endpoint**: `GET /health/`
  - Returns `{"status": "healthy", "service": "pawmatch-backend", "version": "...", "environment": "production", "timestamp": "..."}`.
  - Zero database queries, execution latency `< 1 ms`.
- **Zero-Downtime Deploys**: Render waits for the container health check probe to return HTTP 200 before swapping old web service instances with new ones.
