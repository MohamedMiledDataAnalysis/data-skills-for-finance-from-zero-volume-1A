-- 05_group_by_two.sql - product and status together
SELECT product,
       status,
       COUNT(*)       AS loan_count,
       SUM(principal) AS total_principal
FROM dbo.loans
GROUP BY product, status
ORDER BY product, status;
