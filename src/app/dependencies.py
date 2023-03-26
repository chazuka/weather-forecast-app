from .service.abstractions import WeatherForecastService, GeocoderService

forecaster: WeatherForecastService
geocoder: GeocoderService


def get_forecaster() -> WeatherForecastService:
    """singleton dependency injector for any process/route
    which required the implementation instance of `WeatherForecastService`.
    """
    return forecaster


def get_geocoder() -> GeocoderService:
    """singleton dependency injector for any process/route
    which required the implementation instance of `GeocoderService`.
    """
    return geocoder


