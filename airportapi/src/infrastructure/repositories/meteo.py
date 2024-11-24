"""A module providing implementation of meteo repository."""


from datetime import datetime
import pickle
from typing import Any, Iterable, Optional

from asyncpg import Record  # type: ignore
import sqlalchemy

from src.core.domain.meteo import MetarReport, MetarReportIn
from src.core.repositories.imeteo import IMeteoRepository
from src.db import database, metar_table


class MeteoRepository(IMeteoRepository):
    """A meteo repository class."""

    async def get_all_reports(self) -> Iterable[Any]:
        """A method returning all meteo reports

        Returns:
            Iterable[Any]: The all meteo reports.
        """

        query = metar_table.select().order_by(metar_table.c.id.asc())
        reports = await database.fetch_all(query)

        return [MetarReport(**self._map_report(report)) for report in reports]

    async def get_by_airport(
        self,
        icao_code: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Iterable[Any]:
        """A method returning all reports from provided airport.

        Args:
            icao_code (str): _description_
            start_date (Optional[datetime], optional): _description_.
                Defaults to None.
            end_date (Optional[datetime], optional): _description_.
                Defaults to None.

        Returns:
            Iterable[Any]: The filtered Metar reports.
        """

        query_conditions = [metar_table.c.icao_code == icao_code]
        if start_date:
            query_conditions.append(metar_table.c.date_time >= start_date)
        if end_date:
            query_conditions.append(metar_table.c.date_time <= end_date)

        query = metar_table \
            .select() \
            .where(sqlalchemy.and_(*query_conditions)) \
            .order_by(metar_table.c.date_time.asc())
        reports = await database.fetch_all(query)

        return [MetarReport(**self._map_report(report)) for report in reports]

    async def get_by_id(self, report_id: int) -> Any | None:
        """A method returning report details by its ID.

        Args:
            report_id (int): The ID of the report.

        Returns:
            Any | None: The Metar report.
        """

        query = metar_table \
            .select() \
            .where(metar_table.c.id == report_id) \
            .order_by(metar_table.c.id.asc())
        report = await database.fetch_one(query)
        report_dict = self._map_report(report)

        return MetarReport(**report_dict) if report else None

    async def add_report(self, report: MetarReportIn) -> Any:
        """A method adding new METAR report to the DB.

        Args:
            report (MetarReportIn): An input METAR report.

        Returns:
            Any: The Metar report.
        """

        query = metar_table.insert().values(**report.model_dump())
        new_airport_id = await database.execute(query)
        new_airport = await self.get_by_id(new_airport_id)

        return new_airport

    async def add_text_report(self, text_report: str) -> Any:
        """A method adding new text METAR report to the DB.

        Args:
            text_report (str): An input text METAR report.

        Returns:
            Any: The Metar report.
        """

        report_object = MetarReportIn.from_text_report(text_report)
        query = metar_table.insert().values(**report_object.model_dump())
        new_report_id = await database.execute(query)
        new_report = await self.get_by_id(new_report_id)

        return MetarReport(**dict(new_report)) \
            if new_report else None

    async def remove_report(self, report_id: int) -> None:
        """A method removing METAR report from DB.

        Args:
            report_id (int): The ID of the report.
        """

        if self.get_by_id(report_id):
            query = metar_table \
                .delete() \
                .where(metar_table.c.id == report_id)
            await database.execute(query)

    def _map_report(self, report: Record | None) -> dict | None:
        """A mapper method returning unpickled sky list.

        Args:
            report (Record | None): The METAR report record.

        Returns:
            dict | None: The mapped METAR record in dict form.
        """

        if not report:
            return None

        report_dict = dict(report)
        report_dict["sky"] = pickle.loads(report_dict["sky"])

        return report_dict
