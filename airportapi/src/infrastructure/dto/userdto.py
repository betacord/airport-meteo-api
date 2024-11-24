"""A module containing user DTO model."""


from pydantic import UUID4, BaseModel, ConfigDict


class UserDTO(BaseModel):
    """A DTO model for user."""

    id: UUID4
    email: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )
