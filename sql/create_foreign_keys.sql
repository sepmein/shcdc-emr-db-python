ALTER TABLE emr_back.emr_activity_info ADD CONSTRAINT emr_activity_info_emr_patient_info_fk FOREIGN KEY (patient_id) REFERENCES emr_back.emr_patient_info(id);
