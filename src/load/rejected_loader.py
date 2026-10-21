import json

import pandas as pd
from sqlalchemy import text

from src.database.connection import get_engine


def load_rejected_patients(rejected_patients: pd.DataFrame) -> int:
    """
    Store rejected patient records and their validation errors.

    Returns:
        Number of rejected records inserted.
    """
    if rejected_patients.empty:
        print("No rejected patient records to store.")
        return 0

    insert_query = text("""
        INSERT INTO audit.rejected_records (
            source_patient_id,
            patient_code,
            source_system,
            rejection_stage,
            rejection_reason,
            rejected_data
        )
        VALUES (
            :source_patient_id,
            :patient_code,
            :source_system,
            :rejection_stage,
            CAST(:rejection_reason AS JSONB),
            CAST(:rejected_data AS JSONB)
        )
    """)

    def to_json_value(value):
        if value is None or pd.isna(value):
            return None
        if hasattr(value, "isoformat"):
            return value.isoformat()
        return value

    engine = get_engine()

    try:
        inserted_count = 0

        with engine.begin() as connection:
            for _, row in rejected_patients.iterrows():
                record = row.to_dict()

                errors = record.get("validation_errors", [])
                if not isinstance(errors, list):
                    errors = [str(errors)]

                rejected_data = {
                    key: to_json_value(value)
                    for key, value in record.items()
                    if key != "validation_errors"
                }

                parameters = {
                    "source_patient_id": to_json_value(
                        record.get("source_patient_id")
                    ),
                    "patient_code": to_json_value(
                        record.get("patient_code")
                    ),
                    "source_system": to_json_value(
                        record.get("source_system")
                    ),
                    "rejection_stage": "VALIDATION",
                    "rejection_reason": json.dumps(errors),
                    "rejected_data": json.dumps(
                        rejected_data,
                        default=str,
                    ),
                }

                connection.execute(insert_query, parameters)
                inserted_count += 1

        print(
            f"Stored {inserted_count} rejected patient records "
            "in audit.rejected_records."
        )
        return inserted_count

    finally:
        engine.dispose()