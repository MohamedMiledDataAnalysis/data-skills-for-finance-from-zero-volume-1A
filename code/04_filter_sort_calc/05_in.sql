-- 05_in.sql - loans in arrears or default
SELECT loan_id, product, principal, status
FROM dbo.loans
WHERE status IN ('30+ DPD', '90+ DPD', 'Default')
ORDER BY loan_id;
