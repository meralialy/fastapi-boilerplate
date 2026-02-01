from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_example():
    """Test the v1 example endpoint returns the expected greeting."""
    response = client.get("/api/v1/example")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"msg": "This is an example endpoint from v1"}
