"""Module containing airport-related domain models"""

from typing import Optional

from pydantic import UUID4, BaseModel, ConfigDict


class AirportIn(BaseModel):
    """Model representing airport's DTO attributes."""
    name: str
    icao_code: str
    iata_code: str
    country_id: int
    latitude: str
    longitude: str
    elevation: int
    vor_freq: Optional[str] = None
    dme_freq: Optional[str] = None
    ils_loc_freq: Optional[str] = None
    ils_gs_freq: Optional[str] = None


class AirportBroker(AirportIn):
    """A broker class including user in the model."""
    user_id: UUID4


class Airport(AirportBroker):
    """Model representing airport's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
