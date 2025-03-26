WITH duplicates AS (
    SELECT ctid, 
           row_number() OVER (PARTITION BY id ORDER BY ctid) AS rn
    FROM emr_back.emr_patient_info
)
DELETE FROM emr_back.emr_patient_info
WHERE ctid IN (
    SELECT ctid 
    FROM duplicates 
    WHERE rn > 1
);