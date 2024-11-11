"""Main module of the app"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from airportapi.api.routers.airport import router as airport_router
from airportapi.api.routers.continent import router as continent_router
from airportapi.api.routers.country import router as country_router
from airportapi.container import Container
from airportapi.db import database
from airportapi.db import init_db

container = Container()
container.wire(modules=[
    "airportapi.api.routers.continent",
    "airportapi.api.routers.country",
    "airportapi.api.routers.airport",
])


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    await init_db()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(airport_router, prefix="/airport")
app.include_router(continent_router, prefix="/continent")
app.include_router(country_router, prefix="/country")


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(
    request: Request,
    exception: HTTPException,
) -> Response:
    """A function handling http exceptions for logging purposes.

    Args:
        request (Request): The incoming HTTP request.
        exception (HTTPException): A related exception.

    Returns:
        Response: The HTTP response.
    """
    return await http_exception_handler(request, exception)
