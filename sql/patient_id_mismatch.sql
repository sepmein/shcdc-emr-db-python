-- emr activity table
-- 查询缺失的患者信息
SELECT emr_activity_info.*
FROM emr_activity_info
LEFT JOIN emr_patient_info ON emr_activity_info.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL;


-- 统计每个组织机构中缺失的患者信息
SELECT emr_activity_info.org_name, COUNT(*) AS missing_count
FROM emr_activity_info
LEFT JOIN emr_patient_info ON emr_activity_info.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL
GROUP BY emr_activity_info.org_name;

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
SELECT DISTINCT ON (emr_activity_info.patient_id)
    emr_activity_info.patient_id,
    emr_activity_info.patient_name,
    emr_activity_info.id_card_type_code,
    emr_activity_info.id_card_type_name,
    emr_activity_info.id_card,
    emr_activity_info.org_code,
    emr_activity_info.org_name
FROM emr_activity_info
LEFT JOIN emr_patient_info 
    ON emr_activity_info.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL
ORDER BY emr_activity_info.patient_id;


-- emr outpatien record
-- 查询缺失的患者信息
SELECT emr_outpatient_record.*
FROM emr_outpatient_record
LEFT JOIN emr_patient_info ON emr_outpatient_record.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL;

-- 统计每个组织机构中缺失的患者信息
SELECT emr_outpatient_record.org_name, COUNT(*) AS missing_count
FROM emr_outpatient_record
LEFT JOIN emr_patient_info ON emr_outpatient_record.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL
GROUP BY emr_outpatient_record.org_name;

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
SELECT DISTINCT ON (emr_outpatient_record.patient_id)
    emr_outpatient_record.patient_id,
    emr_outpatient_record.patient_name,
    emr_outpatient_record.id_card_type_code,
    emr_outpatient_record.id_card_type_name,
    emr_outpatient_record.id_card,
    emr_outpatient_record.org_code,
    emr_outpatient_record.org_name
FROM emr_outpatient_record
LEFT JOIN emr_patient_info 
    ON emr_outpatient_record.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL
ORDER BY emr_outpatient_record.patient_id;


-- emr admission info
-- 查询缺失的患者信息
SELECT emr_admission_info.*
FROM emr_admission_info
LEFT JOIN emr_patient_info ON emr_admission_info.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL;

-- 统计每个组织机构中缺失的患者信息
SELECT emr_admission_info.org_name, COUNT(*) AS missing_count
FROM emr_admission_info
LEFT JOIN emr_patient_info ON emr_admission_info.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL
GROUP BY emr_admission_info.org_name;

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
SELECT DISTINCT ON (emr_admission_info.patient_id)
    emr_admission_info.patient_id,
    emr_admission_info.patient_name,
    emr_admission_info.id_card_type_code,
    emr_admission_info.id_card_type_name,
    emr_admission_info.id_card,
    emr_admission_info.org_code,
    emr_admission_info.org_name
FROM emr_admission_info
LEFT JOIN emr_patient_info 
    ON emr_admission_info.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL
ORDER BY emr_admission_info.patient_id;


-- emr first course
-- 查询缺失的患者信息
SELECT emr_first_course.*
FROM emr_first_course
LEFT JOIN emr_patient_info ON emr_first_course.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL;

-- 统计每个组织机构中缺失的患者信息
SELECT emr_first_course.org_name, COUNT(*) AS missing_count
FROM emr_first_course
LEFT JOIN emr_patient_info ON emr_first_course.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL
GROUP BY emr_first_course.org_name;

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
SELECT DISTINCT ON (emr_first_course.patient_id)
    emr_first_course.patient_id,
    emr_first_course.patient_name,  
    emr_first_course.id_card_type_code,
    emr_first_course.id_card_type_name,
    emr_first_course.id_card,
    emr_first_course.org_code,
    emr_first_course.org_name
FROM emr_first_course
LEFT JOIN emr_patient_info 
    ON emr_first_course.patient_id = emr_patient_info.id
WHERE emr_patient_info.id IS NULL
ORDER BY emr_first_course.patient_id;


