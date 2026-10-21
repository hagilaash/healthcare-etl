import pandas as pd


def transform_patients(patients: list[dict]) -> pd.DataFrame:
    """
    Transform patient records using Pandas.

    The original source data remains unchanged.
    """

    if not patients:
        return pd.DataFrame()

    df = pd.DataFrame(patients)

    # Clean text fields by removing leading and trailing spaces.
    text_columns = [
        "patient_code",
        "first_name",
        "last_name",
        "gender",
        "phone_number",
        "email",
        "address",
        "city",
        "state",
        "postal_code",
        "blood_group",
        "source_system",
    ]

    for column in text_columns:
        if column in df.columns:
            df[column] = df[column].apply(
                lambda value: value.strip()
                if isinstance(value, str)
                else value
            )

    # Standardize email addresses to lowercase.
    if "email" in df.columns:
        df["email"] = df["email"].apply(
            lambda value: value.lower()
            if isinstance(value, str)
            else value
        )

    # Standardize gender values.
    if "gender" in df.columns:
        gender_mapping = {
            "male": "Male",
            "female": "Female",
            "other": "Other",
        }

        df["gender"] = df["gender"].apply(
            lambda value: gender_mapping.get(value.lower(), value)
            if isinstance(value, str)
            else value
        )

    # Normalize empty strings to missing values for key fields.
    required_columns = [
        "patient_code",
        "first_name",
        "last_name",
        "date_of_birth",
        "email",
    ]

    for column in required_columns:
        if column in df.columns:
            df[column] = df[column].replace("", pd.NA)

    print(f"Transformed {len(df)} patient records.")

    return df
