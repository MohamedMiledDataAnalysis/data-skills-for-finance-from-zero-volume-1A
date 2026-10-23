-- 17_applied_exposure.sql - SME customer net exposure in GBP:
-- loans minus deposits (current and savings accounts)
SELECT TOP (10)
       c.customer_id,
       c.last_name,
       COALESCE(dep.deposits_gbp, 0)  AS deposits_gbp,
       COALESCE(ln.loans_gbp, 0)      AS loans_gbp,
       COALESCE(ln.loans_gbp, 0)
         - COALESCE(dep.deposits_gbp, 0) AS net_exposure
FROM dbo.customers AS c
LEFT JOIN (SELECT a.customer_id,
                  CAST(SUM(a.balance
                           / COALESCE(fx.rate_per_gbp, 1))
                       AS DECIMAL(14,2)) AS deposits_gbp
           FROM dbo.accounts AS a
           LEFT JOIN dbo.fx_rates AS fx
               ON  fx.currency  = a.currency
               AND fx.rate_date = '2025-12-31'
           WHERE a.account_type IN ('Current', 'Savings')
           GROUP BY a.customer_id) AS dep
    ON c.customer_id = dep.customer_id
LEFT JOIN (SELECT customer_id,
                  SUM(principal) AS loans_gbp
           FROM dbo.loans
           GROUP BY customer_id) AS ln
    ON c.customer_id = ln.customer_id
WHERE c.segment = 'SME'
ORDER BY net_exposure DESC;
