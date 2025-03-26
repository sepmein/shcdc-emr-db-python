ALTER TABLE emr_back.emr_patient_info ADD CONSTRAINT emr_patient_info_unique UNIQUE (id);
ALTER TABLE emr_back.emr_patient_info ADD CONSTRAINT emr_patient_info_pk PRIMARY KEY (patient_name);
ALTER TABLE emr_back.emr_patient_info ADD CONSTRAINT emr_patient_info_pk_1 PRIMARY KEY (id_card);
