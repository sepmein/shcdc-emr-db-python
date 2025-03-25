import pytest
from unittest.mock import patch, MagicMock
from shcdc_emr_db.db import (
    generate_database_metadata,
    get_db,
    run_sql_query,
    fetch_patient_emr_records
)

def test_generate_database_metadata(mock_db_manager):
    """Test database metadata generation."""
    mock_connection = MagicMock()
    mock_connection.execute.return_value = MagicMock()
    mock_connection.execute.return_value.fetchall.return_value = [
        {"table_name": "test_table", "column_name": "test_column"}
    ]
    
    mock_db_manager.get_connection.return_value = mock_connection
    
    metadata = generate_database_metadata()
    assert metadata is not None
    assert isinstance(metadata, dict)
    assert "test_table" in metadata
    assert "test_column" in metadata["test_table"]

def test_get_db_singleton():
    """Test database manager singleton pattern."""
    db1 = get_db()
    db2 = get_db()
    assert db1 is db2

def test_run_sql_query_success(mock_db_manager):
    """Test successful SQL query execution."""
    mock_connection = MagicMock()
    mock_connection.execute.return_value = MagicMock()
    mock_connection.execute.return_value.fetchall.return_value = [{"result": "test"}]
    
    mock_db_manager.get_connection.return_value = mock_connection
    
    result = run_sql_query("SELECT * FROM test_table")
    assert result == [{"result": "test"}]
    mock_connection.execute.assert_called_once()

def test_run_sql_query_failure(mock_db_manager):
    """Test SQL query execution failure."""
    mock_connection = MagicMock()
    mock_connection.execute.side_effect = Exception("Query failed")
    
    mock_db_manager.get_connection.return_value = mock_connection
    
    with pytest.raises(Exception):
        run_sql_query("SELECT * FROM test_table")

def test_fetch_patient_emr_records_legacy(mock_db_manager):
    """Test legacy fetch_patient_emr_records function."""
    mock_connection = MagicMock()
    mock_connection.execute.return_value = MagicMock()
    mock_connection.execute.return_value.fetchall.return_value = [
        {"patient_id": "12345", "visit_date": "2024-03-24"}
    ]
    
    mock_db_manager.get_connection.return_value = mock_connection
    
    result = fetch_patient_emr_records("12345")
    assert result is not None
    assert len(result) > 0
    assert result[0]["patient_id"] == "12345" 