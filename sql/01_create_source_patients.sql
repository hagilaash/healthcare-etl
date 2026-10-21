CREATE TABLE IF NOT EXISTS source.source_patients (
    source_patient_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
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
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_system VARCHAR(100),
    extracted_at TIMESTAMP
);
