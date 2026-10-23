SELECT product, status, principal FROM dbo.loans;
SELECT COUNT(*) AS n
FROM (SELECT DISTINCT product, status FROM dbo.loans) AS s;
