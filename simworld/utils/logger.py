"""Logger utility module for logging messages with configurable logging levels and handlers."""
import logging
import os
from datetime import datetime


class Logger:
    """Singleton logger class for the simulation application.

    This class provides a centralized logging mechanism with configurable options
    for enabling/disabling logging and console output.
    """
    _instance = None
    _initialized = False
    _logging_enabled = True
    _log_to_console = True
    _log_to_file = False

    @classmethod
    def configure(cls, logging_enabled=True, log_to_console=True, log_to_file=False):
        """Configure global logging settings.

        Args:
            logging_enabled: Whether logging is enabled globally.
            log_to_console: Whether to output logs to console.
            log_to_file: Whether to output logs to file.
        """
        cls._logging_enabled = logging_enabled
        cls._log_to_console = log_to_console
        cls._log_to_file = log_to_file

    def __new__(cls):
        """Create or return the singleton instance of Logger.

        Returns:
            The singleton Logger instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, _logging_enabled=True, _log_to_console=True, _log_to_file=False):
        """Initialize the logger if not already initialized.

        This method sets up file and console handlers based on configuration.
        A log file is created with timestamp in the filename.
        """
        if not Logger._initialized:
            Logger.configure(logging_enabled=_logging_enabled, log_to_console=_log_to_console, log_to_file=_log_to_file)
            # Only initialize logger if logging is enabled in config
            if Logger._logging_enabled:
                # configure root logger
                self.logger = logging.getLogger('SimWorld')
                self.logger.setLevel(logging.DEBUG)

                # file handler - only add if enabled in config
                if Logger._log_to_file:
                    # create logs directory
                    if not os.path.exists('logs'):
                        os.makedirs('logs')

                    # generate log file name, include timestamp
                    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
                    log_filename = f'logs/simworld_{current_time}.log'

                    file_handler = logging.FileHandler(log_filename)
                    file_handler.setLevel(logging.DEBUG)
                    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                    file_handler.setFormatter(formatter)
                    self.logger.addHandler(file_handler)

                # console handler - only add if enabled in config
                if Logger._log_to_console:
                    console_handler = logging.StreamHandler()
                    console_handler.setLevel(logging.INFO)
                    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                    console_handler.setFormatter(formatter)
                    self.logger.addHandler(console_handler)
            else:
                # Create a null logger when logging is disabled
                self.logger = logging.getLogger('SimWorld')
                self.logger.addHandler(logging.NullHandler())

            Logger._initialized = True

    @staticmethod
    def get_logger(name=None):
        """Get a logger instance, optionally as a child logger with the specified name.

        Args:
            name: Optional name for child logger.

        Returns:
            A configured logger instance.
        """
        logger_instance = Logger()
        if name:
            child_logger = logging.getLogger(f'SimWorld.{name}')
            if not Logger._logging_enabled:
                child_logger.handlers = []
                child_logger.addHandler(logging.NullHandler())
                child_logger.propagate = False
            return child_logger
        return logger_instance.logger
