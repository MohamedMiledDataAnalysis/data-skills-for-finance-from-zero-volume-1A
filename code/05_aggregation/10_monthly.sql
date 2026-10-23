-- 10_monthly.sql - money in and out per month, 2025
SELECT YEAR(txn_date)  AS txn_year,
       MONTH(txn_date) AS txn_month,
       COUNT(*)        AS txn_count,
       SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END)
                       AS money_in,
       SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END)
                       AS money_out,
       SUM(amount)     AS net_flow
FROM dbo.transactions
WHERE currency = 'GBP'
GROUP BY YEAR(txn_date), MONTH(txn_date)
ORDER BY txn_year, txn_month;
