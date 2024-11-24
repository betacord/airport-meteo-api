"""A module containing abstract METAR service."""


from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable, Optional

from src.core.domain.meteo import MetarReport, MetarReportIn
from src.infrastructure.dto.meteostats import MeteoStatsDTO


class IMeteoService(ABC):
    """A abstract class providing the METAR service."""

    @abstractmethod
    async def add_report(self, report: MetarReportIn) -> MetarReport:
        """A service method adding a new report to the database.

        Args:
            report (MetarReportIn): The METAR report details.

        Returns:
            MetarReport: The newly added METAR report to the repository.
        """

    @abstractmethod
    async def add_text_report(self, text_report: str) -> MetarReport:
        """A service method adding a new text report to the database.

        Args:
            text_report (str): The METAR report in text form.

        Returns:
            MetarReport: The newly added METAR report to the repository.
        """

    @abstractmethod
    async def get_all_reports(self) -> Iterable[MetarReport]:
        """A service method getting all METAR reports from the repository.

        Returns:
            Iterable[MetarReport]: All METAR reports.
        """

    @abstractmethod
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

    @abstractmethod
    async def get_by_id(self, report_id: int) -> MetarReport | None:
        """A method returning METAR report by provided ID.

        Args:
            report_id (int): The ID of the report.

        Returns:
            MetarReport | None: The METAR report instance.
        """

    @abstractmethod
    async def remove_report(self, report_id: int) -> None:
        """A service method removing report by provided ID.

        Args:
            report_id (int): The ID of thr report.
        """

    @abstractmethod
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
