# PawMatch File Structure

```text
PawMatch/
├── .github/
│   └── workflows/
│       └── backend.yml
├── backend/
│   ├── apps/
│   │   ├── accounts/
│   │   │   ├── api/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── serializers.py
│   │   │   │   ├── urls.py
│   │   │   │   └── views.py
│   │   │   ├── documentation/
│   │   │   │   └── rbac_swagger.py
│   │   │   ├── management/
│   │   │   │   └── commands/
│   │   │   │       └── sync_rbac.py
│   │   │   ├── migrations/
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── profile.py
│   │   │   │   ├── rbac.py
│   │   │   │   └── user.py
│   │   │   ├── policies/
│   │   │   │   └── __init__.py
│   │   │   ├── selectors/
│   │   │   │   └── __init__.py
│   │   │   ├── services/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth_service.py
│   │   │   │   ├── password_service.py
│   │   │   │   ├── profile_service.py
│   │   │   │   ├── registration_service.py
│   │   │   │   └── role_service.py
│   │   │   ├── templates/
│   │   │   │   └── emails/
│   │   │   │       ├── password_reset.html
│   │   │   │       ├── password_reset.txt
│   │   │   │       ├── verification.html
│   │   │   │       └── verification.txt
│   │   │   ├── tests/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── test_authentication.py
│   │   │   │   ├── test_authorization.py
│   │   │   │   ├── test_drf_integration.py
│   │   │   │   ├── test_models.py
│   │   │   │   ├── test_password.py
│   │   │   │   ├── test_profile.py
│   │   │   │   ├── test_rbac_admin_tooling.py
│   │   │   │   ├── test_rbac_api.py
│   │   │   │   ├── test_rbac_e2e.py
│   │   │   │   ├── test_rbac_events_logging.py
│   │   │   │   ├── test_rbac_sync.py
│   │   │   │   ├── test_registration.py
│   │   │   │   └── test_role_service.py
│   │   │   ├── validators/
│   │   │   │   └── __init__.py
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── auth_decorators.py
│   │   │   ├── config.py
│   │   │   ├── constants.py
│   │   │   ├── events.py
│   │   │   ├── exceptions.py
│   │   │   ├── managers.py
│   │   │   ├── permissions.py
│   │   │   ├── permissions_drf.py
│   │   │   ├── role_permissions.py
│   │   │   ├── roles.py
│   │   │   ├── signals.py
│   │   │   ├── throttles.py
│   │   │   └── utils.py
│   │   ├── administration/
│   │   │   ├── api/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── serializers.py
│   │   │   │   ├── urls.py
│   │   │   │   └── views.py
│   │   │   ├── migrations/
│   │   │   ├── selectors/
│   │   │   ├── services/
│   │   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   └── models.py
│   │   ├── adoptions/
│   │   │   ├── api/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── serializers.py
│   │   │   │   ├── urls.py
│   │   │   │   └── views.py
│   │   │   ├── migrations/
│   │   │   ├── selectors/
│   │   │   ├── services/
│   │   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   └── models.py
│   │   ├── audit_logs/
│   │   │   ├── api/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── serializers.py
│   │   │   │   ├── urls.py
│   │   │   │   └── views.py
│   │   │   ├── migrations/
│   │   │   ├── selectors/
│   │   │   ├── services/
│   │   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   └── models.py
│   │   ├── core/
│   │   │   ├── api/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── serializers.py
│   │   │   │   ├── urls.py
│   │   │   │   └── views.py
│   │   │   ├── migrations/
│   │   │   ├── selectors/
│   │   │   ├── services/
│   │   │   ├── tests/
│   │   │   │   ├── __init__.py
│   │   │   │   └── test_health.py
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── choices.py
│   │   │   ├── exceptions.py
│   │   │   ├── middleware.py
│   │   │   ├── mixins.py
│   │   │   ├── models.py
│   │   │   ├── pagination.py
│   │   │   ├── permissions.py
│   │   │   ├── responses.py
│   │   │   ├── signals.py
│   │   │   ├── utils.py
│   │   │   └── validators.py
│   │   ├── notifications/
│   │   │   ├── api/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── serializers.py
│   │   │   │   ├── urls.py
│   │   │   │   └── views.py
│   │   │   ├── migrations/
│   │   │   ├── selectors/
│   │   │   ├── services/
│   │   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   └── models.py
│   │   ├── pets/
│   │   │   ├── api/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── serializers.py
│   │   │   │   ├── urls.py
│   │   │   │   └── views.py
│   │   │   ├── migrations/
│   │   │   ├── selectors/
│   │   │   ├── services/
│   │   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   └── models.py
│   │   ├── shelters/
│   │   │   ├── api/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── serializers.py
│   │   │   │   ├── urls.py
│   │   │   │   └── views.py
│   │   │   ├── migrations/
│   │   │   │   ├── __init__.py
│   │   │   │   └── 0001_initial.py
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── document.py
│   │   │   │   ├── invitation.py
│   │   │   │   ├── member.py
│   │   │   │   ├── shelter.py
│   │   │   │   └── verification.py
│   │   │   ├── selectors/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── invitation_selector.py
│   │   │   │   ├── member_selector.py
│   │   │   │   ├── shelter_selector.py
│   │   │   │   └── verification_selector.py
│   │   │   ├── services/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── invitation_service.py
│   │   │   │   ├── member_service.py
│   │   │   │   ├── shelter_service.py
│   │   │   │   └── verification_service.py
│   │   │   ├── tests/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── test_document_model.py
│   │   │   │   ├── test_invitation_model.py
│   │   │   │   ├── test_invitation_service.py
│   │   │   │   ├── test_member_model.py
│   │   │   │   ├── test_member_service.py
│   │   │   │   ├── test_shelter_model.py
│   │   │   │   ├── test_shelter_service.py
│   │   │   │   ├── test_verification_model.py
│   │   │   │   └── test_verification_service.py
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── constants.py
│   │   │   ├── exceptions.py
│   │   │   ├── permissions.py
│   │   │   ├── signals.py
│   │   │   └── validators.py
│   │   └── __init__.py
│   ├── config/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   └── urls.py
│   │   │   ├── __init__.py
│   │   │   ├── urls.py
│   │   │   └── versioning.py
│   │   ├── settings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   ├── logging.py
│   │   │   ├── production.py
│   │   │   └── staging.py
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── requirements/
│   │   ├── base.txt
│   │   ├── development.txt
│   │   ├── production.txt
│   │   └── testing.txt
│   ├── .dockerignore
│   ├── .gitignore
│   ├── Dockerfile
│   ├── README.md
│   ├── build.sh
│   ├── docker-compose.yml
│   ├── filestructure.md
│   ├── gunicorn.conf.py
│   ├── manage.py
│   ├── pyproject.toml
│   └── render.yaml
├── docs/
│   ├── adr/
│   │   ├── ADR-001-Choose-Django.md
│   │   ├── ADR-002-Use-UUIDs.md
│   │   ├── ADR-003-Choose-PostgreSQL.md
│   │   ├── ADR-004-Cloudinary.md
│   │   ├── ADR-005-Celery-Redis.md
│   │   ├── ADR-006-Render.md
│   │   ├── ADR-007-Vercel.md
│   │   ├── ADR-008-JWT.md
│   │   └── README.md
│   ├── ai/
│   │   ├── AI_CONTEXT.md
│   │   ├── AI_DEVELOPMENT_RULES.md
│   │   ├── AI_LIMITATIONS.md
│   │   ├── AI_WORKFLOW.md
│   │   ├── CODING_CONVENTIONS.md
│   │   ├── PROMPT_GUIDELINES.md
│   │   └── README.md
│   ├── api/
│   │   ├── API_CHANGELOG.md
│   │   ├── BRUNO.md
│   │   ├── FILTERING.md
│   │   ├── OPENAPI.md
│   │   ├── PAGINATION.md
│   │   ├── POSTMAN.md
│   │   ├── RATE_LIMITING.md
│   │   ├── README.md
│   │   └── REQUEST_RESPONSE_STANDARDS.md
│   ├── architecture/
│   │   ├── API_SPECIFICATION_V1.md
│   │   ├── AUTH_ARCHITECTURE.md
│   │   ├── AUTHENTICATION_FLOW.md
│   │   ├── AUTHENTICATION.md
│   │   ├── AUTHORIZATION_ARCHITECTURE.md
│   │   ├── DATABASE_SCHEMA.md
│   │   ├── DEPLOYMENT_ARCHITECTURE.md
│   │   ├── ERROR_CODES.md
│   │   ├── MEDIA_STORAGE.md
│   │   ├── PASSWORD_MANAGEMENT.md
│   │   ├── PRODUCT_ROADMAP.md
│   │   ├── PROFILE_MANAGEMENT.md
│   │   ├── RBAC_MANAGEMENT.md
│   │   ├── RBAC.md
│   │   ├── README.md
│   │   ├── REGISTRATION_FLOW.md
│   │   ├── SECURITY_ARCHITECTURE.md
│   │   ├── SYSTEM_ARCHITECTURE.md
│   │   ├── TECHNOLOGY_STACK.md
│   │   └── VERSIONING.md
│   ├── backend/
│   │   ├── CELERY.md
│   │   ├── CLOUDINARY.md
│   │   ├── DJANGO_GUIDELINES.md
│   │   ├── LOGGING.md
│   │   ├── MODEL_GUIDELINES.md
│   │   ├── PROJECT_STRUCTURE.md
│   │   ├── README.md
│   │   ├── REDIS.md
│   │   ├── SERIALIZER_GUIDELINES.md
│   │   ├── SERVICE_LAYER.md
│   │   ├── SIGNALS.md
│   │   ├── TESTING.md
│   │   └── VIEWSET_GUIDELINES.md
│   ├── deployment/
│   │   ├── BACKUP_STRATEGY.md
│   │   ├── CLOUDINARY.md
│   │   ├── DEVELOPMENT.md
│   │   ├── DISASTER_RECOVERY.md
│   │   ├── ENVIRONMENT_VARIABLES.md
│   │   ├── POSTGRESQL.md
│   │   ├── PRODUCTION.md
│   │   ├── README.md
│   │   ├── REDIS.md
│   │   ├── RENDER.md
│   │   ├── STAGING.md
│   │   └── VERCEL.md
│   ├── development/
│   │   ├── BRANCHING_STRATEGY.md
│   │   ├── CODE_REVIEW.md
│   │   ├── CODING_STANDARDS.md
│   │   ├── COMMIT_CONVENTION.md
│   │   ├── CONTRIBUTING.md
│   │   ├── GIT_WORKFLOW.md
│   │   ├── README.md
│   │   └── RELEASE_PROCESS.md
│   ├── frontend/
│   │   ├── API_INTEGRATION.md
│   │   ├── COMPONENT_GUIDELINES.md
│   │   ├── FORM_GUIDELINES.md
│   │   ├── PROJECT_STRUCTURE.md
│   │   ├── README.md
│   │   ├── ROUTING.md
│   │   ├── STATE_MANAGEMENT.md
│   │   └── UI_STANDARDS.md
│   ├── security/
│   │   ├── AUDIT_LOGS.md
│   │   ├── AUTHENTICATION.md
│   │   ├── AUTHORIZATION.md
│   │   ├── DATA_PROTECTION.md
│   │   ├── JWT_POLICY.md
│   │   ├── PASSWORD_POLICY.md
│   │   ├── README.md
│   │   └── SECURITY_HEADERS.md
│   ├── testing/
│   │   ├── API_TESTING.md
│   │   ├── INTEGRATION_TESTS.md
│   │   ├── PERFORMANCE_TESTING.md
│   │   ├── README.md
│   │   ├── SECURITY_TESTING.md
│   │   ├── TESTING_STRATEGY.md
│   │   └── UNIT_TESTS.md
│   ├── PawMatch_AI_Functional_Requirements_Specification.md
│   ├── PRODUCT_ROADMAP.md
│   ├── README.md
│   ├── TECHNOLOGY_STACK.md
│   └── VERSION_1_FOUNDATION.md
├── frontend/
│   └── PawMatch/
│       ├── public/
│       │   ├── favicon.svg
│       │   └── icons.svg
│       ├── src/
│       │   ├── assets/
│       │   │   ├── hero.png
│       │   │   ├── react.svg
│       │   │   └── vite.svg
│       │   ├── App.css
│       │   ├── App.jsx
│       │   ├── index.css
│       │   └── main.jsx
│       ├── index.html
│       ├── package.json
│       ├── README.md
│       └── vite.config.js
├── .gitignore
├── AGENTS.md
├── Auth_phases.md
├── docker-compose.yml
├── filestructure.md
├── phase.md
├── RBAC_MANAGEMENT.md
├── README.md
├── render.yaml
└── shelter_phases.md
```
