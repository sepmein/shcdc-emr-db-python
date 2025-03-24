# SHCDC EMR Database Package

A Python package for managing Electronic Medical Record (EMR) database operations using SQLAlchemy.

## Features

- Database connection management with SQLAlchemy
- Query execution with standardized error handling
- EMR-specific database operations
- Database metadata generation
- Legacy support functions

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from shcdc_emr_db import DatabaseManager, QueryExecutor, EMRRecordManager

# Initialize database manager
db_manager = DatabaseManager()

# Create query executor
query_executor = QueryExecutor(db_manager)

# Create EMR record manager
emr_manager = EMRRecordManager(query_executor)

# Fetch patient records
records = emr_manager.fetch_patient_emr_records(patient_id="123", limit=10)
```

## Configuration

Create a `config/database.ini` file with the following structure:

```ini
[postgresql]
host = your_host
port = your_port
database = your_database
user = your_user
password = your_password
```

## Development

To set up the development environment:

1. Clone the repository
2. Create a virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install the package in development mode:
   ```bash
   pip install -e .
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
