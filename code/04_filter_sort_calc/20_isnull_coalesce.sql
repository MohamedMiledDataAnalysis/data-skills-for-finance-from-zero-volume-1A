-- 20_isnull_coalesce.sql - replacing NULL
SELECT TOP (5) loan_id,
       product,
       ltv,
       ISNULL(ltv, 0)          AS ltv_isnull,
       COALESCE(ltv, 0)        AS ltv_coalesce,
       COALESCE(CAST(ltv AS VARCHAR(10)), 'n/a')
                               AS ltv_text
FROM dbo.loans
WHERE loan_id IN ('L00005', 'L00006', 'L00007',
                  'L00009', 'L00010')
ORDER BY loan_id;
