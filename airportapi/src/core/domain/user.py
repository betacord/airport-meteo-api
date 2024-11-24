"""A model containing user-related models."""


from pydantic import BaseModel, ConfigDict, UUID1


class UserIn(BaseModel):
    """An input user model."""
    email: str
    password: str


class User(UserIn):
    """The user model class."""
    id: UUID1

    model_config = ConfigDict(from_attributes=True, extra="ignore")
