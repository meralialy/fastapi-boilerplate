from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class FutureTimestampError(ValueError):
    """Exception raised when the timestamp is in the future."""

    def __init__(self) -> None:
        super().__init__("Timestamp cannot be in the future")


class HealthResponse(BaseModel):
    """Schema for the health check response."""

    status: Literal["healthy", "unhealthy", "degraded"] = Field(
        description="Current operational status of the application"
    )

    timestamp: datetime = Field(description="The precise time the health check was performed (UTC)")

    @field_validator("timestamp")
    @classmethod
    def ensure_not_future(cls, v: datetime) -> datetime:
        """
        Validate that the timestamp is not in the future.

        Allows a 60-second buffer to account for potential clock skew between systems.
        """
        if v.timestamp() > datetime.now(tz=UTC).timestamp() + 60:
            raise FutureTimestampError()
        return v
