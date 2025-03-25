import pytest
from unittest.mock import patch, MagicMock
from shcdc_emr_db.db import QueryExecutor, QueryError

def test_query_executor_initialization(mock_db_manager):
    """Test QueryExecutor initialization."""
    executor = QueryExecutor(mock_db_manager)
    assert executor is not None
    assert executor.db_manager == mock_db_manager

def test_execute_query_success(query_executor, sample_query_result):
    """Test successful query execution."""
    mock_connection = MagicMock()
    mock_connection.execute.return_value = MagicMock()
    mock_connection.execute.return_value.fetchall.return_value = sample_query_result
    
    query_executor.db_manager.get_connection.return_value = mock_connection
    
    result = query_executor.execute_query("SELECT * FROM test_table")
    assert result == sample_query_result
    mock_connection.execute.assert_called_once()

def test_execute_query_with_params(query_executor, sample_query_result):
    """Test query execution with parameters."""
    mock_connection = MagicMock()
    mock_connection.execute.return_value = MagicMock()
    mock_connection.execute.return_value.fetchall.return_value = sample_query_result
    
    query_executor.db_manager.get_connection.return_value = mock_connection
    
    params = {"param1": "value1"}
    result = query_executor.execute_query("SELECT * FROM test_table WHERE col = :param1", params)
    assert result == sample_query_result
    mock_connection.execute.assert_called_once()

def test_execute_query_failure(query_executor):
    """Test query execution failure."""
    mock_connection = MagicMock()
    mock_connection.execute.side_effect = Exception("Query failed")
    
    query_executor.db_manager.get_connection.return_value = mock_connection
    
    with pytest.raises(QueryError):
        query_executor.execute_query("SELECT * FROM test_table")

def test_execute_query_with_transaction(query_executor, sample_query_result):
    """Test query execution within transaction."""
    mock_connection = MagicMock()
    mock_connection.execute.return_value = MagicMock()
    mock_connection.execute.return_value.fetchall.return_value = sample_query_result
    
    query_executor.db_manager.get_connection.return_value = mock_connection
    
    with query_executor.transaction():
        result = query_executor.execute_query("SELECT * FROM test_table")
        assert result == sample_query_result
    
    mock_connection.begin.assert_called_once()
    mock_connection.commit.assert_called_once() 