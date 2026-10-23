SELECT TOP (5) loan_id, product, principal
FROM dbo.loans
ORDER BY principal DESC;
