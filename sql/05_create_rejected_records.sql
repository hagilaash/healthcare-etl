CREATE TABLE IF NOT EXISTS audit.rejected_records (
    rejected_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    source_patient_id INTEGER,
    patient_code VARCHAR(30),

    source_system VARCHAR(100),
    rejection_stage VARCHAR(50) NOT NULL,
    rejection_reason JSONB NOT NULL,

    rejected_data JSONB NOT NULL,

    rejected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
