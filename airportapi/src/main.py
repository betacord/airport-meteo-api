"""Main module of the app"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from src.api.routers.airport import router as airport_router
from src.api.routers.continent import router as continent_router
from src.api.routers.country import router as country_router
from src.api.routers.meteo import router as meteo_router
from src.api.routers.user import router as user_router
from src.container import Container
from src.db import database, init_db

container = Container()
container.wire(modules=[
    "src.api.routers.continent",
    "src.api.routers.country",
    "src.api.routers.airport",
    "src.api.routers.meteo",
    "src.api.routers.user",
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
app.include_router(meteo_router, prefix="/meteo")
app.include_router(user_router, prefix="")


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
