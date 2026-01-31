from pydantic import BaseModel, Field


class InfoResponse(BaseModel):
    """Schema for the application information response."""

    name: str = Field(description="The formal name of the application as defined in pyproject.toml")
    version: str = Field(description="The semantic version (SemVer) of the current deployment")
    debug: bool = Field(description="Indicates if the application is running with verbose error reporting enabled")
