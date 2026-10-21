from sqlalchemy import text

from src.database.connection import get_engine


def extract_patients() -> list[dict]:
    """Extract patient records from the source PostgreSQL table."""

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
        FROM source.source_patients
        ORDER BY source_patient_id
    """)

    engine = get_engine()

    try:
        with engine.connect() as connection:
            result = connection.execute(query)
            patients = [
                dict(row)
                for row in result.mappings().all()
            ]

        print(f"Extracted {len(patients)} patient records.")
        return patients

    finally:
        engine.dispose()
