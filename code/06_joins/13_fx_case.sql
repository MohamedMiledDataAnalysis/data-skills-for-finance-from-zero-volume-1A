-- 13_fx_case.sql - the same rate chosen with CASE
SELECT a.currency,
       COUNT(*) AS accounts,
       SUM(a.balance) AS balance_local,
       CAST(SUM(a.balance /
                CASE WHEN a.currency = 'GBP' THEN 1
                     ELSE fx.rate_per_gbp END)
            AS DECIMAL(14,2)) AS balance_gbp,
       SUM(CASE WHEN a.currency <> 'GBP'
                 AND fx.rate_per_gbp IS NULL
                THEN 1 ELSE 0 END) AS missing_rates
FROM dbo.accounts AS a
LEFT JOIN dbo.fx_rates AS fx
    ON  fx.currency  = a.currency
    AND fx.rate_date = '2025-12-31'
GROUP BY a.currency
ORDER BY a.currency;
