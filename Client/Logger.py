import logging
from logging.handlers import RotatingFileHandler
import os
import time

class SingletonMeta(type):
    """
    A metaclass for creating a singleton instance. This ensures that only one instance
    of the Logger class is created throughout the application lifecycle. Any subsequent
    instantiation will return the same instance, preserving the logging configuration
    and state.
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=SingletonMeta):
    """
    This logger supports conditional logging to either the console or a file. When logging
    to a file, it employs a RotatingFileHandler to manage log file sizes and perform automatic
    log file rotation, which helps in handling disk space efficiently.

    The logger can be configured to log messages with timestamps in the Apache format, making
    it suitable for various applications, including web servers and long-running applications.

    Features:
    - Singleton design pattern: Ensures a single instance of the logger throughout the application.
    - Supports console and file logging.
    - Automatic log file rotation with a configurable size limit and backup count.
    - Timestamps in Apache format for easy readability and standardization.
    - Easy to integrate and use across multiple modules or parts of an application.

    Usage:
    - Initialize once, then use throughout the application without needing to pass the logger object.
    - Automatically falls back to a default log filename based on the current timestamp if none is provided.

    Initialisation Examples:
    1. Log to console: 
        Logger().info("Starting yaR...")
    2. Log to file with a custom filename:
        Logger(log_to_file=True, filename="yar.log").info("Starting yaR...")
    3. Log to file with a default filename:
        Logger(log_to_file=True).info("Starting yaR...")
    """
    def __init__(self, log_to_file=False, filename=None):
        if not hasattr(self, 'initialized'):  # Prevents reinitialization
            self.logger = logging.getLogger(__name__)
            self.log_to_file = log_to_file
            self.filename = filename if filename is not None else self._default_filename()
            self.setup_logger()
            self.initialized = True

    def _default_filename(self):
        """
        Generates a default filename for the log file using the current timestamp.
        Format: logs/YYYY-MM-DD_HH-MM-SS.log
        """
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        default_directory = "logs"
        if not os.path.exists(default_directory):
            os.makedirs(default_directory)
        return os.path.join(default_directory, f"{timestamp}.log")

    def setup_logger(self):
        """
        Configures the logger to log to either the console or a file, with automatic
        file rotation. The log messages include timestamps in the Apache format.
        """
        if self.log_to_file:
            handler = RotatingFileHandler(self.filename, maxBytes=5000000, backupCount=5)
        else:
            handler = logging.StreamHandler()

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='[%d/%b/%Y:%H:%M:%S]')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
