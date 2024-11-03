"""Module containing country repository database implementation."""

from typing import Iterable

from airportapi.core.domain.location import Country, CountryIn
from airportapi.core.repositories.icountry import ICountryRepository
from airportapi.infrastructure.repositories.db import countries


class CountryMockRepository(ICountryRepository):
    """A class implementing the mocked country repository."""

    async def get_country_by_id(self, country_id: int) -> Country | None:
        """The method getting a country from the temporary data storage.

        Args:
            country_id (int): The id of the country.

        Returns:
            Country | None: The country data if exists.
        """

        return next(
            (obj for obj in countries if obj.id == country_id),
            None,
        )

    async def get_all_countries(self) -> Iterable[Country]:
        """The abstract getting all countries from the data storage.

        Returns:
            Iterable[Country]: The collection of the all countries.
        """

        return countries

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

        return filter(lambda x: x.continent_id == continent_id, countries)

    async def add_country(self, data: CountryIn) -> None:
        """The abstract adding new country to the data storage.

        Args:
            data (CountryIn): The attributes of the country.
        """

        countries.append(data)

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

        if country_pos := \
                next(filter(lambda x: x.id == country_id, countries)):
            countries[country_pos] = data

            return Country(id=0, **data.model_dump())

        return None

    async def delete_country(self, country_id: int) -> bool:
        """The abstract updating removing country from the data storage.

        Args:
            country_id (int): The country id.
        """

        if country_pos := \
                next(filter(lambda x: x.id == country_id, countries)):
            countries.remove(country_pos)
            return True

        return False
