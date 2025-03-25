import pytest
import os
from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from shcdc_emr_db.db import DatabaseManager, QueryExecutor, EMRRecordManager

@pytest.fixture
def test_config():
    """Create a test configuration."""
    config = ConfigParser()
    config['postgresql'] = {
        'host': 'localhost',
        'port': '5432',
        'database': 'test_db',
        'user': 'test_user',
        'password': 'test_password'
    }
    return config

@pytest.fixture
def mock_db_manager(mocker):
    """Create a mocked database manager."""
    mock_manager = mocker.Mock(spec=DatabaseManager)
    mock_manager.get_connection.return_value = mocker.Mock()
    return mock_manager

@pytest.fixture
def query_executor(mock_db_manager):
    """Create a query executor with mocked database manager."""
    return QueryExecutor(mock_db_manager)

@pytest.fixture
def emr_record_manager(query_executor):
    """Create an EMR record manager with mocked query executor."""
    return EMRRecordManager(query_executor)

@pytest.fixture
def sample_patient_data():
    """Sample patient data for testing."""
    return {
        "patient_id": "12345",
        "visit_id": "V001",
        "visit_date": "2024-03-24",
        "diagnosis": "Test Diagnosis",
        "treatment": "Test Treatment"
    }

@pytest.fixture
def sample_query_result():
    """Sample query result for testing."""
    return [
        {
            "patient_id": "12345",
            "visit_id": "V001",
            "visit_date": "2024-03-24",
            "diagnosis": "Test Diagnosis",
            "treatment": "Test Treatment"
        }
    ] 