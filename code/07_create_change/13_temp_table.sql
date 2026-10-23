-- 13_temp_table.sql - SQL Server only: a scratch table
DROP TABLE IF EXISTS #arrears;

SELECT loan_id, customer_id, product, principal, status
INTO #arrears
FROM dbo.loans
WHERE status <> 'Performing';

SELECT product,
       COUNT(*)       AS loans,
       SUM(principal) AS principal
FROM #arrears
GROUP BY product
ORDER BY principal DESC;

DROP TABLE #arrears;
