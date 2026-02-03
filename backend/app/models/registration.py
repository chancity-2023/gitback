"""
Pydantic models for tournament registration validation.
"""

from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class RegistrationRequest(BaseModel):
    """Request model for tournament registration submission - accepts flexible formats."""
    
    # Team Information
    team_name: str = Field(
        ...,
        description="Team/School/Club name"
    )
    category: str = Field(
        ...,
        description="Tournament category"
    )
    team_size: int = Field(
        ...,
        description="Number of players"
    )
    
    # Contact Person Details
    contact_name: str = Field(
        ...,
        description="Contact person full name"
    )
    designation: str = Field(
        ...,
        description="Contact person designation"
    )
    email: str = Field(
        ...,
        description="Contact email address"
    )
    phone: str = Field(
        ...,
        description="Primary phone number"
    )
    alt_phone: Optional[str] = Field(
        default="",
        description="Alternate phone number (optional)"
    )
    
    # Team Members
    players: str = Field(
        ...,
        description="List of player names and details"
    )
    
    # Consents
    terms_accepted: bool = Field(
        ...,
        description="Terms and conditions acceptance"
    )
    newsletter_subscribed: bool = Field(
        default=False,
        description="Newsletter subscription preference"
    )
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "team_name": "Chancity Warriors",
                "category": "senior",
                "team_size": 10,
                "contact_name": "Rajesh Kumar",
                "designation": "coach",
                "email": "rajesh@example.com",
                "phone": "9876543210",
                "alt_phone": "9123456789",
                "players": "1. John Doe - 25 - Raider\\n2. Jane Smith - 23 - Defender",
                "terms_accepted": True,
                "newsletter_subscribed": False
            }
        }


class RegistrationResponse(BaseModel):
    """Response model for successful registration."""
    
    registration_id: str = Field(
        ...,
        description="Unique registration identifier"
    )
    status: str = Field(
        default="pending",
        description="Registration status"
    )
    created_at: datetime = Field(
        ...,
        description="Registration timestamp"
    )
    message: str = Field(
        default="Registration submitted successfully",
        description="Success message"
    )
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "registration_id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "pending",
                "created_at": "2026-01-31T22:00:00Z",
                "message": "Registration submitted successfully"
            }
        }


class ErrorResponse(BaseModel):
    """Response model for errors."""
    
    error: str = Field(
        ...,
        description="Error type"
    )
    detail: str = Field(
        ...,
        description="Detailed error message"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Error timestamp"
    )
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "detail": "Invalid phone number format",
                "timestamp": "2026-01-31T22:00:00Z"
            }
        }
