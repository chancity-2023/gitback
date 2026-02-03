"""
Appwrite Cloud SDK integration service.
Handles all database operations with Appwrite.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import uuid
import logging

from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.exception import AppwriteException

from app.config import settings

# Configure logging
logger = logging.getLogger(__name__)


class AppwriteService:
    """Service class for Appwrite operations."""
    
    def __init__(self):
        """Initialize Appwrite client."""
        self.client = None
        self.databases = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize Appwrite client with configuration."""
        try:
            self.client = Client()
            self.client.set_endpoint(settings.appwrite_endpoint)
            self.client.set_project(settings.appwrite_project_id)
            self.client.set_key(settings.appwrite_api_key)
            
            self.databases = Databases(self.client)
            logger.info("Appwrite client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Appwrite client: {str(e)}")
            raise
    
    def create_registration(self, registration_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new tournament registration in Appwrite.
        
        Args:
            registration_data: Dictionary containing registration information
            
        Returns:
            Dictionary with registration_id and created_at timestamp
            
        Raises:
            AppwriteException: If document creation fails
        """
        try:
            # Generate unique registration ID
            registration_id = str(uuid.uuid4())
            created_at = datetime.utcnow()
            
            # Prepare document data
            document_data = {
                "registration_id": registration_id,
                "team_name": registration_data["team_name"],
                "category": registration_data["category"],
                "team_size": registration_data["team_size"],
                "contact_name": registration_data["contact_name"],
                "designation": registration_data["designation"],
                "email": registration_data["email"],
                "phone": registration_data["phone"],
                "alt_phone": registration_data.get("alt_phone", ""),
                "players": registration_data["players"],
                "terms_accepted": registration_data["terms_accepted"],
                "newsletter_subscribed": registration_data.get("newsletter_subscribed", False),
                "status": "pending",
                "created_at": created_at.isoformat()
            }
            
            # Create document in Appwrite
            response = self.databases.create_document(
                database_id=settings.appwrite_database_id,
                collection_id=settings.appwrite_collection_id,
                document_id=registration_id,
                data=document_data
            )
            
            logger.info(f"Registration created successfully: {registration_id}")
            
            return {
                "registration_id": registration_id,
                "status": "pending",
                "created_at": created_at,
                "message": "Registration submitted successfully"
            }
            
        except AppwriteException as e:
            logger.error(f"Appwrite error creating registration: {str(e)}")
            raise Exception(f"Failed to create registration: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error creating registration: {str(e)}")
            raise Exception(f"An unexpected error occurred: {str(e)}")
    
    def get_registration(self, registration_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a registration by ID.
        
        Args:
            registration_id: The unique registration identifier
            
        Returns:
            Dictionary with registration data or None if not found
            
        Raises:
            AppwriteException: If retrieval fails
        """
        try:
            response = self.databases.get_document(
                database_id=settings.appwrite_database_id,
                collection_id=settings.appwrite_collection_id,
                document_id=registration_id
            )
            
            logger.info(f"Registration retrieved successfully: {registration_id}")
            
            return {
                "registration_id": response["registration_id"],
                "status": response["status"],
                "created_at": datetime.fromisoformat(response["created_at"]),
                "message": "Registration found"
            }
            
        except AppwriteException as e:
            if "404" in str(e):
                logger.warning(f"Registration not found: {registration_id}")
                return None
            logger.error(f"Appwrite error retrieving registration: {str(e)}")
            raise Exception(f"Failed to retrieve registration: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error retrieving registration: {str(e)}")
            raise Exception(f"An unexpected error occurred: {str(e)}")


# Global service instance
appwrite_service = AppwriteService()


# Convenience functions
def get_appwrite_client() -> AppwriteService:
    """Get the global Appwrite service instance."""
    return appwrite_service


def create_registration(registration_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new registration."""
    return appwrite_service.create_registration(registration_data)


def get_registration(registration_id: str) -> Optional[Dict[str, Any]]:
    """Get registration by ID."""
    return appwrite_service.get_registration(registration_id)
