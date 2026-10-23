-- ex5_ltv_band.sql - LTV bands with a label for NULL
SELECT loan_id,
       product,
       ltv,
       CASE
           WHEN ltv IS NULL THEN 'Not applicable'
           WHEN ltv > 90    THEN 'High (>90%)'
           WHEN ltv > 75    THEN 'Medium (75-90%)'
           ELSE                  'Low (<=75%)'
       END AS ltv_band
FROM dbo.loans
WHERE loan_id BETWEEN 'L00005' AND 'L00012'
ORDER BY loan_id;
