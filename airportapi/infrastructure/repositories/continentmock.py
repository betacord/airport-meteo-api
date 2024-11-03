"""Module containing continent repository implementation."""

from typing import Iterable

from airportapi.core.domain.location import Continent, ContinentIn
from airportapi.core.repositories.icontinent import IContinentRepository
from airportapi.infrastructure.repositories.db import continents


class ContinentRepository(IContinentRepository):
    """A class implementing the continent repository."""

    async def get_continent_by_id(self, continent_id: int) -> Continent | None:
        """The method getting a continent from the data storage.

        Args:
            continent_id (int): The id of the continent.

        Returns:
            continent | None: The continent data if exists.
        """

        return next(
            (obj for obj in continents if obj.id == continent_id),
            None,
        )

    async def get_all_continents(self) -> Iterable[Continent]:
        """The method getting all continents from the data storage.

        Returns:
            Iterable[Continent]: The collection of the all continents.
        """

        return continents

    async def add_continent(self, data: ContinentIn) -> None:
        """The method adding new continent to the data storage.

        Args:
            data (ContinentIn): The attributes of the continent.
        """

        continents.append(data)

    async def update_continent(
        self,
        continent_id: int,
        data: ContinentIn,
    ) -> Continent | None:
        """The method updating continent data in the data storage.

        Args:
            continent_id (int): The continent id.
            data (ContinentIn): The attributes of the continent.

        Returns:
            Continent | None: The updated continent.
        """

        if continent_pos := \
                next(filter(lambda x: x.id == continent_id, continents)):
            continents[continent_pos] = data

            return Continent(id=0, **data.model_dump())

        return None

    async def delete_continent(self, continent_id: int) -> bool:
        """The method updating removing continent from the data storage.

        Args:
            continent_id (int): The continent id.

        Returns:
            bool: Success of the operation.
        """

        if continent_pos := \
                next(filter(lambda x: x.id == continent_id, continents)):
            continents.remove(continent_pos)
            return True

        return False
