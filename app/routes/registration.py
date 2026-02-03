"""
Tournament registration API routes.
"""

from typing import Dict, Any
from datetime import datetime
import logging

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.models.registration import (
    RegistrationRequest,
    RegistrationResponse,
    ErrorResponse
)
from app.services import create_registration, get_registration

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/api/v1/registrations",
    tags=["registrations"]
)


@router.post(
    "",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Registration created successfully",
            "model": RegistrationResponse
        },
        400: {
            "description": "Invalid request data",
            "model": ErrorResponse
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse
        }
    },
    summary="Create Tournament Registration",
    description="Submit a new tournament registration with team and contact details"
)
async def create_tournament_registration(
    registration: RegistrationRequest
) -> RegistrationResponse:
    """
    Create a new tournament registration.
    
    This endpoint accepts registration data for the Chancity Open Kabaddi Tournament.
    All fields are validated before submission to the database.
    
    Args:
        registration: The registration request data
        
    Returns:
        RegistrationResponse with registration_id and status
        
    Raises:
        HTTPException: If validation fails or database operation fails
    """
    try:
        logger.info(f"Received registration request for team: {registration.team_name}")
        
        # Convert Pydantic model to dictionary
        registration_data = registration.model_dump()
        
        # Create registration in Appwrite
        result = create_registration(registration_data)
        
        logger.info(f"Registration created successfully: {result['registration_id']}")
        
        return RegistrationResponse(**result)
        
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create registration. Please try again later."
        )


@router.get(
    "/{registration_id}",
    response_model=RegistrationResponse,
    responses={
        200: {
            "description": "Registration found",
            "model": RegistrationResponse
        },
        404: {
            "description": "Registration not found",
            "model": ErrorResponse
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse
        }
    },
    summary="Get Registration by ID",
    description="Retrieve a tournament registration by its unique identifier"
)
async def get_tournament_registration(
    registration_id: str
) -> RegistrationResponse:
    """
    Retrieve a tournament registration by ID.
    
    Args:
        registration_id: The unique registration identifier (UUID)
        
    Returns:
        RegistrationResponse with registration details
        
    Raises:
        HTTPException: If registration not found or database operation fails
    """
    try:
        logger.info(f"Retrieving registration: {registration_id}")
        
        result = get_registration(registration_id)
        
        if result is None:
            logger.warning(f"Registration not found: {registration_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Registration {registration_id} not found"
            )
        
        logger.info(f"Registration retrieved successfully: {registration_id}")
        
        return RegistrationResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve registration. Please try again later."
        )
