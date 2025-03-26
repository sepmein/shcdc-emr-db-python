-- 创建emr_activity_info表的唯一约束
Create unique constraint for emr_activity_info table
ALTER TABLE emr_back.emr_activity_info ADD CONSTRAINT emr_activity_info_unique UNIQUE (id);

-- check id duplicates
SELECT id, COUNT(*) 
FROM emr_back.emr_activity_info 
GROUP BY id 
HAVING COUNT(*) > 1;