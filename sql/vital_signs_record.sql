
-- check id duplicates
SELECT id, COUNT(*) 
FROM emr_back.emr_vital_signs_record 
GROUP BY id 
HAVING COUNT(*) > 1;

WITH duplicates AS (
    SELECT ctid, 
           row_number() OVER (PARTITION BY id ORDER BY ctid) AS rn
    FROM emr_back.emr_vital_signs_record
)
DELETE FROM emr_back.emr_vital_signs_record
WHERE ctid IN (
    SELECT ctid 
    FROM duplicates 
    WHERE rn > 1
);

-- 创建emr_vital_signs_record表的唯一约束
ALTER TABLE emr_back.emr_vital_signs_record ADD CONSTRAINT emr_vital_signs_record_unique UNIQUE (id);


-- emr daily course
-- 查询缺失的患者信息
SELECT emr_vital_signs_record.*
FROM emr_vital_signs_record
LEFT JOIN emr_patient_info ON emr_vital_signs_record.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL;

-- count total number of missing patients
SELECT COUNT(*)
FROM emr_vital_signs_record
LEFT JOIN emr_patient_info ON emr_vital_signs_record.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL;


-- 统计每个组织机构中缺失的患者信息
SELECT emr_vital_signs_record.org_name, COUNT(*) AS missing_count
FROM emr_vital_signs_record
LEFT JOIN emr_patient_info ON emr_vital_signs_record.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL
GROUP BY emr_vital_signs_record.org_name;

-- 插入缺失的患者信息
INSERT INTO emr_patient_info (
    id,
    patient_name,
    id_card_type_code,
    id_card_type_name,
    id_card,
    org_code,
    org_name
)
SELECT DISTINCT ON (emr_vital_signs_record.patient_id)
    emr_vital_signs_record.patient_id,
    emr_vital_signs_record.patient_name,  
    emr_vital_signs_record.id_card_type_code,
    emr_vital_signs_record.id_card_type_name,
    emr_vital_signs_record.id_card,
    emr_vital_signs_record.org_code,
    emr_vital_signs_record.org_name
FROM emr_vital_signs_record
LEFT JOIN emr_patient_info 
    ON emr_vital_signs_record.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL
ORDER BY emr_vital_signs_record.patient_id;

-- 创建emr_vital_signs_record表的外键约束
ALTER TABLE emr_back.emr_vital_signs_record ADD CONSTRAINT emr_vital_signs_record_emr_patient_info_fk FOREIGN KEY (patient_id) REFERENCES emr_back.emr_patient_info(id);


