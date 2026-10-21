import re
from datetime import date

import pandas as pd


EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$"
)


def validate_patients(
    patients: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Validate transformed patient records.

    Returns:
        A tuple containing valid records and rejected records.
        Rejected records include a validation_errors column.
    """

    if patients.empty:
        empty = patients.copy()
        empty["validation_errors"] = pd.Series(dtype="object")
        return empty, empty.copy()

    df = patients.copy()

    # Normalize dates so they can be validated consistently.
    df["date_of_birth"] = pd.to_datetime(
        df["date_of_birth"],
        errors="coerce",
    ).dt.date

    today = date.today()
    errors_by_row = []

    for _, row in df.iterrows():
        errors = []

        if pd.isna(row.get("patient_code")):
            errors.append("Patient code is required.")

        if pd.isna(row.get("first_name")):
            errors.append("First name is required.")

        if pd.isna(row.get("last_name")):
            errors.append("Last name is required.")

        dob = row.get("date_of_birth")

        if pd.isna(dob):
            errors.append("Date of birth is missing or invalid.")
        elif dob > today:
            errors.append("Date of birth cannot be in the future.")

        email = row.get("email")

        if pd.isna(email):
            errors.append("Email is required.")
        elif not EMAIL_PATTERN.fullmatch(str(email)):
            errors.append("Email format is invalid.")

        errors_by_row.append(errors)

    df["validation_errors"] = errors_by_row

    # Reject every record sharing a duplicate patient code.
    non_missing_codes = df["patient_code"].notna()

    duplicate_codes = df.loc[
        non_missing_codes, "patient_code"
    ].duplicated(keep=False)

    duplicate_indexes = duplicate_codes[
        duplicate_codes
    ].index

    for index in duplicate_indexes:
        df.at[index, "validation_errors"].append(
            "Patient code is duplicated within this batch."
        )

    valid_mask = df["validation_errors"].map(len).eq(0)

    valid_patients = df.loc[valid_mask].copy()
    rejected_patients = df.loc[~valid_mask].copy()

    print(f"Valid records: {len(valid_patients)}")
    print(f"Rejected records: {len(rejected_patients)}")

    return valid_patients, rejected_patients
