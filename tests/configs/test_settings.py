import os
from unittest.mock import mock_open, patch

from app.configs.settings import Settings, get_pyproject_details


def test_get_pyproject_details_parsing():
    """Test that project details are correctly parsed from a TOML file."""
    toml_data = b'[project]\nname = "parsed-name"\nversion = "2.0.0"\n'

    # Patch pathlib.Path.open to return our mock TOML data
    with patch("pathlib.Path.open", mock_open(read_data=toml_data)):
        details = get_pyproject_details()
        assert details["name"] == "parsed-name"
        assert details["version"] == "2.0.0"


def test_get_pyproject_details_defaults():
    """Test that default values are returned when the file cannot be read."""
    with patch("pathlib.Path.open", side_effect=FileNotFoundError):
        details = get_pyproject_details()
        assert details["name"] == "fastapi-boilerplate"
        assert details["version"] == "0.0.0"


def test_settings_env_overrides():
    """Test that environment variables override default settings."""
    # Use patch.dict to safely modify os.environ for this test only
    with patch.dict(os.environ, {"APP_ENV": "production", "DEBUG": "false"}):
        settings = Settings()
        assert settings.APP_ENV == "production"
        assert settings.DEBUG is False
