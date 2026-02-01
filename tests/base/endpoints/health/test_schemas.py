from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from app.base.endpoints.health.schemas import HealthResponse


def test_health_response_valid():
    """Test that HealthResponse accepts valid data."""
    data = {
        "status": "healthy",
        "timestamp": datetime.now(tz=UTC),
    }
    response = HealthResponse.model_validate(data)
    assert response.status == "healthy"


def test_health_response_invalid_status():
    """Test that HealthResponse rejects invalid status values."""
    data = {"status": "invalid", "timestamp": datetime.now(tz=UTC)}
    with pytest.raises(ValidationError):
        HealthResponse.model_validate(data)


def test_health_response_future_timestamp():
    """Test that HealthResponse rejects timestamps in the future."""
    future_time = datetime.now(tz=UTC) + timedelta(hours=1)
    data = {"status": "healthy", "timestamp": future_time}
    with pytest.raises(ValidationError) as exc:
        HealthResponse.model_validate(data)
    assert "Timestamp cannot be in the future" in str(exc.value)
