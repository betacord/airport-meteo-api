"""A module containing country endpoints."""

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from airportapi.container import Container
from airportapi.core.domain.location import Country, CountryIn
from airportapi.infrastructure.services.icountry import ICountryService

router = APIRouter()


@router.post("/create", response_model=Country, status_code=201)
@inject
async def create_country(
    country: CountryIn,
    service: ICountryService = Depends(Provide[Container.country_service])
) -> dict:
    """An endpoint for adding new countries.

    Args:
        country (CountryIn): The country data.
        service (ICountryService, optional): The injected service dependency.

    Returns:
        dict: The new country attributes.
    """

    await service.add_country(country)

    return {**country.model_dump(), "id": 0}


@router.get("/all", response_model=list[Country], status_code=200)
@inject
async def get_all_countries(
    service: ICountryService = Depends(Provide[Container.country_service]),
) -> list:
    """An endpoint for getting all countries.

    Args:
        service (ICountryService, optional): The injected service dependency.

    Returns:
        dict: The country attributes collection.
    """

    countries = await service.get_all_countries()

    return [{**country.model_dump(), "id": 0}
            for i, country in enumerate(countries)]


@router.get("/{country_id}", response_model=Country, status_code=200)
@inject
async def get_country_by_id(
    country_id: int,
    service: ICountryService = Depends(Provide[Container.country_service]),
) -> dict:
    """An endpoint for getting country details by id.

    Args:
        country_id (int): The id of the country.
        service (ICountryService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if country does not exist.

    Returns:
        dict: The requested country attributes.
    """

    if country := await service.get_country_by_id(country_id=country_id):
        return {**country.model_dump(), "id": country_id}

    raise HTTPException(status_code=404, detail="Country not found")


@router.get(
        "/continent/{continent_id}",
        response_model=list[Country],
        status_code=200,
)
@inject
async def get_country_by_continent(
    continent_id: int,
    service: ICountryService = Depends(Provide[Container.country_service]),
) -> list:
    """An endpoint for getting countries by continent.

    Args:
        continent_id (int): The id of the continent.
        service (ICountryService, optional): The injected service dependency.

    Returns:
        dict: The requested countries.
    """

    countries = await service.get_countries_by_continent(continent_id)

    return [{**country.model_dump(), "id": 0}
            for i, country in enumerate(countries)]


@router.put("/{country_id}", response_model=Country, status_code=201)
@inject
async def update_country(
    country_id: int,
    updated_country: CountryIn,
    service: ICountryService = Depends(Provide[Container.country_service]),
) -> dict:
    """An endpoint for updating country data.

    Args:
        country_id (int): The id of the country.
        updated_country (CountryIn): The updated country details.
        service (ICountryService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if country does not exist.

    Returns:
        dict: _description_
    """

    if await service.get_country_by_id(country_id=country_id):
        await service.update_country(
            country_id=country_id,
            data=updated_country,
        )
        return {**updated_country.model_dump(), "id": country_id}

    raise HTTPException(status_code=404, detail="Country not found")


@router.delete("/{country_id}", status_code=204)
@inject
async def delete_country(
    country_id: int,
    service: ICountryService = Depends(Provide[Container.country_service]),
) -> None:
    """An endpoint for deleting countries.

    Args:
        country_id (int): The id of the country.
        service (ICountryService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if country does not exist.
    """

    if await service.get_country_by_id(country_id=country_id):
        await service.delete_country(country_id)

        return

    raise HTTPException(status_code=404, detail="Country not found")
