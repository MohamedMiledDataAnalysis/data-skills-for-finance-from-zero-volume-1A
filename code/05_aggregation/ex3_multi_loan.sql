-- ex3_multi_loan.sql - customers holding five or more loans
SELECT customer_id,
       COUNT(*)       AS loan_count,
       SUM(principal) AS total_principal
FROM dbo.loans
GROUP BY customer_id
HAVING COUNT(*) >= 5
ORDER BY loan_count DESC, total_principal DESC;
