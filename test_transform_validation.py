import pandas as pd

from src.transform.patient_transformer import transform_patients
from src.validate.patient_validator import validate_patients


sample_patients = [
    {
        "patient_code": " TEST001 ",
        "first_name": " Arun ",
        "last_name": " Kumar ",
        "date_of_birth": "1995-04-12",
        "email": " ARUN.KUMAR@EXAMPLE.COM ",
        "gender": "male",
    },
    {
        "patient_code": "TEST002",
        "first_name": "Priya",
        "last_name": "Sharma",
        "date_of_birth": "1998-08-23",
        "email": "invalid-email",
        "gender": "female",
    },
]

original_first_name = sample_patients[0]["first_name"]

transformed = transform_patients(sample_patients)

valid_patients, rejected_patients = validate_patients(transformed)

print("\n--- Transformed Data ---")
print(
    transformed[
        ["patient_code", "first_name", "email", "gender"]
    ].to_string(index=False)
)

print("\n--- Valid Records ---")
print(valid_patients[["patient_code", "first_name", "email"]])

print("\n--- Rejected Records ---")
print(
    rejected_patients[
        ["patient_code", "email", "validation_errors"]
    ].to_string(index=False)
)

# Basic checks
assert transformed.iloc[0]["first_name"] == "Arun"
assert transformed.iloc[0]["email"] == "arun.kumar@example.com"
assert transformed.iloc[0]["gender"] == "Male"

assert len(valid_patients) == 1
assert len(rejected_patients) == 1

# Confirm the original input was not changed.
assert sample_patients[0]["first_name"] == original_first_name

print("\nAll transformation and validation checks passed.")
