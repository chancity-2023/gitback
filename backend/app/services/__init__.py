"""Service layer initialization."""

from .appwrite_service import (
    get_appwrite_client,
    create_registration,
    get_registration
)

__all__ = [
    "get_appwrite_client",
    "create_registration",
    "get_registration"
]
