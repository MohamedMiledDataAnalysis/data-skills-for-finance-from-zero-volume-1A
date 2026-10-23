-- 04_group_by.sql - the loan book by product
SELECT product,
       COUNT(*)        AS loan_count,
       SUM(principal)  AS total_principal
FROM dbo.loans
GROUP BY product
ORDER BY total_principal DESC;
