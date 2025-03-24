"""
Database utility functions for connecting to and querying PostgreSQL.
Provides a unified interface for database operations with proper connection management.
"""

from configparser import ConfigParser, NoSectionError
import json
from typing import Literal, List, Dict, Any, Optional, Union, TypeVar, cast
from contextlib import contextmanager

from sqlalchemy import text, exc as sa_exc, create_engine, Engine
from sqlalchemy.engine.row import Row
from langchain_community.utilities import SQLDatabase

T = TypeVar('T', bound=Dict[str, Any])

class DatabaseError(Exception):
    """Base class for database errors"""
    pass

class ConfigError(DatabaseError):
    """Configuration related errors"""
    pass

class QueryError(DatabaseError):
    """Query execution related errors"""
    pass

class DatabaseManager:
    """Manages database connections and provides unified interface for database operations"""
    
    def __init__(self, config_file: str = "config/database.ini", section: str = "postgresql"):
        self._config_file = config_file
        self._section = section
        self._config = None
        self._engine = None
        self._sqlalchemy_db = None

    @property
    def config(self) -> Dict[str, str]:
        """Lazy load and cache database configuration"""
        if not self._config:
            self._config = self._load_config()
        return self._config

    @property
    def engine(self) -> Engine:
        """Lazy load and cache SQLAlchemy engine"""
        if not self._engine:
            self._engine = self._create_engine()
        return self._engine

    @property
    def sqlalchemy_db(self) -> SQLDatabase:
        """Lazy load and cache SQLDatabase instance"""
        if not self._sqlalchemy_db:
            self._sqlalchemy_db = self._create_sqlalchemy_db()
        return self._sqlalchemy_db

    def _load_config(self) -> Dict[str, str]:
        """Read database configuration from the specified INI file"""
        parser = ConfigParser()
        parser.read(self._config_file)

        if not parser.has_section(self._section):
            raise ConfigError(f"Section {self._section} not found in {self._config_file}")

        return dict(parser.items(self._section))

    def _create_connection_string(self) -> str:
        """Create database connection string from config"""
        return f"postgresql://{self.config['user']}:{self.config['password']}@{self.config['host']}:{self.config['port']}/{self.config['database']}"

    def _create_engine(self) -> Engine:
        """Create SQLAlchemy engine instance"""
        return create_engine(self._create_connection_string())

    def _create_sqlalchemy_db(self) -> SQLDatabase:
        """Create SQLDatabase instance"""
        return SQLDatabase.from_uri(self._create_connection_string())

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        with self.engine.connect() as connection:
            yield connection

class QueryExecutor:
    """Handles query execution with standardized error handling"""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def execute(
        self, 
        query: str, 
        params: Optional[Dict[str, Any]] = None,
        fetch: Literal["all", "one", "cursor"] = "all"
    ) -> List[Dict[str, Any]]:
        """
        Execute SQL query with standardized error handling and result formatting
        """
        try:
            if fetch == "cursor":
                result = self.db_manager.sqlalchemy_db.run(query, fetch="cursor")
                return cast(List[Dict[str, Any]], result or [])
            
            with self.db_manager.get_connection() as conn:
                result = conn.execute(text(query), parameters=params or {})
                
                if fetch == "one":
                    row = result.fetchone()
                    return [dict(row._mapping)] if row else []
                
                rows = result.fetchall()
                return [dict(row._mapping) for row in rows] if rows else []

        except sa_exc.SQLAlchemyError as e:
            raise QueryError(f"Database error: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Unexpected error: {str(e)}")

class EMRRecordManager:
    """Handles EMR-specific database operations"""

    def __init__(self, query_executor: QueryExecutor):
        self.query_executor = query_executor

    def fetch_patient_emr_records(
        self,
        patient_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Fetch patient EMR records, optionally filtered by patient ID.
        """
        try:
            sql = """
            SELECT 
                op.outpatient_record_id,
                pi.patient_id,
                pi.patient_name,
                pi.gender,
                pi.age,
                op.visit_time,
                op.dept_name,
                op.clinic_diagnosis,
                op.chief_complaint,
                op.present_illness,
                op.physical_examination
            FROM 
                emr_back.emr_outpatient_record op
            JOIN 
                emr_back.emr_patient_info pi ON op.patient_id = pi.patient_id
            """

            params = {"limit": limit}
            if patient_id:
                sql += " WHERE pi.patient_id = :patient_id"
                params["patient_id"] = patient_id

            sql += " ORDER BY op.visit_time DESC LIMIT :limit"
            
            return self.query_executor.execute(sql, params=params)

        except (QueryError, DatabaseError) as e:
            print(f"Error fetching EMR records: {e}")
            return []

    def format_emr_for_analysis(self, record: Dict[str, Any]) -> str:
        """Format an EMR record into a text string suitable for LLM analysis."""
        return f"""
PATIENT INFORMATION:
- ID: {record.get('patient_id', 'N/A')}
- Name: {record.get('patient_name', 'N/A')}
- Gender: {record.get('gender', 'N/A')}
- Age: {record.get('age', 'N/A')}
- Visit Time: {record.get('visit_time', 'N/A')}
- Department: {record.get('dept_name', 'N/A')}

CLINICAL INFORMATION:
- Diagnosis: {record.get('clinic_diagnosis', 'N/A')}
- Chief Complaint: {record.get('chief_complaint', 'N/A')}
- Present Illness: {record.get('present_illness', 'N/A')}
- Physical Examination: {record.get('physical_examination', 'N/A')}
"""

def generate_database_metadata(
    schema: str = "emr_back",
    output_file: Optional[str] = None
) -> Dict[str, Any]:
    """Generate database metadata using direct SQLAlchemy queries."""
    try:
        db_manager = DatabaseManager()
        query_executor = QueryExecutor(db_manager)

        # Tables query
        tables_query = """
        SELECT 
            table_name,
            (SELECT count(*) FROM information_schema.columns 
             WHERE table_schema = :schema AND table_name = t.table_name) AS column_count,
            obj_description(pgc.oid) AS table_description
        FROM 
            information_schema.tables t
        JOIN 
            pg_class pgc ON pgc.relname = t.table_name
        JOIN 
            pg_namespace nsp ON nsp.oid = pgc.relnamespace AND nsp.nspname = :schema
        WHERE 
            table_schema = :schema
            AND table_type = 'BASE TABLE'
        ORDER BY 
            table_name;
        """

        tables = query_executor.execute(tables_query, {"schema": schema})
        
        metadata: Dict[str, Any] = {"schema": schema, "tables": {}}

        for table in tables:
            if not isinstance(table, dict):
                continue
                
            table_name = str(table.get("table_name", ""))
            if not table_name:
                continue

            # Columns query
            columns_query = """
            SELECT 
                column_name,
                data_type,
                character_maximum_length,
                column_default,
                is_nullable,
                col_description(
                    (:schema || '.' || :table_name)::regclass::oid,
                    ordinal_position
                ) as column_description
            FROM 
                information_schema.columns
            WHERE 
                table_schema = :schema
                AND table_name = :table_name
            ORDER BY 
                ordinal_position;
            """

            columns = query_executor.execute(
                columns_query,
                {"schema": schema, "table_name": table_name}
            )

            # Primary keys query
            pk_query = """
            SELECT 
                kcu.column_name
            FROM 
                information_schema.table_constraints tc
            JOIN 
                information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
            WHERE 
                tc.constraint_type = 'PRIMARY KEY'
                AND tc.table_schema = :schema
                AND tc.table_name = :table_name;
            """

            pk_rows = query_executor.execute(
                pk_query,
                {"schema": schema, "table_name": table_name}
            )
            
            primary_keys = [str(row.get("column_name", "")) for row in pk_rows if isinstance(row, dict)]

            # Foreign keys query
            fk_query = """
            SELECT
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM
                information_schema.table_constraints AS tc
            JOIN
                information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN
                information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE
                tc.constraint_type = 'FOREIGN KEY'
                AND tc.table_schema = :schema
                AND tc.table_name = :table_name;
            """

            foreign_keys = query_executor.execute(
                fk_query,
                {"schema": schema, "table_name": table_name}
            )

            # Ensure column_count is an integer
            try:
                column_count = int(table.get("column_count", 0))
            except (TypeError, ValueError):
                column_count = 0

            metadata["tables"][table_name] = {
                "description": table.get("table_description"),
                "column_count": column_count,
                "columns": columns,
                "primary_keys": primary_keys,
                "foreign_keys": foreign_keys,
            }

        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, default=str)

        return metadata

    except Exception as e:
        print(f"Error generating metadata: {e}")
        return {"schema": schema, "tables": {}}

# Create global instances for convenience
db_manager = DatabaseManager()
query_executor = QueryExecutor(db_manager)
emr_manager = EMRRecordManager(query_executor)

# Backwards compatibility functions
def get_db() -> SQLDatabase:
    """Get SQLAlchemy database connection (legacy support)."""
    return db_manager.sqlalchemy_db

def run_sql_query(
    query: str,
    fetch: Literal["all", "one", "cursor"] = "cursor"
) -> List[Dict[str, Any]]:
    """Run SQL query and return results (legacy support)."""
    return query_executor.execute(query, fetch=fetch)

def fetch_patient_emr_records(
    patient_id: Optional[str] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """Fetch patient EMR records (legacy support)."""
    return emr_manager.fetch_patient_emr_records(patient_id, limit)
