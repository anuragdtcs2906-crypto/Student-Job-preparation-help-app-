from pydantic import BaseModel, Field, field_validator
from app.utils.anonymous_id import validate_anonymous_id, normalize_anonymous_id


class AnonymousAuthRequest(BaseModel):
    """Payload for authenticating or resuming with an existing anonymous ID."""

    anonymous_id: str = Field(..., description="Unique 8-character anonymous ID")

    @field_validator("anonymous_id")
    @classmethod
    def check_valid_id(cls, v: str) -> str:
        normalized = normalize_anonymous_id(v)
        if not validate_anonymous_id(normalized):
            raise ValueError("Invalid anonymous ID format. Must be 8 valid alphanumeric characters.")
        return normalized
