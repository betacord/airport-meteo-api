"""A module containing continent endpoints."""

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from airportapi.container import Container
from airportapi.core.domain.airport import Airport, AirportIn
from airportapi.infrastructure.services.iairport import IAirportService

router = APIRouter()


@router.post("/create", response_model=Airport, status_code=201)
@inject
async def create_airport(
    airport: AirportIn,
    service: IAirportService = Depends(Provide[Container.airport_service]),
) -> dict:
    """An endpoint for adding new airport.

    Args:
        airport (AirportIn): The airport data.
        service (IAirportService, optional): The injected service dependency.

    Returns:
        dict: The new airport attributes.
    """

    await service.add_airport(airport)

    return {**airport.model_dump(), "id": 0}


@router.get("/all", response_model=list[Airport], status_code=200)
@inject
async def get_all_airports(
    service: IAirportService = Depends(Provide[Container.airport_service]),
) -> list:
    """An endpoint for getting all airports.

    Args:
        service (IAirportService, optional): The injected service dependency.

    Returns:
        list: The airport attributes collection.
    """

    airports = await service.get_all()

    return [{**airport.model_dump(), "id": 0}
            for i, airport in enumerate(airports)]


@router.get(
        "/country/{country_id}",
        response_model=list[Airport],
        status_code=200,
)
@inject
async def get_airports_by_country(
    country_id: int,
    service: IAirportService = Depends(Provide[Container.airport_service]),
) -> list:
    """An endpoint for getting airports by country.

    Args:
        country_id (int): The id of the country.
        service (IAirportService, optional): The injected service dependency.

    Returns:
        list: The airport details collection.
    """

    airports = await service.get_by_country(country_id)

    return [{**airport.model_dump(), "id": 0}
            for i, airport in enumerate(airports)]


@router.get(
        "/continent/{continent_id}",
        response_model=list[Airport],
        status_code=200,
)
@inject
async def get_airports_by_continent(
    continent_id: int,
    service: IAirportService = Depends(Provide[Container.airport_service]),
) -> list:
    """An endpoint for getting airports by continent.

    Args:
        country_id (int): The id of the continent.
        service (IAirportService, optional): The injected service dependency.

    Returns:
        list: The airport details collection.
    """

    airports = await service.get_by_continent(continent_id)

    return [{**airport.model_dump(), "id": 0}
            for i, airport in enumerate(airports)]


@router.get(
        "/{airport_id}",
        response_model=Airport,
        status_code=200,
)
@inject
async def get_airport_by_id(
    airport_id: int,
    service: IAirportService = Depends(Provide[Container.airport_service]),
) -> dict | None:
    """An endpoint for getting airport by id.

    Args:
        airport_id (int): The id of the airport.
        service (IAirportService, optional): The injected service dependency.

    Returns:
        dict | None: The airport details.
    """

    if airport := await service.get_by_id(airport_id):
        return {**airport.model_dump(), "id": airport_id}

    raise HTTPException(status_code=404, detail="Airport not found")


@router.get(
        "/icao/{icao_code}",
        response_model=Airport,
        status_code=200,
)
@inject
async def get_airport_by_icao(
    icao_code: str,
    service: IAirportService = Depends(Provide[Container.airport_service]),
) -> dict | None:
    """An endpoint for getting airport by ICAO code.

    Args:
        icao_code (str): The ICAO code of the airport.
        service (IAirportService, optional): The injected service dependency.

    Returns:
        dict | None: The airport details.
    """

    if airport := await service.get_by_icao(icao_code):
        return {**airport.model_dump(), "id": 0}

    raise HTTPException(status_code=404, detail="Airport not found")


@router.get(
        "/iata/{iata_code}",
        response_model=Airport,
        status_code=200,
)
@inject
async def get_airport_by_iata(
    iata_code: str,
    service: IAirportService = Depends(Provide[Container.airport_service]),
) -> dict | None:
    """An endpoint for getting airport by IATA code.

    Args:
        iata_code (str): The IATA code of the airport.
        service (IAirportService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if airport does not exist.

    Returns:
        dict | None: The airport details.
    """

    if airport := await service.get_by_iata(iata_code):
        return {**airport.model_dump(), "id": 0}

    raise HTTPException(status_code=404, detail="Airport not found")


@router.get(
        "/user/{user_id}",
        response_model=list[Airport],
        status_code=200,
)
@inject
async def get_airports_by_user(
    user_id: int,
    service: IAirportService = Depends(Provide[Container.airport_service]),
) -> list:
    """An endpoint for getting airports by user who added them.

    Args:
        user_id (int): The id of the user.
        service (IAirportService, optional): The injected service dependency.

    Returns:
        list: The airport details collection.
    """

    airports = await service.get_by_user(user_id)

    return [{**airport.model_dump(), "id": 0}
            for i, airport in enumerate(airports)]


@router.get(
        "/location",
        response_model=list[Airport],
        status_code=200,
)
@inject
async def get_airports_by_location(
    latitude: float,
    longitude: float,
    radius: float,
    service: IAirportService = Depends(Provide[Container.airport_service]),
) -> list:
    """An endpoint for getting airports by location.

    Args:
        latitude (float): The latitude of search center point.
        longitude (float): The longitude of search center point.
        radius (float): The radius of search.
        service (IAirportService, optional): The injected service dependency.

    Returns:
        list: The airport details collection.
    """

    airports = await service.get_by_location(
        latitude=latitude,
        longitude=longitude,
        radius=radius,
    )

    return [{**airport.model_dump(), "id": 0}
            for i, airport in enumerate(airports)]


@router.put("/{airport_id}", response_model=Airport, status_code=201)
@inject
async def update_airport(
    airport_id: int,
    updated_airport: AirportIn,
    service: IAirportService = Depends(Provide[Container.airport_service]),
) -> dict:
    """An endpoint for updating airport data.

    Args:
        airport_id (int): The id of the airport.
        updated_airport (AirportIn): The updated airport details.
        service (IAirporttService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if airport does not exist.

    Returns:
        dict: The updated airport details.
    """

    if await service.get_by_id(airport_id=airport_id):
        await service.update_airport(
            airport_id=airport_id,
            data=updated_airport,
        )
        return {**updated_airport.model_dump(), "id": airport_id}

    raise HTTPException(status_code=404, detail="Airport not found")


@router.delete("/{airport_id}", status_code=204)
@inject
async def delete_airport(
    airport_id: int,
    service: IAirportService = Depends(Provide[Container.airport_service]),
) -> None:
    """An endpoint for deleting airports.

    Args:
        airport_id (int): The id of the airport.
        service (IcontinentService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if airport does not exist.
    """

    if await service.get_by_id(airport_id=airport_id):
        await service.delete_airport(airport_id)

        return

    raise HTTPException(status_code=404, detail="Airport not found")
