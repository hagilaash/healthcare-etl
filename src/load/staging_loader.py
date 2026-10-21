from sqlalchemy import text

from src.database.connection import get_engine


def load_patients_to_staging(patients: list[dict]) -> int:
    """Insert extracted patients into staging, skipping existing source IDs."""

    if not patients:
        print("No patient records to stage.")
        return 0

    insert_query = text("""
        INSERT INTO staging.staging_patients (
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
        )
        VALUES (
            :source_patient_id,
            :patient_code,
            :first_name,
            :last_name,
            :date_of_birth,
            :gender,
            :phone_number,
            :email,
            :address,
            :city,
            :state,
            :postal_code,
            :blood_group,
            :registration_date,
            :source_system,
            :extracted_at
        )
        ON CONFLICT DO NOTHING
    """)

    engine = get_engine()

    try:
        with engine.begin() as connection:
            inserted = 0

            for patient in patients:
                result = connection.execute(insert_query, patient)
                inserted += result.rowcount

        print(f"Loaded {inserted} patient records into staging.")
        return inserted

    finally:
        engine.dispose()
