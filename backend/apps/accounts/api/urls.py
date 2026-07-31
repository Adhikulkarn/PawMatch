"""
URL routing table for Accounts, Registration & Authentication API endpoints.
"""

from django.urls import path

from apps.accounts.api.views import (
    CurrentUserAPIView,
    CustomTokenRefreshView,
    LoginAPIView,
    LogoutAPIView,
    RegisterAPIView,
    ResendVerificationAPIView,
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
]
