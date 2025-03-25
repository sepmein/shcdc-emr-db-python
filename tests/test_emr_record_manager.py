import pytest
from unittest.mock import patch, MagicMock
from shcdc_emr_db.db import EMRRecordManager, QueryError

def test_emr_record_manager_initialization(query_executor):
    """Test EMRRecordManager initialization."""
    manager = EMRRecordManager(query_executor)
    assert manager is not None
    assert manager.query_executor == query_executor

def test_fetch_patient_emr_records_success(emr_record_manager, sample_query_result):
    """Test successful fetching of patient EMR records."""
    emr_record_manager.query_executor.execute_query.return_value = sample_query_result
    
    result = emr_record_manager.fetch_patient_emr_records(patient_id="12345", limit=10)
    assert result == sample_query_result
    emr_record_manager.query_executor.execute_query.assert_called_once()

def test_fetch_patient_emr_records_with_date_range(emr_record_manager, sample_query_result):
    """Test fetching patient EMR records with date range."""
    emr_record_manager.query_executor.execute_query.return_value = sample_query_result
    
    result = emr_record_manager.fetch_patient_emr_records(
        patient_id="12345",
        start_date="2024-01-01",
        end_date="2024-12-31",
        limit=10
    )
    assert result == sample_query_result
    emr_record_manager.query_executor.execute_query.assert_called_once()

def test_fetch_patient_emr_records_failure(emr_record_manager):
    """Test failure in fetching patient EMR records."""
    emr_record_manager.query_executor.execute_query.side_effect = QueryError("Query failed")
    
    with pytest.raises(QueryError):
        emr_record_manager.fetch_patient_emr_records(patient_id="12345")

def test_fetch_patient_emr_records_with_empty_result(emr_record_manager):
    """Test fetching patient EMR records with empty result."""
    emr_record_manager.query_executor.execute_query.return_value = []
    
    result = emr_record_manager.fetch_patient_emr_records(patient_id="12345")
    assert result == []
    emr_record_manager.query_executor.execute_query.assert_called_once()

def test_fetch_patient_emr_records_with_invalid_params(emr_record_manager):
    """Test fetching patient EMR records with invalid parameters."""
    with pytest.raises(ValueError):
        emr_record_manager.fetch_patient_emr_records(patient_id="")
    
    with pytest.raises(ValueError):
        emr_record_manager.fetch_patient_emr_records(patient_id="12345", limit=0) 