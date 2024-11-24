"""A module containing functions for periodically METAR uploading."""


import asyncio
import os

import aiohttp

API_HOST = os.getenv("API_HOST", "app")
API_PORT = os.getenv("API_PORT", "8000")
METAR_ENDPOINT = (
    "https://tgftp.nws.noaa.gov/data/observations"
    "/metar/stations/{icao_code}.TXT"
)
ALL_AIRPORTS_ENDPOINT = f"http://{API_HOST}:{API_PORT}/airport/all"
SEND_REPORT_ENDPOINT = f"http://{API_HOST}:{API_PORT}/meteo/create"


async def fetch_airports(session: aiohttp.ClientSession) -> dict:
    """A coroutine fetching airport data.

    Args:
        session (aiohttp.ClientSession): The HTTP session.

    Returns:
        dict: The airport details.
    """

    async with session.get(ALL_AIRPORTS_ENDPOINT) as response:
        response.raise_for_status()
        return await response.json()


async def fetch_metar(
        session: aiohttp.ClientSession,
        icao_code: str,
) -> str | None:
    """A coroutine for fetching METAR report from external service.

    Args:
        session (aiohttp.ClientSession): The HTTP session.
        icao_code (str): The airport's ICAO code.

    Returns:
        str | None: The METAR report if available.
    """

    try:
        async with session.get(
            METAR_ENDPOINT.format(
                icao_code=icao_code.upper(),
            ),
        ) as response:
            response.raise_for_status()
            text = await response.text()
            return text.split("\n")[1]
    except aiohttp.ClientResponseError:
        print(f"Error while getting METAR data for {icao_code}")
        return None


async def post_metar(session: aiohttp.ClientSession, metar_data: str) -> None:
    """A coroutine uploading metar report.

    Args:
        session (aiohttp.ClientSession): The HTTP session object.
        metar_data (str): The METAR report.
    """

    try:
        async with session.post(
            f"{SEND_REPORT_ENDPOINT}?report={metar_data}",
        ) as response:
            response.raise_for_status()
    except aiohttp.ClientResponseError as e:
        print(f"Error while sending METAR: {e}")


async def process_airport(
        session: aiohttp.ClientSession,
        airport: dict,
) -> None:
    """A coroutine processing airport data.

    Args:
        session (aiohttp.ClientSession): The HTTP session object.
        airport (dict): The airport data.
    """

    icao_code = airport["icao_code"]
    if not icao_code:
        print(f"Missing ICAO for airport: {airport['name']}. Skipping...")
        return

    metar_data = await fetch_metar(session, icao_code)
    if metar_data:
        await post_metar(session, metar_data)


async def main() -> None:
    """The main coroutine processing data"""
    async with aiohttp.ClientSession() as session:
        airports = await fetch_airports(session)
        tasks = [process_airport(session, airport) for airport in airports]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
