"""A module providing database access."""

import asyncio

import databases
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.mutable import MutableList
from asyncpg.exceptions import (    # type: ignore
    CannotConnectNowError,
    ConnectionDoesNotExistError,
)

from src.config import config

metadata = sqlalchemy.MetaData()

continent_table = sqlalchemy.Table(
    "continents",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("alias", sqlalchemy.String),
)

country_table = sqlalchemy.Table(
    "countries",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("alias", sqlalchemy.String),
    sqlalchemy.Column(
        "continent_id",
        sqlalchemy.ForeignKey("continents.id"),
        nullable=False,
    ),
)

airport_table = sqlalchemy.Table(
    "airports",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("icao_code", sqlalchemy.String),
    sqlalchemy.Column("iata_code", sqlalchemy.String),
    sqlalchemy.Column(
        "country_id",
        sqlalchemy.ForeignKey("countries.id"),
        nullable=False,
    ),
    sqlalchemy.Column("latitude", sqlalchemy.String),
    sqlalchemy.Column("longitude", sqlalchemy.String),
    sqlalchemy.Column("elevation", sqlalchemy.Integer),
    sqlalchemy.Column("vor_freq", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("dme_freq", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("ils_loc_freq", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("ils_gs_freq", sqlalchemy.String, nullable=True),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.ForeignKey("users.id"),
        nullable=False,
    ),
)

metar_table = sqlalchemy.Table(
    "metars",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("icao_code", sqlalchemy.String),
    sqlalchemy.Column("date_time", sqlalchemy.DateTime, nullable=True),
    sqlalchemy.Column("wind_speed", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("wind_direction", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("wind_var_from", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("wind_var_to", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("wind_gust", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("rvr", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("rvr_direction", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("dew_point", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column(
        "sky",
        MutableList.as_mutable(sqlalchemy.PickleType),  # type: ignore
        nullable=True,
        default=[],
    ),
    sqlalchemy.Column("temp", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("qnh", sqlalchemy.Float, nullable=True),
)

user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sqlalchemy.text("gen_random_uuid()"),
    ),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
)

db_uri = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}/{config.DB_NAME}"
)

engine = create_async_engine(
    db_uri,
    echo=True,
    future=True,
    pool_pre_ping=True,
)

database = databases.Database(
    db_uri,
    force_rollback=True,
)


async def init_db(retries: int = 5, delay: int = 5) -> None:
    """Function initializing the DB.

    Args:
        retries (int, optional): Number of retries of connect to DB.
            Defaults to 5.
        delay (int, optional): Delay of connect do DB. Defaults to 2.
    """
    for attempt in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(metadata.create_all)
            return
        except (
            OperationalError,
            DatabaseError,
            CannotConnectNowError,
            ConnectionDoesNotExistError,
        ) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay)

    raise ConnectionError("Could not connect to DB after several retries.")
