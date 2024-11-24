"""A module containing continent endpoints."""

from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from src.infrastructure.utils import consts
from src.container import Container
from src.core.domain.airport import Airport, AirportIn, AirportBroker
from src.infrastructure.dto.airportdto import AirportDTO
from src.infrastructure.services.iairport import IAirportService

bearer_scheme = HTTPBearer()

router = APIRouter()


@router.post("/create", response_model=Airport, status_code=201)
@inject
async def create_airport(
    airport: AirportIn,
    service: IAirportService = Depends(Provide[Container.airport_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for adding new airport.

    Args:
        airport (AirportIn): The airport data.
        service (IAirportService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict: The new airport attributes.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    extended_airport_data = AirportBroker(
        user_id=user_uuid,
        **airport.model_dump(),
    )
    new_airport = await service.add_airport(extended_airport_data)

    return new_airport.model_dump() if new_airport else {}


@router.get("/all", response_model=Iterable[AirportDTO], status_code=200)
@inject
async def get_all_airports(
    service: IAirportService = Depends(Provide[Container.airport_service]),
) -> Iterable:
    """An endpoint for getting all airports.

    Args:
        service (IAirportService, optional): The injected service dependency.

    Returns:
        Iterable: The airport attributes collection.
    """

    airports = await service.get_all()

    return airports


@router.get(
        "/country/{country_id}",
        response_model=Iterable[Airport],
        status_code=200,
)
@inject
async def get_airports_by_country(
    country_id: int,
    service: IAirportService = Depends(Provide[Container.airport_service]),
) -> Iterable:
    """An endpoint for getting airports by country.

    Args:
        country_id (int): The id of the country.
        service (IAirportService, optional): The injected service dependency.

    Returns:
        Iterable: The airport details collection.
    """

    airports = await service.get_by_country(country_id)

    return airports


@router.get(
        "/continent/{continent_id}",
        response_model=Iterable[Airport],
        status_code=200,
)
@inject
async def get_airports_by_continent(
    continent_id: int,
    service: IAirportService = Depends(Provide[Container.airport_service]),
) -> Iterable:
    """An endpoint for getting airports by continent.

    Args:
        country_id (int): The id of the continent.
        service (IAirportService, optional): The injected service dependency.

    Returns:
        Iterable: The airport details collection.
    """

    airports = await service.get_by_continent(continent_id)

    return airports


@router.get(
        "/{airport_id}",
        response_model=AirportDTO,
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
        return airport.model_dump()

    raise HTTPException(status_code=404, detail="Airport not found")


@router.get(
        "/icao/{icao_code}",
        response_model=AirportDTO,
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
        return airport.model_dump()

    raise HTTPException(status_code=404, detail="Airport not found")


@router.get(
        "/iata/{iata_code}",
        response_model=AirportDTO,
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
        return airport.model_dump()

    raise HTTPException(status_code=404, detail="Airport not found")


@router.get(
        "/user/{user_id}",
        response_model=Iterable[Airport],
        status_code=200,
)
@inject
async def get_airports_by_user(
    user_id: int,
    service: IAirportService = Depends(Provide[Container.airport_service]),
) -> Iterable:
    """An endpoint for getting airports by user who added them.

    Args:
        user_id (int): The id of the user.
        service (IAirportService, optional): The injected service dependency.

    Returns:
        Iterable: The airport details collection.
    """

    airports = await service.get_by_user(user_id)

    return airports


@router.get(
        "/location",
        response_model=Iterable[Airport],
        status_code=200,
)
@inject
async def get_airports_by_location(
    latitude: float,
    longitude: float,
    radius: float,
    service: IAirportService = Depends(Provide[Container.airport_service]),
) -> Iterable:
    """An endpoint for getting airports by location.

    Args:
        latitude (float): The latitude of search center point.
        longitude (float): The longitude of search center point.
        radius (float): The radius of search.
        service (IAirportService, optional): The injected service dependency.

    Returns:
        Iterable: The airport details collection.
    """

    airports = await service.get_by_location(
        latitude=latitude,
        longitude=longitude,
        radius=radius,
    )

    return airports


@router.put("/{airport_id}", response_model=Airport, status_code=201)
@inject
async def update_airport(
    airport_id: int,
    updated_airport: AirportIn,
    service: IAirportService = Depends(Provide[Container.airport_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """An endpoint for updating airport data.

    Args:
        airport_id (int): The id of the airport.
        updated_airport (AirportIn): The updated airport details.
        service (IAirporttService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 404 if airport does not exist.

    Returns:
        dict: The updated airport details.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if airport_data := await service.get_by_id(airport_id=airport_id):
        if str(airport_data.user_id) != user_uuid:
            raise HTTPException(status_code=403, detail="Unauthorized")

        extended_updated_airport = AirportBroker(
            user_id=user_uuid,
            **updated_airport.model_dump(),
        )
        updated_airport_data = await service.update_airport(
            airport_id=airport_id,
            data=extended_updated_airport,
        )
        return updated_airport_data.model_dump() if updated_airport_data \
            else {}

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
