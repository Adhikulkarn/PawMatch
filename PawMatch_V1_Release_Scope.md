# PawMatch V1 Release Scope

## Document Information

| Field | Value |
|---|---|
| Document Title | PawMatch V1 Release Scope |
| Project Name | PawMatch |
| Version | 1.0 |
| Status | Draft |
| Date | 29 July 2026 |
| Reference Document | `PawMatch_AI_Functional_Requirements_Specification.md` |

## 1. Purpose

This document defines the Version 1 release scope for PawMatch. It converts the broader Functional Requirements Specification into a focused launch plan for the first production release.

The goal of V1 is to deliver a working pet adoption platform with secure access control, verified shelter onboarding, pet listing and discovery, adoption processing, basic communication, and operational visibility for administrators.

## 2. V1 Product Goal

PawMatch V1 will enable:

- users to register, sign in, and manage their profile
- shelters to register and be verified before publishing pets
- shelters to create and manage pet listings
- adopters to search, filter, and review pets
- adopters to submit adoption requests
- shelters and admins to review and manage the adoption workflow
- the platform team to monitor users, shelters, pets, and applications from an admin dashboard

## 3. In-Scope Features for V1

### 3.1 Authentication and RBAC

Included in V1:

- user registration
- login and logout
- password reset
- session handling
- role-based access control

Roles in V1:

- Admin
- Shelter
- Adopter

Minimum access model:

- Admin can verify shelters, monitor platform activity, and manage core records
- Shelter can manage shelter profile, pet listings, and adoption applications
- Adopter can manage profile, browse pets, and submit adoption applications

Mapped FRS areas:

- FR-001
- FR-002
- FR-003
- Security Section 13.1, 13.2, 13.5

### 3.2 User Profiles

Included in V1:

- create profile
- edit personal details
- upload profile photo
- manage contact details
- basic visibility rules based on role

Mapped FRS areas:

- FR-004
- FR-005

### 3.3 Shelter Registration and Verification

Included in V1:

- shelter account registration
- shelter profile submission
- document submission for verification
- admin review and approval or rejection
- verified status required before pet publishing

Mapped FRS areas:

- FR-015 as functional reference for organization verification workflow
- FR-047 for admin review and moderation support

### 3.4 Pet Management

Included in V1:

- create pet listing
- edit pet listing
- deactivate pet listing
- upload pet images
- mark pet availability status

Minimum pet data:

- name
- species
- breed
- age
- gender
- size
- health summary
- temperament summary
- adoption status
- location
- photos

Mapped FRS areas:

- FR-006
- FR-007
- FR-008

### 3.5 Pet Search and Filters

Included in V1:

- browse pet listings
- keyword search
- filter by species
- filter by breed
- filter by age range
- filter by gender
- filter by size
- filter by location
- filter by availability status

Mapped FRS areas:

- FR-009

### 3.6 Pet Details

Included in V1:

- dedicated pet details page
- full pet profile display
- image gallery
- shelter information
- adoption call to action

Pet details must show:

- all core pet attributes
- description
- vaccination or health summary if available
- adoption requirements if defined by shelter

Mapped FRS areas:

- FR-006
- FR-009

### 3.7 Adoption Workflow

Included in V1:

- adoption application form
- application submission by adopter
- shelter review queue
- application status updates
- approve or reject decision
- adoption completion state
- audit trail of status changes

Minimum application statuses:

- Submitted
- Under Review
- Approved
- Rejected
- Closed

Mapped FRS areas:

- FR-010
- FR-011
- FR-013

### 3.8 Admin Dashboard

Included in V1:

- overview of total users
- overview of verified and pending shelters
- overview of active pet listings
- overview of adoption applications
- shelter verification management
- basic moderation controls

Mapped FRS areas:

- FR-047
- FR-048

### 3.9 Basic Notifications

Included in V1:

- account registration confirmation
- password reset notification
- shelter verification approval or rejection notification
- adoption application submission confirmation
- adoption status update notification

Preferred delivery for V1:

- in-app notifications
- email notifications if infrastructure is available at launch

Mapped FRS areas:

- FR-034
- FR-050

### 3.10 Basic Analytics

Included in V1:

- total registered users
- total shelters
- total verified shelters
- total pet listings
- total active adoptions
- total completed adoptions

Analytics scope for V1:

- summary metrics only
- no predictive analytics
- no AI insights

Mapped FRS areas:

- FR-014
- FR-049

## 4. Out of Scope for V1

The following areas from the full FRS are excluded from V1:

- AI pet matching
- AI health assistant
- AI image recognition
- behavior prediction
- lost pet finder
- nutrition planner
- training coach
- veterinarian portal
- health records
- marketplace
- subscriptions
- payments
- community features
- events
- advanced reporting
- advanced workflow automation
- multi-language support
- tele-veterinary services

These may be considered for V1.1, V2, or later roadmap phases.

## 5. Core V1 User Journeys

### 5.1 Adopter Journey

1. Register account
2. Complete user profile
3. Search and filter pets
4. Open pet details
5. Submit adoption application
6. Receive application status updates

### 5.2 Shelter Journey

1. Register shelter account
2. Submit verification details
3. Get approved by admin
4. Create and publish pet listings
5. Review incoming adoption applications
6. Approve or reject applicants

### 5.3 Admin Journey

1. Review shelter verification requests
2. Approve or reject shelters
3. Monitor users, pets, and applications
4. Review platform summary metrics
5. Moderate core records when required

## 6. V1 Success Criteria

V1 will be considered release-ready when:

- all three V1 roles can authenticate successfully
- RBAC prevents unauthorized access to protected features
- shelters cannot publish pets until verified
- verified shelters can create and manage pet listings
- adopters can search pets and submit applications
- shelters can process applications end to end
- admins can review shelter verification requests and see platform summaries
- notifications are triggered for key account and adoption events
- basic analytics are visible in the admin dashboard

## 7. Delivery Notes

- V1 should prioritize reliability and clean workflow execution over AI functionality
- all V1 modules should be designed so future AI and monetization features can be added without major redesign
- auditability is important for shelter verification and adoption status changes

## 8. Traceability to the Main FRS

This V1 scope is a narrowed release view derived from the main project specification in `PawMatch_AI_Functional_Requirements_Specification.md`.

Primary FRS references for V1:

- Authentication: FR-001 to FR-003
- User Profiles: FR-004 to FR-005
- Pet Management: FR-006 to FR-008
- Pet Discovery and Adoption: FR-009 to FR-011
- Shelter Operations: FR-013
- Organization Verification: FR-015
- Notifications: FR-034
- Administration: FR-047 to FR-048
- Analytics: FR-014 and FR-049

## 9. Recommended Next Documents

After approving this V1 scope, the next useful documents are:

- V1 product requirements document
- V1 user stories and acceptance criteria
- V1 database schema
- V1 API specification
- V1 release plan and milestone breakdown
