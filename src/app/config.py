from pydantic import BaseSettings


class Settings(BaseSettings):
    """class Settings
    contains application wide settings
    it loaded from environment variables
    recommended to manage it via .env file
    """
    SERVER_HOST: str = '127.0.0.1'
    SERVER_PORT: int = 8000

    OPENWEATHERMAP_API_KEY: str
    DEFAULT_GEOCODE_LIMIT: int = 3
    MAX_GEOCODE_LIMIT: int = 5

    class Config:
        env_file = ".env"
