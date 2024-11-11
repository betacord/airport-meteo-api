"""A module containing DTO models for output airports."""


from typing import Optional
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict

from airportapi.core.domain.location import Continent
from airportapi.infrastructure.dto.countrydto import CountryDTO


class AirportDTO(BaseModel):
    """A model representing DTO for airport data."""
    id: int
    name: str
    icao_code: str
    iata_code: str
    country: CountryDTO
    latitude: str
    longitude: str
    elevation: int
    vor_freq: Optional[str] = None
    dme_freq: Optional[str] = None
    ils_loc_freq: Optional[str] = None
    ils_gs_freq: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "AirportDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            AirportDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),  # type: ignore
            name=record_dict.get("name"),  # type: ignore
            icao_code=record_dict.get("icao_code"),  # type: ignore
            iata_code=record_dict.get("iata_code"),  # type: ignore
            country=CountryDTO(
                id=record_dict.get("id_1"),
                name=record_dict.get("name_1"),
                alias=record_dict.get("alias"),
                continent=Continent(
                    id=record_dict.get("id_2"),  # type: ignore
                    name=record_dict.get("name_2"),  # type: ignore
                    alias=record_dict.get("alias_1"),  # type: ignore
                ),
            ),
            latitude=record_dict.get("latitude"),  # type: ignore
            longitude=record_dict.get("longitude"),  # type: ignore
            elevation=record_dict.get("elevation"),  # type: ignore
            vor_freq=record_dict.get("vor_freq"),
            dme_freq=record_dict.get("dme_freq"),
            ils_loc_freq=record_dict.get("ils_loc_freq"),
            ils_gs_freq=record_dict.get("ils_gs_freq"),
        )
