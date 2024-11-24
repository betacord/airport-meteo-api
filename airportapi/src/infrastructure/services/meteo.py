"""A module containing implementation of METAR service."""


from datetime import datetime
from typing import Iterable, Optional

import numpy as np

from src.core.domain.meteo import MetarReport, MetarReportIn
from src.core.repositories.imeteo import IMeteoRepository
from src.infrastructure.dto.meteostats import MeteoStatsDTO
from src.infrastructure.services.imeteo import IMeteoService


class MeteoService(IMeteoService):
    """A abstract class providing the METAR service."""

    _repository: IMeteoRepository

    def __init__(self, repository: IMeteoRepository) -> None:
        """The initializer of the service class.

        Args:
            repository (IMeteoRepository): The reference to the repository.
        """

        self._repository = repository

    async def add_report(self, report: MetarReportIn) -> MetarReport:
        """A service method adding a new report to the database

        Args:
            report (MetarReportIn): The METAR report details.

        Returns:
            MetarReport: The newly added METAR report to the repository.
        """

        return await self._repository.add_report(report)

    async def add_text_report(self, text_report: str) -> MetarReport:
        """A service method adding a new text report to the database.

        Args:
            text_report (str): The METAR report in text form.

        Returns:
            MetarReport: The newly added METAR report to the repository.
        """

        return await self._repository.add_text_report(text_report)

    async def get_all_reports(self) -> Iterable[MetarReport]:
        """A service method getting all METAR reports from the repository.

        Returns:
            Iterable[MetarReport]: All METAR reports.
        """

        return await self._repository.get_all_reports()

    async def get_by_airport(
        self,
        icao_code: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Iterable[MetarReport]:
        """A method returning all METAR reports from the airport.

        Args:
            icao_code (str): The ICAO code of the airport.
            start_date (Optional[datetime], optional): Start datetime.
                Defaults to None.
            end_date (Optional[datetime], optional): End datetime.
                Defaults to None.

        Returns:
            Iterable[MetarReport]: The filtered METAR reports.
        """

        return await self._repository.get_by_airport(
            icao_code=icao_code,
            start_date=start_date,
            end_date=end_date,
        )

    async def get_by_id(self, report_id: int) -> MetarReport | None:
        """A method returning METAR report by provided ID.

        Args:
            report_id (int): The ID of the report.

        Returns:
            MetarReport | None: The METAR report instance.
        """

        return await self._repository.get_by_id(report_id)

    async def remove_report(self, report_id: int) -> None:
        """A service method removing report by provided ID.

        Args:
            report_id (int): The ID of thr report.
        """

        await self._repository.remove_report(report_id)

    async def get_stats(
        self,
        icao_code: str,
        start_date: Optional[datetime],
        end_date: Optional[datetime],
    ) -> MeteoStatsDTO:
        """The service method returning meteo stats from provided period.

        Args:
            icao_code (str): The ICAO code of the airport.
            start_date (datetime, optional): Start date of the stats.
            end_date (datetime, optional): End date of the stats.

        Returns:
            MeteoStatsDTO: The basic meteo stats.
        """

        # TODO: split into smaller methods
        reports = await self._repository.get_by_airport(
            icao_code=icao_code,
            start_date=start_date,
            end_date=end_date,
        )

        temperatures, wind_speeds, rvrs, dew_points, qnhs = [], [], [], [], []

        for report in reports:
            temperatures.append(report.temp)
            wind_speeds.append(report.wind_speed)
            rvrs.append(report.rvr)
            dew_points.append(report.dew_point)
            qnhs.append(report.qnh)

        temperatures_arr = np.array(temperatures)
        wind_speeds_arr = np.array(wind_speeds)
        rvrs_arr = np.array(rvrs)
        dew_points_arr = np.array(dew_points)
        qnhs_arr = np.array(qnhs)

        return MeteoStatsDTO(
            start_time=start_date,
            end_time=end_date,
            icao_code=icao_code,
            avg_temperature=temperatures_arr.mean(),
            min_temperature=temperatures_arr.min(),
            max_temperature=temperatures_arr.max(),
            avg_wind_speed=wind_speeds_arr.mean(),
            min_wind_speed=wind_speeds_arr.min(),
            max_wind_speed=wind_speeds_arr.max(),
            avg_rvr=rvrs_arr.mean(),
            min_rvr=rvrs_arr.min(),
            max_rvr=rvrs_arr.max(),
            avg_dew_point=dew_points_arr.mean(),
            min_dew_point=dew_points_arr.min(),
            max_dew_point=dew_points_arr.max(),
            avg_qhn=qnhs_arr.mean(),
            min_qhn=qnhs_arr.min(),
            max_qhn=qnhs_arr.max(),
        )
