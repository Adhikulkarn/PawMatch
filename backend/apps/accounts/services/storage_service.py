"""
Storage abstraction service layer for PawMatch.
Decouples media storage operations (avatar saving, deletion, URL generation) from core business logic.
"""

import logging
import os
from abc import ABC, abstractmethod
from typing import Any

from django.core.files.storage import default_storage

logger = logging.getLogger("apps.accounts")


class StorageProvider(ABC):
    """Abstract interface for media file storage operations."""

    @abstractmethod
    def save_file(self, file_obj: Any, destination_path: str) -> str:
        """Saves file to storage and returns relative path/identifier."""
        pass

    @abstractmethod
    def delete_file(self, file_path: str) -> bool:
        """Deletes file from storage."""
        pass

    @abstractmethod
    def get_url(self, file_path: str) -> str:
        """Returns public media URL for stored file."""
        pass


class LocalStorageProvider(StorageProvider):
    """Concrete storage provider using Django default_storage engine."""

    def save_file(self, file_obj: Any, destination_path: str) -> str:
        saved_name = default_storage.save(destination_path, file_obj)
        return saved_name

    def delete_file(self, file_path: str) -> bool:
        if file_path and default_storage.exists(file_path):
            default_storage.delete(file_path)
            return True
        return False

    def get_url(self, file_path: str) -> str:
        if not file_path:
            return ""
        if default_storage.exists(file_path):
            return default_storage.url(file_path)
        return file_path


class StorageService:
    """Service accessor for media storage operations."""

    _provider = LocalStorageProvider()

    @classmethod
    def get_provider(cls) -> StorageProvider:
        return cls._provider

    @classmethod
    def save_avatar(cls, file_obj: Any, user_id: Any) -> str:
        """Generates a secure avatar filename and saves using active provider."""
        ext = os.path.splitext(file_obj.name)[1].lower()
        destination_path = f"users/avatars/{user_id}{ext}"

        # Delete existing file if present at destination path
        cls._provider.delete_file(destination_path)

        saved_path = cls._provider.save_file(file_obj, destination_path)
        return saved_path

    @classmethod
    def delete_avatar(cls, file_path: str) -> bool:
        """Deletes stored avatar file."""
        return cls._provider.delete_file(file_path)
