-- 13b_sme_count_check.sql - SME arrears by count, same
-- population as the ALCO summary
SELECT COUNT(*) AS sme_loans,
       SUM(CASE WHEN status <> 'Performing' THEN 1 ELSE 0 END)
           AS in_arrears,
       CAST(100.0
            * SUM(CASE WHEN status <> 'Performing'
                       THEN 1 ELSE 0 END)
            / COUNT(*) AS DECIMAL(5,2)) AS arrears_pct_count
FROM dbo.loans
WHERE product = 'SME'
  AND origination_date < '2025-07-01';
