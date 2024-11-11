"""Module containing country repository database implementation."""

from typing import Any, Iterable

from asyncpg import Record  # type: ignore

from airportapi.core.domain.location import Country, CountryIn
from airportapi.core.repositories.icountry import ICountryRepository
from airportapi.db import country_table, database


class CountryMockRepository(ICountryRepository):
    """A class implementing the database country repository."""

    async def get_country_by_id(self, country_id: int) -> Any | None:
        """The method getting a country from the temporary data storage.

        Args:
            country_id (int): The id of the country.

        Returns:
            Any | None: The country data if exists.
        """

        country = await self._get_by_id(country_id)

        return Country(**dict(country)) if country else None

    async def get_all_countries(self) -> Iterable[Any]:
        """The abstract getting all countries from the data storage.

        Returns:
            Iterable[Any]: The collection of the all countries.
        """

        query = country_table.select().order_by(country_table.c.name.asc())
        countries = await database.fetch_all(query)

        return [Country(**dict(country)) for country in countries]

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

        query = country_table \
            .select() \
            .where(country_table.c.continent_id == continent_id) \
            .order_by(country_table.c.name.asc())
        countries = await database.fetch_all(query)

        return [Country(**dict(country)) for country in countries]

    async def add_country(self, data: CountryIn) -> Any | None:
        """The abstract adding new country to the data storage.

        Args:
            data (CountryIn): The attributes of the country.

        Returns:
            Any | None: The newly created country.
        """

        query = country_table.insert().values(**data.model_dump())
        new_country_id = await database.execute(query)
        new_country = await self._get_by_id(new_country_id)

        return Country(**dict(new_country)) if new_country else None

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

        if self._get_by_id(country_id):
            query = (
                country_table.update()
                .where(country_table.c.id == country_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            country = await self._get_by_id(country_id)

            return Country(**dict(country)) if country else None

        return None

    async def delete_country(self, country_id: int) -> bool:
        """The abstract updating removing country from the data storage.

        Args:
            country_id (int): The country id.
        """

        if self._get_by_id(country_id):
            query = country_table \
                .delete() \
                .where(country_table.c.id == country_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, country_id: int) -> Record | None:
        """A private method getting country from the DB based on its ID.

        Args:
            country_id (int): The ID of the country.

        Returns:
            Any | None: Country record if exists.
        """

        query = (
            country_table.select()
            .where(country_table.c.id == country_id)
            .order_by(country_table.c.name.asc())
        )

        return await database.fetch_one(query)
