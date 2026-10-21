from sqlalchemy import text

from src.database.connection import get_engine


def get_pending_staging_patients() -> list[dict]:
    """Retrieve patient records that are waiting to be processed."""

    query = text("""
        SELECT
            source_patient_id,
            patient_code,
            first_name,
            last_name,
            date_of_birth,
            gender,
            phone_number,
            email,
            address,
            city,
            state,
            postal_code,
            blood_group,
            registration_date,
            source_system,
            extracted_at
        FROM staging.staging_patients
        WHERE processing_status = 'PENDING'
        ORDER BY staging_id
    """)

    engine = get_engine()

    try:
        with engine.connect() as connection:
            result = connection.execute(query)
            patients = [dict(row) for row in result.mappings().all()]

        print(f"Retrieved {len(patients)} pending staging records.")
        return patients

    finally:
        engine.dispose()