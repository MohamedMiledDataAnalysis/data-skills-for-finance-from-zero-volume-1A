-- ex6_ltv_bands.sql - mortgage exposure by LTV band
SELECT CASE
           WHEN ltv > 90 THEN '3 High (>90%)'
           WHEN ltv > 75 THEN '2 Medium (75-90%)'
           ELSE               '1 Low (<=75%)'
       END                                   AS ltv_band,
       COUNT(*)                              AS mortgages,
       SUM(principal)                        AS exposure,
       CAST(SUM(principal * interest_rate)
            / SUM(principal) AS DECIMAL(5,2)) AS wavg_rate
FROM dbo.loans
WHERE product = 'Mortgage'
GROUP BY CASE
             WHEN ltv > 90 THEN '3 High (>90%)'
             WHEN ltv > 75 THEN '2 Medium (75-90%)'
             ELSE               '1 Low (<=75%)'
         END
ORDER BY ltv_band;
