-- 02_aggregates_rounded.sql - predictable decimals
SELECT CAST(AVG(principal) AS DECIMAL(14,2))  AS avg_principal,
       CAST(AVG(interest_rate) AS DECIMAL(5,2)) AS avg_rate,
       MIN(origination_date)                  AS first_loan,
       MAX(origination_date)                  AS last_loan
FROM dbo.loans;
