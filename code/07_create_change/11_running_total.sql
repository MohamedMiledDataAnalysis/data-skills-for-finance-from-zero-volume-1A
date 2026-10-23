-- 11_running_total.sql - monthly net flow and running total
WITH monthly AS (
    SELECT MONTH(txn_date) AS txn_month,
           SUM(amount)     AS net_flow
    FROM dbo.transactions
    WHERE currency = 'GBP'
      AND txn_date >= '2025-01-01'
      AND txn_date <  '2026-01-01'
    GROUP BY MONTH(txn_date)
)
SELECT txn_month,
       net_flow,
       SUM(net_flow) OVER (ORDER BY txn_month
                           ROWS UNBOUNDED PRECEDING)
           AS running_total
FROM monthly
ORDER BY txn_month;
