"""
Domain-specific exceptions for PawMatch Accounts & Authentication module.
"""

from rest_framework.exceptions import APIException


class AccountsException(APIException):
    """Base domain exception for Accounts module."""

    status_code = 400
    default_detail = "An accounts domain error occurred."
    default_code = "accounts_error"


class AuthenticationException(AccountsException):
    status_code = 401
    default_detail = "Invalid email or password."
    default_code = "invalid_credentials"


class AccountDisabledException(AccountsException):
    status_code = 401
    default_detail = "Your account has been disabled."
    default_code = "account_disabled"


class RegistrationException(AccountsException):
    status_code = 400
    default_detail = "Registration failed."
    default_code = "registration_failed"


class InvalidTokenException(AccountsException):
    status_code = 400
    default_detail = "Verification token is invalid, expired, or already used."
    default_code = "invalid_token"


class ExpiredTokenException(InvalidTokenException):
    default_detail = "Verification token has expired."
    default_code = "token_expired"


class TokenAlreadyUsedException(InvalidTokenException):
    default_detail = "Verification token has already been consumed."
    default_code = "token_already_used"


class EmailAlreadyVerifiedException(AccountsException):
    status_code = 400
    default_detail = "Email address is already verified."
    default_code = "email_already_verified"
