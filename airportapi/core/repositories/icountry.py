"""Module containing country repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from airportapi.core.domain.location import CountryIn


class ICountryRepository(ABC):
    """An abstract class representing protocol of country repository."""

    @abstractmethod
    async def get_country_by_id(self, country_id: int) -> Any | None:
        """The abstract getting a country from the data storage.

        Args:
            country_id (int): The id of the country.

        Returns:
            Any | None: The country data if exists.
        """

    @abstractmethod
    async def get_all_countries(self) -> Iterable[Any]:
        """The abstract getting all countries from the data storage.

        Returns:
            Iterable[Any]: The collection of the all countries.
        """

    @abstractmethod
    async def get_countries_by_continent(
        self,
        continent_id: int,
    ) -> Iterable[Any]:
        """The abstract getting all provided continent's countries
            from the data storage.

        Args:
            continent_id (int): The id of the continent.

        Returns:
            Iterable[Any]: The collection of the countries.
        """

    @abstractmethod
    async def add_country(self, data: CountryIn) -> Any | None:
        """The abstract adding new country to the data storage.

        Args:
            data (CountryIn): The attributes of the country.

        Returns:
            Any | None: The newly created country.
        """

    @abstractmethod
    async def update_country(
        self,
        country_id: int,
        data: CountryIn,
    ) -> Any | None:
        """The abstract updating country data in the data storage.

        Args:
            country_id (int): The country id.
            data (CountryIn): The attributes of the country.

        Returns:
            Any | None: The updated country.
        """

    @abstractmethod
    async def delete_country(self, country_id: int) -> bool:
        """The abstract updating removing country from the data storage.

        Args:
            country_id (int): The country id.

        Returns:
            bool: Success of the operation.
        """
