"""A module providing DTO model with meteo statistics."""


from datetime import datetime
from pydantic import BaseModel, ConfigDict


class MeteoStatsDTO(BaseModel):
    """A model with meteo statistics"""

    start_time: datetime
    end_time: datetime
    icao_code: str

    avg_temperature: float
    min_temperature: float
    max_temperature: float

    avg_wind_speed: float
    min_wind_speed: float
    max_wind_speed: float

    avg_rvr: float
    min_rvr: float
    max_rvr: float

    avg_dew_point: float
    min_dew_point: float
    max_dew_point: float

    avg_qhn: float
    min_qhn: float
    max_qhn: float

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )
