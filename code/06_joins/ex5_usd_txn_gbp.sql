-- ex5_usd_txn_gbp.sql - USD transactions converted at the
-- rate of the transaction date
SELECT TOP (5)
       t.transaction_id,
       t.txn_date,
       t.amount,
       fx.rate_per_gbp,
       CAST(t.amount / fx.rate_per_gbp AS DECIMAL(14,2))
           AS amount_gbp
FROM dbo.transactions AS t
INNER JOIN dbo.fx_rates AS fx
    ON  fx.currency  = t.currency
    AND fx.rate_date = t.txn_date
WHERE t.currency = 'USD'
ORDER BY t.txn_date, t.transaction_id;

SELECT COUNT(*) AS usd_txns
FROM dbo.transactions
WHERE currency = 'USD';

SELECT COUNT(*) AS usd_txns_with_rate
FROM dbo.transactions AS t
INNER JOIN dbo.fx_rates AS fx
    ON  fx.currency  = t.currency
    AND fx.rate_date = t.txn_date
WHERE t.currency = 'USD';
