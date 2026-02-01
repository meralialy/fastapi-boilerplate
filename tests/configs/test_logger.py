import logging
import sys
from unittest.mock import patch

from app.configs.logger import LOG_FORMAT, setup_logging


def test_setup_logging_configuration():
    """Test that setup_logging configures the logger correctly."""
    with patch("logging.basicConfig") as mock_basic_config:
        logger = setup_logging()

        # Verify the returned logger name
        assert logger.name == "fastapi-boilerplate"

        # Verify basicConfig arguments
        mock_basic_config.assert_called_once()
        call_kwargs = mock_basic_config.call_args[1]

        assert call_kwargs["level"] == logging.INFO
        assert call_kwargs["format"] == LOG_FORMAT

        handlers = call_kwargs["handlers"]
        assert len(handlers) == 1
        assert isinstance(handlers[0], logging.StreamHandler)
        assert handlers[0].stream == sys.stdout
