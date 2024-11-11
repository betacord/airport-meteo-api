"""A module containing DTO models for country."""


from pydantic import BaseModel, ConfigDict  # type: ignore

from airportapi.core.domain.location import Continent


class CountryDTO(BaseModel):
    """A model representing DTO for country data."""
    id: int
    name: str
    alias: str
    continent: Continent

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )
