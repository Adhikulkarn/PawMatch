# PawMatch_V1_REST_API_Specification.md

## 1. Document Information

| Field | Value |
|---|---|
| Document Title | PawMatch V1 REST API Specification |
| Project | PawMatch |
| Version | 1.0 |
| Status | Draft API Contract |
| Date | 2026-07-29 |
| API Style | REST |
| OpenAPI Target | OpenAPI 3.0 via `drf-spectacular` |
| Backend Stack | Django, Django REST Framework, SimpleJWT, PostgreSQL |
| Source of Truth | `PawMatch_AI_Functional_Requirements_Specification.md`, `PawMatch_V1_Release_Scope.md` |

## 2. Architectural Standards

- Base URL: `/api/v1/`
- All endpoints use trailing slashes.
- All resource identifiers are `UUIDv4`.
- All request and response payload fields use `snake_case`.
- All query parameters use `snake_case`.
- All timestamps use ISO-8601 UTC format, for example: `2026-07-29T12:30:00Z`.
- JSON is the default request and response format unless multipart upload is required.
- `PATCH` is the default update method.
- `DELETE` performs soft deletion where deletion is allowed.
- Server-side authorization is mandatory for every protected endpoint.
- Cross-organization access is denied by default.

## 3. Authentication

### 3.1 Authentication Model

- Authentication type: JWT Bearer authentication
- Token implementation: `SimpleJWT`
- Header format: `Authorization: Bearer <access_token>`
- Token refresh uses refresh token rotation as recommended for production deployments.
- All authentication traffic must be served over TLS 1.2+.

### 3.2 Token Response Format

```json
{
  "access": "...",
  "refresh": "..."
}
```

### 3.3 Session and Credential Rules

- Institutional account registration requires verification before publish privileges are granted.
- Password reset links or OTPs expire after 15 minutes.
- All active sessions must be invalidated after password reset, password change, or account suspension.
- Default dashboard inactivity timeout: 30 minutes.

## 4. Headers

### 4.1 Standard Request Headers

| Header | Required | Notes |
|---|---|---|
| `Accept: application/json` | Yes | Default for all endpoints |
| `Content-Type: application/json` | Yes | Required for JSON request bodies |
| `Authorization: Bearer <access_token>` | Protected endpoints | JWT access token |
| `Content-Type: multipart/form-data` | Upload endpoints | Required for avatar, pet images, verification documents |

### 4.2 Standard Response Headers

| Header | Notes |
|---|---|
| `Content-Type: application/json` | JSON response payload |
| `Location` | Recommended on create endpoints |
| `X-RateLimit-Limit` | Recommended for throttled endpoints |
| `X-RateLimit-Remaining` | Recommended for throttled endpoints |
| `Retry-After` | Recommended for `429 Too Many Requests` |

## 5. Versioning

- URI versioning is mandatory.
- Current version: `/api/v1/`
- Breaking changes require `/api/v2/`.
- Non-breaking additive changes may be introduced within V1.
- Deprecated fields must remain available for at least one full minor release cycle before removal.

## 6. Naming Conventions

- Resource names use plural nouns where appropriate.
- Resource paths use lowercase kebab-free path segments.
- JSON keys use `snake_case`.
- Enum values use uppercase machine-readable constants.
- Foreign keys use `_id` suffix.
- Boolean fields should read as predicates where possible, for example `is_primary`, `is_read`.

## 7. Pagination Standard

### 7.1 Pagination Style

- Pagination type: DRF page-number pagination
- Default query params:
  - `page`
  - `page_size`
- Default `page_size`: 20
- Maximum `page_size`: 100

### 7.2 Paginated Response Envelope

```json
{
  "status": "success",
  "data": {
    "count": 0,
    "next": null,
    "previous": null,
    "results": []
  }
}
```

## 8. Filtering Standard

- Filtering uses query parameters only.
- Repeated filters should use comma-separated values only if explicitly documented; otherwise single-value exact match is assumed.
- Date filters use ISO-8601 timestamps or `YYYY-MM-DD` where explicitly defined.
- Boolean filters use `true` or `false`.

### 8.1 Common Filter Operators

| Pattern | Meaning |
|---|---|
| `field=value` | Exact match |
| `field__in=a,b` | List membership where supported |
| `created_at__gte=value` | Greater than or equal |
| `created_at__lte=value` | Less than or equal |

## 9. Sorting Standard

- Sorting uses the `ordering` query parameter.
- Ascending sort: `ordering=created_at`
- Descending sort: `ordering=-created_at`
- Only documented sortable fields may be used.

## 10. Search Standard

- Search uses the `search` query parameter.
- Search is case-insensitive unless otherwise noted.
- Search behavior must be backed by indexed fields in production.
- No dedicated `/search/` endpoints are allowed for V1 resources documented here.

## 11. File Upload Standard

### 11.1 Supported Upload Types

| Upload Type | Formats | Maximum Size |
|---|---|---|
| Avatar images | `JPEG`, `PNG`, `WEBP` | 5 MB |
| Pet images | `JPEG`, `PNG`, `WEBP` | 5 MB |
| Verification documents | `PDF`, `JPEG`, `PNG` | 10 MB |

### 11.2 Upload Rules

- Pet image limit: 10 images per pet.
- Upload endpoints use `multipart/form-data`.
- File validation must occur before persistence.
- Uploaded media should be stored outside the application container and referenced by URL.
- Soft-deleted media may be retained for recovery according to operational policy.

## 12. Rate Limiting

Recommended DRF throttling:

| Scope | Rate |
|---|---|
| Anonymous | `60/min` |
| Authenticated | `300/min` |
| Login | `5/min` |
| Register | `5/hour` |
| Forgot Password | `3/hour` |
| Reset Password | `5/hour` |
| Upload Endpoints | `30/min` |
| Admin Endpoints | `120/min` |

Recommended DRF throttle scopes:

- `anon`
- `user`
- `auth_login`
- `auth_register`
- `auth_forgot_password`
- `auth_reset_password`
- `uploads`
- `admin`

## 13. Error Codes

### 13.1 HTTP Status Codes Used

| Status | Meaning |
|---|---|
| `200 OK` | Successful retrieval or update |
| `201 Created` | Successful creation |
| `204 No Content` | Successful delete or logout without response body |
| `400 Bad Request` | Validation failure or malformed request |
| `401 Unauthorized` | Missing or invalid authentication |
| `403 Forbidden` | Authenticated but not allowed |
| `404 Not Found` | Resource not found or not visible |
| `409 Conflict` | Business rule conflict |
| `415 Unsupported Media Type` | Invalid upload format |
| `429 Too Many Requests` | Throttled |
| `500 Internal Server Error` | Unexpected server error |

### 13.2 Reusable Error Codes

| Code | Meaning |
|---|---|
| `VALIDATION_ERROR` | Request payload or query parameter invalid |
| `AUTHENTICATION_REQUIRED` | No valid access token |
| `INVALID_CREDENTIALS` | Login failed |
| `ACCOUNT_LOCKED` | Too many failed attempts |
| `ACCOUNT_INACTIVE` | Account disabled or soft-deleted |
| `ACCOUNT_NOT_VERIFIED` | Email or account verification incomplete |
| `PERMISSION_DENIED` | Role or ownership restriction |
| `RESOURCE_NOT_FOUND` | Resource missing |
| `DUPLICATE_RESOURCE` | Unique constraint violation |
| `RATE_LIMIT_EXCEEDED` | Throttle hit |
| `INVALID_TOKEN` | Token invalid or expired |
| `TOKEN_BLACKLISTED` | Token revoked |
| `INVALID_FILE_TYPE` | File format not allowed |
| `FILE_TOO_LARGE` | File exceeds limit |
| `MAX_IMAGES_EXCEEDED` | Pet image limit exceeded |
| `VERIFICATION_REQUIRED` | Shelter must be verified before publishing |
| `BUSINESS_RULE_VIOLATION` | Domain rule failure |
| `APPLICATION_LIMIT_REACHED` | Concurrent application limit exceeded |
| `PET_NOT_AVAILABLE` | Pet not open for applications |
| `STATUS_TRANSITION_NOT_ALLOWED` | Invalid state update |
| `CONFLICTING_OPERATION` | Update conflicts with current state |

## 14. Response Schemas

### 14.1 Single Object

```json
{
  "status": "success",
  "data": {}
}
```

### 14.2 Paginated Response

```json
{
  "status": "success",
  "data": {
    "count": 0,
    "next": null,
    "previous": null,
    "results": []
  }
}
```

### 14.3 Error Response

```json
{
  "status": "error",
  "code": "ERROR_CODE",
  "message": "...",
  "errors": []
}
```

### 14.4 Validation Error Detail

```json
{
  "status": "error",
  "code": "VALIDATION_ERROR",
  "message": "One or more fields are invalid.",
  "errors": [
    {
      "field": "email",
      "message": "Enter a valid email address."
    }
  ]
}
```

## 15. Enumerations

### 15.1 `user_role`

- `ADMIN`
- `SHELTER`
- `ADOPTER`

### 15.2 `user_status`

- `PENDING_VERIFICATION`
- `ACTIVE`
- `SUSPENDED`
- `DEACTIVATED`

### 15.3 `shelter_verification_status`

- `UNVERIFIED`
- `PENDING`
- `UNDER_REVIEW`
- `VERIFIED`
- `REJECTED`
- `CHANGES_REQUESTED`

### 15.4 `pet_status`

- `DRAFT`
- `AVAILABLE`
- `ON_HOLD`
- `PENDING_ADOPTION`
- `ADOPTED`
- `DEACTIVATED`

### 15.5 `species`

- `DOG`
- `CAT`
- `BIRD`
- `RABBIT`
- `OTHER`

### 15.6 `gender`

- `MALE`
- `FEMALE`
- `UNKNOWN`

### 15.7 `size`

- `SMALL`
- `MEDIUM`
- `LARGE`
- `EXTRA_LARGE`

### 15.8 `application_status`

- `DRAFT`
- `SUBMITTED`
- `UNDER_REVIEW`
- `APPROVED`
- `REJECTED`
- `CLOSED`

### 15.9 `notification_type`

- `ACCOUNT_VERIFICATION`
- `PASSWORD_RESET`
- `SHELTER_VERIFICATION_APPROVED`
- `SHELTER_VERIFICATION_REJECTED`
- `APPLICATION_SUBMITTED`
- `APPLICATION_STATUS_UPDATED`
- `APPLICATION_CLOSED`
- `PET_STATUS_UPDATED`

### 15.10 `notification_channel`

- `IN_APP`
- `EMAIL`

### 15.11 `document_type`

- `REGISTRATION_CERTIFICATE`
- `ADDRESS_PROOF`
- `AUTHORIZED_SIGNATORY_ID`
- `OTHER_SUPPORTING_DOCUMENT`

### 15.12 `pet_image_status`

- `ACTIVE`
- `DELETED`

### 15.13 `audit_action`

- `CREATE`
- `UPDATE`
- `DELETE`
- `VERIFY`
- `REJECT`
- `REQUEST_CHANGES`
- `SUSPEND`
- `MODERATE`

## 16. Reusable Resource Schemas

### 16.1 User

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | User identifier |
| `role` | enum(`user_role`) | Account role |
| `status` | enum(`user_status`) | Account lifecycle state |
| `email` | string | Unique |
| `phone_number` | string, nullable | E.164 recommended |
| `first_name` | string | |
| `last_name` | string | |
| `full_name` | string | Derived or stored |
| `avatar_url` | string, nullable | Public media URL |
| `city` | string, nullable | |
| `state` | string, nullable | |
| `address_line_1` | string, nullable | |
| `address_line_2` | string, nullable | |
| `postal_code` | string, nullable | |
| `household_details` | string, nullable | Adopter profile data |
| `lifestyle_preferences` | object, nullable | Adopter profile data |
| `privacy_settings` | object | Role-based visibility flags |
| `created_at` | datetime | |
| `updated_at` | datetime | |

### 16.2 Shelter

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | Shelter profile identifier |
| `user_id` | UUID | Owning shelter account |
| `name` | string | Shelter display name |
| `description` | string, nullable | |
| `email` | string | Public contact email |
| `phone_number` | string | Public contact number |
| `website_url` | string, nullable | |
| `city` | string | |
| `state` | string | |
| `address_line_1` | string | |
| `address_line_2` | string, nullable | |
| `postal_code` | string, nullable | |
| `verification_status` | enum(`shelter_verification_status`) | |
| `is_publish_enabled` | boolean | Derived from verification status |
| `created_at` | datetime | |
| `updated_at` | datetime | |

### 16.3 Shelter Verification

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | Verification request identifier |
| `shelter_id` | UUID | Related shelter |
| `status` | enum(`shelter_verification_status`) | |
| `submitted_at` | datetime, nullable | |
| `reviewed_at` | datetime, nullable | |
| `reviewed_by` | UUID, nullable | Admin user id |
| `review_notes` | string, nullable | Approval, rejection, or change request notes |
| `documents` | array | Uploaded verification documents |
| `created_at` | datetime | |
| `updated_at` | datetime | |

### 16.4 Verification Document

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | |
| `verification_id` | UUID, nullable | Null until submission if pre-uploaded |
| `document_type` | enum(`document_type`) | |
| `file_url` | string | |
| `file_name` | string | |
| `file_size` | integer | Bytes |
| `mime_type` | string | |
| `uploaded_at` | datetime | |

### 16.5 Pet

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | |
| `shelter_id` | UUID | Owning shelter |
| `name` | string | |
| `species` | enum(`species`) | |
| `breed` | string | |
| `age_months` | integer | Estimated or exact |
| `gender` | enum(`gender`) | |
| `size` | enum(`size`) | |
| `description` | string, nullable | |
| `health_summary` | string | Includes vaccination or health summary if available |
| `temperament_summary` | string, nullable | |
| `adoption_requirements` | string, nullable | |
| `special_needs` | boolean | |
| `city` | string | |
| `state` | string | |
| `status` | enum(`pet_status`) | |
| `primary_image_url` | string, nullable | |
| `created_at` | datetime | |
| `updated_at` | datetime | |
| `deleted_at` | datetime, nullable | Soft delete marker |

### 16.6 Pet Image

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | |
| `pet_id` | UUID | |
| `image_url` | string | |
| `caption` | string, nullable | |
| `display_order` | integer | Zero-based or one-based, implementation-defined but consistent |
| `is_primary` | boolean | |
| `status` | enum(`pet_image_status`) | |
| `created_at` | datetime | |
| `updated_at` | datetime | |

### 16.7 Adoption Application

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | |
| `pet_id` | UUID | |
| `applicant_id` | UUID | Adopter user id |
| `shelter_id` | UUID | Derived from pet |
| `status` | enum(`application_status`) | |
| `home_environment` | string | |
| `household_members` | string | |
| `prior_pet_experience` | string | |
| `availability_for_home_visit` | boolean | |
| `additional_notes` | string, nullable | |
| `submitted_at` | datetime, nullable | |
| `reviewed_at` | datetime, nullable | |
| `reviewed_by` | UUID, nullable | Shelter or admin reviewer |
| `review_notes` | string, nullable | |
| `created_at` | datetime | |
| `updated_at` | datetime | |

### 16.8 Application History Event

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | |
| `application_id` | UUID | |
| `from_status` | enum(`application_status`), nullable | |
| `to_status` | enum(`application_status`) | |
| `changed_by` | UUID | |
| `notes` | string, nullable | |
| `created_at` | datetime | |

### 16.9 Notification

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | |
| `user_id` | UUID | Recipient |
| `type` | enum(`notification_type`) | |
| `channel` | enum(`notification_channel`) | V1 requires in-app; email is optional infrastructure support |
| `title` | string | |
| `message` | string | |
| `related_resource_type` | string, nullable | For example `application`, `verification`, `pet` |
| `related_resource_id` | UUID, nullable | |
| `is_read` | boolean | |
| `created_at` | datetime | |
| `read_at` | datetime, nullable | |

### 16.10 Audit Log

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | |
| `actor_id` | UUID | Admin actor |
| `action` | enum(`audit_action`) | |
| `resource_type` | string | |
| `resource_id` | UUID | |
| `summary` | string | |
| `metadata` | object | Implementation-specific structured context |
| `created_at` | datetime | |

### 16.11 Analytics Summary

| Field | Type | Notes |
|---|---|---|
| `total_users` | integer | |
| `total_shelters` | integer | |
| `total_verified_shelters` | integer | |
| `total_pet_listings` | integer | |
| `total_active_adoptions` | integer | Open active application volume |
| `total_completed_adoptions` | integer | Completed adoption volume |
| `generated_at` | datetime | Snapshot time |

## 17. RBAC Matrix

| Endpoint Group | Public | Adopter | Shelter | Admin |
|---|---|---|---|---|
| Auth register, login, refresh, verify, resend, forgot, reset | Yes | Yes | Yes | Yes |
| Auth logout | No | Yes | Yes | Yes |
| `GET /users/me/` | No | Yes | Yes | Yes |
| `PATCH /users/me/` | No | Yes | Yes | Yes |
| `PATCH /users/me/avatar/` | No | Yes | Yes | Yes |
| `DELETE /users/me/` | No | Yes | Yes | Yes |
| `GET /users/` | No | No | No | Yes |
| `GET /users/{id}/` | No | No | No | Yes |
| `PATCH /users/{id}/` | No | No | No | Yes |
| `POST /shelters/` | No | No | Yes | Yes |
| `GET /shelters/` | Yes | Yes | Yes | Yes |
| `GET /shelters/me/` | No | No | Yes | Yes |
| `PATCH /shelters/me/` | No | No | Yes | Yes |
| `GET /shelters/{id}/` | Yes | Yes | Yes | Yes |
| Shelter verification self-service endpoints | No | No | Yes | Yes |
| Shelter verification admin endpoints | No | No | No | Yes |
| `GET /pets/` and `GET /pets/{id}/` | Yes | Yes | Yes | Yes |
| `POST /pets/` | No | No | Verified shelter only | Yes |
| `PATCH /pets/{id}/`, `DELETE /pets/{id}/` | No | No | Owning shelter only | Yes |
| Pet image endpoints write | No | No | Owning shelter only | Yes |
| Pet image endpoints read | Yes | Yes | Yes | Yes |
| `POST /applications/` | No | Yes | No | Yes |
| `GET /applications/` | No | Own only | Own shelter applications only | Yes |
| `GET /applications/{id}/` | No | Own only | Own shelter applications only | Yes |
| `PATCH /applications/{id}/` | No | Own draft only | Own shelter review only | Yes |
| `GET /applications/{id}/history/` | No | Own only | Own shelter applications only | Yes |
| Notifications endpoints | No | Own only | Own only | Own only |
| Admin endpoints | No | No | No | Yes |
| Analytics summary | No | No | No | Yes |
| Shelter analytics me | No | No | Yes | Yes |

## 18. OpenAPI Tags

- `Authentication`
- `Users`
- `Shelters`
- `Verification`
- `Pets`
- `Pet Images`
- `Applications`
- `Notifications`
- `Admin`
- `Analytics`

## 19. Endpoint Specifications

## 19.1 Authentication

### `POST /auth/register/`

- Purpose: Register a new adopter or shelter account.
- Authentication Required: No
- Allowed Roles: Public
- Headers: `Accept`, `Content-Type: application/json`
- Path Parameters: None
- Query Parameters: None
- Request Body:

| Field | Type | Required | Notes |
|---|---|---|---|
| `role` | enum(`user_role`) | Yes | `ADOPTER` or `SHELTER` only for V1 |
| `email` | string | Yes | Unique |
| `phone_number` | string | No | Recommended for verification workflows |
| `password` | string | Yes | Must satisfy password policy |
| `first_name` | string | Yes | |
| `last_name` | string | Yes | |

- Success Response: `201 Created`, Single Object containing `user` summary and verification status.
- Possible Error Responses: `400`, `409`, `429`
- Notes:
  - Shelter accounts are created with `PENDING_VERIFICATION` or equivalent non-publishable state.
  - Duplicate email or phone registrations must be rejected.

### `POST /auth/login/`

- Purpose: Authenticate a user and issue JWT tokens.
- Authentication Required: No
- Allowed Roles: Public
- Headers: `Accept`, `Content-Type: application/json`
- Path Parameters: None
- Query Parameters: None
- Request Body:

| Field | Type | Required | Notes |
|---|---|---|---|
| `email` | string | Yes | Email-based login for V1 |
| `password` | string | Yes | |

- Success Response: `200 OK`, Single Object containing `access`, `refresh`, and current `user`.
- Possible Error Responses: `400`, `401`, `429`
- Notes:
  - Only verified active accounts may log in.
  - After repeated failed attempts, account lock behavior should apply.

### `POST /auth/refresh/`

- Purpose: Obtain a new access token using a refresh token.
- Authentication Required: No
- Allowed Roles: Public
- Headers: `Accept`, `Content-Type: application/json`
- Path Parameters: None
- Query Parameters: None
- Request Body:

| Field | Type | Required |
|---|---|---|
| `refresh` | string | Yes |

- Success Response: `200 OK`, Single Object containing new `access` and optionally rotated `refresh`.
- Possible Error Responses: `400`, `401`
- Notes:
  - Implementation should align with `SimpleJWT` configuration.

### `POST /auth/logout/`

- Purpose: Revoke the current refresh token and end the session.
- Authentication Required: Yes
- Allowed Roles: Adopter, Shelter, Admin
- Headers: `Accept`, `Content-Type: application/json`, `Authorization`
- Path Parameters: None
- Query Parameters: None
- Request Body:

| Field | Type | Required |
|---|---|---|
| `refresh` | string | Yes |

- Success Response: `204 No Content`
- Possible Error Responses: `400`, `401`
- Notes:
  - Refresh token blacklisting is recommended.

### `POST /auth/verify-email/`

- Purpose: Verify account ownership using OTP or verification token.
- Authentication Required: No
- Allowed Roles: Public
- Headers: `Accept`, `Content-Type: application/json`
- Path Parameters: None
- Query Parameters: None
- Request Body:

| Field | Type | Required | Notes |
|---|---|---|---|
| `email` | string | Yes | |
| `verification_token` | string | No | One of token or OTP required |
| `otp_code` | string | No | One of token or OTP required |

- Success Response: `200 OK`, Single Object containing verification result and user status.
- Possible Error Responses: `400`, `404`, `409`, `429`
- Notes:
  - For shelter accounts, email verification does not replace admin verification.

### `POST /auth/resend-verification/`

- Purpose: Resend email verification token or OTP.
- Authentication Required: No
- Allowed Roles: Public
- Headers: `Accept`, `Content-Type: application/json`
- Path Parameters: None
- Query Parameters: None
- Request Body:

| Field | Type | Required |
|---|---|---|
| `email` | string | Yes |

- Success Response: `200 OK`, Single Object with resend acknowledgement.
- Possible Error Responses: `400`, `404`, `409`, `429`
- Notes:
  - Response should not leak unnecessary account state details.

### `POST /auth/forgot-password/`

- Purpose: Start password reset flow.
- Authentication Required: No
- Allowed Roles: Public
- Headers: `Accept`, `Content-Type: application/json`
- Path Parameters: None
- Query Parameters: None
- Request Body:

| Field | Type | Required |
|---|---|---|
| `email` | string | Yes |

- Success Response: `200 OK`, Single Object with neutral confirmation message.
- Possible Error Responses: `400`, `429`
- Notes:
  - Response must not disclose whether the account exists.

### `POST /auth/reset-password/`

- Purpose: Complete password reset with reset token or OTP.
- Authentication Required: No
- Allowed Roles: Public
- Headers: `Accept`, `Content-Type: application/json`
- Path Parameters: None
- Query Parameters: None
- Request Body:

| Field | Type | Required |
|---|---|---|
| `email` | string | Yes |
| `reset_token` | string | No |
| `otp_code` | string | No |
| `new_password` | string | Yes |

- Success Response: `200 OK`, Single Object with password reset acknowledgement.
- Possible Error Responses: `400`, `401`, `429`
- Notes:
  - All active sessions must be revoked after success.

### `POST /auth/change-password/`

- Purpose: Change password for an authenticated user.
- Authentication Required: Yes
- Allowed Roles: Adopter, Shelter, Admin
- Headers: `Accept`, `Content-Type: application/json`, `Authorization`
- Path Parameters: None
- Query Parameters: None
- Request Body:

| Field | Type | Required |
|---|---|---|
| `current_password` | string | Yes |
| `new_password` | string | Yes |

- Success Response: `200 OK`, Single Object with acknowledgement.
- Possible Error Responses: `400`, `401`, `403`
- Notes:
  - All active sessions except the current one may be revoked immediately; revoking all sessions is recommended.

## 19.2 Users

### `GET /users/me/`

- Purpose: Retrieve the authenticated user's profile.
- Authentication Required: Yes
- Allowed Roles: Adopter, Shelter, Admin
- Headers: `Accept`, `Authorization`
- Path Parameters: None
- Query Parameters: None
- Request Body: None
- Success Response: `200 OK`, Single Object containing `User`.
- Possible Error Responses: `401`, `404`
- Notes:
  - Response should include role-relevant profile fields only.

### `PATCH /users/me/`

- Purpose: Partially update the authenticated user's profile.
- Authentication Required: Yes
- Allowed Roles: Adopter, Shelter, Admin
- Headers: `Accept`, `Content-Type: application/json`, `Authorization`
- Path Parameters: None
- Query Parameters: None
- Request Body:

| Field | Type | Required | Notes |
|---|---|---|---|
| `first_name` | string | No | |
| `last_name` | string | No | |
| `phone_number` | string | No | |
| `city` | string | No | |
| `state` | string | No | |
| `address_line_1` | string | No | |
| `address_line_2` | string | No | |
| `postal_code` | string | No | |
| `household_details` | string | No | Adopter-focused |
| `lifestyle_preferences` | object | No | Adopter-focused |
| `privacy_settings` | object | No | |

- Success Response: `200 OK`, Single Object containing updated `User`.
- Possible Error Responses: `400`, `401`, `403`
- Notes:
  - Immutable fields such as `role` should not be patchable here.

### `PATCH /users/me/avatar/`

- Purpose: Upload or replace the authenticated user's avatar.
- Authentication Required: Yes
- Allowed Roles: Adopter, Shelter, Admin
- Headers: `Accept`, `Content-Type: multipart/form-data`, `Authorization`
- Path Parameters: None
- Query Parameters: None
- Request Body:

| Field | Type | Required | Notes |
|---|---|---|---|
| `avatar` | file | Yes | JPEG, PNG, WEBP up to 5 MB |

- Success Response: `200 OK`, Single Object containing updated avatar metadata and `avatar_url`.
- Possible Error Responses: `400`, `401`, `415`
- Notes:
  - Previous avatar replacement policy is implementation-specific.

### `DELETE /users/me/`

- Purpose: Soft delete the authenticated user's account.
- Authentication Required: Yes
- Allowed Roles: Adopter, Shelter, Admin
- Headers: `Accept`, `Authorization`
- Path Parameters: None
- Query Parameters: None
- Request Body: None
- Success Response: `204 No Content`
- Possible Error Responses: `401`, `403`, `409`
- Notes:
  - This endpoint performs account deactivation, not hard deletion.
  - Authentication tokens must be revoked.

### `GET /users/`

- Purpose: List users for administration.
- Authentication Required: Yes
- Allowed Roles: Admin
- Headers: `Accept`, `Authorization`
- Path Parameters: None
- Query Parameters:

| Parameter | Type | Notes |
|---|---|---|
| `page` | integer | Standard pagination |
| `page_size` | integer | Standard pagination |
| `search` | string | Search by name, email |
| `ordering` | string | `created_at`, `email`, `status`, `role` |
| `role` | enum(`user_role`) | Filter by role |
| `status` | enum(`user_status`) | Filter by status |
| `created_at__gte` | datetime | Optional |
| `created_at__lte` | datetime | Optional |

- Request Body: None
- Success Response: `200 OK`, Paginated Response of `User`.
- Possible Error Responses: `401`, `403`
- Notes:
  - Admin-only management endpoint.

### `GET /users/{id}/`

- Purpose: Retrieve a single user for administration.
- Authentication Required: Yes
- Allowed Roles: Admin
- Headers: `Accept`, `Authorization`
- Path Parameters:

| Parameter | Type | Notes |
|---|---|---|
| `id` | UUID | User id |

- Query Parameters: None
- Request Body: None
- Success Response: `200 OK`, Single Object containing `User`.
- Possible Error Responses: `401`, `403`, `404`
- Notes:
  - Sensitive fields should remain excluded unless explicitly required.

### `PATCH /users/{id}/`

- Purpose: Partially update a user account for administration and moderation.
- Authentication Required: Yes
- Allowed Roles: Admin
- Headers: `Accept`, `Content-Type: application/json`, `Authorization`
- Path Parameters:

| Parameter | Type |
|---|---|
| `id` | UUID |

- Query Parameters: None
- Request Body:

| Field | Type | Required | Notes |
|---|---|---|---|
| `status` | enum(`user_status`) | No | For suspend or reactivate actions |
| `first_name` | string | No | |
| `last_name` | string | No | |
| `phone_number` | string | No | |
| `privacy_settings` | object | No | Admin support use |

- Success Response: `200 OK`, Single Object containing updated `User`.
- Possible Error Responses: `400`, `401`, `403`, `404`, `409`
- Notes:
  - All admin changes should generate audit log entries.

## 19.3 Shelters

### `POST /shelters/`

- Purpose: Create the authenticated shelter user's shelter profile.
- Authentication Required: Yes
- Allowed Roles: Shelter, Admin
- Headers: `Accept`, `Content-Type: application/json`, `Authorization`
- Path Parameters: None
- Query Parameters: None
- Request Body:

| Field | Type | Required |
|---|---|---|
| `name` | string | Yes |
| `description` | string | No |
| `email` | string | Yes |
| `phone_number` | string | Yes |
| `website_url` | string | No |
| `city` | string | Yes |
| `state` | string | Yes |
| `address_line_1` | string | Yes |
| `address_line_2` | string | No |
| `postal_code` | string | No |

- Success Response: `201 Created`, Single Object containing `Shelter`.
- Possible Error Responses: `400`, `401`, `403`, `409`
- Notes:
  - One shelter profile per shelter account is recommended in V1.

### `GET /shelters/`

- Purpose: List shelters visible to the public.
- Authentication Required: No
- Allowed Roles: Public
- Headers: `Accept`
- Path Parameters: None
- Query Parameters:

| Parameter | Type | Notes |
|---|---|---|
| `page` | integer | |
| `page_size` | integer | |
| `search` | string | Search by shelter name, city, state |
| `ordering` | string | `name`, `created_at`, `verification_status` |
| `city` | string | |
| `state` | string | |
| `verification_status` | enum(`shelter_verification_status`) | Public clients should typically query `VERIFIED` |

- Request Body: None
- Success Response: `200 OK`, Paginated Response of `Shelter`.
- Possible Error Responses: `400`
- Notes:
  - Public listings should default to verified shelters only unless admin context is applied internally.

### `GET /shelters/me/`

- Purpose: Retrieve the authenticated shelter's own shelter profile.
- Authentication Required: Yes
- Allowed Roles: Shelter, Admin
- Headers: `Accept`, `Authorization`
- Path Parameters: None
- Query Parameters: None
- Request Body: None
- Success Response: `200 OK`, Single Object containing `Shelter`.
- Possible Error Responses: `401`, `403`, `404`
- Notes:
  - Includes verification status and publish eligibility.

### `PATCH /shelters/me/`

- Purpose: Partially update the authenticated shelter's shelter profile.
- Authentication Required: Yes
- Allowed Roles: Shelter, Admin
- Headers: `Accept`, `Content-Type: application/json`, `Authorization`
- Path Parameters: None
- Query Parameters: None
- Request Body:

| Field | Type | Required |
|---|---|---|
| `name` | string | No |
| `description` | string | No |
| `email` | string | No |
| `phone_number` | string | No |
| `website_url` | string | No |
| `city` | string | No |
| `state` | string | No |
| `address_line_1` | string | No |
| `address_line_2` | string | No |
| `postal_code` | string | No |

- Success Response: `200 OK`, Single Object containing updated `Shelter`.
- Possible Error Responses: `400`, `401`, `403`, `404`
- Notes:
  - Verification status is not directly editable here.

### `GET /shelters/{id}/`

- Purpose: Retrieve a shelter profile by id.
- Authentication Required: No
- Allowed Roles: Public
- Headers: `Accept`
- Path Parameters:

| Parameter | Type |
|---|---|
| `id` | UUID |

- Query Parameters: None
- Request Body: None
- Success Response: `200 OK`, Single Object containing `Shelter`.
- Possible Error Responses: `404`
- Notes:
  - Public access should resolve only to visible shelters.

## 19.4 Shelter Verification

### `POST /shelters/me/verifications/documents/`

- Purpose: Upload a verification document for the authenticated shelter.
- Authentication Required: Yes
- Allowed Roles: Shelter, Admin
- Headers: `Accept`, `Content-Type: multipart/form-data`, `Authorization`
- Path Parameters: None
- Query Parameters: None
- Request Body:

| Field | Type | Required | Notes |
|---|---|---|---|
| `document_type` | enum(`document_type`) | Yes | |
| `file` | file | Yes | PDF, JPEG, PNG up to 10 MB |

- Success Response: `201 Created`, Single Object containing `Verification Document`.
- Possible Error Responses: `400`, `401`, `403`, `415`
- Notes:
  - Documents may be uploaded before formal verification submission.

### `POST /shelters/me/verifications/`

- Purpose: Submit the shelter verification request for admin review.
- Authentication Required: Yes
- Allowed Roles: Shelter, Admin
- Headers: `Accept`, `Content-Type: application/json`, `Authorization`
- Path Parameters: None
- Query Parameters: None
- Request Body:

| Field | Type | Required | Notes |
|---|---|---|---|
| `document_ids` | array[UUID] | Yes | Uploaded document ids |
| `notes` | string | No | Optional submission notes |

- Success Response: `201 Created`, Single Object containing `Shelter Verification`.
- Possible Error Responses: `400`, `401`, `403`, `409`
- Notes:
  - Required document types should be validated server-side.
  - Re-submission after rejection or changes requested is allowed.

### `GET /shelters/me/verifications/`

- Purpose: List the authenticated shelter's verification requests.
- Authentication Required: Yes
- Allowed Roles: Shelter, Admin
- Headers: `Accept`, `Authorization`
- Path Parameters: None
- Query Parameters:

| Parameter | Type | Notes |
|---|---|---|
| `page` | integer | |
| `page_size` | integer | |
| `ordering` | string | `created_at`, `status`, `submitted_at` |
| `status` | enum(`shelter_verification_status`) | |

- Request Body: None
- Success Response: `200 OK`, Paginated Response of `Shelter Verification`.
- Possible Error Responses: `401`, `403`
- Notes:
  - Most implementations will return a small result set, but pagination remains standard.

### `GET /shelter-verifications/`

- Purpose: List shelter verification requests for admin review.
- Authentication Required: Yes
- Allowed Roles: Admin
- Headers: `Accept`, `Authorization`
- Path Parameters: None
- Query Parameters:

| Parameter | Type | Notes |
|---|---|---|
| `page` | integer | |
| `page_size` | integer | |
| `ordering` | string | `created_at`, `status`, `submitted_at` |
| `status` | enum(`shelter_verification_status`) | |
| `shelter_id` | UUID | |
| `search` | string | Search by shelter name |

- Request Body: None
- Success Response: `200 OK`, Paginated Response of `Shelter Verification`.
- Possible Error Responses: `401`, `403`
- Notes:
  - Primary admin queue for verification operations.

### `GET /shelter-verifications/{id}/`

- Purpose: Retrieve one shelter verification request.
- Authentication Required: Yes
- Allowed Roles: Admin
- Headers: `Accept`, `Authorization`
- Path Parameters:

| Parameter | Type |
|---|---|
| `id` | UUID |

- Query Parameters: None
- Request Body: None
- Success Response: `200 OK`, Single Object containing `Shelter Verification`.
- Possible Error Responses: `401`, `403`, `404`
- Notes:
  - Should include related documents and shelter summary.

### `PATCH /shelter-verifications/{id}/`

- Purpose: Review and update a shelter verification request.
- Authentication Required: Yes
- Allowed Roles: Admin
- Headers: `Accept`, `Content-Type: application/json`, `Authorization`
- Path Parameters:

| Parameter | Type |
|---|---|
| `id` | UUID |

- Query Parameters: None
- Request Body:

| Field | Type | Required | Notes |
|---|---|---|---|
| `status` | enum(`shelter_verification_status`) | Yes | `UNDER_REVIEW`, `VERIFIED`, `REJECTED`, `CHANGES_REQUESTED` |
| `review_notes` | string | No | Required for rejection or change request by policy |

- Success Response: `200 OK`, Single Object containing updated `Shelter Verification`.
- Possible Error Responses: `400`, `401`, `403`, `404`, `409`
- Notes:
  - On `VERIFIED`, shelter publish privileges must be enabled.
  - All review actions must be audit logged.

## 19.5 Pets

### `GET /pets/`

- Purpose: Browse, search, and filter pet listings.
- Authentication Required: No
- Allowed Roles: Public
- Headers: `Accept`
- Path Parameters: None
- Query Parameters:

| Parameter | Type | Notes |
|---|---|---|
| `page` | integer | |
| `page_size` | integer | |
| `search` | string | Search by pet name or breed |
| `ordering` | string | `created_at`, `name`, `age_months` |
| `species` | enum(`species`) | |
| `breed` | string | |
| `gender` | enum(`gender`) | |
| `size` | enum(`size`) | |
| `city` | string | |
| `state` | string | |
| `status` | enum(`pet_status`) | Public clients should use `AVAILABLE` |
| `shelter_id` | UUID | |
| `special_needs` | boolean | Optional V1 filter aligned to FRS |
| `age_months__gte` | integer | Recommended filter |
| `age_months__lte` | integer | Recommended filter |

- Request Body: None
- Success Response: `200 OK`, Paginated Response of `Pet`.
- Possible Error Responses: `400`
- Notes:
  - This endpoint replaces any dedicated pet search endpoint.
  - Public responses should exclude soft-deleted and non-visible listings.

### `POST /pets/`

- Purpose: Create a pet listing.
- Authentication Required: Yes
- Allowed Roles: Verified Shelter, Admin
- Headers: `Accept`, `Content-Type: application/json`, `Authorization`
- Path Parameters: None
- Query Parameters: None
- Request Body:

| Field | Type | Required |
|---|---|---|
| `name` | string | Yes |
| `species` | enum(`species`) | Yes |
| `breed` | string | Yes |
| `age_months` | integer | Yes |
| `gender` | enum(`gender`) | Yes |
| `size` | enum(`size`) | Yes |
| `description` | string | No |
| `health_summary` | string | Yes |
| `temperament_summary` | string | No |
| `adoption_requirements` | string | No |
| `special_needs` | boolean | No |
| `city` | string | Yes |
| `state` | string | Yes |
| `status` | enum(`pet_status`) | No | Defaults to `AVAILABLE` or `DRAFT` depending on workflow |

- Success Response: `201 Created`, Single Object containing `Pet`.
- Possible Error Responses: `400`, `401`, `403`, `409`
- Notes:
  - Shelter must be verified before publishing.
  - If creation without publication is supported, `status=DRAFT` is permitted.

### `GET /pets/{id}/`

- Purpose: Retrieve pet listing details.
- Authentication Required: No
- Allowed Roles: Public
- Headers: `Accept`
- Path Parameters:

| Parameter | Type |
|---|---|
| `id` | UUID |

- Query Parameters: None
- Request Body: None
- Success Response: `200 OK`, Single Object containing `Pet` with shelter summary and images.
- Possible Error Responses: `404`
- Notes:
  - Pet detail must expose all core pet attributes required by V1.

### `PATCH /pets/{id}/`

- Purpose: Partially update a pet listing, including status changes.
- Authentication Required: Yes
- Allowed Roles: Owning Shelter, Admin
- Headers: `Accept`, `Content-Type: application/json`, `Authorization`
- Path Parameters:

| Parameter | Type |
|---|---|
| `id` | UUID |

- Query Parameters: None
- Request Body:

| Field | Type | Required | Notes |
|---|---|---|---|
| `name` | string | No | |
| `species` | enum(`species`) | No | |
| `breed` | string | No | |
| `age_months` | integer | No | |
| `gender` | enum(`gender`) | No | |
| `size` | enum(`size`) | No | |
| `description` | string | No | |
| `health_summary` | string | No | |
| `temperament_summary` | string | No | |
| `adoption_requirements` | string | No | |
| `special_needs` | boolean | No | |
| `city` | string | No | |
| `state` | string | No | |
| `status` | enum(`pet_status`) | No | |

- Success Response: `200 OK`, Single Object containing updated `Pet`.
- Possible Error Responses: `400`, `401`, `403`, `404`, `409`
- Notes:
  - Invalid status transitions must be rejected.
  - When a pet is moved to `ADOPTED`, related open applications should be closed according to business rules.

### `DELETE /pets/{id}/`

- Purpose: Soft delete or deactivate a pet listing.
- Authentication Required: Yes
- Allowed Roles: Owning Shelter, Admin
- Headers: `Accept`, `Authorization`
- Path Parameters:

| Parameter | Type |
|---|---|
| `id` | UUID |

- Query Parameters: None
- Request Body: None
- Success Response: `204 No Content`
- Possible Error Responses: `401`, `403`, `404`, `409`
- Notes:
  - Deletion must be blocked if an approved adoption is in progress.
  - Soft deletion should map to `DEACTIVATED` and/or `deleted_at`.

## 19.6 Pet Images

### `GET /pets/{pet_id}/images/`

- Purpose: List images for a pet.
- Authentication Required: No
- Allowed Roles: Public
- Headers: `Accept`
- Path Parameters:

| Parameter | Type |
|---|---|
| `pet_id` | UUID |

- Query Parameters:

| Parameter | Type | Notes |
|---|---|---|
| `ordering` | string | `display_order`, `created_at` |

- Request Body: None
- Success Response: `200 OK`, Single Object containing array of `Pet Image`.
- Possible Error Responses: `404`
- Notes:
  - Responses should include only active images.

### `POST /pets/{pet_id}/images/`

- Purpose: Upload an image for a pet listing.
- Authentication Required: Yes
- Allowed Roles: Owning Shelter, Admin
- Headers: `Accept`, `Content-Type: multipart/form-data`, `Authorization`
- Path Parameters:

| Parameter | Type |
|---|---|
| `pet_id` | UUID |

- Query Parameters: None
- Request Body:

| Field | Type | Required | Notes |
|---|---|---|---|
| `image` | file | Yes | JPEG, PNG, WEBP up to 5 MB |
| `caption` | string | No | |
| `display_order` | integer | No | |
| `is_primary` | boolean | No | |

- Success Response: `201 Created`, Single Object containing `Pet Image`.
- Possible Error Responses: `400`, `401`, `403`, `404`, `409`, `415`
- Notes:
  - Maximum of 10 images per pet.

### `PATCH /pets/{pet_id}/images/{id}/`

- Purpose: Update pet image metadata such as order, caption, or primary flag.
- Authentication Required: Yes
- Allowed Roles: Owning Shelter, Admin
- Headers: `Accept`, `Content-Type: application/json`, `Authorization`
- Path Parameters:

| Parameter | Type |
|---|---|
| `pet_id` | UUID |
| `id` | UUID |

- Query Parameters: None
- Request Body:

| Field | Type | Required |
|---|---|---|
| `caption` | string | No |
| `display_order` | integer | No |
| `is_primary` | boolean | No |

- Success Response: `200 OK`, Single Object containing updated `Pet Image`.
- Possible Error Responses: `400`, `401`, `403`, `404`, `409`
- Notes:
  - If `is_primary=true`, the system should enforce a single primary image.

### `DELETE /pets/{pet_id}/images/{id}/`

- Purpose: Soft delete a pet image.
- Authentication Required: Yes
- Allowed Roles: Owning Shelter, Admin
- Headers: `Accept`, `Authorization`
- Path Parameters:

| Parameter | Type |
|---|---|
| `pet_id` | UUID |
| `id` | UUID |

- Query Parameters: None
- Request Body: None
- Success Response: `204 No Content`
- Possible Error Responses: `401`, `403`, `404`
- Notes:
  - Soft delete is recommended to support operational recovery.

## 19.7 Adoption Applications

### `POST /applications/`

- Purpose: Create an adoption application.
- Authentication Required: Yes
- Allowed Roles: Adopter, Admin
- Headers: `Accept`, `Content-Type: application/json`, `Authorization`
- Path Parameters: None
- Query Parameters: None
- Request Body:

| Field | Type | Required |
|---|---|---|
| `pet_id` | UUID | Yes |
| `home_environment` | string | Yes |
| `household_members` | string | Yes |
| `prior_pet_experience` | string | Yes |
| `availability_for_home_visit` | boolean | Yes |
| `additional_notes` | string | No |

- Success Response: `201 Created`, Single Object containing `Adoption Application`.
- Possible Error Responses: `400`, `401`, `403`, `404`, `409`
- Notes:
  - Pet must be `AVAILABLE`.
  - Adopter may not exceed 3 concurrent pending or under-review applications.

### `GET /applications/`

- Purpose: List adoption applications visible to the requester.
- Authentication Required: Yes
- Allowed Roles: Adopter, Shelter, Admin
- Headers: `Accept`, `Authorization`
- Path Parameters: None
- Query Parameters:

| Parameter | Type | Notes |
|---|---|---|
| `page` | integer | |
| `page_size` | integer | |
| `ordering` | string | `created_at`, `submitted_at`, `status` |
| `status` | enum(`application_status`) | |
| `pet_id` | UUID | |
| `shelter_id` | UUID | Admin or shelter-owned only |
| `applicant_id` | UUID | Admin only |

- Request Body: None
- Success Response: `200 OK`, Paginated Response of `Adoption Application`.
- Possible Error Responses: `401`, `403`
- Notes:
  - Adopters see only their own applications.
  - Shelters see only applications for their own pets.

### `GET /applications/{id}/`

- Purpose: Retrieve a single adoption application.
- Authentication Required: Yes
- Allowed Roles: Adopter, Shelter, Admin
- Headers: `Accept`, `Authorization`
- Path Parameters:

| Parameter | Type |
|---|---|
| `id` | UUID |

- Query Parameters: None
- Request Body: None
- Success Response: `200 OK`, Single Object containing `Adoption Application`.
- Possible Error Responses: `401`, `403`, `404`
- Notes:
  - Ownership and organization checks are mandatory.

### `PATCH /applications/{id}/`

- Purpose: Update an adoption application.
- Authentication Required: Yes
- Allowed Roles: Adopter, Shelter, Admin
- Headers: `Accept`, `Content-Type: application/json`, `Authorization`
- Path Parameters:

| Parameter | Type |
|---|---|
| `id` | UUID |

- Query Parameters: None
- Request Body:

Adopter self-update, draft only:

| Field | Type | Required |
|---|---|---|
| `home_environment` | string | No |
| `household_members` | string | No |
| `prior_pet_experience` | string | No |
| `availability_for_home_visit` | boolean | No |
| `additional_notes` | string | No |
| `status` | enum(`application_status`) | No |

Shelter or admin review update:

| Field | Type | Required | Notes |
|---|---|---|---|
| `status` | enum(`application_status`) | Yes | `UNDER_REVIEW`, `APPROVED`, `REJECTED`, `CLOSED` |
| `review_notes` | string | No | Recommended for reject or close |

- Success Response: `200 OK`, Single Object containing updated `Adoption Application`.
- Possible Error Responses: `400`, `401`, `403`, `404`, `409`
- Notes:
  - Adopters may only edit their own `DRAFT` applications.
  - Shelters may only review applications linked to their own pets.
  - Approval should move the related pet to a non-public hold state.

### `GET /applications/{id}/history/`

- Purpose: Retrieve status and workflow history for an application.
- Authentication Required: Yes
- Allowed Roles: Adopter, Shelter, Admin
- Headers: `Accept`, `Authorization`
- Path Parameters:

| Parameter | Type |
|---|---|
| `id` | UUID |

- Query Parameters:

| Parameter | Type | Notes |
|---|---|---|
| `ordering` | string | `created_at`, `-created_at` |

- Request Body: None
- Success Response: `200 OK`, Single Object containing array of `Application History Event`.
- Possible Error Responses: `401`, `403`, `404`
- Notes:
  - This endpoint is the audit trail for application status changes.

## 19.8 Notifications

### `GET /notifications/`

- Purpose: List notifications for the authenticated user.
- Authentication Required: Yes
- Allowed Roles: Adopter, Shelter, Admin
- Headers: `Accept`, `Authorization`
- Path Parameters: None
- Query Parameters:

| Parameter | Type | Notes |
|---|---|---|
| `page` | integer | |
| `page_size` | integer | |
| `ordering` | string | `created_at`, `-created_at` |
| `is_read` | boolean | |
| `type` | enum(`notification_type`) | |

- Request Body: None
- Success Response: `200 OK`, Paginated Response of `Notification`.
- Possible Error Responses: `401`
- Notes:
  - V1 requires in-app notification center support.

### `GET /notifications/unread-count/`

- Purpose: Retrieve unread notification count for the authenticated user.
- Authentication Required: Yes
- Allowed Roles: Adopter, Shelter, Admin
- Headers: `Accept`, `Authorization`
- Path Parameters: None
- Query Parameters: None
- Request Body: None
- Success Response: `200 OK`, Single Object with:

| Field | Type |
|---|---|
| `unread_count` | integer |

- Possible Error Responses: `401`
- Notes:
  - Intended for lightweight badge polling.

### `PATCH /notifications/{id}/`

- Purpose: Update a notification read state.
- Authentication Required: Yes
- Allowed Roles: Adopter, Shelter, Admin
- Headers: `Accept`, `Content-Type: application/json`, `Authorization`
- Path Parameters:

| Parameter | Type |
|---|---|
| `id` | UUID |

- Query Parameters: None
- Request Body:

| Field | Type | Required |
|---|---|---|
| `is_read` | boolean | Yes |

- Success Response: `200 OK`, Single Object containing updated `Notification`.
- Possible Error Responses: `400`, `401`, `403`, `404`
- Notes:
  - Only the notification owner may update it.

### `POST /notifications/read-all/`

- Purpose: Mark all notifications as read for the authenticated user.
- Authentication Required: Yes
- Allowed Roles: Adopter, Shelter, Admin
- Headers: `Accept`, `Authorization`
- Path Parameters: None
- Query Parameters: None
- Request Body: None
- Success Response: `200 OK`, Single Object with:

| Field | Type |
|---|---|
| `updated_count` | integer |

- Possible Error Responses: `401`
- Notes:
  - Action endpoint retained for efficiency and explicit V1 scope support.

### `DELETE /notifications/{id}/`

- Purpose: Soft delete a notification from the user's notification center.
- Authentication Required: Yes
- Allowed Roles: Adopter, Shelter, Admin
- Headers: `Accept`, `Authorization`
- Path Parameters:

| Parameter | Type |
|---|---|
| `id` | UUID |

- Query Parameters: None
- Request Body: None
- Success Response: `204 No Content`
- Possible Error Responses: `401`, `403`, `404`
- Notes:
  - This only affects user visibility, not system audit records.

## 19.9 Admin

### `GET /admin/dashboard/`

- Purpose: Retrieve admin dashboard summary metrics for V1 operations.
- Authentication Required: Yes
- Allowed Roles: Admin
- Headers: `Accept`, `Authorization`
- Path Parameters: None
- Query Parameters:

| Parameter | Type | Notes |
|---|---|---|
| `date_from` | date | Optional |
| `date_to` | date | Optional |

- Request Body: None
- Success Response: `200 OK`, Single Object containing:

| Field | Type |
|---|---|
| `total_users` | integer |
| `total_shelters` | integer |
| `total_verified_shelters` | integer |
| `total_pending_shelter_verifications` | integer |
| `total_active_pet_listings` | integer |
| `total_applications` | integer |
| `generated_at` | datetime |

- Possible Error Responses: `401`, `403`
- Notes:
  - This is an operational dashboard, not AI analytics.

### `GET /admin/users/`

- Purpose: List users in admin namespace.
- Authentication Required: Yes
- Allowed Roles: Admin
- Headers: `Accept`, `Authorization`
- Path Parameters: None
- Query Parameters: Same as `GET /users/`
- Request Body: None
- Success Response: `200 OK`, Paginated Response of `User`.
- Possible Error Responses: `401`, `403`
- Notes:
  - May map to the same underlying service as `/users/` with an admin tag in OpenAPI.

### `GET /admin/shelters/`

- Purpose: List shelters in admin namespace.
- Authentication Required: Yes
- Allowed Roles: Admin
- Headers: `Accept`, `Authorization`
- Path Parameters: None
- Query Parameters:

| Parameter | Type | Notes |
|---|---|---|
| `page` | integer | |
| `page_size` | integer | |
| `search` | string | |
| `ordering` | string | `created_at`, `name`, `verification_status` |
| `verification_status` | enum(`shelter_verification_status`) | |
| `city` | string | |
| `state` | string | |

- Request Body: None
- Success Response: `200 OK`, Paginated Response of `Shelter`.
- Possible Error Responses: `401`, `403`
- Notes:
  - Intended for operational review and moderation support.

### `GET /admin/applications/`

- Purpose: List adoption applications in admin namespace.
- Authentication Required: Yes
- Allowed Roles: Admin
- Headers: `Accept`, `Authorization`
- Path Parameters: None
- Query Parameters:

| Parameter | Type | Notes |
|---|---|---|
| `page` | integer | |
| `page_size` | integer | |
| `ordering` | string | `created_at`, `submitted_at`, `status` |
| `status` | enum(`application_status`) | |
| `pet_id` | UUID | |
| `shelter_id` | UUID | |
| `applicant_id` | UUID | |

- Request Body: None
- Success Response: `200 OK`, Paginated Response of `Adoption Application`.
- Possible Error Responses: `401`, `403`
- Notes:
  - Supports platform monitoring, not day-to-day shelter review.

### `GET /admin/audit-logs/`

- Purpose: List admin audit log entries.
- Authentication Required: Yes
- Allowed Roles: Admin
- Headers: `Accept`, `Authorization`
- Path Parameters: None
- Query Parameters:

| Parameter | Type | Notes |
|---|---|---|
| `page` | integer | |
| `page_size` | integer | |
| `ordering` | string | `created_at`, `-created_at` |
| `actor_id` | UUID | |
| `action` | enum(`audit_action`) | |
| `resource_type` | string | |
| `resource_id` | UUID | |
| `created_at__gte` | datetime | |
| `created_at__lte` | datetime | |

- Request Body: None
- Success Response: `200 OK`, Paginated Response of `Audit Log`.
- Possible Error Responses: `401`, `403`
- Notes:
  - Covers moderation, verification, and sensitive admin changes.

### `PATCH /admin/pets/{id}/moderation/`

- Purpose: Apply admin moderation updates to a pet listing.
- Authentication Required: Yes
- Allowed Roles: Admin
- Headers: `Accept`, `Content-Type: application/json`, `Authorization`
- Path Parameters:

| Parameter | Type |
|---|---|
| `id` | UUID |

- Query Parameters: None
- Request Body:

| Field | Type | Required | Notes |
|---|---|---|---|
| `status` | enum(`pet_status`) | No | For moderation-driven deactivation or restoration |
| `moderation_notes` | string | Yes | Required rationale |

- Success Response: `200 OK`, Single Object containing updated `Pet`.
- Possible Error Responses: `400`, `401`, `403`, `404`, `409`
- Notes:
  - This endpoint exists because moderation is an administrative action, not a standard shelter edit.
  - All moderation actions must create audit logs.

## 19.10 Analytics

### `GET /analytics/summary/`

- Purpose: Retrieve platform-level V1 summary analytics.
- Authentication Required: Yes
- Allowed Roles: Admin
- Headers: `Accept`, `Authorization`
- Path Parameters: None
- Query Parameters:

| Parameter | Type | Notes |
|---|---|---|
| `date_from` | date | Optional |
| `date_to` | date | Optional |

- Request Body: None
- Success Response: `200 OK`, Single Object containing `Analytics Summary`.
- Possible Error Responses: `401`, `403`
- Notes:
  - V1 analytics are summary metrics only.
  - No predictive, AI-driven, premium, or marketplace analytics are included.

### `GET /analytics/shelters/me/`

- Purpose: Retrieve summary analytics for the authenticated shelter.
- Authentication Required: Yes
- Allowed Roles: Shelter, Admin
- Headers: `Accept`, `Authorization`
- Path Parameters: None
- Query Parameters:

| Parameter | Type | Notes |
|---|---|---|
| `date_from` | date | Optional |
| `date_to` | date | Optional |

- Request Body: None
- Success Response: `200 OK`, Single Object containing:

| Field | Type |
|---|---|
| `shelter_id` | UUID |
| `total_pet_listings` | integer |
| `total_active_pet_listings` | integer |
| `total_applications_received` | integer |
| `total_submitted_applications` | integer |
| `total_under_review_applications` | integer |
| `total_approved_applications` | integer |
| `total_rejected_applications` | integer |
| `total_completed_adoptions` | integer |
| `generated_at` | datetime |

- Possible Error Responses: `401`, `403`, `404`
- Notes:
  - This endpoint implements V1 basic analytics only.

## 20. Complete Endpoint Reference Table

| Method | Endpoint | Tag | Auth | Roles |
|---|---|---|---|---|
| `POST` | `/api/v1/auth/register/` | Authentication | No | Public |
| `POST` | `/api/v1/auth/login/` | Authentication | No | Public |
| `POST` | `/api/v1/auth/refresh/` | Authentication | No | Public |
| `POST` | `/api/v1/auth/logout/` | Authentication | Yes | Adopter, Shelter, Admin |
| `POST` | `/api/v1/auth/verify-email/` | Authentication | No | Public |
| `POST` | `/api/v1/auth/resend-verification/` | Authentication | No | Public |
| `POST` | `/api/v1/auth/forgot-password/` | Authentication | No | Public |
| `POST` | `/api/v1/auth/reset-password/` | Authentication | No | Public |
| `POST` | `/api/v1/auth/change-password/` | Authentication | Yes | Adopter, Shelter, Admin |
| `GET` | `/api/v1/users/me/` | Users | Yes | Adopter, Shelter, Admin |
| `PATCH` | `/api/v1/users/me/` | Users | Yes | Adopter, Shelter, Admin |
| `PATCH` | `/api/v1/users/me/avatar/` | Users | Yes | Adopter, Shelter, Admin |
| `DELETE` | `/api/v1/users/me/` | Users | Yes | Adopter, Shelter, Admin |
| `GET` | `/api/v1/users/` | Users | Yes | Admin |
| `GET` | `/api/v1/users/{id}/` | Users | Yes | Admin |
| `PATCH` | `/api/v1/users/{id}/` | Users | Yes | Admin |
| `POST` | `/api/v1/shelters/` | Shelters | Yes | Shelter, Admin |
| `GET` | `/api/v1/shelters/` | Shelters | No | Public |
| `GET` | `/api/v1/shelters/me/` | Shelters | Yes | Shelter, Admin |
| `PATCH` | `/api/v1/shelters/me/` | Shelters | Yes | Shelter, Admin |
| `GET` | `/api/v1/shelters/{id}/` | Shelters | No | Public |
| `POST` | `/api/v1/shelters/me/verifications/documents/` | Verification | Yes | Shelter, Admin |
| `POST` | `/api/v1/shelters/me/verifications/` | Verification | Yes | Shelter, Admin |
| `GET` | `/api/v1/shelters/me/verifications/` | Verification | Yes | Shelter, Admin |
| `GET` | `/api/v1/shelter-verifications/` | Verification | Yes | Admin |
| `GET` | `/api/v1/shelter-verifications/{id}/` | Verification | Yes | Admin |
| `PATCH` | `/api/v1/shelter-verifications/{id}/` | Verification | Yes | Admin |
| `GET` | `/api/v1/pets/` | Pets | No | Public |
| `POST` | `/api/v1/pets/` | Pets | Yes | Verified Shelter, Admin |
| `GET` | `/api/v1/pets/{id}/` | Pets | No | Public |
| `PATCH` | `/api/v1/pets/{id}/` | Pets | Yes | Owning Shelter, Admin |
| `DELETE` | `/api/v1/pets/{id}/` | Pets | Yes | Owning Shelter, Admin |
| `GET` | `/api/v1/pets/{pet_id}/images/` | Pet Images | No | Public |
| `POST` | `/api/v1/pets/{pet_id}/images/` | Pet Images | Yes | Owning Shelter, Admin |
| `PATCH` | `/api/v1/pets/{pet_id}/images/{id}/` | Pet Images | Yes | Owning Shelter, Admin |
| `DELETE` | `/api/v1/pets/{pet_id}/images/{id}/` | Pet Images | Yes | Owning Shelter, Admin |
| `POST` | `/api/v1/applications/` | Applications | Yes | Adopter, Admin |
| `GET` | `/api/v1/applications/` | Applications | Yes | Adopter, Shelter, Admin |
| `GET` | `/api/v1/applications/{id}/` | Applications | Yes | Adopter, Shelter, Admin |
| `PATCH` | `/api/v1/applications/{id}/` | Applications | Yes | Adopter, Shelter, Admin |
| `GET` | `/api/v1/applications/{id}/history/` | Applications | Yes | Adopter, Shelter, Admin |
| `GET` | `/api/v1/notifications/` | Notifications | Yes | Adopter, Shelter, Admin |
| `GET` | `/api/v1/notifications/unread-count/` | Notifications | Yes | Adopter, Shelter, Admin |
| `PATCH` | `/api/v1/notifications/{id}/` | Notifications | Yes | Adopter, Shelter, Admin |
| `POST` | `/api/v1/notifications/read-all/` | Notifications | Yes | Adopter, Shelter, Admin |
| `DELETE` | `/api/v1/notifications/{id}/` | Notifications | Yes | Adopter, Shelter, Admin |
| `GET` | `/api/v1/admin/dashboard/` | Admin | Yes | Admin |
| `GET` | `/api/v1/admin/users/` | Admin | Yes | Admin |
| `GET` | `/api/v1/admin/shelters/` | Admin | Yes | Admin |
| `GET` | `/api/v1/admin/applications/` | Admin | Yes | Admin |
| `GET` | `/api/v1/admin/audit-logs/` | Admin | Yes | Admin |
| `PATCH` | `/api/v1/admin/pets/{id}/moderation/` | Admin | Yes | Admin |
| `GET` | `/api/v1/analytics/summary/` | Analytics | Yes | Admin |
| `GET` | `/api/v1/analytics/shelters/me/` | Analytics | Yes | Shelter, Admin |

## 21. Versioning Strategy

- Version is encoded in the URL path.
- V1 contracts are append-only for backward-compatible changes.
- Breaking schema or behavior changes require a new version.
- Deprecated fields and endpoints should be clearly marked in generated OpenAPI descriptions before removal.

## 22. Naming Standards

- Use plural nouns for collection resources.
- Use `snake_case` for all JSON field names and query parameters.
- Use `_id` suffix for related identifiers.
- Use uppercase enum constants in schemas and examples.

## 23. Pagination Standard

- DRF page-number pagination is the platform standard.
- All list endpoints return the standard paginated response envelope.
- Clients must not assume fixed page lengths.

## 24. Filtering Standard

- Filtering is implemented through query parameters.
- All unsupported filter parameters should return `400 Bad Request`.
- Access control rules still apply after filtering.

## 25. Sorting Standard

- Sorting is implemented with `ordering`.
- Only documented fields are sortable.
- Invalid `ordering` fields should return `400 Bad Request`.

## 26. Search Standard

- Search is implemented with `search`.
- Search should be applied only to documented searchable fields.
- Pet search is integrated into `GET /pets/`; no dedicated pet search endpoint exists in V1.

## 27. Upload Standard

- Upload endpoints must enforce type and size validation before storage.
- Files should be virus-scanned in production environments where infrastructure supports it.
- Uploaded file references in API responses should use absolute media URLs.

## 28. Rate Limiting

- Apply DRF throttling at view or scope level.
- Authentication and upload endpoints require stricter throttles than general authenticated reads.
- Repeated abuse events should be audit logged for operational review.

## 29. OpenAPI Implementation Notes

- Generate schema with `drf-spectacular`.
- Apply tags exactly as defined in Section 18.
- Promote reusable serializers and components for:
  - success envelope
  - paginated envelope
  - error envelope
  - enums
  - shared resource schemas
- Document multipart endpoints explicitly in OpenAPI with binary file fields.
- Mark all UUID path parameters with `format: uuid`.

## 30. V1 Scope Guardrails

- This specification documents only PawMatch V1 scope.
- Excluded from this contract:
  - AI pet matching
  - AI health assistant
  - AI image recognition
  - behavior prediction
  - lost pet finder
  - nutrition planner
  - training coach
  - veterinarian features
  - health records
  - marketplace
  - payments
  - community
  - events
  - premium subscriptions
  - predictive or AI analytics
