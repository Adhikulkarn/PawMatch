"""
Core infrastructure utility functions for PawMatch.
"""

import os
import uuid
from typing import Any


def generate_unique_filename(instance: Any, filename: str) -> str:
    """Generates a UUID-suffixed file upload path preserving extension."""
    ext = filename.split(".")[-1]
    unique_id = uuid.uuid4().hex[:12]
    app_name = instance._meta.app_label
    model_name = instance._meta.model_name
    return os.path.join(app_name, model_name, f"{unique_id}.{ext}")


def generate_verification_code(length: int = 6) -> str:
    """Generates a numeric verification code."""
    import random

    return "".join([str(random.randint(0, 9)) for _ in range(length)])
