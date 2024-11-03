"""Module containing country repository abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from airportapi.core.domain.location import Country, CountryIn


class ICountryRepository(ABC):
    """An abstract class representing protocol of country repository."""

    @abstractmethod
    async def get_country_by_id(self, country_id: int) -> Country | None:
        """The abstract getting a country from the data storage.

        Args:
            country_id (int): The id of the country.

        Returns:
            Country | None: The country data if exists.
        """

    @abstractmethod
    async def get_all_countries(self) -> Iterable[Country]:
        """The abstract getting all countries from the data storage.

        Returns:
            Iterable[Country]: The collection of the all countries.
        """

    @abstractmethod
    async def get_countries_by_continent(
        self,
        continent_id: int,
    ) -> Iterable[Country]:
        """The abstract getting all provided continent's countries
            from the data storage.

        Args:
            continent_id (int): The id of the continent.

        Returns:
            Iterable[Country]: The collection of the countries.
        """

    @abstractmethod
    async def add_country(self, data: CountryIn) -> None:
        """The abstract adding new country to the data storage.

        Args:
            data (CountryIn): The attributes of the country.
        """

    @abstractmethod
    async def update_country(
        self,
        country_id: int,
        data: CountryIn,
    ) -> Country | None:
        """The abstract updating country data in the data storage.

        Args:
            country_id (int): The country id.
            data (CountryIn): The attributes of the country.

        Returns:
            Country | None: The updated country.
        """

    @abstractmethod
    async def delete_country(self, country_id: int) -> bool:
        """The abstract updating removing country from the data storage.

        Args:
            country_id (int): The country id.

        Returns:
            bool: Success of the operation.
        """
