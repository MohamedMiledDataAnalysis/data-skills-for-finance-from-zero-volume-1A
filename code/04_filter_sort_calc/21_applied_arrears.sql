-- 21_applied_arrears.sql - arrears watch list for credit risk
SELECT loan_id,
       product,
       status,
       principal,
       CAST(principal * interest_rate / 100
            AS DECIMAL(14,2))                    AS interest,
       COALESCE(CAST(ltv AS VARCHAR(10)), 'n/a') AS ltv,
       CASE
           WHEN status = 'Default' THEN 'Red'
           WHEN status = '90+ DPD' THEN 'Amber'
           ELSE 'Yellow'
       END                                       AS flag
FROM dbo.loans
WHERE status IN ('30+ DPD', '90+ DPD', 'Default')
  AND origination_date >= '2022-01-01'
  AND principal >= 100000
ORDER BY principal DESC;
