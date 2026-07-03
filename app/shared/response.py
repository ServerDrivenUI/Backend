from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")
"""Type variable representing the payload data type within the API response."""


class ApiResponse(BaseModel, Generic[T]):
    """
    Generic API response model wrapping payloads and execution errors.
    """

    data: Optional[T] = None
    """The response payload data of type T, or None if an error occurred."""

    error: Optional[str] = None
    """The error message description, or None if the operation was successful."""
