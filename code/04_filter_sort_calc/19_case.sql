-- 19_case.sql - LTV risk bands for mortgages
SELECT loan_id,
       ltv,
       CASE
           WHEN ltv > 90 THEN 'High'
           WHEN ltv > 75 THEN 'Medium'
           ELSE 'Low'
       END AS ltv_band
FROM dbo.loans
WHERE loan_id IN ('L00007', 'L00010', 'L00012',
                  'L00020', 'L00044', 'L00078')
ORDER BY loan_id;
