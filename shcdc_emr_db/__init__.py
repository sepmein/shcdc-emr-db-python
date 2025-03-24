"""
SHCDC EMR Database Package
A Python package for managing Electronic Medical Record (EMR) database operations.
"""

from .db import (
    DatabaseManager,
    QueryExecutor,
    EMRRecordManager,
    DatabaseError,
    ConfigError,
    QueryError,
    generate_database_metadata,
    get_db,
    run_sql_query,
    fetch_patient_emr_records,
)

__version__ = "0.1.0"
__all__ = [
    "DatabaseManager",
    "QueryExecutor",
    "EMRRecordManager",
    "DatabaseError",
    "ConfigError",
    "QueryError",
    "generate_database_metadata",
    "get_db",
    "run_sql_query",
    "fetch_patient_emr_records",
] 