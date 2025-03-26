-- check id duplicates
SELECT id, COUNT(*) 
FROM emr_back.emr_order_item 
GROUP BY id 
HAVING COUNT(*) > 1;

WITH duplicates AS (
    SELECT ctid, 
           row_number() OVER (PARTITION BY id ORDER BY ctid) AS rn
    FROM emr_back.emr_order_item
)
DELETE FROM emr_back.emr_order_item
WHERE ctid IN (
    SELECT ctid 
    FROM duplicates 
    WHERE rn > 1
);

-- 创建emr_order_item表的唯一约束
ALTER TABLE emr_back.emr_order_item ADD CONSTRAINT emr_order_item_unique UNIQUE (id);

-- total number of order_item
SELECT COUNT(*) FROM emr_order_item eeci;

-- total number of records in order that have match in order_item
SELECT COUNT(*)
FROM emr_order ec
INNER JOIN emr_order_item eci ON ec.id = eci.order_id;

-- total number of records in order that have no match in order_item
SELECT COUNT(*)
FROM emr_order ec
LEFT JOIN emr_order_item eci ON ec.id = eci.order_id
WHERE eci.id IS NULL;

-- total number of order_item that have match in order
SELECT COUNT(*)
FROM emr_order_item
INNER JOIN emr_order ON emr_order_item.order_id = emr_order.id;

-- total number of order_item that have no match in order
SELECT COUNT(*)
FROM emr_order_item
LEFT JOIN emr_order ON emr_order_item.order_id = emr_order.id
WHERE emr_order.id IS NULL;

-- 查询缺失的患者信息
SELECT emr_order_item.*
FROM emr_order_item
LEFT JOIN emr_order ON emr_order_item.order_id = emr_order.id
WHERE emr_order.id IS NULL;

-- 统计每个组织机构中缺失的患者信息
-- 机构代码只有在 order 表中存在
SELECT ec.org_name, COUNT(*) AS missing_count
FROM emr_order ec
LEFT JOIN emr_order_item eci ON ec.id = eci.order_id
WHERE eci.id IS NULL
GROUP BY ec.org_name;

-- 创建emr_order_item表的外键约束
-- 大量数据无法链接
ALTER TABLE emr_back.emr_order_item ADD CONSTRAINT emr_order_item_emr_order_fk 
FOREIGN KEY (order_id) REFERENCES emr_back.emr_order(id)
not valid;


