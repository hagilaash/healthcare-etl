CREATE TABLE IF NOT EXISTS staging.staging_patients (
    staging_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    source_patient_id INTEGER NOT NULL,
    patient_code VARCHAR(30),

    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    gender VARCHAR(20),
    phone_number VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    blood_group VARCHAR(5),

    registration_date TIMESTAMP,
    source_system VARCHAR(100),

    processing_status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    validation_errors JSONB,

    extracted_at TIMESTAMP,
    staged_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_staging_processing_status
        CHECK (
            processing_status IN (
                'PENDING',
                'VALID',
                'REJECTED',
                'LOADED'
            )
        )
);
