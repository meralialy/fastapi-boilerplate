import tomllib
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


def get_pyproject_details() -> dict[str, str]:
    """
    Retrieve the project name and version from pyproject.toml.

    Returns:
        dict[str, str]: A dictionary containing 'name' and 'version'.
                        Returns defaults if the file cannot be read.
    """
    defaults = {"name": "fastapi-boilerplate", "version": "0.0.0"}
    try:
        # Resolve path to pyproject.toml relative to this file (app/configs/settings.py -> root)
        path = Path(__file__).parents[2] / "pyproject.toml"

        with path.open("rb") as f:
            pyproject_data = tomllib.load(f)["project"]

        return {
            "name": str(pyproject_data.get("name", defaults["name"])),
            "version": str(pyproject_data.get("version", defaults["version"])),
        }
    except (FileNotFoundError, tomllib.TOMLDecodeError, KeyError):
        # Return default values if file is missing or parsing fails
        return defaults


project_details = get_pyproject_details()


class Settings(BaseSettings):
    """
    Application configuration settings.

    Inherits from Pydantic's BaseSettings to handle environment variable loading
    and validation automatically.
    """

    APP_NAME: str = project_details["name"]
    APP_VERSION: str = project_details["version"]
    APP_ENV: str = "development"
    DEBUG: bool = True

    CORS_ORIGINS: list[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()
