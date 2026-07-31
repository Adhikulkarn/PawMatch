"""
Audit logging service for PawMatch.
Extracts request metadata (Client IP, User-Agent, Browser, OS, Device Type, Request ID)
and records structured audit log instances for security events.
"""

import logging
from typing import Any, Dict, Optional, Tuple

from apps.audit_logs.models import AuditLog
from apps.core.middleware import get_current_request_id

logger = logging.getLogger("security")


class AuditService:
    """
    Service responsible for parsing client metadata and recording security audit trails.
    """

    @staticmethod
    def extract_ip_address(request: Any) -> Optional[str]:
        """Extracts client IP address handling reverse proxy headers."""
        if not request:
            return None
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    @staticmethod
    def parse_user_agent(user_agent_str: str) -> Tuple[str, str, str]:
        """
        Parses User-Agent header into (Browser, OS, Device Type).
        """
        if not user_agent_str:
            return ("Unknown", "Unknown", "Unknown")

        ua = user_agent_str.lower()

        # Browser Detection
        if "edg" in ua:
            browser = "Edge"
        elif "chrome" in ua and "chromium" not in ua:
            browser = "Chrome"
        elif "firefox" in ua:
            browser = "Firefox"
        elif "safari" in ua and "chrome" not in ua:
            browser = "Safari"
        elif "opera" in ua or "opr" in ua:
            browser = "Opera"
        else:
            browser = "Other"

        # OS Detection
        if "windows" in ua:
            os_name = "Windows"
        elif "macintosh" in ua or "mac os" in ua:
            os_name = "macOS"
        elif "android" in ua:
            os_name = "Android"
        elif "iphone" in ua or "ipad" in ua or "ipod" in ua:
            os_name = "iOS"
        elif "linux" in ua:
            os_name = "Linux"
        else:
            os_name = "Other"

        # Device Type Detection
        if "ipad" in ua or "tablet" in ua:
            device_type = "Tablet"
        elif "mobile" in ua or "iphone" in ua or "android" in ua:
            device_type = "Mobile"
        else:
            device_type = "Desktop"

        return (browser, os_name, device_type)

    @classmethod
    def log_event(
        cls,
        action: str,
        request: Any = None,
        user_id: Optional[Any] = None,
        email: str = "",
        status: str = "SUCCESS",
        details: Optional[Dict[str, Any]] = None,
    ) -> AuditLog:
        """
        Creates an AuditLog record and emits a structured log entry.
        Never stores passwords, tokens, or sensitive credentials.
        """
        request_id = getattr(request, "request_id", None) or get_current_request_id()
        ip_address = cls.extract_ip_address(request)
        user_agent_str = request.META.get("HTTP_USER_AGENT", "") if request else ""
        browser, os_name, device_type = cls.parse_user_agent(user_agent_str)

        # Sanitize details to ensure sensitive keys are never persisted
        sanitized_details = {}
        if details:
            for k, v in details.items():
                if k.lower() in ("password", "token", "access", "refresh", "secret"):
                    continue
                sanitized_details[k] = v

        audit_entry = AuditLog.objects.create(
            user_id=user_id,
            email=email,
            action=action,
            request_id=request_id,
            ip_address=ip_address,
            user_agent=user_agent_str,
            browser=browser,
            os=os_name,
            device_type=device_type,
            status=status,
            details=sanitized_details,
        )

        logger.info(
            f"Security Audit Event: [{action}] status={status}",
            extra={
                "action": action,
                "user_id": str(user_id) if user_id else None,
                "email": email,
                "request_id": request_id,
                "ip_address": ip_address,
                "browser": browser,
                "os": os_name,
                "device_type": device_type,
                "status": status,
            },
        )

        return audit_entry
