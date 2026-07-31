# PawMatch User Profile Management Architecture

```text
Document ID:     ARCHITECTURE-PROFILE_MANAGEMENT
Status:          Approved Production Architecture Blueprint
Version:         1.4.0
Document Owner:  PawMatch Core Architecture Team
Target Audience: Software Engineers, AI Agents, DevOps, Security Engineers
Last Updated:    July 31, 2026
```

---

## 1. Overview & One-to-One User Profile Architecture

PawMatch separates authentication identity (`User` model) from domain user profile details (`UserProfile` model) via a strict `OneToOneField` relationship.

```mermaid
erDiagram
    User ||--|| UserProfile : "has profile"

    User {
        uuid id PK
        string email UK
        string password
        string first_name
        string last_name
        boolean is_active
        boolean is_email_verified
        boolean is_staff
    }

    UserProfile {
        uuid id PK
        uuid user_id FK
        string phone_number
        image avatar
        text bio
        date date_of_birth
        json preferences
    }
```

### Automatic Profile Creation
Every newly created `User` receives a corresponding `UserProfile` instance automatically via the `post_save` signal in [`apps/accounts/signals.py`](file:///home/spidy/Desktop/projects/PawMatch/backend/apps/accounts/signals.py).

---

## 2. Avatar Storage & Media Lifecyle Architecture

Avatar media management uses a modular `StorageService` with a `StorageProvider` strategy pattern (`LocalStorageProvider`).

```mermaid
sequenceDiagram
    autonumber
    actor User as Authenticated User
    participant API as DRF UploadAvatarAPIView
    participant Service as ProfileService
    participant Validator as ImageValidator
    participant Storage as StorageService / LocalStorageProvider
    participant Audit as AuditService

    User->>API: POST /api/v1/accounts/profile/avatar/ (multipart image)
    API->>Service: upload_avatar(user, avatar_file)
    Service->>Validator: validate_avatar_file(file)
    Validator-->>Service: Validation Passed (<=5MB, JPG/PNG/WEBP)
    Service->>Storage: save_avatar(file, user_id)
    Storage->>Storage: Delete existing avatar if present & save file
    Storage-->>Service: Return relative file path
    Service->>Audit: log_event("AVATAR_UPLOADED")
    Service->>Service: Dispatch AvatarUploadedEvent
    API-->>User: HTTP 200 OK {success: true, data: {avatar: "http://..."}}
```

---

## 3. Account Deactivation Sequence

Account deactivation is a soft operation (`is_active = False`) requiring current password verification:

```mermaid
sequenceDiagram
    autonumber
    actor User as Authenticated User
    participant API as DRF DeactivateAccountAPIView
    participant Service as ProfileService
    participant Event as EventDispatcher
    participant Audit as AuditService

    User->>API: POST /api/v1/accounts/deactivate/ {password}
    API->>Service: deactivate_account(user, password)
    alt Password Invalid
        Service->>Audit: log_event("ACCOUNT_DEACTIVATED", status="FAILED")
        API-->>User: HTTP 401 Unauthorized {success: false, message: "Current password is incorrect."}
    else Password Valid
        Service->>Service: Set user.is_active = False & save
        Service->>Event: dispatch_account_deactivated(user_id, email)
        Service->>Audit: log_event("ACCOUNT_DEACTIVATED", status="SUCCESS")
        API-->>User: HTTP 200 OK {success: true, message: "Account deactivated successfully."}
    end
```

---

## 4. API Specification Summary

| Endpoint | Method | Permission | Description |
|---|---|---|---|
| `/api/v1/accounts/profile/` | GET | `IsAuthenticated` | Retrieves authenticated user profile |
| `/api/v1/accounts/profile/` | PATCH | `IsAuthenticated` | Updates personal details and preferences |
| `/api/v1/accounts/profile/avatar/` | POST | `IsAuthenticated` | Uploads profile avatar (<=5MB, JPG/PNG/WEBP) |
| `/api/v1/accounts/profile/avatar/` | DELETE | `IsAuthenticated` | Deletes profile avatar |
| `/api/v1/accounts/deactivate/` | POST | `IsAuthenticated` | Soft deactivates account with password verification |
