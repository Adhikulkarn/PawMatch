"""
Centralized Enterprise Production Logging Configuration for PawMatch.

Supports:
- Console stdout/stderr logging for Cloud / Container orchestrators (Render, K8s, CloudWatch, Loki, ELK)
- Structured JSON logging (`LOG_FORMAT=json`) & Human-readable Text logging (`LOG_FORMAT=text`)
- Dynamic Request ID injection across thread execution
- Integration for Django, DRF, Security, Gunicorn, and Celery log streams
- Configurable log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from apps.core.middleware import get_current_request_id


class StructuredJSONFormatter(logging.Formatter):
    """
    Structured JSON log formatter optimized for CloudWatch, Loki, ELK, Datadog, and Render.
    """

    def format(self, record):
        log_entry = {
            "@timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", get_current_request_id()),
            "module": record.module,
            "funcName": record.funcName,
            "line": record.lineno,
            "process": record.process,
            "thread": record.thread,
        }

        # Include exception tracebacks if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Include extra context dictionary if attached
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            log_entry["extra"] = record.extra

        return json.dumps(log_entry)


def get_logging_config(
    base_dir: Path, log_level: str = "INFO", log_format: str = "json"
) -> dict:
    """
    Generates enterprise logging configuration dictionary for Django settings.
    """
    logs_dir = base_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Determine default formatter key based on environment config
    selected_formatter = "json" if log_format.lower() == "json" else "verbose"

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "request_id": {
                "()": "apps.core.middleware.RequestIDFilter",
            },
        },
        "formatters": {
            "json": {
                "()": StructuredJSONFormatter,
            },
            "verbose": {
                "format": "[%(asctime)s] [%(levelname)s] [req_id:%(request_id)s] [%(name)s:%(lineno)d] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "simple": {
                "format": "[%(levelname)s] %(message)s",
            },
        },
        "handlers": {
            "console": {
                "level": log_level,
                "class": "logging.StreamHandler",
                "filters": ["request_id"],
                "formatter": selected_formatter,
            },
            "file": {
                "level": log_level,
                "class": "logging.handlers.RotatingFileHandler",
                "filename": logs_dir / "pawmatch.log",
                "maxBytes": 1024 * 1024 * 10,  # 10 MB
                "backupCount": 5,
                "filters": ["request_id"],
                "formatter": selected_formatter,
            },
            "error_file": {
                "level": "ERROR",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": logs_dir / "error.log",
                "maxBytes": 1024 * 1024 * 10,  # 10 MB
                "backupCount": 5,
                "filters": ["request_id"],
                "formatter": selected_formatter,
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": True,
            },
            "django.request": {
                "handlers": ["console", "error_file"],
                "level": "ERROR",
                "propagate": False,
            },
            "django.security": {
                "handlers": ["console", "error_file"],
                "level": "WARNING",
                "propagate": False,
            },
            "django.db.backends": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
            "config.api": {
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": False,
            },
            "apps": {
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": False,
            },
            "security": {
                "handlers": ["console", "error_file"],
                "level": "WARNING",
                "propagate": False,
            },
            "gunicorn.error": {
                "handlers": ["console", "error_file"],
                "level": "INFO",
                "propagate": False,
            },
            "gunicorn.access": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "celery": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }
