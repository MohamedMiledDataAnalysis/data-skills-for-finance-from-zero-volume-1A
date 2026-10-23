-- 12_offset_fetch.sql - page 2 of the mortgage list
SELECT loan_id, customer_id, principal
FROM dbo.loans
WHERE product = 'Mortgage'
ORDER BY principal DESC
OFFSET 5 ROWS
FETCH NEXT 5 ROWS ONLY;
