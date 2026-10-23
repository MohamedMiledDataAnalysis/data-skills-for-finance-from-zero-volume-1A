-- 11_top_order.sql - the five largest mortgages
SELECT TOP (5) loan_id, customer_id, principal, ltv
FROM dbo.loans
WHERE product = 'Mortgage'
ORDER BY principal DESC;
