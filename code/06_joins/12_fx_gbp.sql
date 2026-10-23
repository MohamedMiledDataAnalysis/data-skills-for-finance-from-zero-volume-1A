-- 12_fx_gbp.sql - every balance in GBP at 31 Dec 2025
SELECT a.account_id,
       a.currency,
       a.balance,
       COALESCE(fx.rate_per_gbp, 1) AS rate_per_gbp,
       CAST(a.balance / COALESCE(fx.rate_per_gbp, 1)
            AS DECIMAL(14,2))       AS balance_gbp
FROM dbo.accounts AS a
LEFT JOIN dbo.fx_rates AS fx
    ON  fx.currency  = a.currency
    AND fx.rate_date = '2025-12-31'
WHERE a.account_id IN ('A00001', 'A00002', 'A00003',
                       'A00004', 'A00006')
ORDER BY a.account_id;
