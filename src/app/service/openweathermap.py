from typing import Iterable, Optional

import httpx

from app.models import Geolocation, Location
from .abstractions import WeatherForecastService, GeocoderService


class OpenWeatherMapService(WeatherForecastService, GeocoderService):
    """OpenWeatherService the forecast provider integration client"""
    BASE_URL = 'https://api.openweathermap.org'

    def __init__(self, api_key: str, default_limit: int, max_limit: int) -> None:
        self.api_key: str = api_key
        self.default_limit: int = default_limit
        self.max_Limit: int = max_limit

    async def weather(self, loc: Geolocation) -> dict:
        """get the forecast report of given location"""
        url = f'{self.BASE_URL}/data/2.5/weather'
        params = {'lat': loc.lat,
                  'lon': loc.lon,
                  'appid': self.api_key,
                  'units': 'metric',
                  'lang': 'ID'}
        async with httpx.AsyncClient() as client:
            resp = await client.get(url=url, params=params)
            resp.raise_for_status()
        data = resp.json()
        return data

    async def geocode(self, city: str,
                      state: Optional[str],
                      country: Optional[str],
                      limit: Optional[int]) -> Iterable[Location]:

        if limit is None or limit < 1:
            limit = self.default_limit
        elif limit > self.max_Limit:
            limit = self.max_Limit

        queries = [city]
        for i in [state, country]:
            if i is not None:
                queries.append(i)

        query = ",".join(queries)
        url = f'{self.BASE_URL}/geo/1.0/direct'
        params = {'q': query,
                  'limit': limit,
                  'appid': self.api_key}
        async with httpx.AsyncClient() as client:
            resp = await client.get(url=url, params=params)
            resp.raise_for_status()
        data = resp.json()
        recs = []
        for i in data:
            recs.append(Location(city=i.get('name'),
                                 state=i.get('state'),
                                 country=i.get('country'),
                                 geo=Geolocation(lat=i.get('lat'),
                                                 lon=i.get('lon'))))
        return recs

    async def zip(self, code: str, country: str) -> Location:
        query = ",".join([code, country])
        url = f'{self.BASE_URL}/geo/1.0/zip'
        params = {'zip': query, 'appid': self.api_key}
        async with httpx.AsyncClient() as client:
            resp = await client.get(url=url, params=params)
            resp.raise_for_status()
        data = resp.json()
        loc = Location(city=data.get('name'),
                       zip=data.get('zip'),
                       country=data.get('country'),
                       geo=Geolocation(lat=data.get('lat'),
                                       lon=data.get('lon')))
        return loc
