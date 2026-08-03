# PawMatch Backend File Structure

```text
backend/
├── apps/
│   ├── accounts/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   ├── documentation/
│   │   │   └── rbac_swagger.py
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── sync_rbac.py
│   │   ├── migrations/
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── profile.py
│   │   │   ├── rbac.py
│   │   │   └── user.py
│   │   ├── policies/
│   │   │   └── __init__.py
│   │   ├── selectors/
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── password_service.py
│   │   │   ├── profile_service.py
│   │   │   ├── registration_service.py
│   │   │   └── role_service.py
│   │   ├── templates/
│   │   │   └── emails/
│   │   │       ├── password_reset.html
│   │   │       ├── password_reset.txt
│   │   │       ├── verification.html
│   │   │       └── verification.txt
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_authentication.py
│   │   │   ├── test_authorization.py
│   │   │   ├── test_drf_integration.py
│   │   │   ├── test_models.py
│   │   │   ├── test_password.py
│   │   │   ├── test_profile.py
│   │   │   ├── test_rbac_admin_tooling.py
│   │   │   ├── test_rbac_api.py
│   │   │   ├── test_rbac_e2e.py
│   │   │   ├── test_rbac_events_logging.py
│   │   │   ├── test_rbac_sync.py
│   │   │   ├── test_registration.py
│   │   │   └── test_role_service.py
│   │   ├── validators/
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── auth_decorators.py
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── events.py
│   │   ├── exceptions.py
│   │   ├── managers.py
│   │   ├── permissions.py
│   │   ├── permissions_drf.py
│   │   ├── role_permissions.py
│   │   ├── roles.py
│   │   ├── signals.py
│   │   ├── throttles.py
│   │   └── utils.py
│   ├── administration/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   ├── migrations/
│   │   ├── selectors/
│   │   ├── services/
│   │   ├── tests/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   └── models.py
│   ├── adoptions/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   ├── migrations/
│   │   ├── selectors/
│   │   ├── services/
│   │   ├── tests/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   └── models.py
│   ├── audit_logs/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   ├── migrations/
│   │   ├── selectors/
│   │   ├── services/
│   │   ├── tests/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   └── models.py
│   ├── core/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   ├── migrations/
│   │   ├── selectors/
│   │   ├── services/
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   └── test_health.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── choices.py
│   │   ├── exceptions.py
│   │   ├── middleware.py
│   │   ├── mixins.py
│   │   ├── models.py
│   │   ├── pagination.py
│   │   ├── permissions.py
│   │   ├── responses.py
│   │   ├── signals.py
│   │   ├── utils.py
│   │   └── validators.py
│   ├── notifications/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   ├── migrations/
│   │   ├── selectors/
│   │   ├── services/
│   │   ├── tests/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   └── models.py
│   ├── pets/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   ├── migrations/
│   │   ├── selectors/
│   │   ├── services/
│   │   ├── tests/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   └── models.py
│   ├── shelters/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   ├── migrations/
│   │   │   ├── __init__.py
│   │   │   └── 0001_initial.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── document.py
│   │   │   ├── invitation.py
│   │   │   ├── member.py
│   │   │   ├── shelter.py
│   │   │   └── verification.py
│   │   ├── selectors/
│   │   │   ├── __init__.py
│   │   │   ├── shelter_selector.py
│   │   │   └── verification_selector.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── invitation_service.py
│   │   │   ├── member_service.py
│   │   │   ├── shelter_service.py
│   │   │   └── verification_service.py
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_document_model.py
│   │   │   ├── test_invitation_model.py
│   │   │   ├── test_invitation_service.py
│   │   │   ├── test_member_model.py
│   │   │   ├── test_member_service.py
│   │   │   ├── test_shelter_model.py
│   │   │   ├── test_shelter_service.py
│   │   │   ├── test_verification_model.py
│   │   │   └── test_verification_service.py
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── permissions.py
│   │   ├── signals.py
│   │   └── validators.py
│   └── __init__.py
├── config/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   └── urls.py
│   │   ├── __init__.py
│   │   ├── urls.py
│   │   └── versioning.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── logging.py
│   │   ├── production.py
│   │   └── staging.py
│   ├── __init__.py
│   ├── asgi.py
│   ├── urls.py
│   └── wsgi.py
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   ├── production.txt
│   └── testing.txt
├── .dockerignore
├── .gitignore
├── Dockerfile
├── README.md
├── build.sh
├── docker-compose.yml
├── filestructure.md
├── gunicorn.conf.py
├── manage.py
├── pyproject.toml
└── render.yaml
```
