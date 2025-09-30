import datetime
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

import streamlit as st


class LoggerManager:
    """A Logger Manager that encapsulates the logic for logging messages
    both to the console and optionally to a file.

    Attributes:
        _logger (Logger): The internal logger object.
        formatter (Formatter): The logging formatter.
        log_out_on (bool): Flag to determine if logging to file is enabled.
        log_out_dir (str): Directory path for log files.
    """

    def __init__(
            self,
            name: str,
            log_out_on: bool,
            log_out_dir: str = None,
            level=logging.DEBUG,
            fmt="%(asctime)s - [%(filename)s:%(lineno)d] - %(levelname)s - %(message)s",
    ):
        """Initialize a LoggerManager instance.

        Args:
            name (str): Name of the logger.
            log_out_on (bool): Whether to enable file logging.
            log_out_dir (str, optional): Directory for the log files. Defaults to the current working directory.
            level (int, optional): Logging level. Defaults to logging.DEBUG.
            fmt (str, optional): Logging format string. Defaults to '%(asctime)s - %(name)s - %(levelname)s - %(message)s'.
        """
        self._logger = logging.getLogger(name)
        self._logger.propagate = False
        self.formatter = logging.Formatter(fmt)
        self._logger.setLevel(level)
        self.log_out_on = log_out_on
        self.log_out_dir = log_out_dir if log_out_dir else os.getcwd()
        self._initialize_logging()

    def _initialize_logging(self):
        """Set up the logger by adding the necessary handlers.

        Raises:
            Exception: Raised if there is an error initializing the logger
        """
        try:
            base_path = self._get_base_log_path()
            log_folder_path = base_path / "logs"
            log_folder_path.mkdir(parents=True, exist_ok=True)

            date_str = datetime.datetime.now().strftime("%Y%m%d")
            info_path = log_folder_path / f"log_info_{date_str}.txt"

            # Check if StreamHandler is already added
            if not any(
                    isinstance(handler, logging.StreamHandler)
                    for handler in self._logger.handlers
            ):
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(self.formatter)
                self._logger.addHandler(console_handler)

            # Add filehandler

            if not any(
                    isinstance(handler, logging.FileHandler)
                    for handler in self._logger.handlers
            ):
                info_handler = RotatingFileHandler(
                    info_path, maxBytes=5 * 1024 * 1024, backupCount=5
                )

                info_handler.setFormatter(self.formatter)
                self._logger.addHandler(info_handler)

        except Exception as e:
            raise LoggingInitError(f"Error initializing logging {e}")

    def _get_base_log_path(self) -> Path:
        """Get the base directory path for logging.

        Returns:
            Path: The base directory path as a pathlib.Path object.
        """
        return Path(self.log_out_dir) if self.log_out_on else Path(os.getcwd())

    def get_logger(self):
        """Retrieve the internal logger instance.

        Returns:
            Logger: The internal logger object.
        """
        return self._logger

    def log(self, level, message):
        """Log a message with the given logging level.

        Args:
            level (str): The logging level ('debug', 'info', 'warning', 'error', etc.).
            message (str): The message to be logged.
        """
        log_func = getattr(self._logger, level.lower())
        if log_func:
            log_func(message)


def init_logger(name: str, config: dict):
    """Retrieve the logger from the session state or initialize a new one.

    Args:
        name (str): Name of the logger.
        config (dict): Configuration dictionary containing logging settings.

    Returns:
        Logger: The logger object.
    """
    if 'logger' not in st.session_state:
        logger_manager = LoggerManager(name,
                                       log_out_on=config["LOCAL"]["LOG_OUT_ON"],
                                       log_out_dir=config["LOCAL"]["LOG_OUT_DIR"])
        st.session_state['logger'] = logger_manager.get_logger()
    return st.session_state['logger']


class LoggingInitError(Exception):
    """Exception raised for errors during logging initialization.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Error during logging initialization"):
        """Initializes class to handle logging initialization errors

        Args:
            message (str, optional): Friendlier description of logging init error. Defaults to "Error during logging initialization".
        """
        self.message = message
        super().__init__(self.message)
