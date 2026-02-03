"""
Settings routes for Admin Panel configuration.
Manages application settings like registration open/close status.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
import json
import os

from app.config import settings
from app.services import get_appwrite_client

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/admin/settings", tags=["settings"])

# Settings file path (fallback if Appwrite unavailable)
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "../../settings.json")

# Default settings
DEFAULT_SETTINGS = {
    "registration_open": True
}


class SettingsResponse(BaseModel):
    registration_open: bool


class SettingsUpdateRequest(BaseModel):
    registration_open: Optional[bool] = None


def load_settings() -> dict:
    """Load settings from file."""
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        logger.warning(f"Could not load settings file: {e}")
    return DEFAULT_SETTINGS.copy()


def save_settings(data: dict) -> bool:
    """Save settings to file."""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Could not save settings: {e}")
        return False


@router.get("", response_model=SettingsResponse)
async def get_settings():
    """
    Get current application settings.
    """
    try:
        current_settings = load_settings()
        logger.info(f"Settings retrieved: registration_open={current_settings.get('registration_open', True)}")
        return SettingsResponse(
            registration_open=current_settings.get("registration_open", True)
        )
    except Exception as e:
        logger.error(f"Error getting settings: {str(e)}")
        # Return default if error
        return SettingsResponse(registration_open=True)


@router.patch("", response_model=SettingsResponse)
async def update_settings(request: SettingsUpdateRequest):
    """
    Update application settings.
    """
    try:
        current_settings = load_settings()
        
        # Update only provided fields
        if request.registration_open is not None:
            current_settings["registration_open"] = request.registration_open
            logger.info(f"Registration status updated to: {request.registration_open}")
        
        # Save updated settings
        if save_settings(current_settings):
            return SettingsResponse(
                registration_open=current_settings.get("registration_open", True)
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to save settings")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating settings: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update settings: {str(e)}")


# Public endpoint (no auth required) for checking registration status
@router.get("/public/registration-status")
async def get_registration_status():
    """
    Public endpoint to check if registration is open.
    Used by the public registration form.
    """
    try:
        current_settings = load_settings()
        return {
            "registration_open": current_settings.get("registration_open", True)
        }
    except Exception as e:
        logger.error(f"Error getting registration status: {str(e)}")
        # Default to open if error
        return {"registration_open": True}
