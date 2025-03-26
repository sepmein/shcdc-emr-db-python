
-- check id duplicates
SELECT id, COUNT(*) 
FROM emr_back.emr_ex_lab_item 
GROUP BY id 
HAVING COUNT(*) > 1;

WITH duplicates AS (
    SELECT ctid, 
           row_number() OVER (PARTITION BY id ORDER BY ctid) AS rn
    FROM emr_back.emr_ex_lab_item
)
DELETE FROM emr_back.emr_ex_lab_item
WHERE ctid IN (
    SELECT ctid 
    FROM duplicates 
    WHERE rn > 1
);

-- 创建emr_ex_lab_item表的唯一约束
ALTER TABLE emr_back.emr_ex_lab_item ADD CONSTRAINT emr_ex_lab_item_unique UNIQUE (id);


-- total number of lab_item
SELECT COUNT(*) FROM emr_ex_lab_item eeci;

-- total number of records in order that have match in lab_item
SELECT COUNT(*)
FROM emr_ex_lab ec
INNER JOIN emr_ex_lab_item eci ON ec.id = eci.ex_lab_id;

-- total number of records in order that have no match in lab_item
SELECT COUNT(*)
FROM emr_ex_lab ec
LEFT JOIN emr_ex_lab_item eci ON ec.id = eci.ex_lab_id
WHERE eci.id IS NULL;

-- total number of lab_item that have match in order
SELECT COUNT(*)
FROM emr_ex_lab_item
INNER JOIN emr_ex_lab ON emr_ex_lab_item.ex_lab_id = emr_ex_lab.id;

-- total number of lab_item that have no match in order
SELECT COUNT(*)
FROM emr_ex_lab_item
LEFT JOIN emr_ex_lab ON emr_ex_lab_item.ex_lab_id = emr_ex_lab.id
WHERE emr_ex_lab.id IS NULL;

-- 查询缺失的患者信息
SELECT emr_ex_lab_item.*
FROM emr_ex_lab_item
LEFT JOIN emr_ex_lab ON emr_ex_lab_item.ex_lab_id = emr_ex_lab.id
WHERE emr_ex_lab.id IS NULL;

-- 统计每个组织机构中缺失的患者信息
-- 机构代码只有在 order 表中存在
SELECT ec.org_name, COUNT(*) AS missing_count
FROM emr_ex_lab ec
LEFT JOIN emr_ex_lab_item eci ON ec.id = eci.ex_lab_id
WHERE eci.id IS NULL
GROUP BY ec.org_name;

-- 创建emr_ex_lab_item表的外键约束
-- 大量数据无法链接
ALTER TABLE emr_back.emr_ex_lab_item ADD CONSTRAINT emr_ex_lab_item_emr_ex_lab_fk 
FOREIGN KEY (ex_lab_id) REFERENCES emr_back.emr_ex_lab(id)
not valid;

