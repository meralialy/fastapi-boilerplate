from fastapi import APIRouter

from .schemas import ExampleResponse

router = APIRouter(prefix="/example")


@router.get("", response_model=ExampleResponse)
def get_example() -> ExampleResponse:
    """
    Retrieve a message to verify v1 API connectivity.

    Returns:
        ExampleResponse: A JSON object containing a greeting message.
    """
    return ExampleResponse(msg="This is an example endpoint from v1")
