SELECT loan_id, customer_id, principal
FROM dbo.loans
WHERE product = 'Auto' AND status = 'Default'
ORDER BY loan_id;
