-- 03_aliases.sql - rename columns in the result
USE Northbridge;
SELECT loan_id          AS [Loan ID],
       product          AS loan_product,
       principal        AS principal_gbp,
       origination_date AS start_date
FROM dbo.loans;
