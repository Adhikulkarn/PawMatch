"""
Django Admin interface configuration for the Shelter domain models.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.shelters.models import (
    Shelter,
    ShelterDocument,
    ShelterInvitation,
    ShelterMember,
    ShelterVerification,
)


@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    """Admin configuration for Shelter organization profiles."""

    list_display = (
        "name",
        "slug",
        "city",
        "state",
        "status",
        "is_active",
        "created_at",
    )
    list_filter = (
        "status",
        "is_active",
        "is_deleted",
        "state",
        "country",
    )
    search_fields = (
        "name",
        "slug",
        "legal_name",
        "email",
        "phone_number",
        "city",
        "registration_number",
    )
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    ordering = ("name",)

    fieldsets = (
        (
            _("Organization Identity"),
            {
                "fields": (
                    "name",
                    "slug",
                    "legal_name",
                    "registration_number",
                    "tax_id",
                )
            },
        ),
        (
            _("Contact Information"),
            {
                "fields": (
                    "email",
                    "phone_number",
                    "website",
                )
            },
        ),
        (
            _("Location & Address"),
            {
                "fields": (
                    "address_line1",
                    "address_line2",
                    "city",
                    "state",
                    "postal_code",
                    "country",
                    "latitude",
                    "longitude",
                )
            },
        ),
        (
            _("Branding & Presentation"),
            {
                "fields": (
                    "description",
                    "logo",
                    "banner_image",
                )
            },
        ),
        (
            _("Platform Lifecycle & Operational Status"),
            {
                "fields": (
                    "status",
                    "is_active",
                    "is_deleted",
                )
            },
        ),
        (
            _("System Metadata"),
            {
                "fields": (
                    "id",
                    "created_at",
                    "updated_at",
                    "deleted_at",
                )
            },
        ),
    )


@admin.register(ShelterMember)
class ShelterMemberAdmin(admin.ModelAdmin):
    """Admin configuration for ShelterMember user-to-shelter relationships."""

    list_display = (
        "user",
        "shelter",
        "role",
        "is_active",
        "joined_at",
    )
    list_filter = (
        "role",
        "is_active",
        "shelter",
    )
    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "shelter__name",
    )
    autocomplete_fields = (
        "shelter",
        "user",
    )
    readonly_fields = (
        "id",
        "joined_at",
        "created_at",
        "updated_at",
    )
    ordering = ("-joined_at",)


@admin.register(ShelterVerification)
class ShelterVerificationAdmin(admin.ModelAdmin):
    """Admin configuration for ShelterVerification workflow tracking."""

    list_display = (
        "shelter",
        "status",
        "reviewed_by",
        "submitted_at",
        "reviewed_at",
    )
    list_filter = (
        "status",
        "submitted_at",
        "reviewed_at",
    )
    search_fields = (
        "shelter__name",
        "reviewed_by__email",
        "reviewer_notes",
        "rejection_reason",
    )
    autocomplete_fields = (
        "shelter",
        "reviewed_by",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)


@admin.register(ShelterDocument)
class ShelterDocumentAdmin(admin.ModelAdmin):
    """Admin configuration for uploaded Shelter verification documents."""

    list_display = (
        "file_name",
        "shelter",
        "document_type",
        "status",
        "uploaded_by",
        "verified_by",
        "created_at",
    )
    list_filter = (
        "document_type",
        "status",
        "shelter",
    )
    search_fields = (
        "file_name",
        "shelter__name",
        "uploaded_by__email",
        "verified_by__email",
    )
    autocomplete_fields = (
        "shelter",
        "verification",
        "uploaded_by",
        "verified_by",
    )
    readonly_fields = (
        "id",
        "file_size",
        "mime_type",
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)


@admin.register(ShelterInvitation)
class ShelterInvitationAdmin(admin.ModelAdmin):
    """Admin configuration for Shelter member invitations."""

    list_display = (
        "email",
        "shelter",
        "role",
        "status",
        "invited_by",
        "accepted_by",
        "expires_at",
    )
    list_filter = (
        "role",
        "status",
        "shelter",
    )
    search_fields = (
        "email",
        "token",
        "shelter__name",
        "invited_by__email",
        "accepted_by__email",
    )
    autocomplete_fields = (
        "shelter",
        "invited_by",
        "accepted_by",
    )
    readonly_fields = (
        "id",
        "token",
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)
