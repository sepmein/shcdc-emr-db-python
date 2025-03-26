-- check id duplicates
SELECT id, COUNT(*) 
FROM emr_back.emr_ex_clinical_item 
GROUP BY id 
HAVING COUNT(*) > 1;

WITH duplicates AS (
    SELECT ctid, 
           row_number() OVER (PARTITION BY id ORDER BY ctid) AS rn
    FROM emr_back.emr_ex_clinical_item
)
DELETE FROM emr_back.emr_ex_clinical_item
WHERE ctid IN (
    SELECT ctid 
    FROM duplicates 
    WHERE rn > 1
);

-- 创建emr_ex_clinical_item表的唯一约束
ALTER TABLE emr_back.emr_ex_clinical_item ADD CONSTRAINT emr_ex_clinical_item_unique UNIQUE (id);

-- total number of records in ex_clinical that have match in ex_clinical_item
SELECT COUNT(*)
FROM emr_ex_clinical ec
INNER JOIN emr_ex_clinical_item eci ON ec.id = eci.ex_clinical_id;

-- total number of records in ex_clinical that have no match in ex_clinical_item
SELECT COUNT(*)
FROM emr_ex_clinical ec
LEFT JOIN emr_ex_clinical_item eci ON ec.id = eci.ex_clinical_id
WHERE eci.id IS NULL;

-- emr clinical item connection with clinical 
-- 查询缺失的患者信息
SELECT emr_ex_clinical_item.*
FROM emr_ex_clinical_item
LEFT JOIN emr_ex_clinical ON emr_ex_clinical_item.ex_clinical_id = emr_ex_clinical.id
WHERE emr_ex_clinical.id IS NULL;

-- 统计每个组织机构中缺失的患者信息
-- 机构代码只有在 clinical 表中存在
SELECT ec.org_name, COUNT(*) AS missing_count
FROM emr_ex_clinical ec
LEFT JOIN emr_ex_clinical_item eci ON ec.id = eci.ex_clinical_id
WHERE eci.id IS NULL
GROUP BY ec.org_name;

-- total number of ex_clinical_item
select count(*) from emr_ex_clinical_item eeci ;

-- total number of ex_clinical_item that have match in ex_clinical
SELECT COUNT(*)
FROM emr_ex_clinical_item
INNER JOIN emr_ex_clinical ON emr_ex_clinical_item.ex_clinical_id = emr_ex_clinical.id;

-- total number of ex_clinical_item that have no match in ex_clinical
SELECT COUNT(*)
FROM emr_ex_clinical_item
LEFT JOIN emr_ex_clinical ON emr_ex_clinical_item.ex_clinical_id = emr_ex_clinical.id
WHERE emr_ex_clinical.id IS NULL;

-- 创建emr_ex_clinical_item表的外键约束
-- 大量数据无法链接
ALTER TABLE emr_back.emr_ex_clinical_item ADD CONSTRAINT emr_ex_clinical_item_emr_ex_clinical_fk FOREIGN KEY (ex_clinical_id) REFERENCES emr_back.emr_ex_clinical(id)
not valid;



