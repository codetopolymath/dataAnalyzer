"""
Enterprise Data Analyzer - Logging Configuration
---------------------------------------------

This module provides a centralized logging configuration for the Enterprise Data Analyzer.
It implements structured logging with consistent formatting across all components.
"""

import logging
import logging.handlers
import json
import os
from datetime import datetime
from functools import wraps
from typing import Optional, Dict, Any


class LoggerConfig:
    def __init__(
        self,
        app_name: str,
        log_level: int = logging.INFO,
        log_dir: str = "logs",
        max_bytes: int = 10485760,  # 10MB
        backup_count: int = 5,
    ):
        """
        Initialize logging configuration for a component.

        Args:
            app_name: Name of the component (e.g., 'DataConnector', 'QueryProcessor')
            log_level: Logging level (default: logging.INFO)
            log_dir: Directory to store log files
            max_bytes: Maximum size of each log file before rotation
            backup_count: Number of backup files to keep
        """
        self.app_name = app_name
        self.log_level = log_level
        self.log_dir = log_dir
        self.max_bytes = max_bytes
        self.backup_count = backup_count

        # Create logs directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)

        # Set up logger
        self.logger = self._configure_logger()

    def _configure_logger(self) -> logging.Logger:
        """Configure and return a logger with file and console handlers."""
        logger = logging.getLogger(self.app_name)
        logger.setLevel(self.log_level)

        # Prevent adding handlers multiple times
        if not logger.handlers:
            # File handler with rotation
            log_file = os.path.join(self.log_dir, f"{self.app_name}.log")
            file_handler = logging.handlers.RotatingFileHandler(
                log_file, maxBytes=self.max_bytes, backupCount=self.backup_count
            )

            # Console handler
            console_handler = logging.StreamHandler()

            # Create formatter
            formatter = logging.Formatter(
                "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

            # Add formatter to handlers
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            # Add handlers to logger
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        return logger


def log_operation(logger: logging.Logger):
    """
    Decorator for logging function entry and exit with parameters and results.

    Usage:
        @log_operation(logger)
        def my_function(arg1, arg2):
            pass
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            # Log function entry
            logger.debug(f"Entering {func_name} - Args: {args}, Kwargs: {kwargs}")

            try:
                result = func(*args, **kwargs)
                # Log successful execution
                logger.debug(f"Exiting {func_name} - Result: {result}")
                return result
            except Exception as e:
                # Log error
                logger.error(f"Error in {func_name}: {str(e)}", exc_info=True)
                raise

        return wrapper

    return decorator


# # Example implementation for DataConnector
# class DataConnectorLogger:
#     def __init__(self):
#         config = LoggerConfig("DataConnector")
#         self.logger = config.logger

#     @log_operation(logger)
#     def connect(self, connection_params: Dict[str, Any]):
#         self.logger.info(f"Establishing connection with params: {connection_params}")
#         # Connection logic here

#     @log_operation(logger)
#     def fetch_data(self, query: str):
#         self.logger.info(f"Fetching data with query: {query}")
#         # Data fetching logic here

# # Example implementation for QueryProcessor
# class QueryProcessorLogger:
#     def __init__(self):
#         config = LoggerConfig("QueryProcessor")
#         self.logger = config.logger

#     @log_operation(logger)
#     def process_query(self, query: str):
#         self.logger.info(f"Processing query: {query}")
#         # Query processing logic here

# # Example implementation for VectorProcessor
# class VectorProcessorLogger:
#     def __init__(self):
#         config = LoggerConfig("VectorProcessor")
#         self.logger = config.logger

#     @log_operation(logger)
#     def process_document(self, document_id: str):
#         self.logger.info(f"Processing document: {document_id}")
#         # Vector processing logic here
