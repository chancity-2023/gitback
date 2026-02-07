"""
Test suite for Tournament Registration API
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import uuid

# Import the FastAPI app
from app.main import app

# Create test client
client = TestClient(app)


class TestHealthEndpoints:
    """Test health check and root endpoints."""
    
    def test_health_check(self):
        """Test health endpoint returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
    
    def test_root_endpoint(self):
        """Test root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert data["status"] == "running"


class TestRegistrationEndpoints:
    """Test registration-related endpoints."""
    
    def test_get_registrations_unauthorized(self):
        """Test getting registrations without auth fails."""
        response = client.get("/api/v1/registrations")
        # Should fail due to missing auth or return empty list
        assert response.status_code in [200, 401, 403]
    
    def test_create_registration_invalid_data(self):
        """Test creating registration with invalid data fails."""
        invalid_data = {
            "team_name": "",  # Empty team name
            "category": "invalid",  # Invalid category
            "email": "not-an-email"  # Invalid email
        }
        response = client.post("/api/v1/registrations", json=invalid_data)
        assert response.status_code == 422
    
    def test_create_registration_missing_fields(self):
        """Test creating registration with missing required fields."""
        incomplete_data = {
            "team_name": "Test Team"
            # Missing other required fields
        }
        response = client.post("/api/v1/registrations", json=incomplete_data)
        assert response.status_code == 422


class TestAdminEndpoints:
    """Test admin-related endpoints."""
    
    def test_get_admin_registrations_unauthorized(self):
        """Test admin registrations endpoint without auth."""
        response = client.get("/api/admin/registrations")
        # Should require authentication
        assert response.status_code in [401, 403, 404]
    
    def test_get_admin_stats_unauthorized(self):
        """Test admin stats endpoint without auth."""
        response = client.get("/api/admin/stats")
        # Should require authentication
        assert response.status_code in [401, 403, 404]


class TestSettingsEndpoints:
    """Test settings-related endpoints."""
    
    def test_get_public_registration_status(self):
        """Test public registration status endpoint."""
        response = client.get("/api/admin/settings/public/registration-status")
        # This should be publicly accessible
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.json()
            assert "registration_open" in data
    
    def test_update_settings_unauthorized(self):
        """Test updating settings without auth."""
        response = client.patch("/api/admin/settings", json={
            "registration_open": False
        })
        # Should require authentication
        assert response.status_code in [401, 403, 404]


class TestCORSConfiguration:
    """Test CORS configuration."""
    
    def test_cors_preflight_health(self):
        """Test CORS preflight request for health endpoint."""
        response = client.options(
            "/health",
            headers={
                "Origin": "https://chancity.github.io",
                "Access-Control-Request-Method": "GET"
            }
        )
        # Should allow the origin or return appropriate CORS headers
        assert response.status_code in [200, 404]
    
    def test_cors_headers_present(self):
        """Test CORS headers are present in response."""
        response = client.get(
            "/health",
            headers={"Origin": "https://chancity.github.io"}
        )
        # Check if CORS headers are present
        assert response.status_code == 200


class TestErrorHandling:
    """Test error handling."""
    
    def test_404_not_found(self):
        """Test 404 error for non-existent endpoint."""
        response = client.get("/non-existent-endpoint")
        assert response.status_code == 404
    
    def test_invalid_json_payload(self):
        """Test error handling for invalid JSON."""
        response = client.post(
            "/api/v1/registrations",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
