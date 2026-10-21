from src.extract.patient_extractor import extract_patients
from src.extract.staging_reader import get_pending_staging_patients

from src.load.staging_loader import load_patients_to_staging
from src.load.target_loader import load_patients_to_target
from src.load.rejected_loader import load_rejected_patients
from src.load.staging_status_updater import update_staging_status

from src.transform.patient_transformer import transform_patients
from src.validate.patient_validator import validate_patients


def run_pipeline() -> None:
    """Run the Healthcare ETL pipeline."""

    print("\n=== Healthcare ETL Pipeline Started ===")

    # Step 1: Extract source records.
    source_patients = extract_patients()

    # Step 2: Load source records into staging.
    staged_count = load_patients_to_staging(source_patients)

    print(f"New records staged: {staged_count}")

    # Step 3: Retrieve records waiting for processing.
    pending_patients = get_pending_staging_patients()

    if not pending_patients:
        print("No pending records to process.")
        print("=== Healthcare ETL Pipeline Completed ===")
        return

    # Step 4: Transform records.
    transformed_patients = transform_patients(pending_patients)

    # Step 5: Validate transformed records.
    valid_patients, rejected_patients = validate_patients(
        transformed_patients
    )

    # Step 6: Store rejected records and update their staging status.
    rejected_count = load_rejected_patients(rejected_patients)

    for _, patient in rejected_patients.iterrows():
        errors = patient["validation_errors"]

        update_staging_status(
            source_patient_id=int(patient["source_patient_id"]),
            status="REJECTED",
            validation_errors=errors,
        )

    # Step 7: Load valid records into the target table.
    loaded_count = load_patients_to_target(valid_patients)

    # Step 8: Mark successfully loaded records.
    for _, patient in valid_patients.iterrows():
        update_staging_status(
            source_patient_id=int(patient["source_patient_id"]),
            status="LOADED",
        )

    # Step 9: Print summary.
    print("\n=== ETL Pipeline Summary ===")
    print(f"New records staged: {staged_count}")
    print(f"Valid records: {len(valid_patients)}")
    print(f"Rejected records stored: {rejected_count}")
    print(f"Records inserted into target: {loaded_count}")

    print("\n=== Healthcare ETL Pipeline Completed ===")


if __name__ == "__main__":
    run_pipeline()