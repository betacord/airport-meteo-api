"""Module containing metar report model."""

from datetime import datetime
from typing import Optional, Self

from metar import Metar
from pydantic import BaseModel, ConfigDict


class MetarReportIn(BaseModel):
    """A model representing input METAR report."""

    icao_code: Optional[str]
    date_time: Optional[datetime]
    wind_speed: Optional[float]
    wind_direction: Optional[float]
    wind_var_from: Optional[float]
    wind_var_to: Optional[float]
    wind_gust: Optional[float]
    rvr: Optional[float]
    rvr_direction: Optional[float]
    dew_point: Optional[float]
    sky: Optional[list]
    temp: Optional[float]
    qnh: Optional[float]

    @classmethod
    def from_text_report(
        cls,
        report: str,
    ) -> Self:
        """A method preparing new METAR object based on text form.

        Args:
            report (str): Text METAR report.

        Returns:
            Self: Parsed METAR report.
        """
        obs = Metar.Metar(report)

        return cls(
            icao_code=obs.station_id,
            date_time=obs.time,
            wind_speed=obs.wind_speed.value() if obs.wind_speed else None,
            wind_direction=obs.wind_dir.value() if obs.wind_dir else None,
            wind_var_from=(
                obs.wind_dir_from.value()
                if obs.wind_dir_from else None
            ),
            wind_var_to=obs.wind_dir_to.value() if obs.wind_dir_to else None,
            wind_gust=obs.wind_gust.value() if obs.wind_gust else None,
            rvr=obs.vis.value() if obs.vis else None,
            rvr_direction=obs.vis_dir.value() if obs.vis_dir else None,
            dew_point=obs.dewpt.value() if obs.dewpt else None,
            sky=[(x[0], x[1].value() if x[1] else None) for x in obs.sky],
            temp=obs.temp.value() if obs.temp else None,
            qnh=obs.press.value() if obs.press else None,
        )


class MetarReport(MetarReportIn):
    """A model representing full metar report"""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")
