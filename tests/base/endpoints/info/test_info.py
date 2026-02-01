from fastapi import status
from fastapi.testclient import TestClient

from app.configs.settings import settings
from app.main import app

client = TestClient(app)


def test_get_info():
    """Test that the info endpoint returns the correct application details."""
    response = client.get("/info")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == settings.APP_NAME
    assert data["version"] == settings.APP_VERSION
    assert data["debug"] == settings.DEBUG
