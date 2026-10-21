import json

from sqlalchemy import text

from src.database.connection import get_engine


def update_staging_status(
    source_patient_id: int,
    status: str,
    validation_errors: list[str] | None = None,
) -> None:
    """Update the processing status and validation errors for a staged record."""

    if status not in {"PENDING", "VALID", "REJECTED", "LOADED"}:
        raise ValueError(f"Unsupported staging status: {status}")

    query = text("""
        UPDATE staging.staging_patients
        SET processing_status = :status,
            validation_errors = CAST(:validation_errors AS JSONB)
        WHERE source_patient_id = :source_patient_id
    """)

    errors_json = (
        json.dumps(validation_errors)
        if validation_errors
        else None
    )

    engine = get_engine()

    try:
        with engine.begin() as connection:
            result = connection.execute(
                query,
                {
                    "source_patient_id": source_patient_id,
                    "status": status,
                    "validation_errors": errors_json,
                },
            )

            if result.rowcount != 1:
                raise ValueError(
                    "Expected exactly one staging record for "
                    f"source_patient_id={source_patient_id}; "
                    f"updated {result.rowcount}."
                )

    finally:
        engine.dispose()