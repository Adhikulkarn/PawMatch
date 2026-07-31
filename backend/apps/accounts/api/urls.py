"""
URL routing table for Accounts, Registration, Authentication, Profile Management & Password Management API endpoints.
"""

from django.urls import path

from apps.accounts.api.views import (
    ChangePasswordAPIView,
    CurrentUserAPIView,
    CustomTokenRefreshView,
    DeactivateAccountAPIView,
    ForgotPasswordAPIView,
    LoginAPIView,
    LogoutAPIView,
    RegisterAPIView,
    ResendVerificationAPIView,
    ResetPasswordAPIView,
    UploadAvatarAPIView,
    UserProfileAPIView,
    VerifyEmailAPIView,
)

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("verify-email/", VerifyEmailAPIView.as_view(), name="verify_email"),
    path(
        "resend-verification/",
        ResendVerificationAPIView.as_view(),
        name="resend_verification",
    ),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("me/", CurrentUserAPIView.as_view(), name="me"),
    path("profile/", UserProfileAPIView.as_view(), name="profile"),
    path("profile/avatar/", UploadAvatarAPIView.as_view(), name="avatar"),
    path("deactivate/", DeactivateAccountAPIView.as_view(), name="deactivate"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change_password"),
    path("forgot-password/", ForgotPasswordAPIView.as_view(), name="forgot_password"),
    path("reset-password/", ResetPasswordAPIView.as_view(), name="reset_password"),
]
