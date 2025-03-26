----------------------------------------------------------------------------
-- emr_patient_info 表数据质量检查
----------------------------------------------------------------------------

-- 1. 统计总记录数
SELECT COUNT(*) AS 总记录数 FROM emr_patient_info;

-- 2. 必填字段检查 (id, patient_name, id_card_type_code, id_card_type_name, id_card, org_code, org_name, operation_time)
SELECT 
    SUM(CASE WHEN id IS NULL OR TRIM(id) = '' THEN 1 ELSE 0 END) AS id空值数,
    SUM(CASE WHEN patient_name IS NULL OR TRIM(patient_name) = '' THEN 1 ELSE 0 END) AS 患者姓名空值数,
    SUM(CASE WHEN id_card_type_code IS NULL OR TRIM(id_card_type_code) = '' THEN 1 ELSE 0 END) AS 身份证件类别代码空值数,
    SUM(CASE WHEN id_card_type_name IS NULL OR TRIM(id_card_type_name) = '' THEN 1 ELSE 0 END) AS 身份证件类别名称空值数,
    SUM(CASE WHEN id_card IS NULL OR TRIM(id_card) = '' THEN 1 ELSE 0 END) AS 身份证件号码空值数,
    SUM(CASE WHEN org_code IS NULL OR TRIM(org_code) = '' THEN 1 ELSE 0 END) AS 医疗机构代码空值数,
    SUM(CASE WHEN org_name IS NULL OR TRIM(org_name) = '' THEN 1 ELSE 0 END) AS 医疗机构名称空值数,
    SUM(CASE WHEN operation_time IS NULL THEN 1 ELSE 0 END) AS 操作时间空值数
FROM emr_patient_info;

-- 3. 建议填写字段检查
SELECT 
    SUM(CASE WHEN gender_code IS NULL OR TRIM(gender_code) = '' THEN 1 ELSE 0 END) AS 性别代码空值数,
    SUM(CASE WHEN gender_name IS NULL OR TRIM(gender_name) = '' THEN 1 ELSE 0 END) AS 性别名称空值数,
    SUM(CASE WHEN birth_date IS NULL THEN 1 ELSE 0 END) AS 出生日期空值数,
    SUM(CASE WHEN nationality_code IS NULL OR TRIM(nationality_code) = '' THEN 1 ELSE 0 END) AS 国籍代码空值数,
    SUM(CASE WHEN nationality_name IS NULL OR TRIM(nationality_name) = '' THEN 1 ELSE 0 END) AS 国籍名称空值数,
    SUM(CASE WHEN nation_code IS NULL OR TRIM(nation_code) = '' THEN 1 ELSE 0 END) AS 民族代码空值数,
    SUM(CASE WHEN nation_name IS NULL OR TRIM(nation_name) = '' THEN 1 ELSE 0 END) AS 民族名称空值数,
    SUM(CASE WHEN permanent_addr_code IS NULL OR TRIM(permanent_addr_code) = '' THEN 1 ELSE 0 END) AS 户籍地址代码空值数,
    SUM(CASE WHEN permanent_addr_name IS NULL OR TRIM(permanent_addr_name) = '' THEN 1 ELSE 0 END) AS 户籍地址名称空值数,
    SUM(CASE WHEN permanent_addr_detail IS NULL OR TRIM(permanent_addr_detail) = '' THEN 1 ELSE 0 END) AS 户籍详细地址空值数,
    SUM(CASE WHEN current_addr_code IS NULL OR TRIM(current_addr_code) = '' THEN 1 ELSE 0 END) AS 现住地址代码空值数,
    SUM(CASE WHEN current_addr_name IS NULL OR TRIM(current_addr_name) = '' THEN 1 ELSE 0 END) AS 现住地址名称空值数,
    SUM(CASE WHEN current_addr_detail IS NULL OR TRIM(current_addr_detail) = '' THEN 1 ELSE 0 END) AS 现住详细地址空值数,
    SUM(CASE WHEN workunit IS NULL OR TRIM(workunit) = '' THEN 1 ELSE 0 END) AS 工作单位空值数,
    SUM(CASE WHEN marital_status_code IS NULL OR TRIM(marital_status_code) = '' THEN 1 ELSE 0 END) AS 婚姻状况代码空值数,
    SUM(CASE WHEN marital_status_name IS NULL OR TRIM(marital_status_name) = '' THEN 1 ELSE 0 END) AS 婚姻状况名称空值数,
    SUM(CASE WHEN education_code IS NULL OR TRIM(education_code) = '' THEN 1 ELSE 0 END) AS 学历代码空值数,
    SUM(CASE WHEN education_name IS NULL OR TRIM(education_name) = '' THEN 1 ELSE 0 END) AS 学历名称空值数,
    SUM(CASE WHEN nultitude_type_code IS NULL OR TRIM(nultitude_type_code) = '' THEN 1 ELSE 0 END) AS 人群分类代码空值数,
    SUM(CASE WHEN nultitude_type_name IS NULL OR TRIM(nultitude_type_name) = '' THEN 1 ELSE 0 END) AS 人群分类名称空值数,
    SUM(CASE WHEN tel IS NULL OR TRIM(tel) = '' THEN 1 ELSE 0 END) AS 患者电话空值数,
    SUM(CASE WHEN contacts IS NULL OR TRIM(contacts) = '' THEN 1 ELSE 0 END) AS 联系人姓名空值数,
    SUM(CASE WHEN contacts_tel IS NULL OR TRIM(contacts_tel) = '' THEN 1 ELSE 0 END) AS 联系人电话空值数
FROM emr_patient_info;

-- 4. 分类统计各医疗机构必填字段填写情况
SELECT
    org_name AS 医疗机构名称,
    COUNT(*) AS 记录总数,
    
    -- 必填字段缺失统计
    SUM(CASE WHEN id IS NULL OR TRIM(id) = '' THEN 1 ELSE 0 END) AS ID缺失数,
    ROUND(100.0 * SUM(CASE WHEN id IS NULL OR TRIM(id) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS ID缺失率,
    SUM(CASE WHEN patient_name IS NULL OR TRIM(patient_name) = '' THEN 1 ELSE 0 END) AS 患者姓名缺失数,
    ROUND(100.0 * SUM(CASE WHEN patient_name IS NULL OR TRIM(patient_name) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS 患者姓名缺失率,
    SUM(CASE WHEN id_card_type_code IS NULL OR TRIM(id_card_type_code) = '' THEN 1 ELSE 0 END) AS 证件类型代码缺失数,
    ROUND(100.0 * SUM(CASE WHEN id_card_type_code IS NULL OR TRIM(id_card_type_code) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS 证件类型代码缺失率,
    SUM(CASE WHEN id_card IS NULL OR TRIM(id_card) = '' THEN 1 ELSE 0 END) AS 证件号码缺失数,
    ROUND(100.0 * SUM(CASE WHEN id_card IS NULL OR TRIM(id_card) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS 证件号码缺失率,
    
    -- 综合质量评分（必填字段填写完整率）
    ROUND(100.0 - (
        100.0 * (
            SUM(CASE WHEN id IS NULL OR TRIM(id) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN patient_name IS NULL OR TRIM(patient_name) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN id_card_type_code IS NULL OR TRIM(id_card_type_code) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN id_card_type_name IS NULL OR TRIM(id_card_type_name) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN id_card IS NULL OR TRIM(id_card) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN org_code IS NULL OR TRIM(org_code) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN operation_time IS NULL THEN 1 ELSE 0 END)
        ) / (COUNT(*) * 7)
    ), 2) AS 必填字段完整率
FROM
    emr_patient_info
GROUP BY
    org_name
ORDER BY
    必填字段完整率 DESC, 记录总数 DESC;

-- 5. 分类统计各医疗机构建议填写字段填写情况
SELECT
    org_name AS 医疗机构名称,
    COUNT(*) AS 记录总数,
    
    -- 核心建议填写字段统计
    SUM(CASE WHEN gender_code IS NULL OR TRIM(gender_code) = '' THEN 1 ELSE 0 END) AS 性别代码缺失数,
    ROUND(100.0 * SUM(CASE WHEN gender_code IS NULL OR TRIM(gender_code) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS 性别代码缺失率,
    
    SUM(CASE WHEN birth_date IS NULL THEN 1 ELSE 0 END) AS 出生日期缺失数,
    ROUND(100.0 * SUM(CASE WHEN birth_date IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS 出生日期缺失率,
    
    SUM(CASE WHEN tel IS NULL OR TRIM(tel) = '' THEN 1 ELSE 0 END) AS 电话号码缺失数,
    ROUND(100.0 * SUM(CASE WHEN tel IS NULL OR TRIM(tel) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS 电话号码缺失率,
    
    SUM(CASE WHEN marital_status_code IS NULL OR TRIM(marital_status_code) = '' THEN 1 ELSE 0 END) AS 婚姻状况缺失数,
    ROUND(100.0 * SUM(CASE WHEN marital_status_code IS NULL OR TRIM(marital_status_code) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS 婚姻状况缺失率,
    
    -- 建议填写字段综合完整率（选取10个重要的建议字段）
    ROUND(100.0 - (
        100.0 * (
            SUM(CASE WHEN gender_code IS NULL OR TRIM(gender_code) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN birth_date IS NULL THEN 1 ELSE 0 END) +
            SUM(CASE WHEN nation_code IS NULL OR TRIM(nation_code) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN current_addr_code IS NULL OR TRIM(current_addr_code) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN current_addr_detail IS NULL OR TRIM(current_addr_detail) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN marital_status_code IS NULL OR TRIM(marital_status_code) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN education_code IS NULL OR TRIM(education_code) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN tel IS NULL OR TRIM(tel) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN contacts IS NULL OR TRIM(contacts) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN contacts_tel IS NULL OR TRIM(contacts_tel) = '' THEN 1 ELSE 0 END)
        ) / (COUNT(*) * 10)
    ), 2) AS 建议字段完整率
FROM
    emr_patient_info
GROUP BY
    org_name
ORDER BY
    建议字段完整率 DESC, 记录总数 DESC;

-- 6. 综合数据质量评分（必填+建议字段综合评分）
SELECT
    org_name AS 医疗机构名称,
    COUNT(*) AS 记录总数,
    
    -- 必填字段完整率
    ROUND(100.0 - (
        100.0 * (
            SUM(CASE WHEN id IS NULL OR TRIM(id) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN patient_name IS NULL OR TRIM(patient_name) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN id_card_type_code IS NULL OR TRIM(id_card_type_code) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN id_card_type_name IS NULL OR TRIM(id_card_type_name) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN id_card IS NULL OR TRIM(id_card) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN org_code IS NULL OR TRIM(org_code) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN operation_time IS NULL THEN 1 ELSE 0 END)
        ) / (COUNT(*) * 7)
    ), 2) AS 必填字段完整率,
    
    -- 建议填写字段完整率
    ROUND(100.0 - (
        100.0 * (
            SUM(CASE WHEN gender_code IS NULL OR TRIM(gender_code) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN birth_date IS NULL THEN 1 ELSE 0 END) +
            SUM(CASE WHEN nation_code IS NULL OR TRIM(nation_code) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN current_addr_code IS NULL OR TRIM(current_addr_code) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN current_addr_detail IS NULL OR TRIM(current_addr_detail) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN marital_status_code IS NULL OR TRIM(marital_status_code) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN education_code IS NULL OR TRIM(education_code) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN tel IS NULL OR TRIM(tel) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN contacts IS NULL OR TRIM(contacts) = '' THEN 1 ELSE 0 END) +
            SUM(CASE WHEN contacts_tel IS NULL OR TRIM(contacts_tel) = '' THEN 1 ELSE 0 END)
        ) / (COUNT(*) * 10)
    ), 2) AS 建议字段完整率,
    
    -- 综合评分（必填字段权重70%，建议字段权重30%）
    ROUND(
        (ROUND(100.0 - (
            100.0 * (
                SUM(CASE WHEN id IS NULL OR TRIM(id) = '' THEN 1 ELSE 0 END) +
                SUM(CASE WHEN patient_name IS NULL OR TRIM(patient_name) = '' THEN 1 ELSE 0 END) +
                SUM(CASE WHEN id_card_type_code IS NULL OR TRIM(id_card_type_code) = '' THEN 1 ELSE 0 END) +
                SUM(CASE WHEN id_card_type_name IS NULL OR TRIM(id_card_type_name) = '' THEN 1 ELSE 0 END) +
                SUM(CASE WHEN id_card IS NULL OR TRIM(id_card) = '' THEN 1 ELSE 0 END) +
                SUM(CASE WHEN org_code IS NULL OR TRIM(org_code) = '' THEN 1 ELSE 0 END) +
                SUM(CASE WHEN operation_time IS NULL THEN 1 ELSE 0 END)
            ) / (COUNT(*) * 7)
        ), 2) * 0.7) +
        (ROUND(100.0 - (
            100.0 * (
                SUM(CASE WHEN gender_code IS NULL OR TRIM(gender_code) = '' THEN 1 ELSE 0 END) +
                SUM(CASE WHEN birth_date IS NULL THEN 1 ELSE 0 END) +
                SUM(CASE WHEN nation_code IS NULL OR TRIM(nation_code) = '' THEN 1 ELSE 0 END) +
                SUM(CASE WHEN current_addr_code IS NULL OR TRIM(current_addr_code) = '' THEN 1 ELSE 0 END) +
                SUM(CASE WHEN current_addr_detail IS NULL OR TRIM(current_addr_detail) = '' THEN 1 ELSE 0 END) +
                SUM(CASE WHEN marital_status_code IS NULL OR TRIM(marital_status_code) = '' THEN 1 ELSE 0 END) +
                SUM(CASE WHEN education_code IS NULL OR TRIM(education_code) = '' THEN 1 ELSE 0 END) +
                SUM(CASE WHEN tel IS NULL OR TRIM(tel) = '' THEN 1 ELSE 0 END) +
                SUM(CASE WHEN contacts IS NULL OR TRIM(contacts) = '' THEN 1 ELSE 0 END) +
                SUM(CASE WHEN contacts_tel IS NULL OR TRIM(contacts_tel) = '' THEN 1 ELSE 0 END)
            ) / (COUNT(*) * 10)
        ), 2) * 0.3)
    , 2) AS 综合完整率
FROM
    emr_patient_info
GROUP BY
    org_name
ORDER BY
    综合完整率 DESC, 记录总数 DESC;

-- 12. 人群分类其他是否填写
SELECT
    COUNT(*) AS 人群分类其他未填写记录数
FROM
    emr_patient_info
WHERE
    nultitude_type_code = '99' AND  -- 99代表其他，需根据实际代码调整
    (nultitude_type_other IS NULL OR TRIM(nultitude_type_other) = '');

-- 13. 数据长度检查
SELECT
    SUM(CASE WHEN LENGTH(id) > 80 THEN 1 ELSE 0 END) AS id超长记录数,
    SUM(CASE WHEN LENGTH(patient_name) > 100 THEN 1 ELSE 0 END) AS 患者姓名超长记录数,
    SUM(CASE WHEN LENGTH(id_card_type_code) > 2 THEN 1 ELSE 0 END) AS 身份证件类别代码超长记录数,
    SUM(CASE WHEN LENGTH(id_card_type_name) > 20 THEN 1 ELSE 0 END) AS 身份证件类别名称超长记录数,
    SUM(CASE WHEN LENGTH(id_card) > 50 THEN 1 ELSE 0 END) AS 身份证件号码超长记录数,
    SUM(CASE WHEN gender_code IS NOT NULL AND LENGTH(gender_code) > 2 THEN 1 ELSE 0 END) AS 性别代码超长记录数,
    SUM(CASE WHEN gender_name IS NOT NULL AND LENGTH(gender_name) > 10 THEN 1 ELSE 0 END) AS 性别名称超长记录数,
    SUM(CASE WHEN nationality_code IS NOT NULL AND LENGTH(nationality_code) > 5 THEN 1 ELSE 0 END) AS 国籍代码超长记录数,
    SUM(CASE WHEN nationality_name IS NOT NULL AND LENGTH(nationality_name) > 50 THEN 1 ELSE 0 END) AS 国籍名称超长记录数
FROM
    emr_patient_info;

-- 14. 医疗机构代码与名称是否匹配
SELECT
    org_code, 
    org_name,
    COUNT(*) AS 记录数
FROM
    emr_patient_info
GROUP BY
    org_code, org_name
ORDER BY
    COUNT(*) DESC;

-- 15. 编码表匹配检查示例: 身份证件类别代码值域检查
SELECT 
    id_card_type_code, 
    COUNT(*) AS 记录数
FROM 
    emr_patient_info
WHERE 
    id_card_type_code NOT IN ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '99') -- 根据WS364.3-2023 CV02.01.101调整实际代码
    AND id_card_type_code IS NOT NULL
GROUP BY 
    id_card_type_code;

-- 16. 性别代码值域检查
SELECT 
    gender_code, 
    COUNT(*) AS 记录数
FROM 
    emr_patient_info
WHERE 
    gender_code NOT IN ('1', '2', '9', '0') -- 根据GB/T 2261.1-2003调整实际代码
    AND gender_code IS NOT NULL
GROUP BY 
    gender_code;

-- 17. 综合统计各项数据质量情况
SELECT
    '总记录数' AS 检查项目,
    COUNT(*) AS 记录数,
    '100%' AS 占比
FROM
    emr_patient_info

UNION ALL

SELECT
    '缺失ID记录数',
    SUM(CASE WHEN id IS NULL OR TRIM(id) = '' THEN 1 ELSE 0 END),
    ROUND(100.0 * SUM(CASE WHEN id IS NULL OR TRIM(id) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) || '%'
FROM
    emr_patient_info

UNION ALL

SELECT
    '缺失患者姓名记录数',
    SUM(CASE WHEN patient_name IS NULL OR TRIM(patient_name) = '' THEN 1 ELSE 0 END),
    ROUND(100.0 * SUM(CASE WHEN patient_name IS NULL OR TRIM(patient_name) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) || '%'
FROM
    emr_patient_info

UNION ALL

SELECT
    '缺失身份证件类别代码记录数',
    SUM(CASE WHEN id_card_type_code IS NULL OR TRIM(id_card_type_code) = '' THEN 1 ELSE 0 END),
    ROUND(100.0 * SUM(CASE WHEN id_card_type_code IS NULL OR TRIM(id_card_type_code) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) || '%'
FROM
    emr_patient_info

UNION ALL

SELECT
    '缺失身份证件号码记录数',
    SUM(CASE WHEN id_card IS NULL OR TRIM(id_card) = '' THEN 1 ELSE 0 END),
    ROUND(100.0 * SUM(CASE WHEN id_card IS NULL OR TRIM(id_card) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) || '%'
FROM
    emr_patient_info

UNION ALL

SELECT
    '患者姓名格式不规范记录数',
    COUNT(*),
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM emr_patient_info), 2) || '%'
FROM 
    emr_patient_info
WHERE
    patient_name IS NOT NULL AND (
        patient_name ~ '[0-9]' OR
        patient_name ~ '[^a-zA-Z\u4e00-\u9fa5（）.·]' OR
        patient_name ~ '^[（）.·]' OR
        (patient_name ~ '[\s]' AND patient_name ~ '^[\u4e00-\u9fa5（）.·\s]+$')
    )

UNION ALL

SELECT
    '居民身份证格式错误记录数',
    COUNT(*),
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM emr_patient_info WHERE id_card_type_code = '01'), 2) || '%'
FROM
    emr_patient_info
WHERE
    id_card_type_code = '01' AND
    id_card IS NOT NULL AND
    LENGTH(TRIM(id_card)) NOT IN (15, 18)

ORDER BY 检查项目;

-- 18. 按医疗机构统计数据质量情况
SELECT
    org_name AS 医疗机构名称,
    COUNT(*) AS 患者记录总数,
    SUM(CASE WHEN id IS NULL OR TRIM(id) = '' THEN 1 ELSE 0 END) AS ID缺失数,
    SUM(CASE WHEN patient_name IS NULL OR TRIM(patient_name) = '' THEN 1 ELSE 0 END) AS 患者姓名缺失数,
    SUM(CASE WHEN id_card_type_code IS NULL OR TRIM(id_card_type_code) = '' THEN 1 ELSE 0 END) AS 证件类型代码缺失数,
    SUM(CASE WHEN id_card IS NULL OR TRIM(id_card) = '' THEN 1 ELSE 0 END) AS 证件号码缺失数,
    ROUND(100.0 * SUM(CASE WHEN id IS NULL OR TRIM(id) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS ID缺失率,
    ROUND(100.0 * SUM(CASE WHEN patient_name IS NULL OR TRIM(patient_name) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS 患者姓名缺失率,
    ROUND(100.0 * SUM(CASE WHEN id_card_type_code IS NULL OR TRIM(id_card_type_code) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS 证件类型代码缺失率,
    ROUND(100.0 * SUM(CASE WHEN id_card IS NULL OR TRIM(id_card) = '' THEN 1 ELSE 0 END) / COUNT(*), 2) AS 证件号码缺失率
FROM
    emr_patient_info
GROUP BY
    org_name
ORDER BY
    患者记录总数 DESC;















