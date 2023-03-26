from typing import Optional
from pydantic import BaseModel


class Geolocation(BaseModel):
    lat: float
    lon: float


class Location(BaseModel):
    city: str
    state: Optional[str] = None
    country: str = 'ID'
    zip: Optional[str] = None
    geo: Optional[Geolocation] = None


class Report(BaseModel):
    description: str
    location: Location
