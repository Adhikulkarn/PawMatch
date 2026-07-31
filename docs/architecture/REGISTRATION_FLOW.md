# PawMatch User Registration & Email Verification Architecture

```text
Document ID:     ARCHITECTURE-REGISTRATION_FLOW
Status:          Approved Blueprint
Version:         1.3.0
Document Owner:  PawMatch Architecture & Security Team
Target Audience: Software Engineers, DevOps, Security Auditors, AI Coding Agents
Last Updated:    July 31, 2026
```

---

## 1. Overview

PawMatch implements a secure, asynchronous user onboarding lifecycle with **Email Verification Tokens**, **SHA-256 Token Hashing**, **Transactional Email Services**, and **Security Audit Logging**.

---

## 2. Registration & Account Activation Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Client SPA
    participant API as PawMatch DRF Gateway
    participant RegService as RegistrationService
    participant EmailService as EmailService
    participant Audit as AuditService / AuditLog
    participant DB as PostgreSQL 17

    Note over User, DB: Step 1: User Registration
    User->>API: POST /api/v1/accounts/register/ {email, password, confirm_password, first_name, last_name}
    API->>RegService: register_user(email, password, first_name, last_name)
    RegService->>DB: Check email uniqueness & create inactive user (is_active=False)
    RegService->>RegService: Generate raw token (secrets.token_urlsafe) & SHA-256 hash
    RegService->>DB: Save EmailVerificationToken(user, token_hash, expires_at=now+24h)
    RegService->>EmailService: send_verification_email(user, raw_token)
    EmailService-->>User: Dispatch Verification Email HTML
    RegService->>Audit: log_event("REGISTRATION_SUCCESS")
    API-->>User: HTTP 201 Created {success: true, message: "Registration successful..."}

    Note over User, DB: Step 2: Email Verification
    User->>API: GET /api/v1/accounts/verify-email/?token=<raw_token>
    API->>RegService: verify_email_token(raw_token)
    RegService->>RegService: Compute SHA-256 hash of raw_token
    RegService->>DB: Query EmailVerificationToken by token_hash
    alt Invalid, Expired, or Consumed Token
        RegService->>Audit: log_event("EMAIL_VERIFICATION_FAILED")
        API-->>User: HTTP 400 Bad Request {success: false, message: "..."}
    else Valid Token
        RegService->>DB: Update user (is_active=True, is_email_verified=True)
        RegService->>DB: Mark token as used & invalidate prior active tokens
        RegService->>EmailService: send_welcome_email(user)
        EmailService-->>User: Dispatch Welcome Email HTML
        RegService->>Audit: log_event("EMAIL_VERIFICATION_SUCCESS")
        API-->>User: HTTP 200 OK {success: true, message: "Email verified successfully..."}
    end
```

---

## 3. Verification Token Security Specification

- **Token Generation**: Cryptographically secure 32-byte URL-safe string (`secrets.token_urlsafe(32)`).
- **Database Storage**: Raw tokens are **NEVER** stored in database tables or logs. Database persists only the `SHA-256` hash (`token_hash`).
- **Token Expiration**: Default **24 hours** (`EMAIL_VERIFICATION_TOKEN_EXPIRY_HOURS`).
- **Single-Use Enforcement**: Upon successful verification, token is marked `used_at = now()` and `is_active = False`.
- **Resend Invalidation**: Generating a new verification token automatically invalidates all previous active tokens for that user.

---

## 4. Transactional Email Architecture

- **`EmailService`**: Decouples email composition and delivery from domain logic.
- **HTML & Plain Text Support**: Uses Django template rendering (`apps/accounts/templates/emails/verification_email.html` and `welcome_email.html`).
- **Configurable Frontend URLs**: Bound dynamically via `FRONTEND_URL` and `FRONTEND_VERIFY_EMAIL_URL`.
