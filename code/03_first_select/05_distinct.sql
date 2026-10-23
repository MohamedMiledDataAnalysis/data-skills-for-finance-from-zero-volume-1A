-- 05_distinct.sql - the different values a column holds
USE Northbridge;
SELECT DISTINCT product
FROM dbo.loans
ORDER BY product;

SELECT DISTINCT product, status
FROM dbo.loans
ORDER BY product, status;
