import logging
import os

import toml
from dotenv import load_dotenv, find_dotenv

# Handling API key
_ = load_dotenv(find_dotenv())


def load_config(config_file):
    """Loads the default config file from the config directory.

    Returns:
        Dict: Dictionary of key-value pairs defined in the config file, usually specific to the demo.
    """
    # Loading config file
    CONFIG_PATH = os.path.join("config", "config.toml")
    config = toml.load(config_file)
    return config


def load_logging():
    """Sets up logger for the entire application.

    Returns:
        Logger: Logger object instantiated for the application.
    """
    # Setup logging
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    return logger
