# PawMatch Password Management Architecture

```text
Document ID:     ARCHITECTURE-PASSWORD_MANAGEMENT
Status:          Approved Production Architecture Blueprint
Version:         1.5.0
Document Owner:  PawMatch Core Security & Architecture Team
Target Audience: Software Engineers, AI Agents, DevOps, Security Auditors
Last Updated:    July 31, 2026
```

---

## 1. Overview & Password Lifecycle

PawMatch provides a secure, production-grade password management subsystem supporting authenticated password changes, user-enumeration-resistant forgot password workflows, token-based password resets via generic `AccountToken` models, and security confirmation notifications.

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Client SPA
    participant API as PawMatch DRF Gateway
    participant PwdService as PasswordService
    participant EmailService as EmailService
    participant Audit as AuditService
    participant DB as PostgreSQL 17

    Note over User, DB: Step 1: Forgot Password Request
    User->>API: POST /api/v1/accounts/forgot-password/ {email}
    API->>PwdService: forgot_password(email)
    alt Email Exists & Active
        PwdService->>DB: Invalidate previous active PASSWORD_RESET tokens
        PwdService->>DB: Create AccountToken (token_type=PASSWORD_RESET, expires_at=now+1h)
        PwdService->>EmailService: send_password_reset_email(user, raw_token)
        EmailService-->>User: Dispatch Reset Email HTML
        PwdService->>Audit: log_event("PASSWORD_RESET_REQUESTED")
    else Email Non-Existent or Inactive
        PwdService->>Audit: log_event("PASSWORD_RESET_REQUESTED", status="NON_EXISTENT")
    end
    API-->>User: HTTP 200 OK {success: true, message: "If an account with that email exists..."}

    Note over User, DB: Step 2: Reset Password Execution
    User->>API: POST /api/v1/accounts/reset-password/ {token, new_password, confirm_password}
    API->>PwdService: reset_password(raw_token, new_password, confirm_password)
    PwdService->>DB: Query AccountToken by SHA-256 token_hash
    alt Invalid, Expired, or Consumed Token
        PwdService->>Audit: log_event("PASSWORD_RESET_FAILED")
        API-->>User: HTTP 400 Bad Request {success: false, message: "..."}
    else Valid Token
        PwdService->>DB: Set user password hash (set_password) & save
        PwdService->>DB: Mark token as used (used_at=now, is_active=False)
        PwdService->>EmailService: send_password_changed_email(user)
        EmailService-->>User: Dispatch Password Changed Security Notification HTML
        PwdService->>Audit: log_event("PASSWORD_RESET_COMPLETED")
        API-->>User: HTTP 200 OK {success: true, message: "Password reset successfully..."}
    end
```

---

## 2. Security Guarantees & Principles

1. **User Enumeration Prevention**: `POST /api/v1/accounts/forgot-password/` returns identical HTTP 200 success responses regardless of whether the email exists in the database.
2. **Generic `AccountToken` Reuse**: Uses `AccountTokenType.PASSWORD_RESET`. Database persists only SHA-256 hashes (`token_hash`), never raw tokens.
3. **Single-Use & Expiration**: Tokens expire in **1 hour** (`PASSWORD_RESET_TOKEN_EXPIRY_HOURS`) and are marked consumed (`used_at = now()`) upon use.
4. **Password Validation Rules**:
   - Rejects passwords not matching `confirm_password`.
   - Rejects new passwords identical to current password (`validate_password_not_same`).
   - Rejects recently used passwords (`validate_password_not_reused`).
   - Enforces Django's standard password strength rules (`MinimumLength`, `CommonPassword`, `NumericPassword`).
5. **Security Notifications**: Successful password changes or resets immediately dispatch a security alert HTML email (`password_changed_email.html`).

---

## 3. API Specification Summary

| Endpoint | Method | Permission | Rate Limit | Description |
|---|---|---|---|---|
| `/api/v1/accounts/change-password/` | POST | `IsAuthenticated` | - | Authenticated password change requiring current password |
| `/api/v1/accounts/forgot-password/` | POST | `AllowAny` | `3/min` | Initiates password reset link dispatch |
| `/api/v1/accounts/reset-password/` | POST | `AllowAny` | `3/min` | Resets password using cryptographically verified reset token |
