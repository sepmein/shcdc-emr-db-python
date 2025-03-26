
-- check id duplicates
SELECT id, COUNT(*) 
FROM emr_back.emr_death_info 
GROUP BY id 
HAVING COUNT(*) > 1;

WITH duplicates AS (
    SELECT ctid, 
           row_number() OVER (PARTITION BY id ORDER BY ctid) AS rn
    FROM emr_back.emr_death_info
)
DELETE FROM emr_back.emr_death_info
WHERE ctid IN (
    SELECT ctid 
    FROM duplicates 
    WHERE rn > 1
);

-- 创建emr_death_info表的唯一约束
ALTER TABLE emr_back.emr_death_info ADD CONSTRAINT emr_death_info_unique UNIQUE (id);


-- emr daily course
-- 查询缺失的患者信息
SELECT emr_death_info.*
FROM emr_death_info
LEFT JOIN emr_patient_info ON emr_death_info.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL;

-- count total number of missing patients
SELECT COUNT(*)
FROM emr_death_info
LEFT JOIN emr_patient_info ON emr_death_info.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL;


-- 统计每个组织机构中缺失的患者信息
SELECT emr_death_info.org_name, COUNT(*) AS missing_count
FROM emr_death_info
LEFT JOIN emr_patient_info ON emr_death_info.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL
GROUP BY emr_death_info.org_name;

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
SELECT DISTINCT ON (emr_death_info.patient_id)
    emr_death_info.patient_id,
    emr_death_info.patient_name,  
    emr_death_info.id_card_type_code,
    emr_death_info.id_card_type_name,
    emr_death_info.id_card,
    emr_death_info.org_code,
    emr_death_info.org_name
FROM emr_death_info
LEFT JOIN emr_patient_info 
    ON emr_death_info.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL
ORDER BY emr_death_info.patient_id;

-- 创建emr_death_info表的外键约束
ALTER TABLE emr_back.emr_death_info ADD CONSTRAINT emr_death_info_emr_patient_info_fk FOREIGN KEY (patient_id) REFERENCES emr_back.emr_patient_info(id);


