from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging
from enum import Enum
import json
from pathlib import Path

from utils.logging.config import LoggerConfig

class ConnectorStatus(Enum):
    """status of the data connector"""
    INITIALIZED = "initialized"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"

@dataclass
class ChunkingConfig:
    """chunking configuration for text data"""
    chunk_size: int
    overlap: int
    min_chunk_size: int = 100

    # post __init__ validation
    def __post_init__(self):
        if self.chunk_size < self.min_chunk_size:
            raise ValueError(f"chunk_size must be at least {self.min_chunk_size}")
        if self.overlap >= self.chunk_size:
            raise ValueError("overlap must be less than chunk_size")
        if self.overlap < 0:
            raise ValueError("overlap must be non-negative")

class DataConnector(ABC):
    """
    ABSTRACT BASE CLASS FOR DATA CONNECTORS (to implement and extend)
    Attributes:
        config (Dict): Configuration dictionary containing connection and processing parameters
        status (ConnectorStatus): Current status of the connector
        logger (logging.Logger): Logger instance for this connector
        chunking_config (ChunkingConfig): Configuration for text chunking
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the data connector with the provided configuration.

        Args:
            config: Dictionary containing configuration parameters including:
                - data_sources: Dict of source configurations
                - chunk_size: Size of text chunks
                - overlap: Overlap between chunks
                - logging_level: Optional logging level

        Raises:
            ValueError: If required configuration parameters are missing or invalid
        """
        self._validate_config(config)
        self.config = config
        self.status = ConnectorStatus.INITIALIZED

        # Set up logging
        logger_config = LoggerConfig(app_name=self.__class__.__name__)
        self.logger = logger_config.logger


        # Initialize chunking configuration
        self.chunking_config = ChunkingConfig(
            chunk_size=config['chunk_size'],
            overlap=config['overlap']
        )

        self.connection = None

    @abstractmethod
    def connect(self) -> bool:
        """
        Establish connection to the data source.

        Returns:
            bool: True if connection successful, False otherwise

        Raises:
            NotImplementedError: Must be implemented by concrete classes
        """
        pass

    @abstractmethod
    def fetch_data(self) -> List[Dict[str, Any]]:
        """
        Fetch data from the connected data source.

        Returns:
            List[Dict[str, Any]]: List of data items with their metadata

        Raises:
            NotImplementedError: Must be implemented by concrete classes
            ConnectionError: If not connected to data source
        """
        if self.status != ConnectorStatus.CONNECTED:
            raise ConnectionError("Not connected to data source")

    def chunking(self, text: str) -> List[str]:
        """
        Split input text into chunks according to chunking configuration.

        Args:
            text: Input text to be chunked

        Returns:
            List[str]: List of text chunks
        """
        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            # Calculate end position for current chunk
            end = min(start + self.chunking_config.chunk_size, text_length)

            # If not at text end, try to break at sentence/paragraph
            if end < text_length:
                # Look for natural break points
                break_points = [
                    text.rfind(". ", start, end),
                    text.rfind(".\n", start, end),
                    text.rfind("\n\n", start, end)
                ]

                # Use the latest valid break point
                valid_breaks = [p for p in break_points if p != -1]
                if valid_breaks:
                    end = max(valid_breaks) + 1

            # Extract chunk and add to results
            chunk = text[start:end].strip()
            if chunk:  # Only add non-empty chunks
                chunks.append(chunk)

            # Move start position for next chunk
            start = end - self.chunking_config.overlap

        return chunks

    def _validate_config(self, config: Dict[str, Any]) -> None:
        """
        Validate the provided configuration dictionary.

        Args:
            config: Configuration dictionary to validate

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        required_params = {'chunk_size', 'overlap'}
        missing_params = required_params - set(config.keys())

        if missing_params:
            raise ValueError(f"Missing required configuration parameters: {missing_params}")

        if not isinstance(config.get('data_sources'), dict):
            raise ValueError("Configuration must include 'data_sources' dictionary")

    def save_state(self, filepath: str) -> None:
        """
        Save current connector state to a file.

        Args:
            filepath: Path where state should be saved
        """
        state = {
            'status': self.status.value,
            'config': self.config,
            'chunking_config': {
                'chunk_size': self.chunking_config.chunk_size,
                'overlap': self.chunking_config.overlap
            }
        }

        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)

    @classmethod
    def load_state(cls, filepath: str) -> 'DataConnector':
        """
        Create a new connector instance from saved state.

        Args:
            filepath: Path to saved state file

        Returns:
            DataConnector: New connector instance with restored state
        """
        with open(filepath, 'r') as f:
            state = json.load(f)

        instance = cls(state['config'])
        instance.status = ConnectorStatus(state['status'])
        return instance

    #NOTE: CONTEXT MANAGER IMPLEMENTATION ::: special methods for context manager (used with 'with' statement)
    def __enter__(self):
        """Enable use of connector as context manager."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensure proper cleanup when used as context manager."""
        if self.status == ConnectorStatus.CONNECTED:
            self.disconnect()

    @abstractmethod
    def disconnect(self) -> None:
        """
        Close the connection to the data source.

        Raises:
            NotImplementedError: Must be implemented by concrete classes
        """
        pass
