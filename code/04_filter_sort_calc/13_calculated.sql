-- 13_calculated.sql - annual interest on each loan
SELECT TOP (5) loan_id,
       principal,
       interest_rate,
       principal * interest_rate / 100 AS annual_interest
FROM dbo.loans
ORDER BY loan_id;
