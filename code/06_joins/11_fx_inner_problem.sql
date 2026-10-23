-- 11_fx_inner_problem.sql - an INNER JOIN loses GBP accounts
SELECT COUNT(*) AS accounts_kept
FROM dbo.accounts AS a
INNER JOIN dbo.fx_rates AS fx
    ON  fx.currency  = a.currency
    AND fx.rate_date = '2025-12-31';
