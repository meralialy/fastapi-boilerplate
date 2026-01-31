from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_health():
    """Test that the health check endpoint returns a 200 status and correct structure."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
