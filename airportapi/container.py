"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from airportapi.infrastructure.repositories.airportdb import \
    AirportRepository
from airportapi.infrastructure.repositories.continentdb import \
    ContinentRepository
from airportapi.infrastructure.repositories.countrydb import \
    CountryMockRepository
from airportapi.infrastructure.services.airport import AirportService
from airportapi.infrastructure.services.continent import ContinentService
from airportapi.infrastructure.services.country import CountryService


class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    continent_repository = Singleton(ContinentRepository)
    country_repository = Singleton(CountryMockRepository)
    airport_repository = Singleton(AirportRepository)

    continent_service = Factory(
        ContinentService,
        repository=continent_repository,
    )
    country_service = Factory(
        CountryService,
        repository=country_repository,
    )
    airport_service = Factory(
        AirportService,
        repository=airport_repository,
    )
