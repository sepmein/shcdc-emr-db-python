import pytest
from unittest.mock import patch, MagicMock
from shcdc_emr_db.db import DatabaseManager, DatabaseError, ConfigError

def test_database_manager_initialization(test_config):
    """Test DatabaseManager initialization with valid config."""
    with patch('configparser.ConfigParser.read') as mock_read:
        mock_read.return_value = None
        manager = DatabaseManager()
        assert manager is not None
        assert manager.config is not None

def test_database_manager_invalid_config():
    """Test DatabaseManager initialization with invalid config."""
    with patch('configparser.ConfigParser.read') as mock_read:
        mock_read.side_effect = Exception("Config file not found")
        with pytest.raises(ConfigError):
            DatabaseManager()

def test_get_connection_success(mock_db_manager):
    """Test successful database connection."""
    mock_connection = mock_db_manager.get_connection()
    assert mock_connection is not None
    mock_db_manager.get_connection.assert_called_once()

def test_get_connection_failure(mock_db_manager):
    """Test database connection failure."""
    mock_db_manager.get_connection.side_effect = Exception("Connection failed")
    with pytest.raises(DatabaseError):
        mock_db_manager.get_connection()

def test_connection_context_manager(mock_db_manager):
    """Test database connection context manager."""
    with mock_db_manager as manager:
        assert manager is not None
        mock_db_manager.get_connection.assert_called_once()
        mock_db_manager.close.assert_called_once()

def test_close_connection(mock_db_manager):
    """Test closing database connection."""
    mock_db_manager.close()
    mock_db_manager.close.assert_called_once() 