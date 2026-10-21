# Healthcare ETL Project

**Technology Stack:** Python 3.12.3, Pandas, SQLAlchemy, Psycopg, PostgreSQL 17, Pytest
**Operating System:** Ubuntu 24.04 on WSL2
**Project Location:** `~/projects/healthcare-etl`

## Stage 1: Environment Setup

* Verified Python 3.12.3.
* Verified PostgreSQL host `172.27.80.1`.
* Verified PostgreSQL port `5432`.
* Created project directory `healthcare-etl`.
* Created and activated `.venv`.
* Installed required Python packages.

**Packages:** Pandas, SQLAlchemy, Psycopg, Python-dotenv, Pytest.

## Stage 2: Project Structure

Created the project directories:

* `config/`
* `data/input/`
* `data/processed/`
* `data/rejected/`
* `sql/`
* `src/extract/`
* `src/transform/`
* `src/validate/`
* `src/load/`
* `src/database/`
* `src/utils/`
* `tests/`
* `logs/`

Created initial files:

* `config/settings.py`
* `main.py`
* `requirements.txt`
* `.env.example`
* `.gitignore`
* `README.md`

### Git Ignore Configuration

Added rules to `.gitignore` for:

* Python virtual environment
* Environment variables and secrets
* Python cache files
* Test cache and coverage files
* Log files
* Generated processed and rejected data
* VS Code settings

Kept `.env.example` excluded from the general environment-file ignore rule.

## Stage 3: PostgreSQL Database Setup

**Database:** `healthcare_etl_db`

Created schemas:

* `source`
* `staging`
* `target`
* `audit`

## Stage 4: Database Table Creation

Created the following tables:

| Schema    | Table                            | SQL Script                                 |
| --------- | -------------------------------- | ------------------------------------------ |
| `source`  | `source_patients`                | `sql/01_create_source_patients.sql`        |
| `staging` | `staging_patients`               | `sql/02_create_staging_patients.sql`       |
| `staging` | Unique source patient constraint | `sql/03_add_staging_unique_constraint.sql` |
| `target`  | `target_patients`                | `sql/04_create_target_patients.sql`        |
| `audit`   | `rejected_records`               | `sql/05_create_rejected_records.sql`       |

Verified the schemas, tables, target table columns, rejected-record table, and staging uniqueness constraint.

## Stage 5: Database Connection

Created:

* `config/settings.py`
* `src/database/connection.py`
* `test_connection.py`

Verified the Python connection to `healthcare_etl_db`.

**Result:** Database connection successful.

## Stage 6: Source Extraction and Staging

Created:

* `src/extract/patient_extractor.py`
* `src/load/staging_loader.py`
* `main.py`

Extracted five synthetic patient records from `source.source_patients` and loaded them into `staging.staging_patients`.

Verified duplicate prevention through the unique source patient constraint and `ON CONFLICT DO NOTHING`.

## Stage 7: Transformation and Validation

Created:

* `src/transform/patient_transformer.py`
* `src/validate/patient_validator.py`
* `test_transform_validation.py`

Implemented:

* Text trimming
* Email normalization
* Gender normalization
* Required-field validation
* Date-of-birth validation
* Email format validation
* Duplicate patient-code validation within a batch

Tested transformation and validation independently.

**Result:** Standalone transformation and validation tests passed.

## Stage 8: Target and Rejected Record Loading

Created:

* `src/load/target_loader.py`
* `src/load/rejected_loader.py`
* `src/load/staging_status_updater.py`
* `src/extract/staging_reader.py`

Implemented the components for:

* Reading pending staging records
* Loading valid records into `target.target_patients`
* Recording invalid records in `audit.rejected_records`
* Updating staging statuses and validation errors

## Stage 9: Integrated ETL Pipeline

Updated:

* `main.py`

Integrated the following workflow:

1. Extract source records.
2. Load new records into staging.
3. Read pending staging records.
4. Transform patient data.
5. Validate records.
6. Store rejected records.
7. Load valid records into the target table.
8. Update staging statuses.
9. Display the pipeline summary.

### Initial Pipeline Verification

Successfully executed:

`python main.py`

Results:

* Source records extracted: 5
* New records staged: 0
* Pending records processed: 5
* Valid records: 5
* Rejected records: 0
* Records inserted into target: 5

The five records had already been staged, explaining why no additional staging records were inserted during this run.

## Stage 10: Generate 500 Synthetic Patient Records

Created the SQL file:

* `healthcare_etl_500_synthetic_patients.sql`

The file contains 500 additional synthetic patient records, with patient codes from `SRC1006` through `SRC1505`.

The existing five source records are preserved.

Expected source count after insertion: 505.

## Current ETL Architecture

`source.source_patients`
→ `patient_extractor.py`
→ `staging.staging_patients`
→ `staging_reader.py`
→ `patient_transformer.py`
→ `patient_validator.py`
→ Valid records: `target.target_patients`
→ Invalid records: `audit.rejected_records`

Staging statuses are updated through `staging_status_updater.py`.

## Current Progress

**Completed:**

* Environment setup
* PostgreSQL database and schema setup
* Source, staging, target, and rejected-record table creation
* Python database connection
* Source extraction
* Staging load
* Transformation
* Validation
* Target loader creation
* Rejected-record loader creation
* Integrated pipeline implementation
* Initial five-record pipeline execution
* Generation of 500 synthetic patient records

**Next tasks:**

* Insert and verify the 500 synthetic records.
* Run the pipeline against the larger dataset.
* Verify target, staging, and rejected-record counts.
* Test invalid records and rejection handling.
* Improve transaction management and error recovery.
* Add ETL audit logging.
* Add CSV and JSON source extraction.
* Add automated tests and incremental processing.
* Configure scheduling.
* Complete the project README.


=== Healthcare ETL Pipeline Started ===
Extracted 505 patient records.
Loaded 500 patient records into staging.
New records staged: 500
Retrieved 500 pending staging records.
Transformed 500 patient records.
Valid records: 500
Rejected records: 0
No rejected patient records to store.
Inserted 500 patient records into target.

=== ETL Pipeline Summary ===
New records staged: 500
Valid records: 500
Rejected records stored: 0
Records inserted into target: 500

=== Healthcare ETL Pipeline Completed ===
