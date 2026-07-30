# PawMatch Backend File Structure

This document outlines the file tree and directory structure of the **PawMatch** Django backend.

---

## 1. Directory File Tree

```text
backend/
├── .dockerignore
├── .env
├── .env.development
├── .env.example
├── .env.production
├── .env.staging
├── .gitignore
├── Dockerfile
├── README.md
├── build.sh
├── docker-compose.yml
├── filestructure.md
├── gunicorn.conf.py
├── manage.py
├── render.yaml
├── apps/
│   ├── __init__.py
│   ├── accounts/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── selectors/
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   └── __init__.py
│   │   └── tests/
│   │       └── __init__.py
│   ├── administration/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── selectors/
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   └── __init__.py
│   │   └── tests/
│   │       └── __init__.py
│   ├── adoptions/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── selectors/
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   └── __init__.py
│   │   └── tests/
│   │       └── __init__.py
│   ├── audit_logs/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── selectors/
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   └── __init__.py
│   │   └── tests/
│   │       └── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── choices.py
│   │   ├── exceptions.py
│   │   ├── mixins.py
│   │   ├── models.py
│   │   ├── pagination.py
│   │   ├── permissions.py
│   │   ├── signals.py
│   │   ├── utils.py
│   │   ├── validators.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── selectors/
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   └── __init__.py
│   │   └── tests/
│   │       └── __init__.py
│   ├── notifications/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── selectors/
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   └── __init__.py
│   │   └── tests/
│   │       └── __init__.py
│   ├── pets/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── selectors/
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   └── __init__.py
│   │   └── tests/
│   │       └── __init__.py
│   └── shelters/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── serializers.py
│       │   ├── urls.py
│       │   └── views.py
│       ├── migrations/
│       │   └── __init__.py
│       ├── selectors/
│       │   └── __init__.py
│       ├── services/
│       │   └── __init__.py
│       └── tests/
│           └── __init__.py
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── urls.py
│   │   ├── versioning.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── urls.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── development.py
│       ├── logging.py
│       ├── production.py
│       └── staging.py
└── requirements/
    ├── base.txt
    ├── development.txt
    ├── production.txt
    └── testing.txt
```

---

## 2. Infrastructure & Deployment Files

- **`Dockerfile`**: Multi-stage production container build configuration for OCI compliance.
- **`.dockerignore`**: Excludes caches, virtual environments, logs, and sensitive `.env` files from Docker context.
- **`gunicorn.conf.py`**: Production WSGI server configuration.
- **`build.sh`**: Render deployment script executing static collection and database migrations (`set -o errexit`).
- **`render.yaml`**: Infrastructure-as-Code specification for Render Blueprint deployments.
- **`docker-compose.yml`**: Development orchestration for running backend container locally with expansion slots for Redis and PostgreSQL.
- **`README.md`**: Comprehensive developer and deployment onboarding guide.
