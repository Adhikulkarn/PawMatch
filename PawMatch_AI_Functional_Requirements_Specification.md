_PawMatch AI — Functional Requirements Specification_ 

# **PawMatch AI** 

_AI-Powered Pet Adoption Super App_ 

## **FUNCTIONAL REQUIREMENTS SPECIFICATION** 

(FRS Document) 

|**Document Title**|Functional Requirements Specification – PawMatch AI|
|---|---|
|**Project Name**|PawMatch AI – AI-Powered Pet Adoption Super App|
|**Document Version**|1.0|
|**Document Status**|Draft for Internal Review|
|**Prepared By**|Business Analysis & Solution Architecture Team|
|**Prepared For**|PawMatch AI Project Team – Engineering, QA, UI/UX, and Product<br>Stakeholders|
|**Date of Issue**|27 July 2026|
|**Classification**|Confidential – Internal Use Only|



Page 1 of 70 

_PawMatch AI — Functional Requirements Specification_ 

Page 2 of 70 

_PawMatch AI — Functional Requirements Specification_ 

### **3. Introduction** 

#### **3.1 Purpose** 

This Functional Requirements Specification (FRS) document defines the complete functional and nonfunctional requirements for the development of PawMatch AI, an AI-powered pet adoption superapplication. This document translates the approved PawMatch AI Business Plan into a structured, testable, and traceable set of requirements suitable for use by the development, quality assurance, UI/UX, and project management teams throughout the software development lifecycle. 

This document serves as the authoritative reference for scope agreement between the Project Owner and the development team, and shall be used as the baseline for design, implementation, testing, and acceptance of the PawMatch AI platform. 

#### **3.2 Scope** 

The scope of this document covers all functional modules described in the PawMatch AI Business Plan, including but not limited to: user authentication and profile management, pet listing and adoption workflows, shelter/NGO/veterinarian dashboards, digital pet health records, the suite of AI-powered features (matching, image recognition, health assistant, behavior prediction, lost pet finder, nutrition planning, and training coaching), the reminder and notification system, the pet marketplace, subscription and payment processing, community and events modules, reporting and analytics, and platform administration. 

This document covers the Version 1.0 release scope aligned to the Year 1 roadmap (launch in major Indian cities) as defined in the Business Plan, while noting Year 2/Year 3 capabilities (tele-veterinary consultation, multi-language AI assistant, wearable integration, international expansion) as forward-looking scope items, clearly marked where referenced. 

Out of scope for this document: detailed UI wireframes/visual design specifications (to be produced separately by the UI/UX team using this FRS as functional input), infrastructure provisioning and DevOps runbooks, and third-party vendor contractual terms. 

#### **3.3 Objectives** 

- To provide an unambiguous, testable specification of all functional requirements for the PawMatch AI platform. 

- To establish clear boundaries of system behavior for each user role and module. 

- To provide a basis for effort estimation, sprint planning, and test-case design. 

- To provide a traceability mechanism linking business objectives to functional requirements and, ultimately, to test cases (Section 18). 

- To document assumptions and constraints so that ambiguities in the source Business Plan are resolved in a controlled and visible manner. 

Page 3 of 70 

_PawMatch AI — Functional Requirements Specification_ 

#### **3.4 Intended Audience** 

- Software Developers (Backend, Frontend/Mobile, AI/ML Engineers) – for implementation reference. 

- Quality Assurance Engineers – for test-case design and acceptance testing. 

- UI/UX Designers – for wireframe and interaction design grounded in defined functional flows. 

- Project Managers / Scrum Masters – for scope control, sprint planning, and delivery tracking. 

- Product Owner / Team Lead – for scope validation and sign-off. 

- Business Stakeholders and Investors – for scope transparency and progress evaluation. 

#### **3.5 Definitions** 

|**Term**|**Definition**|
|---|---|
|Adoption Readiness Score|An AI-generated numeric/qualitative score indicating an applicant's<br>suitability to adopt a specific pet, based on home environment, lifestyle,<br>financial capability, prior ownership, and veterinary references.|
|Matching Profile|A structured record of a user's lifestyle, housing, and preference data<br>used by the AI Pet Match feature to recommend suitable pets.|
|Pet Listing|A published record representing a pet available for adoption or fostering,<br>created by a Shelter, NGO, Rescue Organization, or Foster Caregiver.|
|Health Record|A digital, pet-specific record of vaccinations, medical history,<br>prescriptions, surgeries, and lab reports.|
|Premium Subscriber|A Pet Owner account holding an active Premium or Family paid<br>subscription plan.|
|Verified Organization|A Shelter, NGO, Rescue Organization, or Veterinarian account that has<br>completed the Administration verification workflow (FR-012/FR-015/FR-<br>017).|
|AI<br>Recommendation<br>Engine|The backend AI/ML service responsible for pet matching, behavior<br>prediction, nutrition planning, and training-plan generation.|



#### **3.6 Acronyms** 

|**Acronym**|**Expansion**|
|---|---|
|FRS|Functional Requirements Specification|
|SRS|Software Requirements Specification|
|FR|Functional Requirement|
|BR|Business Rule|
|NFR|Non-Functional Requirement|



Page 4 of 70 

_PawMatch AI — Functional Requirements Specification_ 

|**Acronym**|**Expansion**|
|---|---|
|AI|Artificial Intelligence|
|NLP|Natural Language Processing|
|OCR|Optical Character Recognition|
|NGO|Non-Governmental Organization|
|CSR|Corporate Social Responsibility|
|UI/UX|User Interface / User Experience|
|SLA|Service Level Agreement|
|RBAC|Role-Based Access Control|
|PII|Personally Identifiable Information|
|JWT|JSON Web Token|
|UAT|User Acceptance Testing|



#### **3.7 References** 

- PawMatch AI Business Plan – AI-Powered Pet Adoption Super App (source document, provided by Project Owner). 

- IEEE Std 830-1998 – IEEE Recommended Practice for Software Requirements Specifications (structural reference). 

- OWASP Application Security Verification Standard (security requirement reference, Section 13). 

- Payment Card Industry Data Security Standard (PCI-DSS) (payment handling reference, Section 10.1). 

Page 5 of 70 

_PawMatch AI — Functional Requirements Specification_ 

### **4. Product Overview** 

#### **4.1 Business Context** 

Current pet-adoption ecosystems suffer from low adoption conversion rates, fake or unverified listings, weak adopter verification, absence of post-adoption support, and high rates of pet return due to mismatched owner expectations. PawMatch AI addresses these issues by unifying shelters, NGOs, verified breeders, foster homes, veterinarians, and pet owners on a single AI-driven ecosystem that supports the complete pet lifecycle, from matching and adoption through lifelong health, nutrition, training, and community engagement. 

#### **4.2 System Overview** 

PawMatch AI is a multi-sided marketplace and services platform comprising a mobile application (Flutter, Android and iOS), a web-based organizational dashboard (React) for shelters, NGOs, and administrators, and a backend platform (Node.js and Python AI services) that exposes AI-driven matching, diagnostic, and advisory capabilities across the adoption, health, and marketplace domains. 

#### **4.3 Product Perspective** 

PawMatch AI is a new, standalone product. It integrates with third-party services for payments, cloud storage, maps, and communication channels (Section 10) but is not a component of any pre-existing internal system. 

#### **4.4 Business Goals** 

- Increase successful pet adoption rates through AI-based compatibility matching. 

- Reduce pet abandonment and post-adoption returns by improving expectation-setting prior to adoption. 

- Provide shelters and NGOs with tools to reduce administrative overhead and increase adopter reach. 

- Establish a sustainable, diversified revenue model spanning subscriptions, commissions, and partnerships (Section 4.9 references the Business Plan Revenue Model). 

#### **4.5 Project Objectives** 

- Deliver a Year 1 release supporting launch in major Indian cities with 100+ partner shelters, 50,000 registered users, and 10,000 successful adoptions, as targeted in the Business Plan's 3-Year Growth Roadmap. 

- Deliver all AI Features (Section 7.9–7.15) as functioning, production-grade capabilities rather than static content. 

- Establish the technical and functional foundation to support Year 2 (tele-veterinary consultation, marketplace/insurance integration) and Year 3 (multi-language AI assistant, wearable integration, international expansion) roadmap items without requiring architectural rework. 

Page 6 of 70 

_PawMatch AI — Functional Requirements Specification_ 

#### **4.6 Assumptions** 

- The Business Plan's feature descriptions represent the intended Version 1.0 functional scope unless explicitly marked as a Year 2/Year 3 roadmap item. 

- AI Features (matching, image recognition, health assistant, behavior prediction, lost pet finder, nutrition planner, training coach, pet translator) will be implemented as advisory/assistive tools and do not replace professional veterinary diagnosis or treatment. 

- The Pet Translator feature, marked 'Experimental' in the Business Plan, is treated as a post-Version 1.0 research and development initiative and is not included in the Version 1.0 functional requirements baseline; it is documented for completeness in Section 19.3 (Future Enhancements). 

- Payment processing, SMS/WhatsApp messaging, and cloud storage will be provided via licensed third-party services rather than built in-house. 

- Initial launch geography is India, with currency and regulatory assumptions (INR pricing, Indian dataprotection norms) applied accordingly; wherever this document is reused for a different geography, currency and compliance sections must be revisited. 

- 'Verified breeders' referenced in the Business Plan Executive Summary are treated functionally as a sub-type of the Shelter/Rescue Organization role, subject to the same verification workflow (FR-012 pattern), as the Business Plan does not define a separate breeder workflow. 

#### **4.7 Constraints** 

- The system must operate within the technology stack defined in the Business Plan: Flutter for mobile, React for the web dashboard, Node.js and Python for backend/AI services, PostgreSQL and MongoDB for data storage, and Microsoft Azure or AWS for cloud hosting. 

- AI-generated health, behavior, and nutrition guidance must not be presented as a substitute for licensed veterinary diagnosis, in order to manage liability and animal-welfare risk. 

- Subscription pricing is fixed at the Business Plan's stated rates (Premium ₹299/month, Family ₹499/month) for the Version 1.0 baseline. 

#### **4.8 Dependencies** 

- Availability and reliability of third-party Payment Gateway, Maps, Cloud Storage, Email/SMS/WhatsApp, and AI/ML model-hosting services (Section 10). 

- Timely onboarding and document submission by partner shelters, NGOs, and veterinarians for the verification workflow (Section 7.24). 

- Availability of sufficiently large and representative training data for AI Image Recognition, Behavior Prediction, and Recommendation Engine models. 

#### **4.9 Business Goals – Revenue Model Alignment** 

This FRS operationalizes the Business Plan's Revenue Model through the Subscriptions module (Section 7.19), Payments module (Section 7.20), and the commission/partnership-bearing modules: Marketplace (7.18), Veterinarian Portal (7.7), Grooming and Boarding (covered functionally under Marketplace/Vet 

Page 7 of 70 

_PawMatch AI — Functional Requirements Specification_ 

Booking service categories), Pet Insurance purchase flows (covered functionally under Marketplace as an insurance product category), and NGO/Shelter premium dashboard and analytics features (7.14/7.25). 

Page 8 of 70 

_PawMatch AI — Functional Requirements Specification_ 

### **5. Stakeholders** 

This section identifies the principal stakeholder groups for the PawMatch AI platform and their primary interest in the system. 

|**Stakeholder**|**Primary Interest in the System**|
|---|---|
|Project Owner|Overall product vision, business viability, roadmap approval, and final<br>acceptance of delivered functionality.|
|Platform Administrators|Day-to-day operation, moderation, verification, configuration, and<br>integrity of the platform.|
|Pet<br>Owners<br>(Adopters/Sponsors)|Discovering, matching with, and adopting or sponsoring pets; accessing<br>health, nutrition, and training tools.|
|Shelters|Publishing pet listings, managing adoption applications, and reducing<br>administrative overhead.|
|Veterinarians|Publishing bookable services, managing appointments, and maintaining<br>pet health records.|
|NGOs|Managing sponsorship campaigns, rescue operations, and CSR<br>partnerships.|
|Rescue Organizations|Publishing rescued-pet listings and coordinating fostering and adoption.|
|Premium Subscribers|Accessing enhanced AI consultation, matching, and support features<br>under a paid plan.|



Page 9 of 70 

_PawMatch AI — Functional Requirements Specification_ 

### **6. User Roles** 

This section defines each user role's description, responsibilities, permissions, and restrictions within PawMatch AI. Role-based access control (RBAC) shall govern all functional entitlements described in Section 7. 

##### **6.1 Super Administrator** 

An internal PawMatch AI staff role with full administrative control over the platform. 

###### **Responsibilities** 

- Verify and approve institutional accounts (Shelters, NGOs, Veterinarians). 

- Configure platform-wide settings and pricing. 

- Moderate content and manage user/organization suspensions. 

- Access all reports and audit logs. 

###### **Permissions** 

- Full read/write access to all modules. 

- Ability to override role permissions for support purposes. 

- Access to Admin Logs, Security Settings, and Platform Configuration. 

###### **Restrictions** 

- Actions are fully audit-logged and cannot be performed anonymously. 

##### **6.2 Moderator** 

An internal staff role focused on content and community moderation, delegated from Super Administrator. 

###### **Responsibilities** 

- Review flagged Community posts, comments, and reported content. 

- Escalate policy violations to Super Administrator. 

###### **Permissions** 

- Read/write access to Community and moderation queues. 

- Read-only access to user profiles necessary for moderation context. 

###### **Restrictions** 

- Cannot verify institutional accounts, configure platform settings, or access financial/payment data. 

##### **6.3 Pet Owner (Free Tier)** 

A registered individual using the platform to browse, adopt, foster, or care for pets under the Free subscription tier. 

Page 10 of 70 

_PawMatch AI — Functional Requirements Specification_ 

###### **Responsibilities** 

- Maintain an accurate personal and pet profile. 

- Submit adoption applications and manage owned pets' health records. 

###### **Permissions** 

- Browse and search listings, submit adoption applications, use limited AI consultations, access Marketplace and Community features. 

###### **Restrictions** 

- Limited number of AI consultations per month (per BR-016). 

- No access to advanced AI matching, multi-pet family accounts, or priority support. 

##### **6.4 Pet Owner (Premium Subscriber)** 

A Pet Owner holding an active Premium (₹299/month) subscription. 

###### **Responsibilities** 

- Same as Free Tier, with expanded usage of AI features. 

###### **Permissions** 

- Unlimited AI consultations, advanced AI matching, full health records, AI training coach, priority support. 

###### **Restrictions** 

- Single-user account scope (see Family Plan for multi-user households). 

##### **6.5 Pet Owner (Family Plan Subscriber)** 

A Pet Owner holding an active Family (₹499/month) subscription supporting multiple pets and shared family accounts. 

###### **Responsibilities** 

- Manage multiple pets and invite family members to a shared account. 

- Manage shared reminders across family members. 

###### **Permissions** 

- All Premium entitlements, plus multi-pet and multi-user account management and shared reminders. 

###### **Restrictions** 

- Family member sub-accounts inherit permissions defined by the primary account holder. 

##### **6.6 Shelter Administrator** 

A representative of a verified Shelter organization managing that organization's presence on the platform. 

###### **Responsibilities** 

Page 11 of 70 

_PawMatch AI — Functional Requirements Specification_ 

- Publish and manage pet listings. 

- Review and process adoption applications. 

- Maintain the Shelter Dashboard and respond to applicant communications. 

###### **Permissions** 

- Full read/write access to the organization's own listings, applications, and analytics. 

- Read access to Adoption Readiness Scores for applicants to the organization's pets. 

###### **Restrictions** 

- Cannot access another organization's listings, applications, or financial data. 

- Cannot publish listings until organization verification (FR-012) is complete. 

##### **6.7 NGO Administrator** 

A representative of a verified NGO managing rescue, sponsorship, and CSR-related activity on the platform. 

###### **Responsibilities** 

- Manage sponsorship campaigns. 

- Coordinate rescue-related pet listings and events. 

###### **Permissions** 

- Read/write access to the NGO's own campaigns, listings, and events. 

- Read access to sponsorship transaction summaries for its campaigns. 

###### **Restrictions** 

- Cannot access another organization's data. 

- Cannot access platform-wide financial reports. 

##### **6.8 Rescue Organization** 

A verified organization functionally equivalent to a Shelter for the purposes of listing and adoption management, focused on rescued animals. 

###### **Responsibilities** 

- Publish rescued-pet listings. 

- Manage foster placements and adoption applications. 

###### **Permissions** 

- Equivalent permissions to Shelter Administrator, scoped to its own organization. 

###### **Restrictions** 

- Same restrictions as Shelter Administrator. 

##### **6.9 Veterinarian** 

Page 12 of 70 

_PawMatch AI — Functional Requirements Specification_ 

A verified, licensed veterinary practitioner offering bookable services on the platform. 

###### **Responsibilities** 

- Maintain a bookable service profile and availability calendar. 

- Update pet Health Records following consultations. 

###### **Permissions** 

- Read/write access to appointments booked with the practitioner. 

- Write access to Health Records for pets they have treated, subject to owner sharing permission (FR020). 

###### **Restrictions** 

- Cannot access a pet's Health Record without an active appointment or explicit owner-granted sharing access. 

- Cannot access another practitioner's appointment calendar. 

##### **6.10 Foster Caregiver** 

A verified individual temporarily hosting a rescued or shelter animal on behalf of a Shelter, NGO, or Rescue Organization. 

###### **Responsibilities** 

- Provide interim pet care and status updates. 

- Support the pet's transition to permanent adoption. 

###### **Permissions** 

- Read/write access to the fostered pet's listing status and care notes, as delegated by the owning organization. 

###### **Restrictions** 

- Cannot independently publish a listing without an associated Shelter/NGO/Rescue Organization sponsor. 

Page 13 of 70 

_PawMatch AI — Functional Requirements Specification_ 

### **7. Functional Requirements** 

This section constitutes the primary body of the Functional Requirements Specification. Requirements are grouped by module and are numbered sequentially (FR-001 through FR-050) for traceability. Each requirement specifies its actors, priority, preconditions, trigger, main flow, alternative flow, exceptions, postconditions, acceptance criteria, and dependencies. Priority is expressed as High (required for Version 1.0 launch), Medium (required for Version 1.0 but non-blocking for a phased rollout), or Low (may be deferred to an immediate post-launch release). 

#### **7.1 Authentication** 

##### **FR-001  User Registration** 

|**Description**|The system shall allow a new user (Pet Owner, Shelter, NGO, Veterinarian, or<br>Rescue Organization) to create an account by providing mandatory identity,<br>contact, and role information.|
|---|---|
|**Actors**|Pet Owner, Shelter Administrator, NGO Administrator, Veterinarian, Rescue<br>Organization|
|**Priority**|High|
|**Preconditions**|• The user must have a valid email address or mobile number.<br>• The user must not already possess an active account with the same<br>email/mobile number.|
|**Trigger**|The user selects 'Sign Up' on the mobile application or web dashboard.|
|**Postconditions**|• A new user record is created in the database.<br>• A verification email/SMS log entry is created for audit purposes.|
|**Dependencies**|BR-001, BR-002, Section 9 (Validation Rules), Section 10 (Email/SMS<br>Interfaces)|



###### **Main Flow** 

1. The user selects the account type (Pet Owner, Shelter, NGO, Veterinarian, Rescue Organization). 

2. The user enters full name, email address, mobile number, and password. 

3. The system validates the input against the Validation Rules defined in Section 9. 

4. The system sends an OTP/verification link to the registered email or mobile number. 

5. The user enters the OTP or clicks the verification link. 

6. The system creates the user account with a 'Pending Verification' or 'Active' status depending on account type. 

7. For Shelter, NGO, Veterinarian, and Rescue Organization accounts, the system routes the profile to the Administration module for document verification (Section 7.24). 

Page 14 of 70 

_PawMatch AI — Functional Requirements Specification_ 

###### **Alternative Flow** 

- If the user chooses social sign-up (Google/Apple), the system retrieves name and email from the provider and skips password creation. 

###### **Exceptions** 

- If the email/mobile number is already registered, the system displays 'Account already exists' and offers a login/password-reset option. 

- If OTP verification fails after 5 attempts, the system locks the registration attempt for 15 minutes. 

###### **Acceptance Criteria** 

- A new user can successfully register and receive an OTP within 60 seconds. 

- Duplicate registrations using the same email/mobile are rejected. 

- Institutional accounts (Shelter/NGO/Vet) are placed in 'Pending Verification' status until Admin approval. 

##### **FR-002  User Login and Session Management** 

|**Description**|The system shall authenticate registered users via email/mobile and<br>password, or via social login, and shall maintain a secure session for the<br>duration of platform use.|
|---|---|
|**Actors**|All registered users|
|**Priority**|High|
|**Preconditions**|• The user must hold a verified, active account.|
|**Trigger**|The user submits login credentials on the mobile application or web<br>dashboard.|
|**Postconditions**|• A login event is recorded in the Login Logs (Section 12.2).<br>• A valid session token is issued to the client application.|
|**Dependencies**|FR-001, BR-003, Section 13 (Security Requirements)|



**Main Flow** 

8. The user enters registered email/mobile number and password. 

9. The system validates the credentials against stored (hashed) credentials. 

10. The system issues a secure session token (JWT) with a defined expiry. 

11. The system redirects the user to the role-specific home screen (Section 6, User Roles). 

###### **Alternative Flow** 

- The user logs in using biometric authentication (fingerprint/Face ID) if previously enrolled on a mobile device. 

- The user logs in via Google or Apple SSO. 

Page 15 of 70 

_PawMatch AI — Functional Requirements Specification_ 

###### **Exceptions** 

- If credentials are invalid, the system displays a generic 'Invalid email/password' message and increments the failed-attempt counter. 

- After 5 consecutive failed attempts, the account is temporarily locked for 30 minutes and the user is notified by email. 

###### **Acceptance Criteria** 

- A verified user can log in successfully using correct credentials. 

- An account is locked after 5 failed login attempts. 

- Session tokens expire after the configured inactivity period and require re-authentication. 

##### **FR-003  Password Reset and Recovery** 

|**Description**|The system shall provide a self-service mechanism for users to reset a<br>forgotten password through a verified email or mobile number.|
|---|---|
|**Actors**|All registered users|
|**Priority**|Medium|
|**Preconditions**|• The user must have a registered and verified email address or mobile<br>number.|
|**Trigger**|The user selects 'Forgot Password' on the login screen.|
|**Postconditions**|• The password is updated in the system.<br>• A password-change event is recorded in the audit log (Section 12).|
|**Dependencies**|FR-002, BR-003, Section 9.2 (Password Policy)|



###### **Main Flow** 

12. The user enters the registered email or mobile number. 

13. The system generates a time-bound (15-minute) password-reset link or OTP and dispatches it via the Email/SMS interface. 

14. The user opens the link/enters the OTP and defines a new password meeting the password policy (Section 9.2). 

15. The system updates the stored password hash and invalidates all existing sessions for the account. 

###### **Alternative Flow** 

- If the reset link expires before use, the system allows the user to request a new one. 

###### **Exceptions** 

- If the entered email/mobile is not found in the system, the system displays a neutral confirmation message without disclosing account existence, for security purposes. 

###### **Acceptance Criteria** 

Page 16 of 70 

_PawMatch AI — Functional Requirements Specification_ 

- A user can reset a forgotten password within 3 steps. 

- Reset links/OTPs expire after 15 minutes. 

- All active sessions are terminated after a successful password reset. 

#### **7.2 User Profiles** 

##### **FR-004  Create and Edit User Profile** 

|**Description**|The system shall allow users to create and maintain a personal or<br>organizational profile containing demographic, contact, and preference<br>information relevant to their role.|
|---|---|
|**Actors**|Pet Owner, Shelter, NGO, Veterinarian, Rescue Organization|
|**Priority**|High|
|**Preconditions**|• The user must be logged in with a verified account.|
|**Trigger**|The user navigates to the 'My Profile' section and selects 'Edit'.|
||• The user profile record is updated in the database.|
|**Postconditions**|• Updated lifestyle data feeds into the AI Pet Matching module (Section<br>7.9).|
|**Dependencies**|FR-001, Section 9 (Validation Rules), FR-018 (AI Pet Matching)|



###### **Main Flow** 

16. The system displays the current profile fields (name, photo, address, household details, lifestyle preferences, etc.). 

17. The user updates one or more fields. 

18. The system validates the entered data. 

19. The system saves the updated profile and displays a confirmation message. 

###### **Alternative Flow** 

- The user uploads a new profile photo, which is processed and stored via the Cloud Storage interface (Section 10.5). 

###### **Exceptions** 

- If mandatory fields are left blank, the system prevents saving and highlights the missing fields. 

###### **Acceptance Criteria** 

- Profile changes are saved and reflected immediately across the platform. 

- Mandatory field validation prevents incomplete profile submission. 

Page 17 of 70 

_PawMatch AI — Functional Requirements Specification_ 

##### **FR-005  Role-Based Profile View and Visibility Control** 

|**Description**|The system shall display profile information differently depending on the<br>viewer's role and shall allow users to control the visibility of specific profile<br>fields to other users.|
|---|---|
|**Actors**|All registered users, Administrator|
|**Priority**|Medium|
|**Preconditions**|• The profile owner must have completed initial profile creation (FR-004).|
|**Trigger**|Another user (e.g., a Shelter Administrator reviewing an adoption applicant)<br>views a user's profile.|
|**Postconditions**|• Profile visibility settings are persisted and enforced on every subsequent<br>view request.|
|**Dependencies**|FR-004, BR-010, Section 13 (Security Requirements)|



###### **Main Flow** 

20. The system determines the viewer's role and relationship to the profile owner (e.g., adoption applicant vs. shelter reviewer). 

21. The system displays the subset of profile fields permitted for that role and relationship, per BR010. 

22. Fields marked 'private' by the profile owner are withheld unless required for adoption verification. 

###### **Alternative Flow** 

- An Administrator may view the full profile for moderation or verification purposes regardless of privacy settings. 

###### **Exceptions** 

- If a viewer without sufficient permission attempts to access restricted fields, the system denies access and logs the attempt. 

###### **Acceptance Criteria** 

- Restricted fields are not visible to unauthorized roles. 

- Adoption reviewers can view the fields required for Adoption Readiness Scoring (FR-011). 

#### **7.3 Pet Management** 

##### **FR-006  Create Pet Listing** 

||The system shall allow Shelters, NGOs, Rescue Organizations, and verified|
|---|---|
|**Description**|Foster Caregivers to create a listing for a pet available for adoption or<br>fostering.|



Page 18 of 70 

_PawMatch AI — Functional Requirements Specification_ 

|**Actors**|Shelter Administrator, NGO Administrator, Rescue Organization, Foster<br>Caregiver|
|---|---|
|**Priority**|High|
|**Preconditions**|• The creating account must be verified (Section 7.24, Administration).|
|**Trigger**|The user selects 'Add New Pet' from the Shelter/NGO Dashboard.|
|**Postconditions**|• A new pet record is created and linked to the creating organization.<br>• The pet becomes searchable in the Pet Adoption module (Section 7.4).|
|**Dependencies**|FR-023, BR-011, Section 9.4 (Image Upload Constraints)|



**Main Flow** 

23. The user enters pet details: species, breed, estimated age, sex, size, health status, temperament notes, and vaccination status. 

24. The user uploads one or more photographs of the pet. 

25. The system triggers AI Image Recognition (FR-023) to auto-suggest breed, age estimate, and body condition. 

26. The user reviews and confirms/edits AI suggestions. 

27. The system publishes the listing to the Pet Adoption catalogue with status 'Available'. 

###### **Alternative Flow** 

- The listing is created with status 'Draft' if the user chooses to save without publishing. 

- **Exceptions** 

- If mandatory fields (species, photo, health status) are missing, the system blocks publishing and lists the outstanding fields. 

**Acceptance Criteria** 

- A verified shelter can publish a complete pet listing in under 5 minutes. 

- AI-suggested breed/age fields are editable prior to publishing. 

##### **FR-007  Edit, Deactivate, or Remove Pet Listing** 

|**Description**|The system shall allow the owning organization to update pet listing details,<br>mark a pet as adopted/fostered, or remove a listing.|
|---|---|
|**Actors**|Shelter Administrator, NGO Administrator, Rescue Organization|
|**Priority**|High|
|**Preconditions**|• The user must be the owning organization or an Administrator.|
|**Trigger**|The user selects 'Edit' or 'Remove' on an existing pet listing.|



Page 19 of 70 

_PawMatch AI — Functional Requirements Specification_ 

|**Postconditions**|• The pet record and its status history are updated.<br>• Adoption statistics are updated for Reporting (Section 11).|
|---|---|
|**Dependencies**|FR-006, FR-009, BR-011|



###### **Main Flow** 

28. The system displays the current listing details in an editable form. 

29. The user modifies fields or changes the listing status (Available, On Hold, Adopted, Fostered, Deceased). 

30. The system saves the changes and updates the listing's public visibility accordingly. 

###### **Alternative Flow** 

- If status is changed to 'Adopted', the system automatically closes any pending adoption applications for that pet and notifies other applicants (Section 16, Notifications). 

###### **Exceptions** 

- Listings with an active, approved adoption in progress cannot be deleted; they may only be marked 'Adopted' or 'On Hold'. 

###### **Acceptance Criteria** 

- Status changes are reflected in the public catalogue within 1 minute. 

- Deletion is blocked while an approved adoption is pending. 

##### **FR-008  Pet Media Upload and Management** 

|**Description**|The system shall allow authorized users to upload, reorder, and remove<br>photographs and short videos associated with a pet listing, subject to defined<br>file constraints.|
|---|---|
|**Actors**|Shelter Administrator, NGO Administrator, Rescue Organization, Foster<br>Caregiver|
|**Priority**|Medium|
|**Preconditions**|• The pet listing must already exist (FR-006).|
|**Trigger**|The user selects 'Manage Media' on a pet listing.|
|**Postconditions**|• Media assets are linked to the pet record and available across the<br>platform.|
|**Dependencies**|Section 9.4 (Image/Video Constraints), Section 10.5 (Cloud Storage Interface)|



###### **Main Flow** 

31. The user uploads image or video files from a device or cloud storage. 

32. The system validates file type, size, and resolution against Section 9.4. 

Page 20 of 70 

_PawMatch AI — Functional Requirements Specification_ 

33. The system stores the media in Cloud Storage and generates optimized thumbnails. 

34. The user arranges the display order and selects a primary (cover) photo. 

###### **Alternative Flow** 

- The user removes an existing media item, which is soft-deleted and retained for 30 days for recovery purposes. 

###### **Exceptions** 

- Files exceeding the size/format limits are rejected with an explanatory message. 

###### **Acceptance Criteria** 

- A user can upload up to 10 images and 1 video per pet listing. 

- Rejected uploads display a clear reason to the user. 

#### **7.4 Pet Adoption** 

##### **FR-009  Browse and Search Pet Listings** 

|**Description**|The system shall allow users to browse, filter, and search available pet listings<br>by species, breed, age, location, size, and compatibility attributes.|
|---|---|
|**Actors**|Pet Owner (prospective adopter)|
|**Priority**|High|
|**Preconditions**|• None (browsing is available to guest and registered users; applying<br>requires registration).|
|**Trigger**|The user opens the 'Adopt' section of the application.|
|**Postconditions**|• Search interactions are logged for AI recommendation refinement.|
|**Dependencies**|FR-006, FR-019, Section 14 (Performance Requirements)|



###### **Main Flow** 

35. The system displays a paginated catalogue of available pet listings. 

36. The user applies filters (species, breed, age range, distance, size, gender, special needs). 

37. The system returns matching results ranked by relevance and, where AI Pet Matching has been completed, by compatibility score (FR-019). 

###### **Alternative Flow** 

- The user performs a free-text search by pet name or breed keyword. 

###### **Exceptions** 

- If no listings match the applied filters, the system displays a 'No results' message with suggestions to broaden the search. 

###### **Acceptance Criteria** 

Page 21 of 70 

_PawMatch AI — Functional Requirements Specification_ 

- Search results return within 2 seconds under normal load. 

- Filters can be combined without error. 

##### **FR-010  Submit Adoption Application** 

|**Description**|The system shall allow a registered user to submit a formal application to<br>adopt a specific pet listing.|
|---|---|
|**Actors**|Pet Owner|
|**Priority**|High|
|**Preconditions**|• The user must be logged in.<br>• The pet listing must have status 'Available'.|
|**Trigger**|The user selects 'Apply to Adopt' on a pet listing.|
|**Postconditions**|• An adoption application record is created with status 'Submitted'.<br>• The owning organization receives a notification (Section 16).|
|**Dependencies**|FR-004, FR-011, BR-012|



###### **Main Flow** 

38. The system presents the adoption application form, pre-filled with existing profile data where available. 

39. The user completes remaining required fields (home environment, household members, prior pet experience, availability for a home visit). 

40. The user submits the application. 

41. The system computes an Adoption Readiness Score (FR-011) and routes the application to the owning organization's dashboard (Section 7.5). 

###### **Alternative Flow** 

- The user saves the application as a draft to complete later. 

###### **Exceptions** 

- A user may not submit more than 3 concurrent pending applications, per BR-012, to reduce speculative applications. 

###### **Acceptance Criteria** 

- A completed application is submitted and visible in the shelter dashboard within 1 minute. 

- The 3-concurrent-application limit is enforced. 

##### **FR-011  Adoption Application Review, Adoption Readiness Score, and Approval** 

Page 22 of 70 

_PawMatch AI — Functional Requirements Specification_ 

|**Description**|The system shall enable the owning organization to review submitted<br>applications, view the AI-generated Adoption Readiness Score, and approve,<br>reject, or place an application on a waiting list.|
|---|---|
|**Actors**|Shelter Administrator, NGO Administrator, Rescue Organization|
|**Priority**|High|
|**Preconditions**|• At least one adoption application must be submitted for a pet listing (FR-<br>010).|
|**Trigger**|The reviewer opens the 'Applications' tab on the Shelter Dashboard.|
|**Postconditions**|• The application status is updated.<br>• Rejected or waitlisted applicants are notified with a reason category.<br>• Approved adoption triggers pet-status update (FR-007) and health-<br>record transfer initiation (FR-016).|
|**Dependencies**|FR-010, FR-007, FR-016, BR-013|



###### **Main Flow** 

42. The system displays the list of applications for a given pet, ordered by submission date and Adoption Readiness Score. 

43. The reviewer opens an application to view applicant profile, home-environment responses, and Adoption Readiness Score (home environment, lifestyle, financial capability indicators, prior ownership, vet references). 

44. The reviewer may request a home visit, additional documents, or a reference check via in-app chat. 

45. The reviewer approves, rejects, or waitlists the application. 

46. On approval, the system marks the pet as 'On Hold' and schedules pickup/handover coordination. 

###### **Alternative Flow** 

- The reviewer may compare multiple applicants for the same pet side by side. 

- **Exceptions** 

- If the reviewer takes no action within the organization's configured SLA (default 7 days), the system sends an escalation reminder. 

**Acceptance Criteria** 

- Reviewers can approve/reject an application in a single workflow without leaving the dashboard. 

- The Adoption Readiness Score is visible on every application record. 

#### **7.5 Shelter Dashboard** 

**FR-012  Shelter Onboarding and Verification** 

Page 23 of 70 

_PawMatch AI — Functional Requirements Specification_ 

|**Description**|The system shall provide a guided onboarding workflow for shelters to submit<br>registration and legal documentation for verification prior to gaining<br>publishing privileges.|
|---|---|
|**Actors**|Shelter Administrator, Platform Administrator|
|**Priority**|High|
|**Preconditions**|• The shelter must have completed basic registration (FR-001).|
|**Trigger**|The Shelter Administrator selects 'Complete Shelter Verification'.|
|**Postconditions**|• Verification decision and supporting documents are retained for audit<br>(Section 12).|
|**Dependencies**|FR-001, FR-024, BR-014|



**Main Flow** 

47. The shelter uploads registration certificate, address proof, and authorized-signatory identification. 

48. The system routes the submission to the Administration verification queue (Section 7.24). 

49. The Platform Administrator reviews documents and approves or rejects the application. 

50. On approval, the shelter account status changes to 'Verified' and full dashboard access is granted. 

###### **Alternative Flow** 

- The Administrator requests additional documentation, returning the submission to the shelter with comments. 

- **Exceptions** 

- Unverified shelters may access the dashboard in read-only/preview mode but cannot publish pet listings. 

**Acceptance Criteria** 

- A shelter cannot publish listings until verification is approved. 

- Verification decisions are logged with timestamp and reviewing administrator. 

##### **FR-013  Manage Adoption Applications and Pet Listings from Dashboard** 

|**Description**|The system shall provide shelters a consolidated dashboard to manage all pet<br>listings, incoming applications, and adopter communications from a single<br>interface.|
|---|---|
|**Actors**|Shelter Administrator|
|**Priority**|High|
|**Preconditions**|• The shelter account must be verified (FR-012).|



Page 24 of 70 

_PawMatch AI — Functional Requirements Specification_ 

|**Trigger**|The Shelter Administrator logs into the dashboard.|
|---|---|
|**Postconditions**|• Dashboard activity is reflected in real time across all connected staff<br>sessions.|
|**Dependencies**|FR-006, FR-007, FR-011, Section 6 (User Roles)|



- **Main Flow** 

51. The system displays summary widgets: active listings, pending applications, upcoming visits, and vaccination reminders. 

52. The Administrator navigates to manage individual listings (FR-006, FR-007) or applications (FR011). 

53. The Administrator communicates with applicants via integrated in-app chat. 

###### **Alternative Flow** 

- The Administrator delegates access to additional staff accounts with restricted permissions (Section 6). 

###### **Exceptions** 

- Suspended shelter accounts (Section 7.24) lose dashboard write access but retain read access to historical records. 

**Acceptance Criteria** 

- Dashboard summary loads within 2 seconds. 

- Multiple staff accounts can operate under one shelter organization with distinct permissions. 

##### **FR-014  Shelter Analytics and Reporting View** 

|**Description**|The system shall provide shelters with analytics on listing performance,<br>adoption conversion rates, and application volume.|
|---|---|
|**Actors**|Shelter Administrator|
|**Priority**|Medium|
|**Preconditions**|• The shelter must have at least one published listing.|
|**Trigger**|The Shelter Administrator opens the 'Analytics' tab.|
|**Postconditions**|• Generated reports are retained in report history for 12 months.|
|**Dependencies**|FR-025, Section 11 (Reporting Requirements)|



###### **Main Flow** 

54. The system aggregates listing views, application counts, and adoption conversion rate over a selectable date range. 

55. The system displays the data as charts and summary tables. 

Page 25 of 70 

_PawMatch AI — Functional Requirements Specification_ 

56. The Administrator exports the report as PDF or CSV. 

###### **Alternative Flow** 

- Premium Shelter Dashboard subscribers receive extended AI analytics, including predicted time-toadoption (Section 7.25). 

###### **Exceptions** 

- If insufficient data exists for the selected period, the system displays a 'Not enough data' notice. 

###### **Acceptance Criteria** 

- Analytics reflect data no more than 24 hours old. 

- Export functions produce a correctly formatted PDF/CSV file. 

#### **7.6 NGO Dashboard** 

##### **FR-015  NGO Registration and Verification** 

|**Description**|The system shall provide NGOs and Rescue Organizations a verification<br>workflow equivalent to Shelter onboarding, including nonprofit registration<br>validation.|
|---|---|
|**Actors**|NGO Administrator, Platform Administrator|
|**Priority**|High|
|**Preconditions**|• The NGO must have completed basic registration (FR-001).|
|**Trigger**|The NGO Administrator selects 'Complete NGO Verification'.|
|**Postconditions**|• Verified NGOs gain access to sponsorship campaign management (FR-<br>016 module) and CSR partnership tools.|
|**Dependencies**|FR-001, FR-024, BR-014|



###### **Main Flow** 

57. The NGO uploads nonprofit registration certificate, tax-exemption/CSR eligibility documents (where applicable), and authorized-representative identification. 

58. The system routes the submission to the Administration verification queue. 

59. The Platform Administrator approves or rejects the submission. 

###### **Alternative Flow** 

- An NGO may link to an existing Shelter account under the same legal entity, subject to Administrator approval. 

###### **Exceptions** 

- Rejected submissions are returned with a specific reason and may be resubmitted. 

###### **Acceptance Criteria** 

Page 26 of 70 

_PawMatch AI — Functional Requirements Specification_ 

- Verification status is visible to the NGO at all times. 

- Verified NGOs can create sponsorship campaigns immediately upon approval. 

##### **FR-016  Pet Sponsorship Campaign Management** 

|**Description**|The system shall allow verified NGOs to create monthly sponsorship<br>campaigns for rescued or shelter animals and to track sponsor contributions.|
|---|---|
|**Actors**|NGO Administrator, Pet Owner (Sponsor)|
|**Priority**|Medium|
|**Preconditions**|• The NGO account must be verified (FR-015).|
|**Trigger**|The NGO Administrator selects 'Create Sponsorship Campaign'.|
|**Postconditions**|• Sponsorship transactions are recorded and reflected in NGO revenue<br>reports (Section 11).|
|**Dependencies**|FR-021, FR-022, BR-020|



###### **Main Flow** 

60. The Administrator selects a pet record and defines the monthly sponsorship amount and campaign description. 

61. The system publishes the campaign to the Community Feed and Pet Sponsorship module. 

62. A donor selects a campaign and completes a recurring payment via the Payment Gateway (Section 7.20). 

63. The system updates the campaign's funding progress and sends the donor a monthly contribution receipt. 

###### **Alternative Flow** 

- A sponsor may cancel a recurring contribution at any time from 'My Sponsorships'. 

###### **Exceptions** 

- If a recurring payment fails, the system retries per BR-020 and notifies the sponsor before pausing the sponsorship. 

###### **Acceptance Criteria** 

- A sponsor can commit to a monthly contribution in under 3 steps. 

- Failed payments trigger the defined retry and notification sequence. 

#### **7.7 Veterinarian Portal** 

**FR-017  Veterinarian Registration and Verification** 

Page 27 of 70 

_PawMatch AI — Functional Requirements Specification_ 

|**Description**|The system shall allow licensed veterinarians to register, submit credentials<br>for verification, and publish a bookable practice profile.|
|---|---|
|**Actors**|Veterinarian, Platform Administrator|
|**Priority**|High|
|**Preconditions**|• The veterinarian must have completed basic registration (FR-001).|
|**Trigger**|The veterinarian selects 'Complete Veterinarian Verification'.|
|**Postconditions**|• Verified veterinarian profile becomes available in the Vet Booking<br>module.|
|**Dependencies**|FR-001, FR-024, BR-014|



- **Main Flow** 

64. The veterinarian uploads professional license number, clinic registration, and identification documents. 

65. The system routes the submission for Administrator review. 

66. On approval, the veterinarian's clinic profile, service list, and availability calendar become publicly bookable. 

**Alternative Flow** 

- A veterinary clinic with multiple practitioners may add additional practitioner profiles under one verified clinic account. 

**Exceptions** 

- Unverified veterinarian profiles are hidden from search and booking results. 

**Acceptance Criteria** 

- Only verified veterinarians appear in booking search results. 

- License numbers are validated for correct format before submission. 

##### **FR-018  Veterinary Appointment Management** 

|**Description**|The system shall allow pet owners to book, reschedule, or cancel veterinary<br>appointments, and shall allow veterinarians to manage their appointment<br>calendar.|
|---|---|
|**Actors**|Pet Owner, Veterinarian|
|**Priority**|High|
|**Preconditions**|• The veterinarian profile must be verified and have published availability.|
|**Trigger**|The pet owner selects 'Book Appointment' on a veterinarian profile.|



Page 28 of 70 

_PawMatch AI — Functional Requirements Specification_ 

|**Postconditions**|• Appointment record is created/updated.<br>• Reminder entries are scheduled in the Reminder System (Section 7.16).|
|---|---|
|**Dependencies**|FR-017, FR-020, FR-026, BR-021|



###### **Main Flow** 

67. The pet owner selects the pet, desired service (consultation, vaccination, surgery follow-up, teleconsultation), and an available time slot. 

68. The system reserves the slot and requests payment/confirmation where applicable (Section 7.20). 

69. The system sends a confirmation and calendar reminder to both parties. 

70. The veterinarian updates the appointment status (Completed, No-show, Rescheduled) after the visit and, where relevant, updates the pet's Health Record (FR-020). 

###### **Alternative Flow** 

- The pet owner books a tele-veterinary consultation conducted via in-app video (Year 2 roadmap capability, Section 4.5). 

###### **Exceptions** 

- Double-booking of a time slot is prevented at the database level. 

- Cancellations within the clinic's configured cancellation window may incur a fee per BR-021. 

###### **Acceptance Criteria** 

- No two appointments can be booked for the same veterinarian and time slot. 

- Both parties receive a reminder 24 hours before the appointment. 

#### **7.8 Health Records** 

**FR-019  Digital Pet Health Record Creation and Maintenance** 

|**Description**|The system shall provide a digital health record for each pet, storing<br>vaccination history, medical history, prescriptions, surgeries, and lab reports.|
|---|---|
|**Actors**|Pet Owner, Veterinarian, Shelter Administrator|
|**Priority**|High|
|**Preconditions**|• The pet profile must exist in the system (created via FR-006 or added<br>directly by a Pet Owner).|
|**Trigger**|A veterinarian completes a consultation, or a pet owner manually logs a health<br>event.|
|**Postconditions**|• Health record history is available for the pet's lifetime, including after<br>adoption transfer.|



Page 29 of 70 

_PawMatch AI — Functional Requirements Specification_ 

**Dependencies** FR-018, FR-026, BR-015 

###### **Main Flow** 

71. The authorized user selects the pet's Health Record. 

72. The user adds an entry: type (vaccination, medication, surgery, lab report, general note), date, and supporting document/photo. 

73. The system timestamps and stores the entry, attributing it to the entering user/veterinarian. 

74. The system updates the Reminder System with any follow-up dates (e.g., next vaccination due). 

**Alternative Flow** 

- Lab reports and prescriptions may be uploaded as PDF/image attachments via OCR-assisted data extraction. 

- **Exceptions** 

- Health record entries cannot be deleted once finalized; corrections are appended as amendments, preserving the original entry for audit purposes. 

**Acceptance Criteria** 

- Every health event is timestamped, attributed, and immutable once saved. 

- Follow-up reminders are automatically created where a due date is specified. 

##### **FR-020  Health Record Access, Transfer, and Sharing** 

|**Description**|The system shall allow health records to be transferred to a new owner upon<br>adoption and shared securely with a veterinarian at the owner's discretion.|
|---|---|
|**Actors**|Pet Owner, Veterinarian, Shelter Administrator|
|**Priority**|Medium|
|**Preconditions**|• A completed adoption (FR-011) or an explicit sharing request must exist.|
|**Trigger**|An adoption is finalized, or a pet owner selects 'Share Health Record' with a<br>veterinarian.|
|**Postconditions**|• Access grants and revocations are recorded in the audit log (Section 12).|
|**Dependencies**|FR-011, FR-019, Section 13 (Security Requirements)|



**Main Flow** 

75. On adoption finalization, the system automatically transfers ownership of the pet's health record to the new owner's account. 

76. The previous organization retains read-only historical access for compliance purposes. 

77. For sharing, the owner selects a veterinarian and grants time-bound read access to the record. 

**Alternative Flow** 

Page 30 of 70 

_PawMatch AI — Functional Requirements Specification_ 

- The owner may revoke a veterinarian's access at any time. 

###### **Exceptions** 

- Access requests from unauthorized parties are denied and logged. 

###### **Acceptance Criteria** 

- Health records transfer automatically and completely upon adoption finalization. 

- Shared access can be revoked immediately by the owner. 

#### **7.9 AI Pet Matching** 

##### **FR-021  Adopter Preference Questionnaire** 

|**Description**|The system shall present a structured questionnaire capturing lifestyle,<br>housing, household composition, working hours, budget, prior experience,<br>and activity level to drive AI-based pet matching.|
|---|---|
|**Actors**|Pet Owner|
|**Priority**|High|
|**Preconditions**|• The user must be logged in.|
|**Trigger**|The user selects 'Find My Match' from the Adoption home screen.|
|**Postconditions**|• A Matching Profile is created or updated for the user.|
|**Dependencies**|FR-004, FR-022|



###### **Main Flow** 

78. The system presents a multi-step questionnaire covering lifestyle, house size, presence of children, working hours, budget, prior pet-ownership experience, and activity level. 

79. The user submits responses. 

80. The system stores the responses as the user's Matching Profile and passes them to the AI Match Recommendation Engine (FR-022). 

###### **Alternative Flow** 

- The user may retake the questionnaire at any time to refresh recommendations. 

###### **Exceptions** 

- Incomplete questionnaires cannot be submitted; the system highlights unanswered required questions. 

###### **Acceptance Criteria** 

- The questionnaire can be completed in under 3 minutes. 

- Responses are persisted and reusable across sessions. 

Page 31 of 70 

_PawMatch AI — Functional Requirements Specification_ 

##### **FR-022  AI Match Recommendation Generation** 

|**Description**|The system shall use the AI Recommendation Engine to generate a ranked list<br>of suitable pets for a user based on their Matching Profile and shall present a<br>plain-language rationale for each recommendation.|
|---|---|
|**Actors**|Pet Owner, AI Recommendation Engine|
|**Priority**|High|
|**Preconditions**|• The user must have completed the Adopter Preference Questionnaire<br>(FR-021).|
|**Trigger**|The user submits or updates the questionnaire, or opens the 'Recommended<br>for You' screen.|
|**Postconditions**|• Recommendation results and user feedback are logged for AI Usage Logs<br>(Section 12.3).|
|**Dependencies**|FR-021, FR-009, Section 10.6 (AI Services Interface)|



###### **Main Flow** 

81. The system submits the Matching Profile and available pet attributes to the AI Recommendation Engine. 

82. The engine returns a ranked set of pet listings with a compatibility score. 

83. The system displays each recommendation with a natural-language explanation (e.g., compatibility relative to living space and working hours). 

84. The user may accept a recommendation to view full listing details or apply to adopt (FR-010). 

###### **Alternative Flow** 

- The user provides feedback (thumbs up/down) on a recommendation, which is used to refine future results. 

###### **Exceptions** 

- If no pets meet a minimum compatibility threshold, the system displays the closest alternatives with a caveat explaining the mismatch. 

###### **Acceptance Criteria** 

- Recommendations are generated within 5 seconds of questionnaire submission. 

- Each recommendation includes a human-readable rationale. 

#### **7.10 AI Health Assistant** 

##### **FR-023  Conversational Health Query Assistant** 

Page 32 of 70 

_PawMatch AI — Functional Requirements Specification_ 

|**Description**|The system shall provide a conversational AI assistant that accepts natural-<br>language descriptions of pet symptoms and returns possible causes, first-aid<br>guidance, and a recommendation on whether veterinary care is required.|
|---|---|
|**Actors**|Pet Owner, AI Health Assistant|
|**Priority**|High|
|**Preconditions**|• The user must be logged in and have at least one pet profile.|
|**Trigger**|The user opens the AI Pet Assistant chat and describes a symptom (e.g., 'My<br>dog isn't eating').|
|**Postconditions**|• The conversation is logged in AI Usage Logs (Section 12.3) and linked to<br>the pet's Health Record as a note.|
|**Dependencies**|FR-019, FR-024, Section 10.6 (AI Services Interface), BR-030|



###### **Main Flow** 

85. The user submits a free-text query, optionally attaching a photo. 

86. The system sends the query, relevant pet profile data (species, age, known conditions), and any photo to the AI Health Assistant service. 

87. The assistant returns possible reasons, general first-aid guidance, and an urgency assessment (Routine / Monitor / Seek Care Soon / Emergency). 

88. The system displays the response and, where urgency is 'Seek Care Soon' or 'Emergency', surfaces a 'Book Vet Now' action. 

###### **Alternative Flow** 

- The user escalates directly to the Emergency Assistant (FR-024) from within the chat. 

###### **Exceptions** 

- The assistant shall not provide a definitive diagnosis or prescribe medication dosages; all responses include a disclaimer recommending professional veterinary consultation for confirmed diagnosis and treatment. 

**Acceptance Criteria** 

- The assistant responds within 5 seconds for text-only queries. 

- Every response includes an urgency classification and a professional-consultation disclaimer. 

##### **FR-024  AI Emergency Assistant and Escalation** 

|**Description**|The system shall detect emergency indicators from user input (e.g., poisoning,<br>choking, trauma) and immediately provide emergency first-aid guidance<br>together with directions to the nearest emergency veterinary clinic.|
|---|---|
|**Actors**|Pet Owner, AI Health Assistant|



Page 33 of 70 

_PawMatch AI — Functional Requirements Specification_ 

|**Priority**|High|
|---|---|
|**Preconditions**|• The user must be logged in.|
|**Trigger**|The user submits a query containing emergency indicators (e.g., 'My puppy<br>swallowed chocolate').|
|**Postconditions**|• The emergency interaction is flagged and retained in AI Usage Logs for<br>quality review.|
|**Dependencies**|FR-023, Section 10.7 (Maps Interface), BR-030|



**Main Flow** 

89. The system classifies the query as an emergency using the AI Health Assistant's urgency model. 

90. The system immediately displays critical first-aid guidance relevant to the described emergency. 

91. The system queries the Maps Interface (Section 10.7) for the nearest open emergency veterinary clinics and displays contact details and directions. 

92. The system offers a one-tap option to call the clinic or book an urgent tele-consultation. 

###### **Alternative Flow** 

- If the user's location is unavailable, the system prompts for a location or postal code to identify nearby clinics. 

- **Exceptions** 

- If no emergency clinic is found within a configurable radius, the system displays the nearest general veterinary clinics and a poison-control style guidance notice. 

**Acceptance Criteria** 

- Emergency queries are classified and responded to within 3 seconds. 

- At least one nearby clinic is surfaced whenever location data is available. 

#### **7.11 AI Image Recognition** 

**FR-025  Breed, Age, and Basic Health Detection from Photo** 

|**Description**|The system shall analyze an uploaded pet photograph using computer vision<br>to estimate breed, approximate age, weight range, and general body<br>condition.|
|---|---|
|**Actors**|Pet Owner, Shelter Administrator, AI Image Recognition Service|
|**Priority**|High|
|**Preconditions**|• A pet photograph must be uploaded in a supported format (Section 9.4).|
|**Trigger**|The user uploads a pet photo during listing creation (FR-006) or profile setup.|



Page 34 of 70 

_PawMatch AI — Functional Requirements Specification_ 

|**Postconditions**|• AI-suggested values and the user's final confirmed values are both logged<br>for model accuracy tracking.|
|---|---|
|**Dependencies**|FR-006, Section 10.6 (AI Services Interface), BR-030|



###### **Main Flow** 

93. The system submits the image to the AI Image Recognition service. 

94. The service returns predicted breed(s) with confidence scores, estimated age range, estimated weight range, and a body-condition classification. 

95. The system pre-fills the corresponding listing/profile fields with the AI output, marked as 'AIsuggested'. 

96. The user reviews and confirms or edits the suggested values before saving. 

###### **Alternative Flow** 

- If the image quality is insufficient for confident analysis, the system requests a clearer photo. 

###### **Exceptions** 

- If confidence scores fall below the configured threshold, the system flags the result as 'Uncertain' and requires manual confirmation. 

###### **Acceptance Criteria** 

- Breed/age/body-condition suggestions are returned within 5 seconds of upload. 

- All AI-suggested fields remain user-editable prior to save. 

##### **FR-026  Skin Condition and Injury Detection** 

|**Description**|The system shall flag potential visible skin diseases or injuries detected in an<br>uploaded pet photograph and prompt the user toward the AI Health Assistant<br>or veterinary booking.|
|---|---|
|**Actors**|Pet Owner, AI Image Recognition Service|
|**Priority**|Medium|
|**Preconditions**|• A pet photograph must be uploaded.|
|**Trigger**|The AI Image Recognition service processes an uploaded photo (FR-025) and<br>detects a visual anomaly.|
|**Postconditions**|• Detected anomalies are logged for audit and model-improvement<br>purposes.|
|**Dependencies**|FR-025, FR-018, FR-023, BR-030|



###### **Main Flow** 

97. The system analyzes the image for visible indicators of skin conditions or injury. 

Page 35 of 70 

_PawMatch AI — Functional Requirements Specification_ 

98. If an anomaly is detected above the confidence threshold, the system displays a non-diagnostic alert describing the observation. 

99. The system offers the user a direct path to the AI Health Assistant (FR-023) or Vet Booking (FR018). 

###### **Alternative Flow** 

- No action is taken if no anomaly is detected. 

###### **Exceptions** 

- The system explicitly states that the alert is not a medical diagnosis and recommends professional veterinary evaluation. 

###### **Acceptance Criteria** 

- Detected anomalies generate an alert with a clear non-diagnostic disclaimer. 

- The user can proceed directly to booking a veterinary appointment from the alert. 

#### **7.12 Behavior Prediction** 

##### **FR-027  AI Behavior Trait Prediction** 

|**Description**|The system shall generate predicted behavioral traits for a pet — including<br>friendliness, aggression risk, activity/hyperactivity level, anxiety indicators,<br>suitability for children, and suitability for apartment living — based on<br>available profile, breed, and shelter-observation data.|
|---|---|
|**Actors**|Pet Owner, Shelter Administrator, AI Recommendation Engine|
|**Priority**|Medium|
|**Preconditions**|• The pet listing must include breed, age, and any available behavior-<br>observation notes entered by the shelter.|
|**Trigger**|A pet listing is created or updated (FR-006), or a user views a pet's detail page.|
|**Postconditions**|• Predicted trait data feeds into the AI Match Recommendation Engine (FR-<br>022) as a compatibility input.|
|**Dependencies**|FR-006, FR-022, BR-030|



###### **Main Flow** 

100. The system submits the pet's profile and any shelter-observation notes to the AI Recommendation Engine. 

101. The engine returns a set of predicted behavior trait scores/labels. 

102. The system displays the traits on the pet's public listing page as indicative guidance, clearly labeled as AI-predicted. 

###### **Alternative Flow** 

Page 36 of 70 

_PawMatch AI — Functional Requirements Specification_ 

- A shelter may manually override or supplement an AI-predicted trait based on direct observation, and the manual entry takes visual precedence. 

###### **Exceptions** 

- Predicted traits are always presented as indicative rather than guaranteed, with a disclaimer that individual pet behavior can vary. 

###### **Acceptance Criteria** 

- Behavior traits are displayed on every pet listing with sufficient source data. 

- Shelter-entered observations are visually distinguished from AI predictions. 

#### **7.13 Lost Pet Finder** 

##### **FR-028  Report a Lost Pet** 

|**Description**|The system shall allow a pet owner to report a pet as lost, providing a<br>photograph, last-known location, and identifying details for inclusion in the<br>Lost Pet Finder search index.|
|---|---|
|**Actors**|Pet Owner|
|**Priority**|High|
|**Preconditions**|• The user must have a registered pet profile or upload details of the<br>missing pet.|
|**Trigger**|The user selects 'Report Lost Pet'.|
|**Postconditions**|• A Lost Pet record is created with status 'Active' until resolved or expired.|
|**Dependencies**|FR-029, Section 10.7 (Maps Interface)|



###### **Main Flow** 

103. The user enters the pet's details, last-known location (via the Maps Interface), date/time last seen, and uploads a clear photograph. 

104. The system publishes a Lost Pet alert to the Community Feed and nearby shelter/rescue dashboards. 

105. The system indexes the photo for facial-recognition matching (FR-029). 

###### **Alternative Flow** 

- The user may set the alert radius and choose to notify nearby shelters directly. 

###### **Exceptions** 

- Reports without a usable photograph are still published but flagged as 'Limited Match Capability'. 

**Acceptance Criteria** 

- A lost pet report becomes visible in the Community Feed within 2 minutes of submission. 

Page 37 of 70 

_PawMatch AI — Functional Requirements Specification_ 

- Reports remain active for a configurable duration (default 60 days) unless resolved sooner. 

##### **FR-029  AI Facial-Match Search Against Shelter and Community Databases** 

|**Description**|The system shall compare an uploaded lost-pet photograph, or a found-pet<br>photograph, against shelter intake records and community-reported records<br>using AI facial recognition and return likely matches.|
|---|---|
|**Actors**|Pet Owner, Shelter Administrator, AI Image Recognition Service|
|**Priority**|Medium|
|**Preconditions**|• A Lost Pet report (FR-028) or a Found Pet report must exist with a usable<br>photograph.|
|**Trigger**|A new Lost Pet or Found Pet photograph is submitted, or a user manually<br>initiates a match search.|
|**Postconditions**|• Confirmed matches close the corresponding Lost Pet report.|
|**Dependencies**|FR-028, FR-025, Section 10.6 (AI Services Interface), BR-030|



###### **Main Flow** 

106. The system submits the photograph to the AI Image Recognition service for facial-feature extraction. 

107. The service compares extracted features against the shelter-intake and community-report databases. 

108. The system returns a ranked list of potential matches with similarity scores. 

109. The reporting user reviews potential matches and, if a match is confirmed, initiates contact with the matched party via in-app chat. 

###### **Alternative Flow** 

- Shelters may run a bulk match sweep of newly intaken animals against the active Lost Pet database. 

###### **Exceptions** 

- Matches below the minimum similarity threshold are not surfaced, to reduce false positives. 

###### **Acceptance Criteria** 

- A match search returns results within 10 seconds. 

- Users can confirm or dismiss a suggested match directly in the app. 

#### **7.14 Nutrition Planner** 

**FR-030  Generate AI Nutrition Plan** 

Page 38 of 70 

_PawMatch AI — Functional Requirements Specification_ 

|**Description**|The system shall generate a personalized diet plan for a pet based on breed,<br>age, weight, known allergies, and medical conditions recorded in the pet's<br>Health Record.|
|---|---|
|**Actors**|Pet Owner, AI Recommendation Engine|
|**Priority**|Medium|
|**Preconditions**|• The pet profile must include breed, age, and weight; allergy/medical data<br>is optional but improves accuracy.|
|**Trigger**|The user selects 'Get Nutrition Plan' from the pet's profile.|
|**Postconditions**|• The generated plan is saved to the pet's profile and can be linked to<br>Reminder System entries for feeding schedules.|
|**Dependencies**|FR-019, FR-031(Marketplace product linkage), BR-030|



###### **Main Flow** 

110. The system submits the pet's profile and Health Record data to the AI Recommendation Engine. 

111. The engine returns a suggested diet plan, including recommended food categories, approximate portion guidance, and feeding frequency. 

112. The system displays the plan and offers relevant Marketplace product suggestions (Section 7.18). 

###### **Alternative Flow** 

- The user may regenerate the plan after updating weight or medical information. 

###### **Exceptions** 

- The plan explicitly states it is general guidance and recommends veterinary consultation for pets with diagnosed medical conditions. 

###### **Acceptance Criteria** 

- A nutrition plan is generated within 5 seconds of request. 

- The plan updates when underlying weight/medical data changes. 

#### **7.15 Training Coach** 

##### **FR-031  Personalized AI Training Program Generation** 

|**Description**|The system shall generate a personalized, step-by-step training program<br>covering toilet training, basic obedience, behavior correction, leash walking,<br>and puppy care based on the pet's age, breed, and reported behavior<br>challenges.|
|---|---|
|**Actors**|Pet Owner, AI Recommendation Engine|
|**Priority**|Medium|



Page 39 of 70 

_PawMatch AI — Functional Requirements Specification_ 

|**Preconditions**|• The pet profile must include age and breed.|
|---|---|
|**Trigger**|The user selects 'Start Training Coach' and specifies a training goal.|
|**Postconditions**|• Training progress is saved to the pet's profile and reflected in Reminder<br>System entries for daily training sessions.|
|**Dependencies**|FR-019, Section 7.16 (Reminder System), BR-030|



- **Main Flow** 

113. The user selects a training category (toilet training, obedience, behavior correction, leash walking, puppy care) and describes any specific challenges. 

114. The system requests a structured multi-day training plan from the AI Recommendation Engine. 

115. The system displays the plan as a sequence of daily/weekly steps with instructions and estimated duration. 

116. The user marks steps as complete, and the system tracks progress. 

**Alternative Flow** 

- The user may request the AI to adjust the plan if a step is proving ineffective. 

**Exceptions** 

- For behavior challenges indicating potential aggression or safety risk, the system recommends consulting a certified professional trainer or veterinary behaviorist in addition to the generated plan. 

**Acceptance Criteria** 

- A training plan is generated within 5 seconds. 

- Progress tracking persists across sessions. 

#### **7.16 Reminder System** 

##### **FR-032  Create and Manage Reminders** 

|**Description**|The system shall allow users to create, edit, and delete reminders for<br>vaccinations, medications, veterinary visits, deworming, grooming, and pet<br>birthdays, and shall auto-generate reminders from linked events (e.g.,<br>vaccination entries).|
|---|---|
|**Actors**|Pet Owner, Shelter Administrator|
|**Priority**|High|
|**Preconditions**|• A pet profile must exist.|
|**Trigger**|The user manually creates a reminder, or a triggering event occurs (e.g., a<br>vaccination entry with a follow-up date is saved).|



Page 40 of 70 

_PawMatch AI — Functional Requirements Specification_ 

|**Postconditions**|• Reminder records are persisted and linked to the relevant pet and, where<br>applicable, source event.|
|---|---|
|**Dependencies**|FR-019, FR-033, Section 16 (Notifications)|



###### **Main Flow** 

117. The user selects 'Add Reminder', chooses a category, date/time, and recurrence pattern (onetime, weekly, monthly, annually). 

118. The system saves the reminder and schedules delivery via the Notification System (Section 7.17). 

119. The user may edit or delete the reminder at any time before it fires. 

###### **Alternative Flow** 

- The system auto-creates a reminder when a Health Record entry (FR-019) specifies a follow-up date, which the user may edit or dismiss. 

###### **Exceptions** 

- Reminders scheduled in the past are rejected with a validation message. 

###### **Acceptance Criteria** 

- Reminders fire within 1 minute of the scheduled time. 

- Recurring reminders regenerate automatically after each occurrence. 

##### **FR-033  Automated Multi-Channel Reminder Delivery** 

|**Description**|The system shall deliver due reminders to users through push notification,<br>WhatsApp, and/or voice-assistant channels according to the user's notification<br>preferences.|
|---|---|
|**Actors**|Pet Owner, Notification Service|
|**Priority**|High|
|**Preconditions**|• At least one reminder must be due, and the user must have at least one<br>active notification channel configured.|
|**Trigger**|A scheduled reminder reaches its trigger time.|
|**Postconditions**|• Delivery attempts and outcomes are logged (Section 12).|
|**Dependencies**|FR-032, Section 10.2 (Email), 10.3 (SMS/WhatsApp), 10.4 (Push Notifications)|



###### **Main Flow** 

120. The scheduler identifies due reminders. 

121. The system composes the reminder message and dispatches it via the user's preferred channel(s) using the relevant External Interface (Section 10). 

122. The system records delivery status (sent, delivered, failed). 

Page 41 of 70 

_PawMatch AI — Functional Requirements Specification_ 

###### **Alternative Flow** 

- If the primary channel fails, the system falls back to a secondary configured channel. 

###### **Exceptions** 

- If all configured channels fail, the reminder is displayed in-app on next login and flagged as 'Missed Delivery'. 

###### **Acceptance Criteria** 

- At least 99% of reminders are dispatched within 1 minute of their scheduled time. 

- Failed deliveries are retried at least once before being flagged. 

#### **7.17 Notifications** 

##### **FR-034  Multi-Channel Notification Dispatch and Preference Management** 

|**Description**|The system shall generate and dispatch transactional and informational<br>notifications (application updates, messages, reminders, promotional<br>content) across push, email, SMS/WhatsApp, and in-app channels, and shall<br>allow users to manage channel preferences per notification category.|
|---|---|
|**Actors**|All registered users, Notification Service|
|**Priority**|High|
|**Preconditions**|• The user must have at least one verified contact channel.|
|**Trigger**|A system event occurs that requires user notification (e.g., application status<br>change, new message, reminder due).|
|**Postconditions**|• All dispatched notifications are recorded with category, channel, and<br>delivery status.|
|**Dependencies**|FR-033, Section 10 (External Interfaces), BR-025|



###### **Main Flow** 

123. The system identifies the notification category and the recipient's channel preferences. 

124. The system composes the notification content and dispatches it through the enabled channel(s). 

125. The notification is also logged to the in-app Notification Center regardless of external channel delivery. 

###### **Alternative Flow** 

- Users may mute non-essential categories (e.g., promotional) while retaining transactional notifications. 

###### **Exceptions** 

- Legally or safety-critical notifications (e.g., emergency alerts, payment confirmations) cannot be fully muted. 

Page 42 of 70 

_PawMatch AI — Functional Requirements Specification_ 

###### **Acceptance Criteria** 

- Users can independently toggle each notification category and channel. 

- Transactional notifications cannot be disabled entirely. 

#### **7.18 Marketplace** 

##### **FR-035  Browse and Search Marketplace Products** 

|**Description**|The system shall provide a marketplace catalogue of pet food, toys, medicines,<br>accessories, and grooming products that users can browse, filter, and search.|
|---|---|
|**Actors**|Pet Owner|
|**Priority**|High|
|**Preconditions**|• None (browsing available to all logged-in users).|
|**Trigger**|The user opens the 'Marketplace' section.|
|**Postconditions**|• Product views are logged to support recommendation and analytics.|
|**Dependencies**|FR-030, FR-036|



**Main Flow** 

126. The system displays product categories and a search/filter interface (category, price range, brand, pet type). 

127. The user searches or filters products. 

128. The system returns matching results with price, availability, and ratings. 

129. The system surfaces relevant products based on the pet's profile (e.g., nutrition-plan-linked products, FR-030). 

###### **Alternative Flow** 

- The user views a product detail page including images, description, reviews, and related items. 

- **Exceptions** 

- Out-of-stock items are displayed but marked unavailable for purchase. 

**Acceptance Criteria** 

- Search results return within 2 seconds. 

- Out-of-stock items cannot be added to the cart. 

##### **FR-036  Shopping Cart and Checkout** 

Page 43 of 70 

_PawMatch AI — Functional Requirements Specification_ 

|**Description**|The system shall allow users to add products to a cart, apply eligible discounts,<br>and complete purchase via the integrated Payment Gateway.|
|---|---|
|**Actors**|Pet Owner|
|**Priority**|High|
|**Preconditions**|• At least one product must be added to the cart.|
|**Trigger**|The user selects 'Checkout'.|
|**Postconditions**|• An order record is created with status 'Confirmed' and routed for<br>fulfillment.|
|**Dependencies**|FR-035, FR-042, Section 10.1 (Payment Gateway)|



- **Main Flow** 

130. The system displays cart contents, applicable taxes, shipping charges, and any discount codes. 

131. The user confirms or updates the delivery address. 

132. The user selects a payment method and completes payment via the Payment Gateway interface (Section 10.1). 

133. The system creates an order record and sends an order confirmation. 

**Alternative Flow** 

- Premium subscribers may receive discounted shipping or exclusive pricing per their subscription tier. 

**Exceptions** 

- If payment fails, the cart is preserved and the user is prompted to retry or select an alternate payment method. 

**Acceptance Criteria** 

- A user can complete checkout in under 5 steps. 

- Failed payments do not result in order creation or inventory deduction. 

##### **FR-037  Order Tracking and History** 

|**Description**|The system shall allow users to view order status, tracking information, and<br>complete purchase history.|
|---|---|
|**Actors**|Pet Owner|
|**Priority**|Medium|
|**Preconditions**|• At least one order must have been placed (FR-036).|
|**Trigger**|The user opens 'My Orders'.|



Page 44 of 70 

_PawMatch AI — Functional Requirements Specification_ 

|**Postconditions**|• Return/refund requests are routed to Payment Processing (FR-039).|
|---|---|
|**Dependencies**|FR-036, FR-039|



###### **Main Flow** 

134. The system displays a list of past and current orders with status (Confirmed, Processing, Shipped, Delivered, Cancelled, Returned). 

135. The user selects an order to view item details, tracking number, and delivery estimate. 

136. The user may initiate a return/refund request within the applicable window. 

###### **Alternative Flow** 

- The user re-orders a previous purchase in a single action. 

###### **Exceptions** 

- Return requests outside the eligibility window are rejected with an explanatory message. 

###### **Acceptance Criteria** 

- Order status updates are reflected within 1 hour of a fulfillment status change. 

- Users can initiate an eligible return directly from order history. 

#### **7.19 Subscriptions** 

##### **FR-038  Subscription Plan Selection and Upgrade** 

|**Description**|The system shall allow users to view, select, and upgrade between Free,<br>Premium (₹299/month), and Family (₹499/month) subscription plans, as<br>defined in the Revenue Model.|
|---|---|
|**Actors**|Pet Owner|
|**Priority**|High|
|**Preconditions**|• The user must have a registered account.|
|**Trigger**|The user selects 'Upgrade Plan' or attempts to access a Premium-only feature.|
|**Postconditions**|• The user's subscription tier and entitlements are updated in the account<br>record.|
|**Dependencies**|FR-039, BR-022|



**Main Flow** 

137. The system displays available plans with feature comparisons (unlimited AI consultations, advanced AI matching, health records, AI training coach, priority support for Premium; multiple pets, family accounts, and shared reminders for Family). 

138. The user selects a plan and proceeds to payment (Section 7.20). 

Page 45 of 70 

_PawMatch AI — Functional Requirements Specification_ 

139. On successful payment, the system activates the selected plan and unlocks the associated features immediately. 

###### **Alternative Flow** 

- A Free-tier user attempting a Premium-only action is shown an in-context upgrade prompt. 

###### **Exceptions** 

- If payment fails, the plan remains unchanged and the user is notified of the failure reason. 

###### **Acceptance Criteria** 

- Plan changes take effect immediately upon successful payment. 

- Feature entitlements accurately reflect the active plan at all times. 

##### **FR-039  Subscription Renewal, Cancellation, and Payment Handling** 

|**Description**|The system shall process recurring subscription billing, handle renewal<br>failures, and allow users to cancel or downgrade their subscription.|
|---|---|
|**Actors**|Pet Owner, Payment Gateway|
|**Priority**|High|
|**Preconditions**|• An active paid subscription must exist.|
|**Trigger**|A subscription renewal date is reached, or the user selects 'Cancel<br>Subscription'.|
|**Postconditions**|• Billing outcomes are recorded in Subscription Logs (Section 12.4) and<br>Subscription/Revenue Reports (Section 11).|
|**Dependencies**|FR-038, FR-040, BR-022, BR-023|



###### **Main Flow** 

140. On the renewal date, the system initiates an automatic charge via the stored payment method through the Payment Gateway interface. 

141. On success, the subscription period is extended and a receipt is issued. 

142. If the user cancels, the system schedules downgrade to the Free tier at the end of the current billing period, retaining paid access until then. 

###### **Alternative Flow** 

- The user may switch between Premium and Family plans, with the change and any prorated charge applied at the next billing cycle. 

###### **Exceptions** 

- If a renewal payment fails, the system retries per BR-023 and notifies the user; after the maximum retry count, the account is downgraded to Free. 

###### **Acceptance Criteria** 

Page 46 of 70 

_PawMatch AI — Functional Requirements Specification_ 

- Renewal failures trigger the defined retry sequence before downgrade. 

- Cancellations preserve access until the end of the paid period. 

#### **7.20 Payments** 

##### **FR-040  Payment Processing** 

|**Description**|The system shall process one-time and recurring payments for subscriptions,<br>marketplace orders, service bookings, insurance purchases, and sponsorships<br>through an integrated third-party Payment Gateway.|
|---|---|
|**Actors**|Pet Owner, Shelter/NGO (as payment recipient for sponsorships), Payment<br>Gateway|
|**Priority**|High|
|**Preconditions**|• A payable transaction (order, booking, subscription, sponsorship) must<br>exist.|
|**Trigger**|The user confirms a payment action at checkout, booking confirmation, or<br>subscription selection.|
|**Postconditions**|• A payment transaction record is created and linked to the originating<br>order/booking/subscription.|
|**Dependencies**|Section 10.1 (Payment Gateway Interface), BR-024, Section 13 (Security<br>Requirements)|



###### **Main Flow** 

143. The system constructs a payment request with amount, currency, and transaction reference. 

144. The system routes the request to the Payment Gateway interface (Section 10.1) using tokenized/PCI-compliant payment handling. 

145. The Payment Gateway returns a success or failure response. 

146. On success, the system marks the related transaction as paid and triggers downstream fulfillment (order confirmation, booking confirmation, subscription activation, sponsorship credit). 

###### **Alternative Flow** 

- The user pays via UPI, credit/debit card, net banking, or digital wallet as supported by the Payment Gateway. 

###### **Exceptions** 

- On failure, the system displays the gateway-provided failure reason and allows retry without duplicate charging. 

###### **Acceptance Criteria** 

- No order/booking/subscription is confirmed without a successful payment gateway response. 

Page 47 of 70 

_PawMatch AI — Functional Requirements Specification_ 

- Duplicate charges are prevented through idempotent transaction referencing. 

##### **FR-041  Refund and Cancellation Payment Processing** 

|**Description**|The system shall process refunds for eligible cancellations, returns, and<br>disputed transactions back to the original payment method.|
|---|---|
|**Actors**|Pet Owner, Platform Administrator, Payment Gateway|
|**Priority**|Medium|
|**Preconditions**|• An eligible refund request must exist (e.g., approved return, cancelled<br>booking within policy).|
|**Trigger**|A refund is approved by the Administrator or automatically qualifies per policy<br>(e.g., cancellation within the allowed window).|
|**Postconditions**|• Refund outcome is recorded in Revenue Reports and Audit Logs.|
|**Dependencies**|FR-040, FR-037, FR-018, BR-021, BR-024|



###### **Main Flow** 

147. The system validates refund eligibility against the relevant policy (BR-021, BR-024). 

148. The system submits a refund request to the Payment Gateway for the original transaction. 

149. The Payment Gateway processes the refund and returns confirmation. 

150. The system updates the transaction and order/booking status and notifies the user. 

###### **Alternative Flow** 

- Partial refunds are supported for partially fulfilled orders. 

###### **Exceptions** 

- If the Payment Gateway rejects the refund, the system flags the transaction for manual Administrator review. 

###### **Acceptance Criteria** 

- Eligible refunds are initiated within 24 hours of approval. 

- Refund status is visible to the user in Order/Booking history. 

#### **7.21 Community** 

##### **FR-042  Create Community Post** 

|**Description**|
|---|



The system shall allow users to publish posts to the Community Feed, including pet stories, adoption success stories, rescue updates, photos, and videos. 

Page 48 of 70 

_PawMatch AI — Functional Requirements Specification_ 

|**Actors**|Pet Owner, Shelter Administrator, NGO Administrator|
|---|---|
|**Priority**|Medium|
|**Preconditions**|• The user must be logged in.|
|**Trigger**|The user selects 'Create Post' from the Community Feed.|
|**Postconditions**|• The post is stored and becomes visible in relevant users' feeds.|
|**Dependencies**|FR-043, FR-047, BR-026|



###### **Main Flow** 

151. The user composes text and optionally attaches photos or a video. 

152. The user selects a post category (Story, Success Story, Rescue Update, General). 

153. The system runs automated content-moderation checks before publishing. 

154. The system publishes the post to the Community Feed. 

###### **Alternative Flow** 

- The user tags a specific pet or organization profile in the post. 

###### **Exceptions** 

- Posts flagged by automated moderation are held for Administrator review before publishing (Section 7.24). 

###### **Acceptance Criteria** 

- 

- Flagged content is not publicly visible until reviewed. 

##### **FR-043  Comment, Like, and Share on Community Content** 

|**Description**|The system shall allow users to like, comment on, and share Community Feed<br>posts and events.|
|---|---|
|**Actors**|Pet Owner, Shelter Administrator, NGO Administrator|
|**Priority**|Low|
|**Preconditions**|• A community post must exist (FR-042).|
|**Trigger**|The user interacts with a post's like, comment, or share control.|
|**Postconditions**|• Engagement data is available for Community analytics.|
|**Dependencies**|FR-042, FR-047, BR-026|



**Main Flow** 

155. The user selects 'Like', enters a comment, or selects 'Share'. 

Page 49 of 70 

_PawMatch AI — Functional Requirements Specification_ 

156. The system records the interaction and updates the post's engagement counters in real time. 

157. For comments, the system runs automated content moderation prior to public display. 

###### **Alternative Flow** 

- The user reports an inappropriate comment or post, routing it to the moderation queue (Section 7.24). 

###### **Exceptions** 

- Users may retract a like or delete their own comment at any time. 

###### **Acceptance Criteria** 

- Engagement counters update within 2 seconds of interaction. 

- Reported content is routed to moderation within 1 minute. 

#### **7.22 Events** 

##### **FR-044  Create and Publish Pet Event** 

|**Description**|The system shall allow Shelters, NGOs, and Rescue Organizations to create and<br>publish events such as adoption drives, vaccination camps, dog shows, and<br>meetups.|
|---|---|
|**Actors**|Shelter Administrator, NGO Administrator, Rescue Organization|
|**Priority**|Medium|
|**Preconditions**|• The organizing account must be verified.|
|**Trigger**|The organizer selects 'Create Event'.|
|**Postconditions**|• The event record is created and open for registration (FR-045).|
|**Dependencies**|FR-045, Section 10.7 (Maps Interface)|



###### **Main Flow** 

158. The organizer enters event details: title, category, description, date/time, location, and capacity (if limited). 

159. The organizer publishes the event to the Events module and Community Feed. 

160. The system makes the event discoverable via location-based search. 

###### **Alternative Flow** 

- The organizer marks an event as recurring (e.g., monthly vaccination camp). 

###### **Exceptions** 

- Events with a past date cannot be published. 

###### **Acceptance Criteria** 

- Published events are searchable by location and date within 1 minute. 

Page 50 of 70 

_PawMatch AI — Functional Requirements Specification_ 

- Past-dated events are rejected at creation. 

##### **FR-045  Event Registration and Attendance Tracking** 

|**Description**|The system shall allow users to register for events with limited capacity and<br>shall allow organizers to track attendance.|
|---|---|
|**Actors**|Pet Owner, Shelter Administrator|
|**Priority**|Low|
|**Preconditions**|• A published event must exist (FR-044).|
|**Trigger**|The user selects 'Register' on an event listing.|
|**Postconditions**|• Registration and attendance data are available in Event Reports (Section<br>11).|
|**Dependencies**|FR-044, FR-032|



###### **Main Flow** 

161. The system checks remaining capacity. 

162. The system registers the user and sends a confirmation with a reminder scheduled via the Reminder System (FR-032). 

163. On the event date, the organizer may check in attendees via the dashboard. 

###### **Alternative Flow** 

- If the event reaches capacity, the user is offered a waitlist position. 

###### **Exceptions** 

- Duplicate registration by the same user for the same event is prevented. 

###### **Acceptance Criteria** 

- Capacity limits are enforced without overbooking. 

- Waitlisted users are automatically promoted when a spot opens. 

#### **7.23 Reports** 

##### **FR-046  Generate Custom Report** 

|**Description**|The system shall allow authorized roles to generate custom reports across<br>adoption, subscription, revenue, and shelter-performance data, filtered by<br>date range and organization, as detailed in Section 11.|
|---|---|
|**Actors**|Platform Administrator, Shelter Administrator, NGO Administrator|



Page 51 of 70 

_PawMatch AI — Functional Requirements Specification_ 

|**Priority**|Medium|
|---|---|
|**Preconditions**|• The requesting user must hold report-access permissions for the<br>requested data scope.|
|**Trigger**|The user selects 'Generate Report' and defines report parameters.|
|**Postconditions**|• Generated reports are retained in report history for 12 months.|
|**Dependencies**|Section 11 (Reporting Requirements), Section 13 (Security Requirements)|



- **Main Flow** 

164. The user selects a report type (Adoption, Subscription, Revenue, Shelter Performance) and applies filters (date range, organization, region). 

165. The system aggregates the requested data. 

166. The system renders the report on-screen and offers export as PDF or CSV. 

**Alternative Flow** 

- The user schedules a recurring report to be generated and emailed automatically (e.g., monthly). 

- **Exceptions** 

- Users without sufficient permission for a requested data scope are denied and the attempt is logged. 

**Acceptance Criteria** 

- Reports generate within 10 seconds for standard date ranges. 

- Access to cross-organization data is restricted to Platform Administrators. 

#### **7.24 Administration** 

##### **FR-047  User and Content Moderation** 

|**Description**|The system shall provide Platform Administrators tools to review flagged<br>content, verify institutional accounts, and suspend or ban users/organizations<br>that violate platform policy.|
|---|---|
|**Actors**|Platform Administrator|
|**Priority**|High|
|**Preconditions**|• Flagged content or a verification request must exist in the moderation<br>queue.|
|**Trigger**|Content is flagged automatically or reported by a user, or a new institutional<br>account submits verification documents.|
|**Postconditions**|• All moderation and administrative actions are recorded in Admin Logs<br>(Section 12.5).|



Page 52 of 70 

_PawMatch AI — Functional Requirements Specification_ 

**Dependencies** FR-012, FR-015, FR-017, Section 12.5 (Admin Logs) 

###### **Main Flow** 

167. The Administrator reviews the moderation/verification queue. 

168. For content moderation, the Administrator approves, removes, or edits the flagged item. 

169. For account verification, the Administrator reviews submitted documents and approves, rejects, or requests further information. 

170. For policy violations, the Administrator may issue a warning, temporarily suspend, or permanently ban the account. 

###### **Alternative Flow** 

- The Administrator delegates moderation to a Moderator role with restricted permissions (Section 6). 

###### **Exceptions** 

- Suspended/banned accounts retain read-only access to their historical health records for continuity of pet care. 

###### **Acceptance Criteria** 

- Every moderation action is logged with the acting administrator's identity and timestamp. 

- Suspended accounts immediately lose write access to publishing features. 

##### **FR-048  Platform Configuration Management** 

|**Description**|The system shall allow Platform Administrators to configure global platform<br>parameters, including subscription pricing, notification templates, moderation<br>thresholds, and feature toggles.|
|---|---|
|**Actors**|Platform Administrator|
|**Priority**|Medium|
|**Preconditions**|• The Administrator must hold Super Admin permissions (Section 6.1).|
|**Trigger**|The Administrator opens 'Platform Settings'.|
|**Postconditions**|• Configuration change history is retained for audit purposes.|
|**Dependencies**|Section 12.5 (Admin Logs), Section 13 (Security Requirements)|



###### **Main Flow** 

171. The Administrator selects a configuration category (pricing, notifications, moderation thresholds, feature toggles). 

172. The Administrator updates the relevant parameter. 

173. The system validates and applies the change, versioning the prior configuration. 

Page 53 of 70 

_PawMatch AI — Functional Requirements Specification_ 

###### **Alternative Flow** 

- Configuration changes may be scheduled to take effect at a future date (e.g., a pricing change effective next billing cycle). 

###### **Exceptions** 

- Configuration changes affecting active financial transactions require secondary confirmation. 

###### **Acceptance Criteria** 

- Configuration changes take effect without requiring a system restart. 

- All changes are attributable to the administering user. 

#### **7.25 Analytics** 

##### **FR-049  AI Analytics Dashboard for Shelters and Administrators** 

|**Description**|The system shall provide AI-driven analytics — including predicted time-to-<br>adoption, listing performance trends, and adopter-demand patterns — to<br>Premium Shelter Dashboard subscribers and Platform Administrators.|
|---|---|
|**Actors**|Shelter<br>Administrator<br>(Premium),<br>Platform<br>Administrator,<br>AI<br>Recommendation Engine|
|**Priority**|Low|
|**Preconditions**|• The requesting shelter must be subscribed to the Premium Shelter<br>Dashboard tier, or the requester must be a Platform Administrator.|
|**Trigger**|The user opens the 'AI Analytics' tab.|
|**Postconditions**|• Analytics queries are logged in AI Usage Logs (Section 12.3).|
|**Dependencies**|FR-014, FR-038, Section 10.6 (AI Services Interface)|



###### **Main Flow** 

174. The system aggregates historical listing, application, and adoption data for the organization (or platform-wide for Administrators). 

175. The system requests predictive insights from the AI Recommendation Engine (e.g., predicted days-to-adoption per listing, demand trends by breed/region). 

176. The system displays the insights as visual charts with supporting narrative summaries. 

###### **Alternative Flow** 

- The Administrator views platform-wide AI analytics across all organizations for strategic reporting. 

###### **Exceptions** 

- Non-Premium shelters viewing the tab are shown an upgrade prompt in place of AI-driven insights. 

###### **Acceptance Criteria** 

- AI analytics refresh at least daily. 

Page 54 of 70 

_PawMatch AI — Functional Requirements Specification_ 

- Access is correctly restricted to Premium subscribers and Administrators. 

#### **7.26 Settings** 

##### **FR-050  Account, Privacy, and Notification Settings** 

|**Description**|The system shall provide a centralized Settings area where users can manage<br>account details, privacy preferences, notification channel preferences, linked<br>payment methods, and account deletion requests.|
|---|---|
|**Actors**|All registered users|
|**Priority**|Medium|
|**Preconditions**|• The user must be logged in.|
|**Trigger**|The user navigates to 'Settings'.|
|**Postconditions**|• Settings changes are applied immediately and logged where security-<br>relevant (e.g., payment method changes).|
|**Dependencies**|FR-004, FR-034, BR-027, Section 13 (Security Requirements)|



###### **Main Flow** 

177. The system displays configurable sections: Account Details, Privacy, Notifications, Payment Methods, and Data & Account Deletion. 

178. The user updates a setting. 

179. The system validates and saves the change immediately. 

###### **Alternative Flow** 

- The user submits an account-deletion request, which is processed per BR-027 and applicable dataretention requirements. 

###### **Exceptions** 

- Account deletion is blocked while a financial dispute, active subscription commitment, or open adoption process exists, and the user is informed of the blocking condition. 

###### **Acceptance Criteria** 

- All settings changes are saved without requiring re-login. 

- Account deletion requests are acknowledged within 24 hours and completed per the defined retention policy. 

Page 55 of 70 

_PawMatch AI — Functional Requirements Specification_ 

### **8. Business Rules** 

Business Rules define platform-wide policy constraints that apply across multiple functional requirements. They are referenced from Section 7 by ID. 

|**ID**|**Business Rule**|
|---|---|
|BR-001|A single email address or mobile number may be associated with only one active user<br>account.|
|BR-002|Institutional accounts (Shelter, NGO, Veterinarian, Rescue Organization) shall not gain<br>publishing or booking privileges until verification (FR-012/FR-015/FR-017) is approved<br>by a Platform Administrator.|
|BR-003|Passwords must comply with the Password Policy defined in Section 9.2; password<br>changes invalidate all existing sessions.|
|BR-010|Profile fields marked 'private' by a user shall not be visible to other users except<br>Platform Administrators and, where functionally required (e.g., adoption review), the<br>reviewing organization.|
|BR-011|A pet listing may not be deleted while an approved adoption is in progress; it may only<br>be marked 'On Hold' or 'Adopted'.|
|BR-012|A Pet Owner may not hold more than 3 concurrent 'Submitted' or 'Under Review'<br>adoption applications at any time.|
|BR-013|An organization must act on a submitted adoption application within a configurable SLA<br>(default 7 days) before an escalation reminder is triggered.|
|BR-014|Verification approval or rejection of an institutional account must be recorded with the<br>reviewing Administrator's identity and a timestamp.|
|BR-015|Health Record entries are immutable once saved; corrections must be recorded as a<br>new amendment entry referencing the original.|
|BR-016|Free-tier Pet Owners are limited to a configurable maximum number of AI Health<br>Assistant and AI Training Coach consultations per calendar month (default: 5<br>consultations).|
|BR-020|Recurring sponsorship or subscription payments that fail shall be retried according to<br>the retry schedule defined in Section 9.6 before the associated benefit is suspended.|
|BR-021|Veterinary appointment cancellations made within the clinic's configured cancellation<br>window (default 2 hours before the appointment) may incur a cancellation fee, at the<br>clinic's discretion.|
|BR-022|Subscription tier changes (upgrade/downgrade) take effect according to the billing<br>rules defined in FR-039; downgrades take effect at the end of the current paid period.|
|BR-023|A failed subscription renewal payment shall be retried a maximum of 3 times over 7<br>days before the account is automatically downgraded to the Free tier.|



Page 56 of 70 

_PawMatch AI — Functional Requirements Specification_ 

|**ID**|**Business Rule**|
|---|---|
|BR-024|All monetary transactions (orders, bookings, subscriptions, sponsorships) must be<br>processed through the certified Payment Gateway integration; the platform shall not<br>store raw card data.|
|BR-025|Transactional notifications relating to payments, safety, or account security cannot be<br>disabled by the user.|
|BR-026|User-generated content (posts, comments, images) is subject to automated content-<br>moderation screening prior to public visibility; content flagged above the configured<br>risk threshold is held for manual review.|
|BR-027|Account deletion requests are subject to a data-retention period as required by<br>applicable data-protection regulation before permanent erasure; financial and health<br>records may be retained longer where legally required.|
|BR-030|All AI-generated health, behavior, nutrition, and diagnostic outputs must be presented<br>with a disclaimer indicating they are advisory in nature and do not constitute a<br>professional veterinary diagnosis.|



Page 57 of 70 

_PawMatch AI — Functional Requirements Specification_ 

### **9. Validation Rules** 

#### **9.1 General Input Validation** 

- All text input fields shall be validated for maximum length, disallowed characters, and script-injection patterns prior to persistence. 

- Email fields shall conform to standard email address format (RFC 5322) and be verified via OTP/link prior to account activation. 

- Mobile number fields shall be validated for correct country-code and digit-length format, and verified via OTP prior to account activation. 

- Date fields (e.g., appointment date, event date, reminder date) shall not accept past dates where the business context requires a future date (e.g., new appointment bookings, event creation). 

#### **9.2 Password Policy** 

- Minimum length: 8 characters. 

- Must contain at least one uppercase letter, one lowercase letter, one numeral, and one special character. 

- Passwords shall be stored using a salted, industry-standard one-way hashing algorithm (e.g., bcrypt or Argon2); plaintext passwords shall never be stored or logged. 

- The system shall reject the user's 5 most recently used passwords upon password change. 

#### **9.3 Subscription and Payment Validation** 

- A subscription upgrade shall not be marked active until a successful payment confirmation is received from the Payment Gateway. 

- Payment amounts shall be validated server-side against the authoritative price list; client-submitted price values shall not be trusted. 

- Refund amounts shall not exceed the original transaction amount. 

#### **9.4 File and Image Upload Constraints** 

|**Parameter**|**Constraint**|
|---|---|
|Accepted image formats|JPEG, PNG, WEBP|
|Maximum image file size|10 MB per image|
|Maximum images per pet listing|10 images|
|Accepted video formats|MP4, MOV|
|Maximum video file size|100 MB|
|Maximum video length|60 seconds|



Page 58 of 70 

_PawMatch AI — Functional Requirements Specification_ 

|**Parameter**|**Constraint**|
|---|---|
|Accepted document formats (verification,<br>lab reports)|PDF, JPEG, PNG|
|Maximum document file size|15 MB|



#### **9.5 Subscription Plan Validation** 

A user account may hold only one active subscription plan at a time (Free, Premium, or Family). Planentitlement checks shall be evaluated server-side on every access to a Premium-gated feature, not solely at login. 

#### **9.6 Payment Retry Schedule** 

|**Attempt**|**Timing**|**Action on Final Failure**|
|---|---|---|
|1st retry|24 hours after initial failure|Notify user of failed payment|
|2nd retry|72 hours after initial failure|Notify user with urgent reminder|
|3rd retry|7 days after initial failure|Downgrade to Free tier / suspend<br>recurring benefit (per BR-020, BR-<br>023)|



Page 59 of 70 

_PawMatch AI — Functional Requirements Specification_ 

### **10. External Interfaces** 

This section defines the external systems and services with which PawMatch AI integrates. 

|**ID**|**Interface**|**Description**|
|---|---|---|
|10.1|Payment Gateway|Processes one-time and recurring payments for subscriptions,<br>marketplace orders, service bookings, insurance purchases, and<br>sponsorships. Supports UPI, credit/debit card, net banking, and<br>digital wallets. Must be PCI-DSS compliant; the platform shall not<br>store raw payment card data.|
|10.2|Email Service|Delivers account verification, password reset, transactional<br>receipts, and configurable notification-category emails.|
|10.3|SMS<br>/<br>WhatsApp<br>Messaging Service|Delivers OTP verification codes and reminder/notification messages<br>via SMS and WhatsApp Business API, per user channel preference.|
|10.4|Push<br>Notification<br>Service|Delivers real-time mobile push notifications for application status,<br>messages, and reminders via platform-native push services<br>(FCM/APNs).|
|10.5|Cloud Storage Service|Stores and serves pet photographs, videos, verification documents,<br>and health-record attachments (Microsoft Azure Blob Storage or<br>AWS S3, per the defined technology stack).|
|10.6|AI Services Platform|Hosts and serves the Computer Vision, Recommendation Engine,<br>NLP Chatbot, Image Classification, OCR, Voice Recognition, and<br>Predictive Analytics models underlying the AI Features described in<br>Sections 7.9–7.15 and 7.25.|
|10.7|Maps<br>and<br>Geolocation Service|Provides location search, distance-based filtering, and directions for<br>pet listings, veterinary clinics, emergency clinics, and events.|



Page 60 of 70 

_PawMatch AI — Functional Requirements Specification_ 

### **11. Reporting Requirements** 

#### **11.1 Admin Reports** 

- Platform-wide user growth and active-user trends. 

- Platform-wide adoption conversion rate. 

- Moderation and verification queue throughput. 

- Platform revenue by source category. 

#### **11.2 Shelter Reports** 

- Listing performance (views, applications received, time-to-adoption). 

- Application funnel (submitted, approved, rejected, waitlisted). 

- AI-predicted time-to-adoption for active listings (Premium Dashboard, FR-049). 

#### **11.3 Adoption Reports** 

- Adoptions completed by period, region, species, and organization. 

- Average Adoption Readiness Score of approved applicants. 

- Post-adoption return rate (pets re-listed within 90 days of adoption). 

#### **11.4 Subscription Reports** 

- Active subscribers by plan tier. 

- New subscriptions, upgrades, downgrades, and cancellations by period. 

- Subscription renewal success/failure rate. 

#### **11.5 Revenue Reports** 

- Revenue by source: subscriptions, marketplace commissions, veterinary booking commissions, grooming/boarding commissions, insurance commissions, sponsored listings, advertisements, NGO/CSR partnerships, premium shelter dashboards, AI analytics subscriptions. 

- Refund and chargeback summary. 

Page 61 of 70 

_PawMatch AI — Functional Requirements Specification_ 

### **12. Audit Requirements** 

The system shall maintain immutable audit logs for the categories below. Logs shall be retained for a minimum of 12 months (or longer where required by Section 9's data-retention rules) and shall be accessible to Platform Administrators for compliance and investigative purposes. 

#### **12.1 User Activity Logs** 

- Profile updates, adoption application submissions, listing creation/edit/removal, marketplace orders. 

#### **12.2 Login Logs** 

- Successful and failed login attempts, account lockouts, password changes, session terminations. 

#### **12.3 AI Usage Logs** 

- AI Pet Match queries, AI Health Assistant conversations, AI Image Recognition submissions, Lost Pet Finder match searches, and their outcomes, retained for model-quality review and dispute resolution. 

#### **12.4 Subscription Logs** 

- Plan changes, billing attempts, renewal outcomes, cancellations, and refunds. 

#### **12.5 Admin Logs** 

- Verification decisions, moderation actions, account suspensions/bans, and platform configuration changes, each attributed to the acting Administrator. 

Page 62 of 70 

_PawMatch AI — Functional Requirements Specification_ 

### **13. Security Requirements** 

#### **13.1 Authentication** 

- All authentication shall occur over encrypted (TLS 1.2 or higher) connections. 

- Multi-factor verification (OTP) is mandatory for institutional account registration and for password reset. 

#### **13.2 Authorization and Role-Based Access Control** 

- All API endpoints shall enforce server-side authorization checks consistent with the role permissions defined in Section 6. 

- Cross-organization data access (e.g., one Shelter viewing another Shelter's applications) shall be denied by default. 

#### **13.3 Encryption** 

- Data in transit shall be encrypted using TLS 1.2 or higher. 

- Sensitive data at rest (passwords, payment tokens, verification documents, health records) shall be encrypted using industry-standard encryption algorithms. 

#### **13.4 Secure API Access** 

- All API access shall require a valid authentication token. 

- Rate limiting shall be applied to authentication and AI-service endpoints to mitigate abuse and denial-of-service risk. 

#### **13.5 Session Management** 

- Session tokens shall expire after a configurable inactivity period (default 30 minutes for web dashboard sessions; extended duration permitted for mobile app sessions with biometric reauthentication). 

- All active sessions shall be invalidated upon password change or account suspension. 

#### **13.6 Password Policy** 

Refer to Section 9.2 for the complete password policy specification. 

Page 63 of 70 

_PawMatch AI — Functional Requirements Specification_ 

### **14. Non-Functional Requirements** 

|**Category**|**Requirement**|
|---|---|
|Performance|95% of standard API requests shall complete within 2 seconds under expected<br>load; AI-service responses (matching, image recognition) shall complete<br>within 5 seconds.|
|Availability|The production platform shall maintain a minimum of 99.5% uptime, excluding<br>scheduled maintenance windows communicated at least 48 hours in advance.|
|Reliability|The system shall gracefully degrade AI-dependent features (displaying a<br>fallback message) if the AI Services Platform is temporarily unavailable,<br>without impacting core adoption and marketplace transactions.|
|Scalability|The system architecture shall support horizontal scaling to accommodate<br>growth from an initial 50,000 registered users (Year 1) to 20 lakh+ users (Year<br>3) as projected in the Business Plan roadmap.|
|Maintainability|Backend services shall be modular (microservice or well-bounded service-<br>oriented architecture) to allow independent deployment of AI services, core<br>platform services, and the marketplace/payments subsystem.|
|Portability|The mobile application shall run on Android 9+ and iOS 14+; the web<br>dashboard shall support the latest two major versions of Chrome, Safari, Edge,<br>and Firefox.|
|Usability|First-time users shall be able to complete registration and submit an adoption<br>application without external assistance, validated through usability testing<br>prior to launch.|
|Accessibility|The web dashboard and mobile application shall target conformance with<br>WCAG 2.1 Level AA for core adoption and account-management flows.|
|Security|Refer to Section 13 for complete security requirements.|
|Compliance|The platform shall comply with applicable Indian data-protection regulations<br>for the handling of personal data, and with PCI-DSS requirements for payment<br>processing.|



Page 64 of 70 

_PawMatch AI — Functional Requirements Specification_ 

### **15. Error Handling Requirements** 

- All user-facing error messages shall be clear, non-technical, and actionable, avoiding exposure of internal system details (stack traces, database errors, or raw API error codes). 

- Form validation errors shall be displayed inline, adjacent to the relevant field, at the time of submission. 

- Network or service-unavailability errors shall present a retry option where the underlying action is safe to retry. 

- Payment failures shall clearly state the reason category (declined, insufficient funds, gateway timeout) where provided by the Payment Gateway, and shall never result in a partially completed order or duplicate charge. 

- AI-service failures or timeouts shall present a fallback message directing the user to retry later or, for health-related queries, to contact a veterinarian directly, consistent with BR-030. 

- All unhandled system errors shall be logged server-side with a correlation ID that can be referenced in user-facing support communication without exposing sensitive internal detail. 

Page 65 of 70 

_PawMatch AI — Functional Requirements Specification_ 

### **16. Notifications** 

This section consolidates notification categories referenced throughout Section 7. Delivery mechanics are specified in FR-033 and FR-034; external channel integration is specified in Section 10. 

|**Category**|**Example Trigger**|**Default Channels**|**Can Be Muted by**<br>**User**|
|---|---|---|---|
|Account<br>&<br>Security|Password reset, new device<br>login|Email, Push|No|
|Adoption|Application status change, new<br>message from organization|Push, Email|No|
|Reminders|Vaccination, medication, vet<br>visit, deworming, grooming,<br>birthday|Push, WhatsApp, Voice<br>Assistant|Yes (per category)|
|Payments<br>&<br>Subscriptions|Payment<br>success/failure,<br>renewal, refund|Email, Push|No|
|Marketplace|Order confirmation, shipping<br>update, delivery|Push, Email|Yes (marketing only)|
|Community|New comment, like, mention|Push|Yes|
|Events|Registration<br>confirmation,<br>event reminder|Push, Email|Yes|
|Promotional|New<br>feature,<br>offers,<br>campaigns|Push, Email|Yes|



Page 66 of 70 

_PawMatch AI — Functional Requirements Specification_ 

### **17. Acceptance Criteria** 

In addition to the requirement-level acceptance criteria specified within each functional requirement in Section 7, the following overall acceptance criteria shall apply for User Acceptance Testing (UAT) sign-off of the Version 1.0 release: 

- All High-priority functional requirements (Section 7) are implemented and pass their individual acceptance criteria. 

- All Business Rules (Section 8) are enforced and verified through targeted test cases. 

- All Validation Rules (Section 9) are enforced at both client and server layers. 

- Security Requirements (Section 13) are verified through a penetration test or security review prior to production launch. 

- Non-Functional Requirements (Section 14) performance and availability targets are demonstrated under representative load testing. 

- No critical or high-severity defects remain open at the time of UAT sign-off. 

- The Requirement Traceability Matrix (Section 18) shows 100% coverage of Business Plan features to functional requirements and to at least one corresponding test case. 

Page 67 of 70 

_PawMatch AI — Functional Requirements Specification_ 

### **18. Requirement Traceability Matrix** 

The matrix below traces each Business Plan feature area to its corresponding functional requirement(s) in this document, establishing end-to-end traceability from business intent to functional specification. 

|**Business Plan Feature**|**Traced Functional Requirement(s)**|**FRS Section**|
|---|---|---|
|AI Pet Match|FR-021, FR-022|Section 7.9|
|AI Face Recognition|FR-025, FR-026|Section 7.11|
|AI Adoption Score|FR-011|Section 7.4|
|AI Pet Health Assistant|FR-023|Section 7.10|
|AI Behaviour Prediction|FR-027|Section 7.12|
|AI Lost Pet Finder|FR-028, FR-029|Section 7.13|
|AI Nutrition Planner|FR-030|Section 7.14|
|AI Training Coach|FR-031|Section 7.15|
|AI Emergency Assistant|FR-024|Section 7.10|
|AI Pet Translator (Experimental)|Deferred – see Section 19.3|Section 4.6 (Assumptions)|
|Pet Adoption (Dogs, Cats, Birds,<br>Rabbits, Exotic)|FR-006 – FR-011|Section 7.3, 7.4|
|Foster Care|FR-006, FR-010|Section 7.3, 7.4|
|Pet Sponsorship|FR-016|Section 7.6|
|Shelter Management Dashboard|FR-012 – FR-014|Section 7.5|
|Vet Booking|FR-017, FR-018|Section 7.7|
|Grooming Services / Pet Boarding|FR-035, FR-036 (Marketplace service<br>category)|Section 7.18|
|Pet Marketplace|FR-035 – FR-037|Section 7.18|
|Pet Insurance|FR-035,<br>FR-036<br>(Marketplace<br>product category), FR-040|Section 7.18, 7.20|
|Community Feed|FR-042, FR-043|Section 7.21|
|Pet Events|FR-044, FR-045|Section 7.22|
|Pet Health Records|FR-019, FR-020|Section 7.8|
|Reminder System|FR-032, FR-033|Section 7.16|
|Premium AI Assistant|FR-023, FR-038|Section 7.10, 7.19|



Page 68 of 70 

_PawMatch AI — Functional Requirements Specification_ 

|**Business Plan Feature**|**Traced Functional Requirement(s)**|**FRS Section**|
|---|---|---|
|Subscription<br>Plans<br>(Free/Premium/Family)|FR-038, FR-039|Section 7.19|
|Adoption<br>Success<br>Fees<br>/|||
|Commissions<br>/<br>Sponsored<br>Listings / Advertisements|FR-040, FR-041|Section 7.20|
|Premium Shelter Dashboards / AI<br>Analytics for Shelters|FR-014, FR-049|Section 7.5, 7.25|



Page 69 of 70 

_PawMatch AI — Functional Requirements Specification_ 

### **19. Appendix** 

#### **19.1 Glossary** 

Refer to Section 3.5 (Definitions) and Section 3.6 (Acronyms) for the complete glossary of terms used in this document. 

#### **19.2 References** 

Refer to Section 3.7 for the complete list of reference documents and standards. 

#### **19.3 Future Enhancements** 

The following items are identified in the Business Plan as future-facing capabilities and are documented here for continuity, but are outside the Version 1.0 functional requirements baseline defined in Section 7: 

- AI Pet Translator — experimental analysis of barking, meowing, facial expressions, and tail movement to infer emotional state, targeted for post-Version 1.0 research and development. 

- AI-powered tele-veterinary consultations — Year 2 roadmap item; will extend FR-018 (Veterinary Appointment Management) to include in-app video consultation. 

- Expanded marketplace and pet insurance integration — Year 2 roadmap item; will extend Section 7.18 (Marketplace) and the insurance commission revenue stream. 

- Multi-language AI assistant — Year 3 roadmap item; will extend FR-023/FR-024 (AI Health Assistant) with additional language models. 

- Smart wearable integration for pets — Year 3 roadmap item; would introduce a new deviceintegration module for real-time activity and vitals data feeding into Health Records (FR-019) and Behavior Prediction (FR-027). 

- International expansion — Year 3 roadmap item; will require revisiting currency, regulatory/compliance, and localization assumptions stated in Section 4.6 and 4.7. 

Page 70 of 70 

