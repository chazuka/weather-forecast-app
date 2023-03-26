import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles

import app.dependencies
from app.api.routes import router as api
from app.config import Settings
from app.service.openweathermap import OpenWeatherMapService
from app.web.routes import router as web

engine = fastapi.FastAPI()
settings = Settings()


def configure():
    configure_providers()
    configure_router()


def configure_providers():
    """configure service provider dependencies uses in this application
    includes:
        - app.dependencies.forecaster
        - app.dependencies.geocoder
    """
    open_weather_map_service = OpenWeatherMapService(
        api_key=settings.OPENWEATHERMAP_API_KEY,
        default_limit=settings.DEFAULT_GEOCODE_LIMIT,
        max_limit=settings.MAX_GEOCODE_LIMIT)
    app.dependencies.forecaster = open_weather_map_service
    app.dependencies.geocoder = open_weather_map_service


def configure_router():
    """configure all HTTP routing
    includes:
        - api request routing to api package
        - web request routed to web package
        - static asset request go to specific mounted static assets
    """
    engine.include_router(web)
    engine.include_router(api)
    engine.mount('/static', StaticFiles(directory='static'))


if __name__ == '__main__':
    configure()
    uvicorn.run(engine, port=settings.SERVER_PORT, host=settings.SERVER_HOST)
else:
    configure()
