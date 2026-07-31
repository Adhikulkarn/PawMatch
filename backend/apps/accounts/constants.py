"""
Centralized constants for the PawMatch Accounts & Authentication module.
Consolidates audit action names, throttle scopes, template paths, and standard messages.
"""


class AuditAction:
    """Security audit log action names."""

    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    LOGIN_FAILED_CREDENTIALS = "LOGIN_FAILED_CREDENTIALS"
    LOGIN_FAILED_DISABLED = "LOGIN_FAILED_DISABLED"
    LOGOUT_SUCCESS = "LOGOUT_SUCCESS"
    LOGOUT_FAILED = "LOGOUT_FAILED"
    TOKEN_REFRESH_SUCCESS = "TOKEN_REFRESH_SUCCESS"
    TOKEN_REFRESH_FAILED = "TOKEN_REFRESH_FAILED"
    REGISTRATION_SUCCESS = "REGISTRATION_SUCCESS"
    REGISTRATION_FAILED_DUPLICATE = "REGISTRATION_FAILED_DUPLICATE"
    EMAIL_VERIFICATION_SUCCESS = "EMAIL_VERIFICATION_SUCCESS"
    EMAIL_VERIFICATION_FAILED = "EMAIL_VERIFICATION_FAILED"
    VERIFICATION_EMAIL_RESENT = "VERIFICATION_EMAIL_RESENT"
    RESEND_VERIFICATION_FAILED = "RESEND_VERIFICATION_FAILED"


class ThrottleScope:
    """DRF Rate limiting throttle scopes."""

    LOGIN_ANON = "login_anon"
    LOGIN_USER = "login_user"
    REGISTER_ANON = "register_anon"
    RESEND_VERIFICATION = "resend_verification"


class EmailTemplate:
    """Transactional email template paths."""

    VERIFICATION_EMAIL = "emails/verification_email.html"
    WELCOME_EMAIL = "emails/welcome_email.html"


class AuthMessage:
    """User-facing API response message text."""

    LOGIN_SUCCESS = "Login successful."
    LOGOUT_SUCCESS = "Successfully logged out."
    TOKEN_REFRESH_SUCCESS = "Token refreshed successfully."
    CURRENT_USER_RETRIEVED = "Current user profile retrieved successfully."
    REGISTRATION_SUCCESS = (
        "Registration successful. Please check your email to verify your account."
    )
    EMAIL_VERIFIED_SUCCESS = "Email verified successfully. Your account is now active."
    VERIFICATION_RESENT_SUCCESS = "Verification email sent. Please check your inbox."

    INVALID_CREDENTIALS = "Invalid email or password."
    ACCOUNT_DISABLED = "Your account has been disabled."
    TOKEN_INVALID_OR_EXPIRED = "Token is invalid, expired, or already used."
    REFRESH_TOKEN_REQUIRED = "Refresh token is required."
    EMAIL_ALREADY_EXISTS = "A user with that email already exists."
    EMAIL_ALREADY_VERIFIED = "Email address is already verified."
    USER_NOT_FOUND = "User with this email address does not exist."
    PASSWORD_MISMATCH = "Passwords do not match."
