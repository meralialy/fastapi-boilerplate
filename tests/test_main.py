from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_custom_404_handler():
    """Test that the custom 404 exception handler returns the expected JSON structure."""
    response = client.get("/non-existent-route")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["status"] == "error"
    assert data["message"] == "The requested resource does not exist."
    assert data["path"] == "/non-existent-route"
    assert "suggestion" in data
    assert "available_versions" in data


def test_process_time_header():
    """Test that the X-Process-Time header is added to responses."""
    # We can hit the 404 route, as middleware runs for all requests
    response = client.get("/non-existent-route")

    assert "X-Process-Time" in response.headers
    # Check format (ends with 's')
    assert response.headers["X-Process-Time"].endswith("s")


def test_lifespan_events():
    """Test that lifespan events (startup/shutdown) run correctly."""
    with TestClient(app):
        pass  # Just entering and exiting the context triggers lifespan


def test_custom_http_exception_handler_non_404():
    """Test that the custom exception handler handles non-404 HTTP exceptions."""

    # Define a route that raises a specific HTTP exception
    @app.get("/test-exception")
    def raise_exception():
        raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail="Teapot error")

    response = client.get("/test-exception")
    assert response.status_code == status.HTTP_418_IM_A_TEAPOT
    assert response.json() == {"detail": "Teapot error"}
