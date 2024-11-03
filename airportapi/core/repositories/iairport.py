"""Module containing airport repository abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from airportapi.core.domain.airport import Airport, AirportIn


class IAirportRepository(ABC):
    """An abstract class representing protocol of continent repository."""

    @abstractmethod
    async def get_all_airports(self) -> Iterable[Airport]:
        """The abstract getting all airports from the data storage.

        Returns:
            Iterable[Airport]: Airports in the data storage.
        """

    @abstractmethod
    async def get_by_country(self, country_id: int) -> Iterable[Airport]:
        """The abstract getting airports assigned to particular country.

        Args:
            country_id (int): The id of the country.

        Returns:
            Iterable[Airport]: Airports assigned to a country.
        """

    @abstractmethod
    async def get_by_continent(self, continent_id: int) -> Iterable[Airport]:
        """The abstract getting airports assigned to particular continent.

        Args:
            continent_id (int): The id of the continent.

        Returns:
            Iterable[Airport]: Airports assigned to a continent.
        """

    @abstractmethod
    async def get_by_id(self, airport_id: int) -> Airport | None:
        """The abstract getting airport by provided id.

        Args:
            airport_id (int): The id of the airport.

        Returns:
            Airport | None: The airport details.
        """

    @abstractmethod
    async def get_by_icao(self, icao_code: str) -> Airport | None:
        """The abstract getting airport by provided ICAO code.

        Args:
            icao_code (str): The ICAO code of the airport.

        Returns:
            Airport | None: The airport details.
        """

    @abstractmethod
    async def get_by_iata(self, iata_code: str) -> Airport | None:
        """The abstract getting airport by provided IATA code.

        Args:
            icao_code (str): The IATA code of the airport.

        Returns:
            Airport | None: The airport details.
        """

    @abstractmethod
    async def get_by_user(self, user_id: int) -> Iterable[Airport]:
        """The abstract getting airports by user who added them.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[Airport]: The airport collection.
        """

    @abstractmethod
    async def get_by_location(
        self,
        latitude: float,
        longitude: float,
        radius: float,
    ) -> Iterable[Airport]:
        """The abstract getting airports by raduis of the provided location.

        Args:
            latitude (float): The geographical latitude.
            longitude (float): The geographical longitude.
            radius (float): The radius airports to search.

        Returns:
            Iterable[Airport]: The result airport collection.
        """

    @abstractmethod
    async def add_airport(self, data: AirportIn) -> None:
        """The abstract adding new airport to the data storage.

        Args:
            data (AirportIn): The details of the new airport.
        """

    @abstractmethod
    async def update_airport(
        self,
        airport_id: int,
        data: AirportIn,
    ) -> Airport | None:
        """The abstract updating airport data in the data storage.

        Args:
            airport_id (int): The id of the airport.
            data (AirportIn): The details of the updated airport.

        Returns:
            Airport | None: The updated airport details.
        """

    @abstractmethod
    async def delete_airport(self, airport_id: int) -> bool:
        """The abstract updating removing airport from the data storage.

        Args:
            airport_id (int): The id of the airport.

        Returns:
            bool: Success of the operation.
        """
