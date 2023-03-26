from abc import ABC, abstractmethod
from typing import Optional, Iterable

from app.models import Geolocation, Location


class WeatherForecastService(ABC):

    @abstractmethod
    async def weather(self, loc: Geolocation) -> dict:
        pass


class GeocoderService(ABC):

    @abstractmethod
    async def zip(self, code: str, country: str) -> Location:
        pass

    @abstractmethod
    async def geocode(self, city: str,
                      state: Optional[str],
                      country: Optional[str],
                      limit: Optional[int]) -> Iterable[Location]:
        pass
