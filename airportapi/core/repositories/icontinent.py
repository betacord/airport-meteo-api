"""Module containing contient repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from airportapi.core.domain.location import ContinentIn


class IContinentRepository(ABC):
    """An abstract class representing protocol of continent repository."""

    @abstractmethod
    async def get_continent_by_id(self, continent_id: int) -> Any | None:
        """The abstract getting a continent from the data storage.

        Args:
            continent_id (int): The id of the continent.

        Returns:
            Any | None: The continent data if exists.
        """

    @abstractmethod
    async def get_all_continents(self) -> Iterable[Any]:
        """The abstract getting all continents from the data storage.

        Returns:
            Iterable[Any]: The collection of the all continents.
        """

    @abstractmethod
    async def add_continent(self, data: ContinentIn) -> Any | None:
        """The abstract adding new continent to the data storage.

        Args:
            data (ContinentIn): The attributes of the continent.

        Returns:
            Any | None: The newly created continent.
        """

    @abstractmethod
    async def update_continent(
        self,
        continent_id: int,
        data: ContinentIn,
    ) -> Any | None:
        """The abstract updating continent data in the data storage.

        Args:
            continent_id (int): The continent id.
            data (ContinentIn): The attributes of the continent.

        Returns:
            Any | None: The updated continent.
        """

    @abstractmethod
    async def delete_continent(self, continent_id: int) -> bool:
        """The abstract updating removing continent from the data storage.

        Args:
            continent_id (int): The continent id.

        Returns:
            bool: Success of the operation.
        """
