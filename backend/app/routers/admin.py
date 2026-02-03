"""
Admin routes for the Chancity Admin Panel.
Provides endpoints for managing registrations without accessing Appwrite console.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
import logging

from app.config import settings
from app.services import get_appwrite_client

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/admin", tags=["admin"])


# Request/Response Models
class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    message: str
    user: Optional[dict] = None


class StatusUpdateRequest(BaseModel):
    status: str


class RegistrationResponse(BaseModel):
    data: List[dict]
    total: int
    page: int
    limit: int


class StatsResponse(BaseModel):
    total: int
    pending: int
    approved: int
    rejected: int


# Admin credentials (hardcoded as per requirements)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "0000"


@router.post("/login", response_model=LoginResponse)
async def admin_login(request: LoginRequest):
    """
    Authenticate admin user.
    Simple local authentication with hardcoded credentials.
    """
    if request.username == ADMIN_USERNAME and request.password == ADMIN_PASSWORD:
        logger.info("Admin login successful")
        return LoginResponse(
            success=True,
            message="Login successful",
            user={
                "username": "admin",
                "role": "administrator",
                "loginTime": datetime.utcnow().isoformat()
            }
        )
    else:
        logger.warning(f"Failed admin login attempt for user: {request.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.get("/registrations")
async def list_registrations(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None
):
    """
    List all registrations with pagination, search, and filtering.
    """
    try:
        appwrite = get_appwrite_client()
        
        # Build query filters
        queries = []
        
        # Note: Appwrite SDK uses Query class for filtering
        from appwrite.query import Query as AppwriteQuery
        
        # Status filter
        if status and status in ["pending", "approved", "rejected"]:
            queries.append(AppwriteQuery.equal("status", status))
        
        # Server-side search optimization
        # We try to use Appwrite's search capability on team_name first
        if search:
            # If search is provided, we use it in the query
            queries.append(AppwriteQuery.search("team_name", search))
            
        # Calculate offset
        offset = (page - 1) * limit
        
        # List documents with pagination
        response = appwrite.databases.list_documents(
            database_id=settings.appwrite_database_id,
            collection_id=settings.appwrite_collection_id,
            queries=queries + [
                AppwriteQuery.limit(limit),
                AppwriteQuery.offset(offset),
                AppwriteQuery.order_desc("$createdAt")
            ]
        )
        
        documents = response.get("documents", [])
        total = response.get("total", 0)
        
        # Final safety check: if search was provided but returned fewer items than expected 
        # (or if we want to search across multiple fields and indexes aren't perfect), 
        # we can still keep a simplified client-side filter as a secondary measure.
        if search:
            search_lower = search.lower()
            # If documents don't match, we might have over-filtered server-side or 
            # we need to search contact_name etc which might not be indexed for search
            # We'll just return what we got from the search query for performance.
            pass
        
        logger.info(f"Listed {len(documents)} registrations (page {page}, total {total})")
        
        return {
            "data": documents,
            "total": total,
            "page": page,
            "limit": limit
        }
        
    except Exception as e:
        logger.error(f"Error listing registrations: {str(e)}")
        # If search fails (e.g. index not found), try without search filter
        if "search" in str(e).lower():
            try:
                 # Fallback to no-search query
                 response = appwrite.databases.list_documents(
                    database_id=settings.appwrite_database_id,
                    collection_id=settings.appwrite_collection_id,
                    queries=[AppwriteQuery.limit(limit), AppwriteQuery.offset((page - 1) * limit)]
                )
                 return {
                    "data": response.get("documents", []),
                    "total": response.get("total", 0),
                    "page": page,
                    "limit": limit
                }
            except: pass
        raise HTTPException(status_code=500, detail=f"Failed to list registrations: {str(e)}")


@router.get("/registrations/{registration_id}")
async def get_registration(registration_id: str):
    """
    Get a single registration by ID.
    """
    try:
        appwrite = get_appwrite_client()
        
        response = appwrite.databases.get_document(
            database_id=settings.appwrite_database_id,
            collection_id=settings.appwrite_collection_id,
            document_id=registration_id
        )
        
        logger.info(f"Retrieved registration: {registration_id}")
        return response
        
    except Exception as e:
        if "404" in str(e) or "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail="Registration not found")
        logger.error(f"Error getting registration: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get registration: {str(e)}")


@router.patch("/registrations/{registration_id}")
async def update_registration_status(registration_id: str, request: StatusUpdateRequest):
    """
    Update registration status (approve/reject/pending).
    """
    if request.status not in ["pending", "approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status. Must be: pending, approved, or rejected")
    
    try:
        appwrite = get_appwrite_client()
        
        response = appwrite.databases.update_document(
            database_id=settings.appwrite_database_id,
            collection_id=settings.appwrite_collection_id,
            document_id=registration_id,
            data={"status": request.status}
        )
        
        logger.info(f"Updated registration {registration_id} status to: {request.status}")
        
        return {
            "success": True,
            "message": f"Status updated to {request.status}",
            "data": response
        }
        
    except Exception as e:
        if "404" in str(e) or "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail="Registration not found")
        logger.error(f"Error updating registration: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update registration: {str(e)}")


@router.delete("/registrations/{registration_id}")
async def delete_registration(registration_id: str):
    """
    Delete a registration.
    """
    try:
        appwrite = get_appwrite_client()
        
        appwrite.databases.delete_document(
            database_id=settings.appwrite_database_id,
            collection_id=settings.appwrite_collection_id,
            document_id=registration_id
        )
        
        logger.info(f"Deleted registration: {registration_id}")
        
        return {
            "success": True,
            "message": "Registration deleted successfully"
        }
        
    except Exception as e:
        if "404" in str(e) or "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail="Registration not found")
        logger.error(f"Error deleting registration: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete registration: {str(e)}")


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """
    Get dashboard statistics.
    """
    try:
        appwrite = get_appwrite_client()
        
        from appwrite.query import Query as AppwriteQuery
        
        # Get total count
        total_response = appwrite.databases.list_documents(
            database_id=settings.appwrite_database_id,
            collection_id=settings.appwrite_collection_id,
            queries=[AppwriteQuery.limit(1)]
        )
        total = total_response.get("total", 0)
        
        # Get pending count
        pending_response = appwrite.databases.list_documents(
            database_id=settings.appwrite_database_id,
            collection_id=settings.appwrite_collection_id,
            queries=[
                AppwriteQuery.equal("status", "pending"),
                AppwriteQuery.limit(1)
            ]
        )
        pending = pending_response.get("total", 0)
        
        # Get approved count
        approved_response = appwrite.databases.list_documents(
            database_id=settings.appwrite_database_id,
            collection_id=settings.appwrite_collection_id,
            queries=[
                AppwriteQuery.equal("status", "approved"),
                AppwriteQuery.limit(1)
            ]
        )
        approved = approved_response.get("total", 0)
        
        # Get rejected count
        rejected_response = appwrite.databases.list_documents(
            database_id=settings.appwrite_database_id,
            collection_id=settings.appwrite_collection_id,
            queries=[
                AppwriteQuery.equal("status", "rejected"),
                AppwriteQuery.limit(1)
            ]
        )
        rejected = rejected_response.get("total", 0)
        
        logger.info(f"Stats retrieved: total={total}, pending={pending}, approved={approved}, rejected={rejected}")
        
        return StatsResponse(
            total=total,
            pending=pending,
            approved=approved,
            rejected=rejected
        )
        
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        # Return zeros if there's an error
        return StatsResponse(total=0, pending=0, approved=0, rejected=0)
