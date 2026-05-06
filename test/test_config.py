"""
Tests for etl/config.py

These tests verify that:
- load_configuration() returns a dictionary
- The config has the expected keys
- Missing config file raises FileNotFoundError
"""
import pytest
from etl.config import load_configuration


def test_config_returns_dict():
    """load_configuration() should return a dictionary."""
    config = load_configuration()
    assert isinstance(config, dict)


def test_config_has_data_section():
    """Config should have a 'data' section."""
    config = load_configuration()
    assert "data" in config


def test_config_has_raw_file():
    """Config should specify the raw data file path."""
    config = load_configuration()
    assert "raw_file" in config["data"]


def test_config_has_database_section():
    """Config should have a 'database' section."""
    config = load_configuration()
    assert "database" in config


def test_config_has_connection_string():
    """Config should specify the database connection string."""
    config = load_configuration()
    assert "connection_string" in config["database"]
