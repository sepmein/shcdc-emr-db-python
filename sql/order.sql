
-- check id duplicates
SELECT id, COUNT(*) 
FROM emr_back.emr_order 
GROUP BY id 
HAVING COUNT(*) > 1;

WITH duplicates AS (
    SELECT ctid, 
           row_number() OVER (PARTITION BY id ORDER BY ctid) AS rn
    FROM emr_back.emr_order
)
DELETE FROM emr_back.emr_order
WHERE ctid IN (
    SELECT ctid 
    FROM duplicates 
    WHERE rn > 1
);

-- 创建emr_order表的唯一约束
ALTER TABLE emr_back.emr_order ADD CONSTRAINT emr_order_unique UNIQUE (id);


-- emr daily course
-- 查询缺失的患者信息
SELECT emr_order.*
FROM emr_order
LEFT JOIN emr_patient_info ON emr_order.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL;

-- count total number of missing patients
SELECT COUNT(*)
FROM emr_order
LEFT JOIN emr_patient_info ON emr_order.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL;


-- 统计每个组织机构中缺失的患者信息
SELECT emr_order.org_name, COUNT(*) AS missing_count
FROM emr_order
LEFT JOIN emr_patient_info ON emr_order.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL
GROUP BY emr_order.org_name;

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
SELECT DISTINCT ON (emr_order.patient_id)
    emr_order.patient_id,
    emr_order.patient_name,  
    emr_order.id_card_type_code,
    emr_order.id_card_type_name,
    emr_order.id_card,
    emr_order.org_code,
    emr_order.org_name
FROM emr_order
LEFT JOIN emr_patient_info 
    ON emr_order.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL
ORDER BY emr_order.patient_id;

-- 创建emr_order表的外键约束
ALTER TABLE emr_back.emr_order ADD CONSTRAINT emr_order_emr_patient_info_fk FOREIGN KEY (patient_id) REFERENCES emr_back.emr_patient_info(id);


