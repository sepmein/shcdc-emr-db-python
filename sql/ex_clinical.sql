
-- check id duplicates
SELECT id, COUNT(*) 
FROM emr_back.emr_ex_clinical 
GROUP BY id 
HAVING COUNT(*) > 1;

WITH duplicates AS (
    SELECT ctid, 
           row_number() OVER (PARTITION BY id ORDER BY ctid) AS rn
    FROM emr_back.emr_ex_clinical
)
DELETE FROM emr_back.emr_ex_clinical
WHERE ctid IN (
    SELECT ctid 
    FROM duplicates 
    WHERE rn > 1
);

-- 创建emr_ex_clinical表的唯一约束
ALTER TABLE emr_back.emr_ex_clinical ADD CONSTRAINT emr_ex_clinical_unique UNIQUE (id);


-- emr daily course
-- 查询缺失的患者信息
SELECT emr_ex_clinical.*
FROM emr_ex_clinical
LEFT JOIN emr_patient_info ON emr_ex_clinical.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL;

-- count total number of missing patients
SELECT COUNT(*)
FROM emr_ex_clinical
LEFT JOIN emr_patient_info ON emr_ex_clinical.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL;


-- 统计每个组织机构中缺失的患者信息
SELECT emr_ex_clinical.org_name, COUNT(*) AS missing_count
FROM emr_ex_clinical
LEFT JOIN emr_patient_info ON emr_ex_clinical.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL
GROUP BY emr_ex_clinical.org_name;

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
SELECT DISTINCT ON (emr_ex_clinical.patient_id)
    emr_ex_clinical.patient_id,
    emr_ex_clinical.patient_name,  
    emr_ex_clinical.id_card_type_code,
    emr_ex_clinical.id_card_type_name,
    emr_ex_clinical.id_card,
    emr_ex_clinical.org_code,
    emr_ex_clinical.org_name
FROM emr_ex_clinical
LEFT JOIN emr_patient_info 
    ON emr_ex_clinical.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL
ORDER BY emr_ex_clinical.patient_id;

-- 创建emr_ex_clinical表的外键约束
ALTER TABLE emr_back.emr_ex_clinical ADD CONSTRAINT emr_ex_clinical_emr_patient_info_fk FOREIGN KEY (patient_id) REFERENCES emr_back.emr_patient_info(id);


