import logging
import sys

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def setup_logging() -> logging.Logger:
    """
    Configure the logging settings for the application.

    Returns:
        logging.Logger: A configured logger instance with the application name.
    """
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout)  # Stream logs to stdout
        ],
    )

    # Explicitly set the root logger level to INFO
    logging.getLogger().setLevel(logging.INFO)

    return logging.getLogger("fastapi-boilerplate")


logger = setup_logging()
