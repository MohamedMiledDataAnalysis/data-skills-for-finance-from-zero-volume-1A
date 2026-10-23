-- 09_null.sql - NULL is not a value, it is "unknown"
SELECT COUNT(*) AS equals_null
FROM dbo.loans
WHERE ltv = NULL;

SELECT COUNT(*) AS is_null
FROM dbo.loans
WHERE ltv IS NULL;

SELECT COUNT(*) AS is_not_null
FROM dbo.loans
WHERE ltv IS NOT NULL;
