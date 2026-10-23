-- ex4_view_gbp.sql - a view of balances converted to GBP
DROP VIEW IF EXISTS dbo.v_account_gbp;
GO
CREATE VIEW dbo.v_account_gbp AS
SELECT a.account_id,
       a.customer_id,
       a.account_type,
       a.currency,
       a.balance,
       CAST(a.balance / COALESCE(fx.rate_per_gbp, 1)
            AS DECIMAL(14,2)) AS balance_gbp
FROM dbo.accounts AS a
LEFT JOIN dbo.fx_rates AS fx
    ON  fx.currency  = a.currency
    AND fx.rate_date = '2025-12-31';
GO
SELECT c.segment,
       COUNT(*)           AS accounts,
       SUM(v.balance_gbp) AS balance_gbp
FROM dbo.v_account_gbp AS v
INNER JOIN dbo.customers AS c
    ON v.customer_id = c.customer_id
GROUP BY c.segment
ORDER BY balance_gbp DESC;
