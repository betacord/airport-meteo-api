"""Module containing continent database repository implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore

from airportapi.core.domain.location import Continent, ContinentIn
from airportapi.core.repositories.icontinent import IContinentRepository
from airportapi.db import continent_table, database


class ContinentRepository(IContinentRepository):
    """A class implementing the continent repository."""

    async def get_continent_by_id(self, continent_id: int) -> Any | None:
        """The method getting a continent from the data storage.

        Args:
            continent_id (int): The id of the continent.

        Returns:
            Any | None: The continent data if exists.
        """

        continent = await self._get_by_id(continent_id)

        return Continent(**dict(continent)) if continent else None

    async def get_all_continents(self) -> Iterable[Any]:
        """The method getting all continents from the data storage.

        Returns:
            Iterable[Any]: The collection of the all continents.
        """

        query = continent_table.select().order_by(continent_table.c.name.asc())
        continents = await database.fetch_all(query)

        return [Continent(**dict(continent)) for continent in continents]

    async def add_continent(self, data: ContinentIn) -> Any | None:
        """The method adding new continent to the data storage.

        Args:
            data (ContinentIn): The attributes of the continent.

        Returns:
            Any | None: The newly created continent.
        """

        query = continent_table.insert().values(**data.model_dump())
        new_continent_id = await database.execute(query)
        new_continent = await self._get_by_id(new_continent_id)

        return Continent(**dict(new_continent)) if new_continent else None

    async def update_continent(
        self,
        continent_id: int,
        data: ContinentIn,
    ) -> Any | None:
        """The method updating continent data in the data storage.

        Args:
            continent_id (int): The continent id.
            data (ContinentIn): The attributes of the continent.

        Returns:
            Any | None: The updated continent.
        """

        if self._get_by_id(continent_id):
            query = (
                continent_table.update()
                .where(continent_table.c.id == continent_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            continent = await self._get_by_id(continent_id)

            return Continent(**dict(continent)) if continent else None

        return None

    async def delete_continent(self, continent_id: int) -> bool:
        """The method updating removing continent from the data storage.

        Args:
            continent_id (int): The continent id.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(continent_id):
            query = continent_table \
                .delete() \
                .where(continent_table.c.id == continent_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, continent_id: int) -> Record | None:
        """A private method getting continent from the DB based on its ID.

        Args:
            continent_id (int): The ID of the continent.

        Returns:
            Any | None: Continent record if exists.
        """

        query = (
            continent_table.select()
            .where(continent_table.c.id == continent_id)
            .order_by(continent_table.c.name.asc())
        )

        return await database.fetch_one(query)
