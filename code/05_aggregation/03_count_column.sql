-- 03_count_column.sql - COUNT(*) versus COUNT(column)
SELECT COUNT(*)                AS all_rows,
       COUNT(ltv)              AS rows_with_ltv,
       COUNT(DISTINCT product) AS products,
       CAST(AVG(ltv) AS DECIMAL(5,1))   AS avg_ltv,
       CAST(AVG(COALESCE(ltv, 0)) AS DECIMAL(5,1))
                               AS avg_ltv_wrong
FROM dbo.loans;
