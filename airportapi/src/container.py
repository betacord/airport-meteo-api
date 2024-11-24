"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from src.infrastructure.repositories.user import UserRepository
from src.infrastructure.repositories.airportdb import \
    AirportRepository
from src.infrastructure.repositories.continentdb import \
    ContinentRepository
from src.infrastructure.repositories.countrydb import \
    CountryRepository
from src.infrastructure.repositories.meteo import MeteoRepository
from src.infrastructure.services.airport import AirportService
from src.infrastructure.services.continent import ContinentService
from src.infrastructure.services.country import CountryService
from src.infrastructure.services.meteo import MeteoService
from src.infrastructure.services.user import UserService


class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""
    continent_repository = Singleton(ContinentRepository)
    country_repository = Singleton(CountryRepository)
    airport_repository = Singleton(AirportRepository)
    meteo_repository = Singleton(MeteoRepository)
    user_repository = Singleton(UserRepository)

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
    meteo_service = Factory(
        MeteoService,
        repository=meteo_repository,
    )
    user_service = Factory(
        UserService,
        repository=user_repository,
    )
