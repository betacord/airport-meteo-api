"""A module providing abstract of meteo repository."""


from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Iterable, Optional

from src.core.domain.meteo import MetarReportIn


class IMeteoRepository(ABC):
    """A meteo repository class."""

    @abstractmethod
    async def get_all_reports(self) -> Iterable[Any]:
        """A method returning all meteo reports

        Returns:
            Iterable[Any]: The all meteo reports.
        """

    @abstractmethod
    async def get_by_airport(
        self,
        icao_code: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Iterable[Any]:
        """A method returning all reports from provided airport.

        Args:
            icao_code (str): _description_
            start_date (Optional[datetime], optional): Start datetime..
                Defaults to None.
            end_date (Optional[datetime], optional): End datetime..
                Defaults to None.

        Returns:
            Iterable[Any]: The filtered Metar reports.
        """

    @abstractmethod
    async def get_by_id(self, report_id: int) -> Any | None:
        """A method returning report details by its ID.

        Args:
            report_id (int): The ID of the report.

        Returns:
            Any | None: The Metar report.
        """

    @abstractmethod
    async def add_report(self, report: MetarReportIn) -> Any:
        """A method adding new METAR report to the DB.

        Args:
            report (MetarReportIn): An input METAR report.

        Returns:
            Any: The Metar report.
        """

    @abstractmethod
    async def add_text_report(self, text_report: str) -> Any:
        """A method adding new text METAR report to the DB.

        Args:
            text_report (str): An input text METAR report.

        Returns:
            Any: The Metar report.
        """

    @abstractmethod
    async def remove_report(self, report_id: int) -> None:
        """A method removing METAR report from DB.

        Args:
            report_id (int): The ID of the report.
        """
