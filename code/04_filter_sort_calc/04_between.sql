-- 04_between.sql - loans originated in 2024
SELECT loan_id, product, principal, origination_date
FROM dbo.loans
WHERE origination_date BETWEEN '2024-01-01' AND '2024-12-31'
ORDER BY loan_id;
