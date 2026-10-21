ALTER TABLE staging.staging_patients
ADD CONSTRAINT uq_staging_source_patient
UNIQUE (source_patient_id);
