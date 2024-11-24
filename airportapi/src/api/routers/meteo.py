"""A module containing implementation of meteo API router."""

from datetime import datetime
from typing import Iterable, Optional
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from src.core.domain.meteo import MetarReport
from src.container import Container
from src.infrastructure.dto.meteostats import MeteoStatsDTO
from src.infrastructure.services.imeteo import IMeteoService

router = APIRouter()


@router.post("/create", response_model=MetarReport, status_code=201)
@inject
async def create_report(
    report: str,
    service: IMeteoService = Depends(Provide[Container.meteo_service]),
) -> dict:
    """A router method adding a new METAR report to the DB.

    Args:
        report (str): The METAR report in string form.
        service (IMeteoService, optional): A service (injected).

    Returns:
        dict: A METAR report details.
    """

    new_report = await service.add_text_report(report)

    return new_report.model_dump()


@router.get("/all", response_model=Iterable[MetarReport], status_code=200)
@inject
async def get_all_reports(
    service: IMeteoService = Depends(Provide[Container.meteo_service]),
) -> Iterable:
    """A method returning all METAR reports.

    Returns:
        Iterable: METAR reports.
    """

    return await service.get_all_reports()


@router.get("/filter", response_model=Iterable[MetarReport], status_code=200)
@inject
async def filter_reports(
    icao: Optional[str] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    service: IMeteoService = Depends(Provide[Container.meteo_service]),
) -> Iterable:
    """A router method returning filtered METAR reports.

    Args:
        icao (Optional[str], optional): The ICAO airport code.
            Defaults to None.
        start (Optional[str], optional): The start date of the filter.
            Defaults to None.
        end (Optional[str], optional): The end date of the filter.
            Defaults to None.
        service (IMeteoService, optional): The injected service instance.

    Raises:
        HTTPException: Bad request if ICAO code is not provided.

    Returns:
        Iterable: The filtered reports.
    """

    if not icao:
        raise HTTPException(status_code=400, detail="ICAO code not provided")

    start_date, end_date = None, None

    if start:
        start_date = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    if end:
        end_date = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")

    return await service.get_by_airport(
        icao_code=icao,
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/stats", response_model=MeteoStatsDTO, status_code=200)
@inject
async def get_stats(
    icao: Optional[str] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    service: IMeteoService = Depends(Provide[Container.meteo_service]),
) -> MeteoStatsDTO:
    """A router method returning meteo statistics from the airport.

    Args:
        icao (Optional[str], optional): The ICAO airport code.
            Defaults to None.
        start (Optional[str], optional): The start date of the filter.
            Defaults to None.
        end (Optional[str], optional): The end date of the filter.
            Defaults to None.
        service (IMeteoService, optional): The injected service instance.

    Raises:
        HTTPException: Bad request if ICAO code is not provided.

    Returns:
        MeteoStatsDTO: The statistics.
    """

    if not icao:
        raise HTTPException(status_code=400, detail="ICAO code not provided")

    start_date, end_date = None, None

    if start:
        start_date = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    if end:
        end_date = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")

    return await service.get_stats(
        icao_code=icao,
        start_date=start_date,
        end_date=end_date,
    )
