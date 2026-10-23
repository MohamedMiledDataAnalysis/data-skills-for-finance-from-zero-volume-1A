-- 10_distinct_count.sql - distinct values, counted
USE Northbridge;
SELECT COUNT(DISTINCT customer_id) AS customers_with_loans
FROM dbo.loans;
