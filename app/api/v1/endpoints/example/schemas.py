from pydantic import BaseModel


class ExampleResponse(BaseModel):
    """Schema for the example endpoint response."""

    msg: str
