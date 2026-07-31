"""
REST API views for PawMatch Authentication, User Registration & Email Verification.
"""

from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.api.serializers import (
    CurrentUserSerializer,
    LoginSerializer,
    LogoutSerializer,
    RegisterSerializer,
    ResendVerificationSerializer,
    VerifyEmailSerializer,
)
from apps.accounts.constants import AuditAction, AuthMessage
from apps.accounts.services.authentication_service import AuthenticationService
from apps.accounts.services.registration_service import RegistrationService
from apps.accounts.throttles import (
    LoginAnonRateThrottle,
    LoginUserRateThrottle,
    RegisterRateThrottle,
    ResendVerificationRateThrottle,
)
from apps.audit_logs.services.audit_service import AuditService
from apps.core.responses import api_response


class RegisterAPIView(GenericAPIView):
    """
    POST /api/v1/accounts/register/
    Registers a new inactive user, generates an email verification token,
    and dispatches a verification email.
    """

    permission_classes = (AllowAny,)
    throttle_classes = (RegisterRateThrottle,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, _, _ = RegistrationService.register_user(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
            first_name=serializer.validated_data["first_name"],
            last_name=serializer.validated_data["last_name"],
            request=request,
        )

        user_data = CurrentUserSerializer(user, context={"request": request}).data

        return api_response(
            success=True,
            message=AuthMessage.REGISTRATION_SUCCESS,
            data={"user": user_data},
            status_code=status.HTTP_201_CREATED,
        )


class VerifyEmailAPIView(GenericAPIView):
    """
    GET /api/v1/accounts/verify-email/?token=<token>
    POST /api/v1/accounts/verify-email/
    Verifies the email token, activates the user account, and dispatches a welcome email.
    """

    permission_classes = (AllowAny,)
    serializer_class = VerifyEmailSerializer

    def _process_verification(self, request, raw_token: str):
        user = RegistrationService.verify_email_token(
            raw_token=raw_token, request=request
        )
        user_data = CurrentUserSerializer(user, context={"request": request}).data

        return api_response(
            success=True,
            message=AuthMessage.EMAIL_VERIFIED_SUCCESS,
            data={"user": user_data},
            status_code=status.HTTP_200_OK,
        )

    def get(self, request, *args, **kwargs):
        raw_token = request.query_params.get("token", "")
        serializer = self.get_serializer(data={"token": raw_token})
        serializer.is_valid(raise_exception=True)
        return self._process_verification(request, serializer.validated_data["token"])

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self._process_verification(request, serializer.validated_data["token"])


class ResendVerificationAPIView(GenericAPIView):
    """
    POST /api/v1/accounts/resend-verification/
    Invalidates previous tokens, generates a new verification token, and resends verification email.
    """

    permission_classes = (AllowAny,)
    throttle_classes = (ResendVerificationRateThrottle,)
    serializer_class = ResendVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        RegistrationService.resend_verification_email(
            email=serializer.validated_data["email"], request=request
        )

        return api_response(
            success=True,
            message=AuthMessage.VERIFICATION_RESENT_SUCCESS,
            status_code=status.HTTP_200_OK,
        )


class LoginAPIView(GenericAPIView):
    """
    POST /api/v1/accounts/login/
    Authenticates user credentials and returns JWT access & refresh tokens along with user info.
    Protected by DRF rate limiting throttles against brute-force attacks.
    """

    permission_classes = (AllowAny,)
    throttle_classes = (LoginAnonRateThrottle, LoginUserRateThrottle)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user, tokens = AuthenticationService.authenticate_user(
            email=email, password=password, request=request
        )

        user_data = CurrentUserSerializer(user, context={"request": request}).data

        return api_response(
            success=True,
            message=AuthMessage.LOGIN_SUCCESS,
            data={
                "access": tokens["access"],
                "refresh": tokens["refresh"],
                "user": user_data,
            },
            status_code=status.HTTP_200_OK,
        )


class LogoutAPIView(GenericAPIView):
    """
    POST /api/v1/accounts/logout/
    Blacklists the provided refresh token and terminates active user session.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh"]
        AuthenticationService.logout_user(
            refresh_token_str=refresh_token, user=request.user, request=request
        )

        return api_response(
            success=True,
            message=AuthMessage.LOGOUT_SUCCESS,
            status_code=status.HTTP_200_OK,
        )


class CurrentUserAPIView(RetrieveAPIView):
    """
    GET /api/v1/accounts/me/
    Returns current authenticated user profile details.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = CurrentUserSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(
            success=True,
            message=AuthMessage.CURRENT_USER_RETRIEVED,
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


class CustomTokenRefreshView(TokenRefreshView):
    """
    POST /api/v1/accounts/token/refresh/
    Exposes token refresh endpoint with rotated refresh tokens and security audit logging.
    """

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            user_id = (
                getattr(request.user, "id", None)
                if hasattr(request, "user") and request.user.is_authenticated
                else None
            )
            AuditService.log_event(
                action=AuditAction.TOKEN_REFRESH_SUCCESS,
                request=request,
                user_id=user_id,
                status="SUCCESS",
            )
            return api_response(
                success=True,
                message=AuthMessage.TOKEN_REFRESH_SUCCESS,
                data=response.data,
                status_code=status.HTTP_200_OK,
            )
        except Exception as exc:
            AuditService.log_event(
                action=AuditAction.TOKEN_REFRESH_FAILED,
                request=request,
                status="FAILED",
                details={"reason": "Invalid or expired refresh token."},
            )
            raise exc
