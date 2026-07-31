# PawMatch Authorization Architecture Foundation (Phase 1.5.5)

```text
Document ID:     ARCHITECTURE-AUTHORIZATION_FOUNDATION
Status:          Approved Production Architecture Blueprint
Version:         1.5.5
Document Owner:  PawMatch Core Architecture & Security Team
Target Audience: Software Engineers, AI Coding Agents, DevOps, Security Engineers
Last Updated:    July 31, 2026
```

---

## 1. Overview & Architectural Principles

The PawMatch Authorization Framework provides a multi-layered, production-grade access control infrastructure answering the fundamental security question:

$$\text{WHO (User/Role)} \xrightarrow{\text{can perform}} \text{WHAT (Permission/Action)} \xrightarrow{\text{on}} \text{WHICH RESOURCE (Object)} \xrightarrow{\text{under}} \text{WHICH CONDITIONS (Policy)}$$

```mermaid
graph TD
    A[User] -->|has| B[Role]
    B -->|maps to| C[Permission Set]
    C -->|evaluated by| D[AuthorizationService]
    D -->|consults| E[PolicyEngine]
    E -->|evaluates| F[Resource Policy / Object Ownership]
    F -->|Grants or Denies| G[Protected Resource / API View]
```

---

## 2. Authorization Layers

1. **Permission Registry (`apps/accounts/permissions.py`)**: Centralized string constants (`pets.view`, `pets.create`, `shelters.manage`, `medical.manage`, etc.).
2. **Role Definitions (`apps/accounts/roles.py`)**: Platform role constants (`ADMINISTRATOR`, `SHELTER_MANAGER`, `SHELTER_STAFF`, `VETERINARIAN`, `VOLUNTEER`, `ADOPTER`).
3. **Role $\rightarrow$ Permission Mapping (`apps/accounts/role_permissions.py`)**: Declarative mapping dictionary assigning permission sets to roles.
4. **Policy Engine & Policies (`apps/accounts/policies/`)**: Object-level policy evaluation classes (`UserPolicy`, `PetPolicy`) inspecting ownership and multi-tenant isolation.
5. **Authorization Service (`apps/accounts/services/authorization_service.py`)**: Single service entry point executing authorization checks, emitting security events, and recording audit logs.
6. **DRF Permission Classes & Decorators (`permissions_drf.py` & `auth_decorators.py`)**: Declarative view-level enforcement tools (`HasPermission`, `HasRole`, `HasObjectPermission`, `@require_permission`, `@require_role`).

---

## 3. Policy Engine & Multi-Tenant Object Ownership Specification

Policies extend `BasePolicy` and implement `can_view`, `can_create`, `can_update`, `can_delete`, or generic `can_action`.

```mermaid
sequenceDiagram
    autonumber
    actor User as Authenticated User
    participant DRF as DRF View Gateway
    participant Authz as AuthorizationService
    participant Engine as PolicyEngine
    participant Policy as PetPolicy (Target Object Policy)
    participant Audit as AuditService

    User->>DRF: PATCH /api/v1/pets/42/ (Edit Pet)
    DRF->>Authz: authorize(user, "update", pet_instance)
    Authz->>Engine: evaluate(user, "update", pet_instance)
    Engine->>Policy: can_update(user, pet_instance)
    alt Object Ownership Verified (Pet.shelter_id == User.shelter_id OR Superuser)
        Policy-->>Engine: True
        Engine-->>Authz: True
        Authz->>Audit: log_event("AUTHORIZATION_GRANTED")
        Authz->>Authz: Dispatch PermissionGrantedEvent
        DRF-->>User: Execute view action
    else Ownership / Shelter Isolation Violation
        Policy-->>Engine: False
        Engine-->>Authz: False
        Authz->>Audit: log_event("AUTHORIZATION_DENIED")
        Authz->>Authz: Dispatch PermissionDeniedEvent
        Authz-->>DRF: Raise PermissionDeniedException (HTTP 403)
        DRF-->>User: HTTP 403 Forbidden {success: false, message: "..."}
    end
```

---

## 4. Multi-Tenant Shelter Isolation & Extension Strategy

Future business modules (Shelters, Pets, Adoptions, Medical Records) integrate seamlessly by defining a subclass of `BasePolicy` in their respective domain packages and registering it with `PolicyEngine.register_policy(ModelClass, PolicyClass)` without modifying core authentication/authorization code.
