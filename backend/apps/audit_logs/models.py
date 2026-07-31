"""
Audit Log model definition for PawMatch.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.mixins import TimestampedModel, UUIDModel


class AuditLog(UUIDModel, TimestampedModel):
    """
    Stores immutable security and operation audit trail events.
    """

    user_id = models.UUIDField(null=True, blank=True, db_index=True)
    email = models.EmailField(blank=True, default="", db_index=True)
    action = models.CharField(max_length=100, db_index=True)
    request_id = models.CharField(max_length=64, blank=True, default="", db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default="")
    browser = models.CharField(max_length=100, blank=True, default="")
    os = models.CharField(max_length=100, blank=True, default="")
    device_type = models.CharField(max_length=50, blank=True, default="")
    status = models.CharField(max_length=20, default="SUCCESS", db_index=True)
    details = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = _("audit log")
        verbose_name_plural = _("audit logs")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["action", "created_at"]),
            models.Index(fields=["request_id"]),
        ]

    def __str__(self) -> str:
        return f"[{self.action}] {self.email or self.user_id} - {self.created_at}"
