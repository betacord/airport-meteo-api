"""A module containing continent endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from airportapi.container import Container
from airportapi.core.domain.location import Continent, ContinentIn
from airportapi.infrastructure.services.icontinent import IContinentService

router = APIRouter()


@router.post("/create", response_model=Continent, status_code=201)
@inject
async def create_continent(
    continent: ContinentIn,
    service: IContinentService = Depends(Provide[Container.continent_service]),
) -> dict:
    """An endpoint for adding new continent.

    Args:
        continent (ContinentIn): The continent data.
        service (IContinentService, optional): The injected service dependency.

    Returns:
        dict: The new continent attributes.
    """

    new_continent = await service.add_continent(continent)

    return new_continent.model_dump() if new_continent else {}


@router.get("/all", response_model=Iterable[Continent], status_code=200)
@inject
async def get_all_continents(
    service: IContinentService = Depends(Provide[Container.continent_service]),
) -> Iterable:
    """An endpoint for getting all continents.

    Args:
        service (IContinentService, optional): The injected service dependency.

    Returns:
        Iterable: The continent attributes collection.
    """

    continents = await service.get_all_continents()

    return continents


@router.get("/{continent_id}", response_model=Continent, status_code=200)
@inject
async def get_continent_by_id(
    continent_id: int,
    service: IContinentService = Depends(Provide[Container.continent_service]),
) -> dict:
    """An endpoint for getting continent details by id.

    Args:
        continent_id (int): The id of the continent.
        service (IcontinentService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if continent does not exist.

    Returns:
        dict: The requested continent attributes.
    """

    if continent := await service.get_continent_by_id(continent_id):
        return continent.model_dump()

    raise HTTPException(status_code=404, detail="Continent not found")


@router.put("/{continent_id}", response_model=Continent, status_code=201)
@inject
async def update_continent(
    continent_id: int,
    updated_continent: ContinentIn,
    service: IContinentService = Depends(Provide[Container.continent_service]),
) -> dict:
    """An endpoint for updating continent data.

    Args:
        continent_id (int): The id of the continent.
        updated_continent (continentIn): The updated continent details.
        service (IContinentService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if continent does not exist.

    Returns:
        dict: The updated continent details.
    """

    if await service.get_continent_by_id(continent_id=continent_id):
        new_updated_continent = await service.update_continent(
            continent_id=continent_id,
            data=updated_continent,
        )
        return new_updated_continent.model_dump() if new_updated_continent \
            else {}

    raise HTTPException(status_code=404, detail="Continent not found")


@router.delete("/{continent_id}", status_code=204)
@inject
async def delete_continent(
    continent_id: int,
    service: IContinentService = Depends(Provide[Container.continent_service]),
) -> None:
    """An endpoint for deleting continents.

    Args:
        continent_id (int): The id of the continent.
        service (IcontinentService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if continent does not exist.

    Returns:
        dict: Empty if operation finished.
    """

    if await service.get_continent_by_id(continent_id=continent_id):
        await service.delete_continent(continent_id)
        return

    raise HTTPException(status_code=404, detail="Continent not found")
