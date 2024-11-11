"""Module containing airport repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join

from airportapi.core.repositories.iairport import IAirportRepository
from airportapi.core.domain.airport import Airport, AirportIn
from airportapi.db import (
    airport_table,
    continent_table,
    country_table,
    database,
)
from airportapi.infrastructure.dto.airportdto import AirportDTO


class AirportRepository(IAirportRepository):
    """A class representing continent DB repository."""

    async def get_all_airports(self) -> Iterable[Any]:
        """The method getting all airports from the data storage.

        Returns:
            Iterable[Any]: Airports in the data storage.
        """

        query = (
            select(airport_table, country_table, continent_table)
            .select_from(
                join(
                    airport_table,
                    join(
                        country_table,
                        continent_table,
                        country_table.c.continent_id == continent_table.c.id
                    ),
                    airport_table.c.country_id == country_table.c.id
                )
            )
            .order_by(airport_table.c.name.asc())
        )
        airports = await database.fetch_all(query)

        return [AirportDTO.from_record(airport) for airport in airports]

    async def get_by_country(self, country_id: int) -> Iterable[Any]:
        """The method getting airports assigned to particular country.

        Args:
            country_id (int): The id of the country.

        Returns:
            Iterable[Any]: Airports assigned to a country.
        """

        query = airport_table \
            .select() \
            .where(airport_table.c.country_id == country_id) \
            .order_by(airport_table.c.name.asc())
        airports = await database.fetch_all(query)

        return [Airport(**dict(airport)) for airport in airports]

    async def get_by_continent(self, continent_id: int) -> Iterable[Any]:
        """The method getting airports assigned to particular continent.

        Args:
            continent_id (int): The id of the continent.

        Returns:
            Iterable[Any]: Airports assigned to a continent.
        """

        query = (
            select(airport_table)
            .select_from(
                join(
                    airport_table,
                    country_table,
                    airport_table.c.country_id == country_table.c.id,
                )
            )
            .where(country_table.c.continent_id == continent_id)
            .order_by(airport_table.c.name.asc())
        )

        airports = await database.fetch_all(query)

        return [Airport(**dict(airport)) for airport in airports]

    async def get_by_id(self, airport_id: int) -> Any | None:
        """The method getting airport by provided id.

        Args:
            airport_id (int): The id of the airport.

        Returns:
            Any | None: The airport details.
        """

        query = (
            select(airport_table, country_table, continent_table)
            .select_from(
                join(
                    airport_table,
                    join(
                        country_table,
                        continent_table,
                        country_table.c.continent_id == continent_table.c.id
                    ),
                    airport_table.c.country_id == country_table.c.id
                )
            )
            .where(airport_table.c.id == airport_id)
            .order_by(airport_table.c.name.asc())
        )
        airport = await database.fetch_one(query)

        return AirportDTO.from_record(airport) if airport else None

    async def get_by_icao(self, icao_code: str) -> Any | None:
        """The method getting airport by provided ICAO code.

        Args:
            icao_code (str): The ICAO code of the airport.

        Returns:
            Any | None: The airport details.
        """

        query = (
            select(airport_table, country_table, continent_table)
            .select_from(
                join(
                    airport_table,
                    join(
                        country_table,
                        continent_table,
                        country_table.c.continent_id == continent_table.c.id
                    ),
                    airport_table.c.country_id == country_table.c.id
                )
            )
            .where(airport_table.c.icao_code == icao_code)
            .order_by(airport_table.c.name.asc())
        )
        airport = await database.fetch_one(query)

        return AirportDTO.from_record(airport) if airport else None

    async def get_by_iata(self, iata_code: str) -> Any | None:
        """The method getting airport by provided IATA code.

        Args:
            icao_code (str): The IATA code of the airport.

        Returns:
            Any | None: The airport details.
        """

        query = (
            select(airport_table, country_table, continent_table)
            .select_from(
                join(
                    airport_table,
                    join(
                        country_table,
                        continent_table,
                        country_table.c.continent_id == continent_table.c.id
                    ),
                    airport_table.c.country_id == country_table.c.id
                )
            )
            .where(airport_table.c.iata_code == iata_code)
            .order_by(airport_table.c.name.asc())
        )
        airport = await database.fetch_one(query)

        return AirportDTO.from_record(airport) if airport else None

    async def get_by_user(self, user_id: int) -> Iterable[Any]:
        """The method getting airports by user who added them.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[Any]: The airport collection.
        """

        return []

    async def get_by_location(
        self,
        latitude: float,
        longitude: float,
        radius: float,
    ) -> Iterable[Any]:
        """The method getting airports by raduis of the provided location.

        Args:
            latitude (float): The geographical latitude.
            longitude (float): The geographical longitude.
            radius (float): The radius airports to search.

        Returns:
            Iterable[Any]: The result airport collection.
        """

        return []

    async def add_airport(self, data: AirportIn) -> Any | None:
        """The method adding new airport to the data storage.

        Args:
            data (AirportIn): The details of the new airport.

        Returns:
            Airport: Full details of the newly added airport.

        Returns:
            Any | None: The newly added airport.
        """

        query = airport_table.insert().values(**data.model_dump())
        new_airport_id = await database.execute(query)
        new_airport = await self._get_by_id(new_airport_id)

        return Airport(**dict(new_airport)) if new_airport else None

    async def update_airport(
        self,
        airport_id: int,
        data: AirportIn,
    ) -> Any | None:
        """The method updating airport data in the data storage.

        Args:
            airport_id (int): The id of the airport.
            data (AirportIn): The details of the updated airport.

        Returns:
            Any | None: The updated airport details.
        """

        if self._get_by_id(airport_id):
            query = (
                airport_table.update()
                .where(airport_table.c.id == airport_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            airport = await self._get_by_id(airport_id)

            return Airport(**dict(airport)) if airport else None

        return None

    async def delete_airport(self, airport_id: int) -> bool:
        """The method updating removing airport from the data storage.

        Args:
            airport_id (int): The id of the airport.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(airport_id):
            query = airport_table \
                .delete() \
                .where(airport_table.c.id == airport_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, airport_id: int) -> Record | None:
        """A private method getting airport from the DB based on its ID.

        Args:
            airport_id (int): The ID of the airport.

        Returns:
            Any | None: Airport record if exists.
        """

        query = (
            airport_table.select()
            .where(airport_table.c.id == airport_id)
            .order_by(airport_table.c.name.asc())
        )

        return await database.fetch_one(query)
