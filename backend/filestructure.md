# PawMatch Backend File Structure

This document outlines the file tree and directory structure of the **PawMatch** Django backend.

---

## 1. Directory File Tree

```text
backend/
├── .env
├── .env.development
├── .env.example
├── .env.production
├── .env.staging
├── .gitignore
├── filestructure.md
├── manage.py
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

## 2. Directory & Module Details

### Root Environment Files
- **`.env`**: Active local environment file.
- **`.env.example`**: Template environment variable file.
- **`.env.development`**: Environment settings for local development.
- **`.env.staging`**: Pre-production staging configuration.
- **`.env.production`**: Hardened production environment configuration.
- **`manage.py`**: Django CLI management entry point.
- **`.gitignore`**: Version control rules.

---

### `requirements/` (Dependency Modularization)
- **`base.txt`**: Production core packages (Django, DRF, django-environ, dj-database-url, psycopg, whitenoise, Pillow, drf-spectacular, djangorestframework-simplejwt).
- **`development.txt`**: Extends `base.txt` with dev tools (pytest, flake8, black, isort).
- **`production.txt`**: Extends `base.txt` with Gunicorn WSGI server.
- **`testing.txt`**: Extends `base.txt` with test runners and coverage tools.

---

### `config/` (Settings & Router)
- **`settings/`**:
  - `base.py`: Multi-environment decoupled configuration.
  - `development.py`: Development overrides (`DEBUG=True`, console email, SQLite fallback).
  - `staging.py`: Staging security defaults and logging.
  - `production.py`: Hardened production security, HSTS, SSL, WhiteNoise storage.
  - `logging.py`: Centralized logging configuration dictionary.
- **`api/`**: Central API Gateway and v1 route aggregators.

---

### `apps/core/` (Infrastructure Base Modules)
- **`choices.py`**: Common choice enums (`UserRole`, `PetSpecies`, `PetStatus`, `ApplicationStatus`).
- **`exceptions.py`**: Custom DRF error response standardizer.
- **`mixins.py`**: Abstract model mixins (`UUIDModel`, `TimestampedModel`, `SoftDeleteModel`).
- **`pagination.py`**: Standardized pagination classes.
- **`permissions.py`**: Core RBAC permission guards.
- **`signals.py`**: Infrastructure signal definitions.
- **`utils.py`**: Infrastructure helper functions.
- **`validators.py`**: Input validation functions (phone numbers, file sizes).
