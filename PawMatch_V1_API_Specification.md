# PawMatch V1 REST API Specification

**Document Title:** PawMatch V1 REST API Specification  
**Base URL:** `/api/v1/`  
**Authentication:** JSON Web Token (JWT) via `Authorization: Bearer <token>`  
**Response Format:** JSON (`application/json`)  
**Identifier Standard:** UUIDv4  
**Framework Compatibility:** Django REST Framework (DRF) & `drf-spectacular` (OpenAPI 3.0)  
**Date:** 29 July 2026  
**Source of Truth:** PawMatch V1 Release Scope & Functional Requirements Specification (FRS)

---

## 1. Architectural Standards & Design Conventions

### 1.1 Base URL & Trailing Slashes
All API endpoints are versioned with trailing slash enforcement following standard Django REST Framework URL routing:
```
https://api.pawmatch.org/api/v1/
```

### 1.2 Global Request Headers
- `Content-Type: application/json` (Required for JSON request bodies)
- `Authorization: Bearer <JWT_TOKEN>` (Required for authenticated endpoints)
- `Accept: application/json`I’m writing the specification file now. The document is organized as an implementation contract first, with reusable schemas and enums up front so the endpoint sections
  can stay consistent and DRF/OpenAPI-friendly

### 1.3 Data Formatting Standards
- **Identifiers:** UUIDv4 strings (e.g., `550e8400-e29b-41d4-a716-446655440000`).
- **Timestamps:** ISO-8601 UTC standard strings (e.g., `2026-07-29T10:00:00Z`).
- **Property Naming:** `snake_case` across all request/response payload attributes and URL query parameters.
- **HTTP Methods:**
  - `GET`: Safe data retrieval without side effects.
  - `POST`: Resource creation or action handling.
  - `PATCH`: Partial resource state updates.
  - `PUT`: Complete resource replacements.
  - `DELETE`: Resource removal (soft deletion applied where audit compliance is required).

---

## 2. Enumerations

### 2.1 `UserRole`
| Value | Description |
|---|---|
| `Admin` | Platform administrator with full access |
| `Shelter` | Organization managing shelter profile and pet listings |
| `Adopter` | User searching pets and submitting adoption applications |

### 2.2 `ShelterVerificationStatus`
| Value | Description |
|---|---|
| `Unverified` | Initial state upon shelter account creation |
| `Pending` | Verification request and documents submitted for admin review |
| `Verified` | Approved by admin; authorized to publish pet listings |
| `Rejected` | Verification request rejected by admin |

### 2.3 `PetStatus`
| Value | Description |
|---|---|
| `Available` | Open for adoption applications |
| `Pending Adoption` | Application selected; adoption finalization in progress |
| `Adopted` | Pet successfully adopted |
| `Deactivated` | Listing hidden/soft-deleted by shelter or admin |

### 2.4 `ApplicationStatus`
| Value | Description |
|---|---|
| `Submitted` | Initial application submission |
| `Under Review` | Application under active evaluation by shelter |
| `Approved` | Application approved by shelter |
| `Rejected` | Application declined by shelter |
| `Closed` | Adoption workflow finalized or application cancelled |

### 2.5 `NotificationType`
| Value | Description |
|---|---|
| `ACCOUNT_CONFIRMATION` | Welcome and email verification notification |
| `PASSWORD_RESET` | Password reset request notification |
| `SHELTER_VERIFICATION_STATUS` | Shelter verification decision notification |
| `APPLICATION_SUBMITTED` | Confirmation of application submission |
| `APPLICATION_STATUS_UPDATE` | Notice of adoption application status change |

### 2.6 `Gender`
| Value | Description |
|---|---|
| `Male` | Male animal |
| `Female` | Female animal |

### 2.7 `Species`
| Value | Description |
|---|---|
| `Dog` | Canine |
| `Cat` | Feline |
| `Bird` | Avian |
| `Rabbit` | Lagomorph |
| `Other` | Other animal species |

### 2.8 `Size`
| Value | Description |
|---|---|
| `Small` | Under 20 lbs / 9 kg |
| `Medium` | 20–50 lbs / 9–23 kg |
| `Large` | 50–90 lbs / 23–41 kg |
| `Extra Large` | Over 90 lbs / 41 kg |

### 2.9 `DocumentType`
| Value | Description |
|---|---|
| `Registration_Certificate` | Legal organization registration document |
| `Tax_ID_Proof` | Tax identification or non-profit proof |
| `Operating_License` | Animal shelter operating license |

---

## 3. Response Envelopes & Error Handling

### 3.1 Standard Single Item Response Envelope
```json
{
  "status": "success",
  "data": {}
}
```

### 3.2 Standard Paginated List Response Envelope (DRF Style)
All collection endpoints use consistent page-number pagination query parameters:
- `page` (integer, default: 1): Page number.
- `page_size` (integer, default: 20, max: 100): Page size limit.
- `search` (string, optional): Global text search keyword.
- `ordering` (string, optional): Field ordering (e.g., `-created_at`, `name`).

```json
{
  "status": "success",
  "data": {
    "count": 100,
    "next": "https://api.pawmatch.org/api/v1/pets/?page=2&page_size=20",
    "previous": null,
    "results": []
  }
}
```

### 3.3 Common Error Response Schema
```json
{
  "status": "error",
  "code": "ERROR_CODE",
  "message": "Human-readable summary message.",
  "errors": [
    {
      "field": "field_name",
      "message": "Specific field validation message."
    }
  ],
  "timestamp": "2026-07-29T10:00:00Z"
}
```

### 3.4 Reusable Error Codes
| HTTP Status | Error Code | Description |
|---|---|---|
| `400 Bad Request` | `BAD_REQUEST` | Malformed JSON or invalid parameters |
| `401 Unauthorized` | `AUTHENTICATION_FAILED` | Token missing, invalid, or expired |
| `403 Forbidden` | `PERMISSION_DENIED` | Insufficient RBAC role permissions |
| `404 Not Found` | `NOT_FOUND` | Target resource UUID does not exist |
| `409 Conflict` | `RESOURCE_CONFLICT` | Unique constraint violation (e.g. duplicate email) |
| `422 Unprocessable Entity` | `VALIDATION_ERROR` | Request body validation failure |
| `500 Internal Server Error` | `INTERNAL_SERVER_ERROR` | Unhandled server exception |

---

## 4. API Modules & Endpoints

---

### 4.1 Authentication Module

#### 4.1.1 Register User
- **Endpoint:** `/api/v1/auth/register/`
- **HTTP Method:** `POST`
- **Description:** Registers a new user account (Adopter or Shelter role).
- **Authentication Required:** No
- **Allowed Roles:** Public (Unauthenticated)
- **Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "first_name": "Jane",
  "last_name": "Doe",
  "phone": "+1234567890",
  "role": "Adopter"
}
```
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `201 Created`
```json
{
  "status": "success",
  "data": {
    "id": "a3bb189e-8bf9-3888-9912-ace4e6543001",
    "email": "user@example.com",
    "first_name": "Jane",
    "last_name": "Doe",
    "phone": "+1234567890",
    "role": "Adopter",
    "is_active": true,
    "is_email_verified": false,
    "created_at": "2026-07-29T10:00:00Z"
  }
}
```
- **Error Responses:** `400 Bad Request`, `409 Conflict`, `422 Unprocessable Entity`
- **Notes:** Allowed `role` values: `Adopter`, `Shelter`. `Admin` accounts cannot be self-registered. Triggers email verification workflow.

---

#### 4.1.2 Login User
- **Endpoint:** `/api/v1/auth/login/`
- **HTTP Method:** `POST`
- **Description:** Authenticates user credentials and issues JWT access and refresh tokens.
- **Authentication Required:** No
- **Allowed Roles:** Public (Unauthenticated)
- **Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "d98213e4-8bf9-3888-9912-ace4e6543999",
    "token_type": "Bearer",
    "expires_in": 3600,
    "user": {
      "id": "a3bb189e-8bf9-3888-9912-ace4e6543001",
      "email": "user@example.com",
      "first_name": "Jane",
      "last_name": "Doe",
      "role": "Adopter"
    }
  }
}
```
- **Error Responses:** `401 Unauthorized`, `403 Forbidden`
- **Notes:** Returns access token (1-hour validity) and refresh token.

---

#### 4.1.3 Refresh Access Token
- **Endpoint:** `/api/v1/auth/refresh/`
- **HTTP Method:** `POST`
- **Description:** Obtains a fresh access token using a valid refresh token.
- **Authentication Required:** No
- **Allowed Roles:** Public (Unauthenticated)
- **Request Body:**
```json
{
  "refresh_token": "d98213e4-8bf9-3888-9912-ace4e6543999"
}
```
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 3600
  }
}
```
- **Error Responses:** `401 Unauthorized`
- **Notes:** Supports token rotation.

---

#### 4.1.4 Logout User
- **Endpoint:** `/api/v1/auth/logout/`
- **HTTP Method:** `POST`
- **Description:** Blacklists refresh token and revokes active session.
- **Authentication Required:** Yes
- **Allowed Roles:** Admin, Shelter, Adopter
- **Request Body:**
```json
{
  "refresh_token": "d98213e4-8bf9-3888-9912-ace4e6543999"
}
```
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "message": "Successfully logged out."
  }
}
```
- **Error Responses:** `401 Unauthorized`
- **Notes:** Invalidates passed refresh token.

---

#### 4.1.5 Verify Email
- **Endpoint:** `/api/v1/auth/verify-email/`
- **HTTP Method:** `POST`
- **Description:** Verifies user email address using verification token.
- **Authentication Required:** No
- **Allowed Roles:** Public (Unauthenticated)
- **Request Body:**
```json
{
  "token": "email_verification_token_string"
}
```
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "message": "Email address verified successfully."
  }
}
```
- **Error Responses:** `400 Bad Request`, `422 Unprocessable Entity`
- **Notes:** Updates `is_email_verified` to `true`.

---

#### 4.1.6 Resend Email Verification
- **Endpoint:** `/api/v1/auth/resend-verification/`
- **HTTP Method:** `POST`
- **Description:** Resends verification token to user email.
- **Authentication Required:** No
- **Allowed Roles:** Public (Unauthenticated)
- **Request Body:**
```json
{
  "email": "user@example.com"
}
```
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "message": "Verification email sent if account exists."
  }
}
```
- **Error Responses:** `400 Bad Request`
- **Notes:** Generic message prevents email enumeration.

---

#### 4.1.7 Request Password Reset (Forgot Password)
- **Endpoint:** `/api/v1/auth/forgot-password/`
- **HTTP Method:** `POST`
- **Description:** Triggers password reset notification with reset token.
- **Authentication Required:** No
- **Allowed Roles:** Public (Unauthenticated)
- **Request Body:**
```json
{
  "email": "user@example.com"
}
```
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "message": "Password reset instructions sent if account exists."
  }
}
```
- **Error Responses:** `400 Bad Request`
- **Notes:** Generic message prevents email enumeration.

---

#### 4.1.8 Confirm Password Reset
- **Endpoint:** `/api/v1/auth/reset-password/`
- **HTTP Method:** `POST`
- **Description:** Resets password using valid reset token.
- **Authentication Required:** No
- **Allowed Roles:** Public (Unauthenticated)
- **Request Body:**
```json
{
  "token": "reset_token_string",
  "new_password": "NewSecurePassword123!"
}
```
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "message": "Password reset successfully."
  }
}
```
- **Error Responses:** `400 Bad Request`, `422 Unprocessable Entity`
- **Notes:** Revokes existing active refresh tokens upon success.

---

#### 4.1.9 Change Password
- **Endpoint:** `/api/v1/auth/change-password/`
- **HTTP Method:** `POST`
- **Description:** Allows authenticated user to update their current password.
- **Authentication Required:** Yes
- **Allowed Roles:** Admin, Shelter, Adopter
- **Request Body:**
```json
{
  "current_password": "OldPassword123!",
  "new_password": "NewSecurePassword123!"
}
```
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "message": "Password changed successfully."
  }
}
```
- **Error Responses:** `400 Bad Request`, `401 Unauthorized`, `422 Unprocessable Entity`
- **Notes:** Requires current password verification.

---

### 4.2 Users Module

#### 4.2.1 Get Current User Profile
- **Endpoint:** `/api/v1/users/me/`
- **HTTP Method:** `GET`
- **Description:** Retrieves authenticated user's profile.
- **Authentication Required:** Yes
- **Allowed Roles:** Admin, Shelter, Adopter
- **Request Body:** None
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "id": "a3bb189e-8bf9-3888-9912-ace4e6543001",
    "email": "user@example.com",
    "first_name": "Jane",
    "last_name": "Doe",
    "phone": "+1234567890",
    "role": "Adopter",
    "avatar_url": "https://cdn.pawmatch.org/avatars/a3bb189e.jpg",
    "address": {
      "street": "123 Main St",
      "city": "Austin",
      "state": "TX",
      "zip_code": "78701",
      "country": "USA"
    },
    "created_at": "2026-07-29T10:00:00Z"
  }
}
```
- **Error Responses:** `401 Unauthorized`
- **Notes:** Returns current user session model.

---

#### 4.2.2 Update Current User Profile
- **Endpoint:** `/api/v1/users/me/`
- **HTTP Method:** `PATCH`
- **Description:** Partial update of authenticated user's profile details.
- **Authentication Required:** Yes
- **Allowed Roles:** Admin, Shelter, Adopter
- **Request Body:**
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "phone": "+1987654321"
}
```
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "id": "a3bb189e-8bf9-3888-9912-ace4e6543001",
    "first_name": "Jane",
    "last_name": "Smith",
    "phone": "+1987654321",
    "updated_at": "2026-07-29T11:00:00Z"
  }
}
```
- **Error Responses:** `400 Bad Request`, `401 Unauthorized`, `422 Unprocessable Entity`
- **Notes:** Email and role fields are read-only.

---

#### 4.2.3 Upload User Avatar
- **Endpoint:** `/api/v1/users/me/avatar/`
- **HTTP Method:** `POST`
- **Description:** Uploads or updates profile avatar image.
- **Authentication Required:** Yes
- **Allowed Roles:** Admin, Shelter, Adopter
- **Request Body:** `multipart/form-data`
  - `file`: (Binary image, JPEG/PNG/WebP, max 5MB)
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "avatar_url": "https://cdn.pawmatch.org/avatars/a3bb189e.jpg"
  }
}
```
- **Error Responses:** `400 Bad Request`, `401 Unauthorized`
- **Notes:** Supported formats: `image/jpeg`, `image/png`, `image/webp`.

---

#### 4.2.4 List Users
- **Endpoint:** `/api/v1/users/`
- **HTTP Method:** `GET`
- **Description:** Lists platform users with filtering, sorting, and pagination.
- **Authentication Required:** Yes
- **Allowed Roles:** Admin
- **Request Body:** None
- **Query Parameters:**
  - Standard list parameters: `page`, `page_size`, `search`, `ordering`
  - `role` (enum `UserRole`, optional): Filter by role
  - `is_active` (boolean, optional): Filter by account status
- **Path Parameters:** None
- **Success Response:** `200 OK` (Standard Paginated List Envelope)
- **Error Responses:** `401 Unauthorized`, `403 Forbidden`
- **Notes:** Admin role access only.

---

#### 4.2.5 Get User Details
- **Endpoint:** `/api/v1/users/{id}/`
- **HTTP Method:** `GET`
- **Description:** Retrieves specific user profile by ID.
- **Authentication Required:** Yes
- **Allowed Roles:** Admin
- **Request Body:** None
- **Query Parameters:** None
- **Path Parameters:**
  - `id` (UUID, Required): Target user ID.
- **Success Response:** `200 OK` (Standard Single Item Envelope)
- **Error Responses:** `401 Unauthorized`, `403 Forbidden`, `404 Not Found`
- **Notes:** Admin access only.

---

#### 4.2.6 Update User Account / Status
- **Endpoint:** `/api/v1/users/{id}/`
- **HTTP Method:** `PATCH`
- **Description:** Admin endpoint to update user account details or toggle activation state.
- **Authentication Required:** Yes
- **Allowed Roles:** Admin
- **Request Body:**
```json
{
  "is_active": false
}
```
- **Query Parameters:** None
- **Path Parameters:**
  - `id` (UUID, Required): User ID.
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "id": "a3bb189e-8bf9-3888-9912-ace4e6543001",
    "is_active": false,
    "updated_at": "2026-07-29T11:30:00Z"
  }
}
```
- **Error Responses:** `401 Unauthorized`, `403 Forbidden`, `404 Not Found`
- **Notes:** Setting `is_active: false` immediately blocks user login.

---

### 4.3 Shelters Module

#### 4.3.1 Create Shelter Profile
- **Endpoint:** `/api/v1/shelters/`
- **HTTP Method:** `POST`
- **Description:** Creates an initial shelter organization profile associated with the authenticated Shelter user account.
- **Authentication Required:** Yes
- **Allowed Roles:** Shelter
- **Request Body:**
```json
{
  "organization_name": "Happy Paws Rescue",
  "registration_number": "REG-884920",
  "description": "Non-profit animal shelter.",
  "phone": "+15551234567",
  "email": "contact@happypaws.org",
  "website": "https://happypaws.org",
  "address": {
    "street": "789 Shelter Way",
    "city": "Austin",
    "state": "TX",
    "zip_code": "78701",
    "country": "USA"
  }
}
```
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `201 Created`
```json
{
  "status": "success",
  "data": {
    "id": "c7112001-e29b-41d4-a716-446655449000",
    "user_id": "a3bb189e-8bf9-3888-9912-ace4e6543001",
    "organization_name": "Happy Paws Rescue",
    "registration_number": "REG-884920",
    "verification_status": "Unverified",
    "created_at": "2026-07-29T10:00:00Z"
  }
}
```
- **Error Responses:** `400 Bad Request`, `401 Unauthorized`, `409 Conflict`
- **Notes:** Initial `verification_status` defaults to `Unverified`.

---

#### 4.3.2 Get Current Shelter Profile
- **Endpoint:** `/api/v1/shelters/me/`
- **HTTP Method:** `GET`
- **Description:** Retrieves shelter profile belonging to the authenticated Shelter user.
- **Authentication Required:** Yes
- **Allowed Roles:** Shelter
- **Request Body:** None
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `200 OK` (Standard Single Item Envelope)
- **Error Responses:** `401 Unauthorized`, `404 Not Found`
- **Notes:** Includes verification status.

---

#### 4.3.3 Update Current Shelter Profile
- **Endpoint:** `/api/v1/shelters/me/`
- **HTTP Method:** `PATCH`
- **Description:** Partial update of authenticated shelter's profile.
- **Authentication Required:** Yes
- **Allowed Roles:** Shelter
- **Request Body:**
```json
{
  "organization_name": "Happy Paws Rescue Center",
  "phone": "+15559876543"
}
```
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `200 OK` (Standard Single Item Envelope)
- **Error Responses:** `400 Bad Request`, `401 Unauthorized`, `404 Not Found`
- **Notes:** `registration_number` and `verification_status` cannot be edited via this endpoint.

---

#### 4.3.4 List Shelters
- **Endpoint:** `/api/v1/shelters/`
- **HTTP Method:** `GET`
- **Description:** Browses public shelters with filtering, search, and pagination.
- **Authentication Required:** No
- **Allowed Roles:** Public (Unauthenticated), Admin, Shelter, Adopter
- **Request Body:** None
- **Query Parameters:**
  - Standard list parameters: `page`, `page_size`, `search`, `ordering`
  - `verification_status` (enum `ShelterVerificationStatus`, optional): Defaults to `Verified` for public callers
  - `city` (string, optional)
  - `state` (string, optional)
- **Path Parameters:** None
- **Success Response:** `200 OK` (Standard Paginated List Envelope)
- **Error Responses:** `400 Bad Request`
- **Notes:** Public views filter to verified shelters by default.

---

#### 4.3.5 Get Public Shelter Profile
- **Endpoint:** `/api/v1/shelters/{id}/`
- **HTTP Method:** `GET`
- **Description:** Fetches public shelter details by UUID.
- **Authentication Required:** No
- **Allowed Roles:** Public (Unauthenticated), Admin, Shelter, Adopter
- **Request Body:** None
- **Query Parameters:** None
- **Path Parameters:**
  - `id` (UUID, Required): Shelter ID.
- **Success Response:** `200 OK` (Standard Single Item Envelope)
- **Error Responses:** `404 Not Found`
- **Notes:** Confidential verification records are excluded.

---

### 4.4 Shelter Verification Module

#### 4.4.1 Upload Shelter Verification Document
- **Endpoint:** `/api/v1/shelters/me/verifications/documents/`
- **HTTP Method:** `POST`
- **Description:** Uploads verification document (NGO registration certificate, tax proof, operating license).
- **Authentication Required:** Yes
- **Allowed Roles:** Shelter
- **Request Body:** `multipart/form-data`
  - `document_type` (enum `DocumentType`, Required)
  - `file` (Binary file, PDF or image, max 10MB)
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `201 Created`
```json
{
  "status": "success",
  "data": {
    "document_id": "d1002003-e29b-41d4-a716-446655441111",
    "document_type": "Registration_Certificate",
    "file_name": "ngo_certificate.pdf",
    "file_url": "https://cdn.pawmatch.org/docs/d1002003.pdf",
    "uploaded_at": "2026-07-29T10:15:00Z"
  }
}
```
- **Error Responses:** `400 Bad Request`, `401 Unauthorized`
- **Notes:** Allowed formats: PDF, JPEG, PNG.

---

#### 4.4.2 Submit Verification Request
- **Endpoint:** `/api/v1/shelters/me/verifications/`
- **HTTP Method:** `POST`
- **Description:** Submits shelter verification profile and uploaded documents for admin review.
- **Authentication Required:** Yes
- **Allowed Roles:** Shelter
- **Request Body:**
```json
{
  "notes": "All required tax and registration certificates uploaded."
}
```
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `201 Created`
```json
{
  "status": "success",
  "data": {
    "verification_id": "v990011-e29b-41d4-a716-446655440000",
    "shelter_id": "c7112001-e29b-41d4-a716-446655449000",
    "verification_status": "Pending",
    "submitted_at": "2026-07-29T10:20:00Z"
  }
}
```
- **Error Responses:** `400 Bad Request`, `401 Unauthorized`, `409 Conflict`
- **Notes:** Updates shelter status to `Pending`.

---

#### 4.4.3 Get Verification Status & History
- **Endpoint:** `/api/v1/shelters/me/verifications/`
- **HTTP Method:** `GET`
- **Description:** Retrieves verification status, documents, and audit history for current shelter.
- **Authentication Required:** Yes
- **Allowed Roles:** Shelter
- **Request Body:** None
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "shelter_id": "c7112001-e29b-41d4-a716-446655449000",
    "verification_status": "Pending",
    "documents": [
      {
        "document_id": "d1002003-e29b-41d4-a716-446655441111",
        "document_type": "Registration_Certificate",
        "file_name": "ngo_certificate.pdf",
        "uploaded_at": "2026-07-29T10:15:00Z"
      }
    ],
    "history": [
      {
        "status": "Pending",
        "remarks": "Submitted for verification.",
        "timestamp": "2026-07-29T10:20:00Z"
      }
    ]
  }
}
```
- **Error Responses:** `401 Unauthorized`, `404 Not Found`
- **Notes:** Own shelter verification trail.

---

#### 4.4.4 List Shelter Verification Requests (Admin)
- **Endpoint:** `/api/v1/shelter-verifications/`
- **HTTP Method:** `GET`
- **Description:** Lists shelter verification review queue for administrators.
- **Authentication Required:** Yes
- **Allowed Roles:** Admin
- **Request Body:** None
- **Query Parameters:**
  - Standard list parameters: `page`, `page_size`, `search`, `ordering`
  - `status` (enum `ShelterVerificationStatus`, optional, default: `Pending`)
- **Path Parameters:** None
- **Success Response:** `200 OK` (Standard Paginated List Envelope)
- **Error Responses:** `401 Unauthorized`, `403 Forbidden`
- **Notes:** Admin moderation queue.

---

#### 4.4.5 Get Shelter Verification Request Details (Admin)
- **Endpoint:** `/api/v1/shelter-verifications/{id}/`
- **HTTP Method:** `GET`
- **Description:** Fetches full verification submission details and legal documents for review.
- **Authentication Required:** Yes
- **Allowed Roles:** Admin
- **Request Body:** None
- **Query Parameters:** None
- **Path Parameters:**
  - `id` (UUID, Required): Verification ID.
- **Success Response:** `200 OK` (Standard Single Item Envelope)
- **Error Responses:** `401 Unauthorized`, `403 Forbidden`, `404 Not Found`
- **Notes:** Includes document download URLs.

---

#### 4.4.6 Update Shelter Verification Status (Admin)
- **Endpoint:** `/api/v1/shelter-verifications/{id}/`
- **HTTP Method:** `PATCH`
- **Description:** Admin endpoint to approve or reject a shelter verification request.
- **Authentication Required:** Yes
- **Allowed Roles:** Admin
- **Request Body:**
```json
{
  "status": "Verified",
  "remarks": "Legal registration documents verified."
}
```
- **Query Parameters:** None
- **Path Parameters:**
  - `id` (UUID, Required): Verification ID.
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "verification_id": "v990011-e29b-41d4-a716-446655440000",
    "shelter_id": "c7112001-e29b-41d4-a716-446655449000",
    "verification_status": "Verified",
    "reviewed_by": "admin-uuid-001",
    "updated_at": "2026-07-29T10:30:00Z"
  }
}
```
- **Error Responses:** `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`
- **Notes:** Rejection requires `remarks`. Approval enables pet publishing.

---

### 4.5 Pets Module

#### 4.5.1 List & Filter Pets
- **Endpoint:** `/api/v1/pets/`
- **HTTP Method:** `GET`
- **Description:** Primary pet discovery and search endpoint. Supports full-text search, multi-field filtering, sorting, and pagination.
- **Authentication Required:** No
- **Allowed Roles:** Public (Unauthenticated), Admin, Shelter, Adopter
- **Request Body:** None
- **Query Parameters:**
  - Standard list parameters: `page`, `page_size`, `search`, `ordering`
  - `species` (enum `Species`, optional)
  - `breed` (string, optional)
  - `gender` (enum `Gender`, optional)
  - `size` (enum `Size`, optional)
  - `min_age` (integer, optional)
  - `max_age` (integer, optional)
  - `city` (string, optional)
  - `state` (string, optional)
  - `status` (enum `PetStatus`, optional, default: `Available`)
  - `shelter_id` (UUID, optional): Filter by shelter
- **Path Parameters:** None
- **Success Response:** `200 OK` (Standard Paginated List Envelope)
- **Error Responses:** `400 Bad Request`
- **Notes:** Replaces dedicated `/pets/search` route following REST best practices.

---

#### 4.5.2 Create Pet Listing
- **Endpoint:** `/api/v1/pets/`
- **HTTP Method:** `POST`
- **Description:** Creates a new pet listing under the authenticated shelter.
- **Authentication Required:** Yes
- **Allowed Roles:** Shelter (Verified status required)
- **Request Body:**
```json
{
  "name": "Buddy",
  "species": "Dog",
  "breed": "Golden Retriever",
  "age_years": 2,
  "age_months": 4,
  "gender": "Male",
  "size": "Medium",
  "health_summary": "Vaccinated, neutered, microchipped.",
  "temperament_summary": "Friendly, good with children.",
  "description": "Buddy is a loving Golden Retriever.",
  "location": {
    "city": "Austin",
    "state": "TX",
    "zip_code": "78701"
  },
  "adoption_requirements": "Requires fenced yard."
}
```
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `201 Created`
```json
{
  "status": "success",
  "data": {
    "id": "e5504001-e29b-41d4-a716-446655448888",
    "shelter_id": "c7112001-e29b-41d4-a716-446655449000",
    "name": "Buddy",
    "species": "Dog",
    "breed": "Golden Retriever",
    "status": "Available",
    "created_at": "2026-07-29T10:45:00Z"
  }
}
```
- **Error Responses:** `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`
- **Notes:** Shelter must be `Verified` to create listings.

---

#### 4.5.3 Get Pet Details
- **Endpoint:** `/api/v1/pets/{id}/`
- **HTTP Method:** `GET`
- **Description:** Retrieves full profile details for a specific pet including images and shelter contact info.
- **Authentication Required:** No
- **Allowed Roles:** Public (Unauthenticated), Admin, Shelter, Adopter
- **Request Body:** None
- **Query Parameters:** None
- **Path Parameters:**
  - `id` (UUID, Required): Pet ID.
- **Success Response:** `200 OK` (Standard Single Item Envelope)
- **Error Responses:** `404 Not Found`
- **Notes:** Public pet detail view.

---

#### 4.5.4 Update Pet Listing / Status
- **Endpoint:** `/api/v1/pets/{id}/`
- **HTTP Method:** `PATCH`
- **Description:** Partial update of pet listing fields or status (`Available`, `Pending Adoption`, `Adopted`, `Deactivated`).
- **Authentication Required:** Yes
- **Allowed Roles:** Shelter (Owner), Admin
- **Request Body:**
```json
{
  "status": "Pending Adoption",
  "health_summary": "Fully vaccinated, neutered."
}
```
- **Query Parameters:** None
- **Path Parameters:**
  - `id` (UUID, Required): Pet ID.
- **Success Response:** `200 OK` (Standard Single Item Envelope)
- **Error Responses:** `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`
- **Notes:** Only shelter owner or Admin can modify listing.

---

#### 4.5.5 Deactivate / Delete Pet Listing
- **Endpoint:** `/api/v1/pets/{id}/`
- **HTTP Method:** `DELETE`
- **Description:** Soft-deletes a pet listing (sets `status` to `Deactivated`).
- **Authentication Required:** Yes
- **Allowed Roles:** Shelter (Owner), Admin
- **Request Body:** None
- **Query Parameters:** None
- **Path Parameters:**
  - `id` (UUID, Required): Pet ID.
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "message": "Pet listing deactivated."
  }
}
```
- **Error Responses:** `401 Unauthorized`, `403 Forbidden`, `404 Not Found`
- **Notes:** Soft deletion maintains auditability for historical adoptions.

---

### 4.6 Pet Images Module

#### 4.6.1 List Pet Images
- **Endpoint:** `/api/v1/pets/{pet_id}/images/`
- **HTTP Method:** `GET`
- **Description:** Lists image gallery for a pet.
- **Authentication Required:** No
- **Allowed Roles:** Public (Unauthenticated), Admin, Shelter, Adopter
- **Request Body:** None
- **Query Parameters:** None
- **Path Parameters:**
  - `pet_id` (UUID, Required): Pet ID.
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": [
    {
      "id": "img-990011-uuid",
      "url": "https://cdn.pawmatch.org/pets/buddy_01.jpg",
      "is_primary": true,
      "uploaded_at": "2026-07-29T10:50:00Z"
    }
  ]
}
```
- **Error Responses:** `404 Not Found`
- **Notes:** Primary image listed first.

---

#### 4.6.2 Upload Pet Image
- **Endpoint:** `/api/v1/pets/{pet_id}/images/`
- **HTTP Method:** `POST`
- **Description:** Uploads a photo to a pet listing gallery.
- **Authentication Required:** Yes
- **Allowed Roles:** Shelter (Owner), Admin
- **Request Body:** `multipart/form-data`
  - `file` (Binary image file, max 5MB, format: JPEG/PNG/WebP)
  - `is_primary` (boolean, optional, default: false)
- **Query Parameters:** None
- **Path Parameters:**
  - `pet_id` (UUID, Required): Pet ID.
- **Success Response:** `201 Created`
```json
{
  "status": "success",
  "data": {
    "id": "img-990011-uuid",
    "pet_id": "e5504001-e29b-41d4-a716-446655448888",
    "url": "https://cdn.pawmatch.org/pets/buddy_01.jpg",
    "is_primary": false,
    "uploaded_at": "2026-07-29T10:50:00Z"
  }
}
```
- **Error Responses:** `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`
- **Notes:** Maximum 10 photos per pet listing.

---

#### 4.6.3 Update Pet Image Metadata
- **Endpoint:** `/api/v1/pets/{pet_id}/images/{id}/`
- **HTTP Method:** `PATCH`
- **Description:** Updates image flags (e.g., set `is_primary: true`).
- **Authentication Required:** Yes
- **Allowed Roles:** Shelter (Owner), Admin
- **Request Body:**
```json
{
  "is_primary": true
}
```
- **Query Parameters:** None
- **Path Parameters:**
  - `pet_id` (UUID, Required): Pet ID.
  - `id` (UUID, Required): Image ID.
- **Success Response:** `200 OK` (Standard Single Item Envelope)
- **Error Responses:** `401 Unauthorized`, `403 Forbidden`, `404 Not Found`
- **Notes:** Setting `is_primary: true` automatically unsets primary status on other images for this pet.

---

#### 4.6.4 Delete Pet Image
- **Endpoint:** `/api/v1/pets/{pet_id}/images/{id}/`
- **HTTP Method:** `DELETE`
- **Description:** Removes a photo from a pet's gallery.
- **Authentication Required:** Yes
- **Allowed Roles:** Shelter (Owner), Admin
- **Request Body:** None
- **Query Parameters:** None
- **Path Parameters:**
  - `pet_id` (UUID, Required): Pet ID.
  - `id` (UUID, Required): Image ID.
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "message": "Image deleted successfully."
  }
}
```
- **Error Responses:** `401 Unauthorized`, `403 Forbidden`, `404 Not Found`
- **Notes:** If primary image is deleted, next image is designated primary.

---

### 4.7 Adoption Applications Module

#### 4.7.1 Submit Adoption Application
- **Endpoint:** `/api/v1/applications/`
- **HTTP Method:** `POST`
- **Description:** Submits a pet adoption application.
- **Authentication Required:** Yes
- **Allowed Roles:** Adopter
- **Request Body:**
```json
{
  "pet_id": "e5504001-e29b-41d4-a716-446655448888",
  "housing_type": "House",
  "owns_home": true,
  "has_yard": true,
  "yard_fenced": true,
  "current_pets_description": "One 5-year-old neutered Beagle.",
  "family_members_count": 3,
  "has_children": true,
  "experience_description": "10+ years pet care experience.",
  "reason_for_adoption": "Looking for family dog."
}
```
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `201 Created`
```json
{
  "status": "success",
  "data": {
    "id": "app-880011-e29b-41d4-a716-446655442222",
    "pet_id": "e5504001-e29b-41d4-a716-446655448888",
    "adopter_id": "a3bb189e-8bf9-3888-9912-ace4e6543001",
    "status": "Submitted",
    "submitted_at": "2026-07-29T11:00:00Z"
  }
}
```
- **Error Responses:** `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `409 Conflict`
- **Notes:** Triggers in-app application submission notification.

---

#### 4.7.2 List Adoption Applications
- **Endpoint:** `/api/v1/applications/`
- **HTTP Method:** `GET`
- **Description:** Lists adoption applications scoped by role (Adopter sees own applications; Shelter sees applications for their pets; Admin sees all).
- **Authentication Required:** Yes
- **Allowed Roles:** Admin, Shelter, Adopter
- **Request Body:** None
- **Query Parameters:**
  - Standard list parameters: `page`, `page_size`, `search`, `ordering`
  - `status` (enum `ApplicationStatus`, optional)
  - `pet_id` (UUID, optional)
- **Path Parameters:** None
- **Success Response:** `200 OK` (Standard Paginated List Envelope)
- **Error Responses:** `401 Unauthorized`
- **Notes:** RBAC filters application visibility automatically.

---

#### 4.7.3 Get Application Details
- **Endpoint:** `/api/v1/applications/{id}/`
- **HTTP Method:** `GET`
- **Description:** Fetches questionnaire answers and review state for an adoption application.
- **Authentication Required:** Yes
- **Allowed Roles:** Admin, Shelter (Owner), Adopter (Applicant)
- **Request Body:** None
- **Query Parameters:** None
- **Path Parameters:**
  - `id` (UUID, Required): Application ID.
- **Success Response:** `200 OK` (Standard Single Item Envelope)
- **Error Responses:** `401 Unauthorized`, `403 Forbidden`, `404 Not Found`
- **Notes:** Restricted to applicant adopter, managing shelter, or Admin.

---

#### 4.7.4 Update Application Status
- **Endpoint:** `/api/v1/applications/{id}/`
- **HTTP Method:** `PATCH`
- **Description:** Updates review stage (`Submitted`, `Under Review`, `Approved`, `Rejected`, `Closed`) and remarks.
- **Authentication Required:** Yes
- **Allowed Roles:** Shelter (Owner), Admin
- **Request Body:**
```json
{
  "status": "Approved",
  "remarks": "Applicant meets all home requirements."
}
```
- **Query Parameters:** None
- **Path Parameters:**
  - `id` (UUID, Required): Application ID.
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "id": "app-880011-e29b-41d4-a716-446655442222",
    "status": "Approved",
    "updated_at": "2026-07-29T11:30:00Z"
  }
}
```
- **Error Responses:** `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`
- **Notes:** Triggers status update notification to applicant.

---

#### 4.7.5 Get Application Audit Trail
- **Endpoint:** `/api/v1/applications/{id}/history/`
- **HTTP Method:** `GET`
- **Description:** Fetches status change log for an adoption application.
- **Authentication Required:** Yes
- **Allowed Roles:** Admin, Shelter (Owner), Adopter (Applicant)
- **Request Body:** None
- **Query Parameters:** None
- **Path Parameters:**
  - `id` (UUID, Required): Application ID.
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": [
    {
      "status": "Submitted",
      "changed_by": "a3bb189e-8bf9-3888-9912-ace4e6543001",
      "remarks": "Application submitted.",
      "timestamp": "2026-07-29T11:00:00Z"
    },
    {
      "status": "Approved",
      "changed_by": "shelter-user-uuid",
      "remarks": "Approved after review.",
      "timestamp": "2026-07-29T11:30:00Z"
    }
  ]
}
```
- **Error Responses:** `401 Unauthorized`, `403 Forbidden`, `404 Not Found`
- **Notes:** Full status transition log.

---

### 4.8 Notifications Module

#### 4.8.1 List User Notifications
- **Endpoint:** `/api/v1/notifications/`
- **HTTP Method:** `GET`
- **Description:** Fetches in-app notifications for authenticated user.
- **Authentication Required:** Yes
- **Allowed Roles:** Admin, Shelter, Adopter
- **Request Body:** None
- **Query Parameters:**
  - Standard list parameters: `page`, `page_size`, `search`, `ordering`
  - `is_read` (boolean, optional): Filter read/unread notifications
- **Path Parameters:** None
- **Success Response:** `200 OK` (Standard Paginated List Envelope)
- **Error Responses:** `401 Unauthorized`
- **Notes:** Includes unread counter metadata.

---

#### 4.8.2 Update Notification State
- **Endpoint:** `/api/v1/notifications/{id}/`
- **HTTP Method:** `PATCH`
- **Description:** Marks a single notification as read or unread.
- **Authentication Required:** Yes
- **Allowed Roles:** Admin, Shelter, Adopter
- **Request Body:**
```json
{
  "is_read": true
}
```
- **Query Parameters:** None
- **Path Parameters:**
  - `id` (UUID, Required): Notification ID.
- **Success Response:** `200 OK` (Standard Single Item Envelope)
- **Error Responses:** `401 Unauthorized`, `404 Not Found`
- **Notes:** Updates unread state.

---

#### 4.8.3 Mark All Notifications as Read
- **Endpoint:** `/api/v1/notifications/read-all/`
- **HTTP Method:** `POST`
- **Description:** Bulk updates all unread notifications for current user to read.
- **Authentication Required:** Yes
- **Allowed Roles:** Admin, Shelter, Adopter
- **Request Body:** None
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "message": "All notifications marked as read."
  }
}
```
- **Error Responses:** `401 Unauthorized`
- **Notes:** Action endpoint for notification tray management.

---

#### 4.8.4 Delete Notification
- **Endpoint:** `/api/v1/notifications/{id}/`
- **HTTP Method:** `DELETE`
- **Description:** Removes a notification.
- **Authentication Required:** Yes
- **Allowed Roles:** Admin, Shelter, Adopter
- **Request Body:** None
- **Query Parameters:** None
- **Path Parameters:**
  - `id` (UUID, Required): Notification ID.
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "message": "Notification deleted."
  }
}
```
- **Error Responses:** `401 Unauthorized`, `404 Not Found`
- **Notes:** Permanently removes notification item.

---

### 4.9 Admin Dashboard Module

#### 4.9.1 Get Admin Dashboard Overview
- **Endpoint:** `/api/v1/admin/dashboard/overview/`
- **HTTP Method:** `GET`
- **Description:** Fetches system-wide real-time operational summary metrics.
- **Authentication Required:** Yes
- **Allowed Roles:** Admin
- **Request Body:** None
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "total_users": 1250,
    "total_shelters": 45,
    "verified_shelters": 38,
    "pending_shelters": 7,
    "active_pet_listings": 310,
    "total_applications": 890,
    "pending_applications": 120
  }
}
```
- **Error Responses:** `401 Unauthorized`, `403 Forbidden`
- **Notes:** Admin command center dashboard metrics.

---

#### 4.9.2 List System Audit Logs
- **Endpoint:** `/api/v1/admin/audit-logs/`
- **HTTP Method:** `GET`
- **Description:** Browses system audit log records.
- **Authentication Required:** Yes
- **Allowed Roles:** Admin
- **Request Body:** None
- **Query Parameters:**
  - Standard list parameters: `page`, `page_size`, `search`, `ordering`
  - `action` (string, optional)
  - `actor_id` (UUID, optional)
- **Path Parameters:** None
- **Success Response:** `200 OK` (Standard Paginated List Envelope)
- **Error Responses:** `401 Unauthorized`, `403 Forbidden`
- **Notes:** Platform governance audit log view.

---

#### 4.9.3 Moderate Pet Listing
- **Endpoint:** `/api/v1/admin/pets/{id}/moderation/`
- **HTTP Method:** `PATCH`
- **Description:** Flags or unflags a pet listing for moderation review.
- **Authentication Required:** Yes
- **Allowed Roles:** Admin
- **Request Body:**
```json
{
  "is_flagged": true,
  "reason": "Inappropriate listing media."
}
```
- **Query Parameters:** None
- **Path Parameters:**
  - `id` (UUID, Required): Pet ID.
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "pet_id": "e5504001-e29b-41d4-a716-446655448888",
    "is_flagged": true,
    "updated_at": "2026-07-29T11:45:00Z"
  }
}
```
- **Error Responses:** `401 Unauthorized`, `403 Forbidden`, `404 Not Found`
- **Notes:** Flagged pets are automatically hidden from public discovery.

---

### 4.10 Analytics Module

#### 4.10.1 Get Macro Analytics Summary
- **Endpoint:** `/api/v1/analytics/summary/`
- **HTTP Method:** `GET`
- **Description:** Retrieves aggregate platform performance metrics.
- **Authentication Required:** Yes
- **Allowed Roles:** Admin
- **Request Body:** None
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "total_registered_users": 1250,
    "total_shelters": 45,
    "total_verified_shelters": 38,
    "total_pet_listings": 420,
    "total_active_adoptions": 85,
    "total_completed_adoptions": 235
  }
}
```
- **Error Responses:** `401 Unauthorized`, `403 Forbidden`
- **Notes:** Non-predictive, summary-only analytics for V1 scope.

---

#### 4.10.2 Get Shelter Operational Analytics
- **Endpoint:** `/api/v1/analytics/shelter/summary/`
- **HTTP Method:** `GET`
- **Description:** Retrieves performance statistics for authenticated shelter.
- **Authentication Required:** Yes
- **Allowed Roles:** Shelter
- **Request Body:** None
- **Query Parameters:** None
- **Path Parameters:** None
- **Success Response:** `200 OK`
```json
{
  "status": "success",
  "data": {
    "shelter_id": "c7112001-e29b-41d4-a716-446655449000",
    "total_listings": 15,
    "available_pets": 8,
    "pending_adoptions": 3,
    "completed_adoptions": 4,
    "total_applications_received": 42
  }
}
```
- **Error Responses:** `401 Unauthorized`, `403 Forbidden`
- **Notes:** Scoped strictly to authenticated shelter's metrics.

---

## 5. Complete Endpoint Reference Table

| Module | Method | Endpoint | Description | Auth Required | Allowed Roles |
|---|---|---|---|---|---|
| **Authentication** | `POST` | `/api/v1/auth/register/` | Register new user account | No | Public |
| **Authentication** | `POST` | `/api/v1/auth/login/` | Authenticate user & issue JWT | No | Public |
| **Authentication** | `POST` | `/api/v1/auth/refresh/` | Refresh JWT access token | No | Public |
| **Authentication** | `POST` | `/api/v1/auth/logout/` | Blacklist refresh token | Yes | Admin, Shelter, Adopter |
| **Authentication** | `POST` | `/api/v1/auth/verify-email/` | Verify user email address | No | Public |
| **Authentication** | `POST` | `/api/v1/auth/resend-verification/` | Resend verification email | No | Public |
| **Authentication** | `POST` | `/api/v1/auth/forgot-password/` | Request password reset token | No | Public |
| **Authentication** | `POST` | `/api/v1/auth/reset-password/` | Confirm password reset | No | Public |
| **Authentication** | `POST` | `/api/v1/auth/change-password/` | Change password | Yes | Admin, Shelter, Adopter |
| **Users** | `GET` | `/api/v1/users/me/` | Get current user profile | Yes | Admin, Shelter, Adopter |
| **Users** | `PATCH` | `/api/v1/users/me/` | Update current user profile | Yes | Admin, Shelter, Adopter |
| **Users** | `POST` | `/api/v1/users/me/avatar/` | Upload profile avatar | Yes | Admin, Shelter, Adopter |
| **Users** | `GET` | `/api/v1/users/` | List users (paginated) | Yes | Admin |
| **Users** | `GET` | `/api/v1/users/{id}/` | Get user by ID | Yes | Admin |
| **Users** | `PATCH` | `/api/v1/users/{id}/` | Update user / toggle status | Yes | Admin |
| **Shelters** | `POST` | `/api/v1/shelters/` | Create shelter profile | Yes | Shelter |
| **Shelters** | `GET` | `/api/v1/shelters/me/` | Get current shelter profile | Yes | Shelter |
| **Shelters** | `PATCH` | `/api/v1/shelters/me/` | Update shelter profile | Yes | Shelter |
| **Shelters** | `GET` | `/api/v1/shelters/` | List shelters | No | Public, Admin, Shelter, Adopter |
| **Shelters** | `GET` | `/api/v1/shelters/{id}/` | Get public shelter profile | No | Public, Admin, Shelter, Adopter |
| **Shelter Verification** | `POST` | `/api/v1/shelters/me/verifications/documents/` | Upload verification document | Yes | Shelter |
| **Shelter Verification** | `POST` | `/api/v1/shelters/me/verifications/` | Submit verification request | Yes | Shelter |
| **Shelter Verification** | `GET` | `/api/v1/shelters/me/verifications/` | Get verification status/history | Yes | Shelter |
| **Shelter Verification** | `GET` | `/api/v1/shelter-verifications/` | List verification requests | Yes | Admin |
| **Shelter Verification** | `GET` | `/api/v1/shelter-verifications/{id}/` | Get verification details | Yes | Admin |
| **Shelter Verification** | `PATCH` | `/api/v1/shelter-verifications/{id}/` | Approve/Reject verification | Yes | Admin |
| **Pets** | `GET` | `/api/v1/pets/` | List & filter pet listings | No | Public, Admin, Shelter, Adopter |
| **Pets** | `POST` | `/api/v1/pets/` | Create pet listing | Yes | Shelter (Verified) |
| **Pets** | `GET` | `/api/v1/pets/{id}/` | Get pet details | No | Public, Admin, Shelter, Adopter |
| **Pets** | `PATCH` | `/api/v1/pets/{id}/` | Update pet listing / status | Yes | Shelter (Owner), Admin |
| **Pets** | `DELETE` | `/api/v1/pets/{id}/` | Deactivate pet listing | Yes | Shelter (Owner), Admin |
| **Pet Images** | `GET` | `/api/v1/pets/{pet_id}/images/` | List pet images | No | Public, Admin, Shelter, Adopter |
| **Pet Images** | `POST` | `/api/v1/pets/{pet_id}/images/` | Upload pet photo | Yes | Shelter (Owner), Admin |
| **Pet Images** | `PATCH` | `/api/v1/pets/{pet_id}/images/{id}/` | Update image / set primary | Yes | Shelter (Owner), Admin |
| **Pet Images** | `DELETE` | `/api/v1/pets/{pet_id}/images/{id}/` | Delete pet photo | Yes | Shelter (Owner), Admin |
| **Adoption Applications** | `POST` | `/api/v1/applications/` | Submit adoption application | Yes | Adopter |
| **Adoption Applications** | `GET` | `/api/v1/applications/` | List adoption applications | Yes | Admin, Shelter, Adopter |
| **Adoption Applications** | `GET` | `/api/v1/applications/{id}/` | Get application details | Yes | Admin, Shelter (Owner), Adopter (Applicant) |
| **Adoption Applications** | `PATCH` | `/api/v1/applications/{id}/` | Update application status | Yes | Shelter (Owner), Admin |
| **Adoption Applications** | `GET` | `/api/v1/applications/{id}/history/` | Get application audit trail | Yes | Admin, Shelter (Owner), Adopter (Applicant) |
| **Notifications** | `GET` | `/api/v1/notifications/` | List user notifications | Yes | Admin, Shelter, Adopter |
| **Notifications** | `PATCH` | `/api/v1/notifications/{id}/` | Update notification state | Yes | Admin, Shelter, Adopter |
| **Notifications** | `POST` | `/api/v1/notifications/read-all/` | Bulk mark notifications read | Yes | Admin, Shelter, Adopter |
| **Notifications** | `DELETE` | `/api/v1/notifications/{id}/` | Delete notification | Yes | Admin, Shelter, Adopter |
| **Admin Dashboard** | `GET` | `/api/v1/admin/dashboard/overview/` | Get admin overview stats | Yes | Admin |
| **Admin Dashboard** | `GET` | `/api/v1/admin/audit-logs/` | List system audit logs | Yes | Admin |
| **Admin Dashboard** | `PATCH` | `/api/v1/admin/pets/{id}/moderation/` | Flag pet listing | Yes | Admin |
| **Analytics** | `GET` | `/api/v1/analytics/summary/` | Get macro summary analytics | Yes | Admin |
| **Analytics** | `GET` | `/api/v1/analytics/shelter/summary/` | Get shelter summary analytics | Yes | Shelter |

---

## 6. Role-Based Access Control (RBAC) Matrix

| Module / Action | Public | Adopter | Shelter | Admin |
|---|:---:|:---:|:---:|:---:|
| **Auth Operations (Register, Login, Password Reset, Email Verification)** | Full | Full | Full | Full |
| **Manage Own Profile & Avatar (`/users/me/`)** | ❌ | Full | Full | Full |
| **User Directory Management (`/users/`)** | ❌ | ❌ | ❌ | Full |
| **Manage Own Shelter Profile (`/shelters/me/`)** | ❌ | ❌ | Own Shelter | Full |
| **View Shelter Profiles (`/shelters/`)** | Verified Only | Verified Only | Verified Only | Full |
| **Submit Shelter Verification (`/shelters/me/verifications/`)** | ❌ | ❌ | Own Shelter | Full |
| **Review Shelter Verifications (`/shelter-verifications/`)** | ❌ | ❌ | ❌ | Full |
| **Browse & Filter Pets (`/pets/`)** | Available Only | Available Only | Available Only | Full |
| **Create Pet Listings (`/pets/`)** | ❌ | ❌ | Verified Only | Full |
| **Update / Delete Pet Listings (`/pets/{id}/`)** | ❌ | ❌ | Own Pets | Full |
| **Upload / Manage Pet Media (`/pets/{id}/images/`)** | View Only | View Only | Own Pets | Full |
| **Submit Adoption Application (`/applications/`)** | ❌ | Full | ❌ | ❌ |
| **Review Applications & Change Status (`/applications/`)** | ❌ | View Own | Own Pets | Full |
| **View Application Audit Trail (`/applications/{id}/history/`)** | ❌ | View Own | Own Pets | Full |
| **Manage Notifications (`/notifications/`)** | ❌ | Own | Own | Own |
| **Access Admin Dashboard & Audit Logs (`/admin/`)** | ❌ | ❌ | ❌ | Full |
| **Access Operational Analytics (`/analytics/`)** | ❌ | ❌ | Own Shelter | Macro System |
