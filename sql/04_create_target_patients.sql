CREATE TABLE IF NOT EXISTS target.target_patients (
    target_patient_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    source_patient_id INTEGER NOT NULL UNIQUE,
    patient_code VARCHAR(30) NOT NULL UNIQUE,

    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(20),

    phone_number VARCHAR(20),
    email VARCHAR(255) NOT NULL,
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    blood_group VARCHAR(5),

    registration_date TIMESTAMP,
    source_system VARCHAR(100),

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
