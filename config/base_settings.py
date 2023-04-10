# Pydantic imports
from pydantic import BaseSettings


class Settings(BaseSettings):
    """A class for application settings.

    Attributes:
        DATABASE_URL (str): A string representing the URL for connecting to the database.
        DATA_UPLOAD_MAX_MEMORY_SIZE (int): An integer representing the maximum file size during data upload.
        ALLOWED_MIME_TYPES (str): A string representing the allowed MIME types (e.g. 'image/png,image/jpeg' for images).
        ORIGINS (str): A string representing the allowed origins for CORS (e.g. 'http://localhost:8080,http://127.0.0.1:8080' for localhost).
    """

    DATABASE_URL: str
    DATA_UPLOAD_MAX_MEMORY_SIZE: int
    ALLOWED_MIME_TYPES: str
    ORIGINS: str

    class Config:
        """A class for configuration settings.

        Attributes:
            env_file (str): A string representing the path to the environment file.
        """

        env_file = "./.env"


def get_settings():
    return Settings()
