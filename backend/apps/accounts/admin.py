"""
Django Admin interface configuration for PawMatch Custom User, UserProfile, and AccountToken models.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import AccountToken, User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User Admin interface configuration.
    """

    model = User

    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "is_email_verified",
    )
    list_filter = (
        "is_staff",
        "is_active",
        "is_superuser",
        "is_email_verified",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
    )
    ordering = ("email",)

    fieldsets = (
        (
            _("Personal Information"),
            {
                "fields": (
                    "email",
                    "password",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "profile_image",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_email_verified",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important Dates"),
            {
                "fields": (
                    "last_login",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    readonly_fields = ("created_at", "updated_at", "last_login")

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_email_verified",
                ),
            },
        ),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserProfile model.
    """

    list_display = (
        "user",
        "phone_number",
        "date_of_birth",
        "created_at",
    )
    search_fields = (
        "user__email",
        "phone_number",
        "bio",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(AccountToken)
class AccountTokenAdmin(admin.ModelAdmin):
    """
    Admin configuration for generic AccountToken model.
    """

    list_display = (
        "user",
        "token_type",
        "is_active",
        "expires_at",
        "used_at",
        "created_at",
    )
    list_filter = (
        "token_type",
        "is_active",
        "expires_at",
        "used_at",
    )
    search_fields = (
        "user__email",
        "token_hash",
    )
    readonly_fields = (
        "token_hash",
        "created_at",
        "updated_at",
    )
