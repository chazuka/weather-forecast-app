from typing import Optional, Annotated

import fastapi

from app.dependencies import get_forecaster, get_geocoder
from app.models import Location
from app.service.abstractions import WeatherForecastService, GeocoderService

router = fastapi.APIRouter(prefix='/api', tags=['api'])


@router.get('/weather/{city}')
async def weather(forecaster: Annotated[WeatherForecastService, fastapi.Depends(get_forecaster)],
                  geocoder: Annotated[GeocoderService, fastapi.Depends(get_geocoder)],
                  loc: Location = fastapi.Depends()):
    """get current weather forecast for given Location
    parameters:
        - city: str, city name in url path
        - state: str, optional state name from query
        - country: str, optional 2 char country name from query
        - zip: str, optional zip code from query
        - geo.lat: float, optional latitude from query
        - geo.lon: float, optional longitude from query
    returns:
        dictionary, example:
        {
          "coord": {
            "lon": 115.2565,
            "lat": -8.6832
          },
          "weather": [
            {
              "id": 500,
              "main": "Rain",
              "description": "hujan rintik-rintik",
              "icon": "10d"
            }
          ],
          "base": "stations",
          "main": {
            "temp": 29.99,
            "feels_like": 36.99,
            "temp_min": 29.96,
            "temp_max": 29.99,
            "pressure": 1007,
            "humidity": 79
          },
          "visibility": 10000,
          "wind": {
            "speed": 2.57,
            "deg": 350
          },
          "rain": {
            "1h": 0.39
          },
          "clouds": {
            "all": 40
          },
          "dt": 1679651657,
          "sys": {
            "type": 2,
            "id": 2020640,
            "country": "ID",
            "sunrise": 1679610166,
            "sunset": 1679653683
          },
          "timezone": 28800,
          "id": 7350978,
          "name": "Banjar Taman",
          "cod": 200
        }
    """
    if loc.geo is not None:
        pass
    elif loc.zip is not None and loc.country is not None:
        loc = await geocoder.zip(loc.zip, loc.country)
    else:
        recs = await geocoder.geocode(city=loc.city, state=loc.state, country=loc.country, limit=1)
        for i in recs:
            loc = i

    result = await forecaster.weather(loc.geo)
    return fastapi.responses.JSONResponse(result)
