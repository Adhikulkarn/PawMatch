"""
Django Admin interface configuration for PawMatch Custom User, UserProfile, Groups, and Permissions.
Enhanced for RBAC management, role summaries, user role displays, and permission summaries.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import AccountToken, User, UserProfile
from apps.accounts.services.rbac_service import ROLE_TO_GROUP_NAME
from apps.accounts.services.role_service import RoleService

GROUP_NAME_TO_ROLE = {v: k for k, v in ROLE_TO_GROUP_NAME.items()}

try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass


@admin.register(Group)
class EnhancedGroupAdmin(admin.ModelAdmin):
    """
    Enhanced Admin interface configuration for Django Groups & Role Permissions.
    Provides role code resolution, permission counting, and permission search.
    """

    list_display = ("name", "role_code_display", "permission_count")
    search_fields = ("name", "permissions__name", "permissions__codename")
    filter_horizontal = ("permissions",)

    @admin.display(description=_("Role Code"))
    def role_code_display(self, obj: Group) -> str:
        role = GROUP_NAME_TO_ROLE.get(obj.name, "-")
        return format_html("<code>{}</code>", role)

    @admin.display(description=_("Permissions Count"))
    def permission_count(self, obj: Group) -> int:
        return obj.permissions.count()


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Django Permission model.
    """

    list_display = ("name", "codename", "content_type")
    list_filter = ("content_type__app_label", "content_type")
    search_fields = ("name", "codename")
    ordering = ("content_type__app_label", "codename")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User Admin interface configuration with RBAC Role & Permission display.
    """

    model = User

    list_display = (
        "email",
        "first_name",
        "last_name",
        "roles_display",
        "is_staff",
        "is_active",
        "is_email_verified",
    )
    list_filter = (
        "is_staff",
        "is_active",
        "is_superuser",
        "is_email_verified",
        "groups",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
    )
    ordering = ("email",)

    readonly_fields = (
        "created_at",
        "updated_at",
        "last_login",
        "roles_summary_display",
        "permissions_summary_display",
    )

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
            _("Role & Authorization Summary"),
            {
                "fields": (
                    "roles_summary_display",
                    "permissions_summary_display",
                ),
            },
        ),
        (
            _("Permissions & Access Controls"),
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

    @admin.display(description=_("Assigned Roles"))
    def roles_display(self, obj: User) -> str:
        roles = sorted(list(RoleService.get_roles(obj)))
        if not roles:
            return "-"
        return ", ".join(roles)

    @admin.display(description=_("Assigned Roles"))
    def roles_summary_display(self, obj: User) -> str:
        roles = sorted(list(RoleService.get_roles(obj)))
        if not roles:
            return mark_safe("<em>No roles assigned</em>")
        badges = " ".join(
            [
                f"<span style='background:#007bff; color:#fff; padding:2px 8px; border-radius:4px; font-size:12px; font-weight:bold;'>{r}</span>"
                for r in roles
            ]
        )
        return mark_safe(badges)

    @admin.display(description=_("Aggregated Permissions"))
    def permissions_summary_display(self, obj: User) -> str:
        perms = sorted(list(RoleService.get_permissions(obj)))
        if not perms:
            return mark_safe("<em>No permissions assigned</em>")
        perm_items = "".join([f"<li><code>{p}</code></li>" for p in perms])
        return mark_safe(f"<ul style='margin:0; padding-left:18px;'>{perm_items}</ul>")


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
