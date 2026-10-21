import pandas as pd
from sqlalchemy import text

from src.database.connection import get_engine


def load_patients_to_target(patients: pd.DataFrame) -> int:
    """Load validated patient records into the target table."""

    if patients.empty:
        print("No valid patient records to load.")
        return 0

    query = text("""
        INSERT INTO target.target_patients (
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
            source_system
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
            :source_system
        )
        ON CONFLICT DO NOTHING
    """)

    columns = [
        "source_patient_id",
        "patient_code",
        "first_name",
        "last_name",
        "date_of_birth",
        "gender",
        "phone_number",
        "email",
        "address",
        "city",
        "state",
        "postal_code",
        "blood_group",
        "registration_date",
        "source_system",
    ]

    engine = get_engine()

    try:
        inserted_count = 0

        with engine.begin() as connection:
            for record in patients[columns].to_dict(orient="records"):
                clean_record = {
                    key: None if pd.isna(value) else value
                    for key, value in record.items()
                }
                result = connection.execute(query, clean_record)
                inserted_count += result.rowcount

        print(f"Inserted {inserted_count} patient records into target.")
        return inserted_count

    finally:
        engine.dispose()