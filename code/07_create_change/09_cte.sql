-- 09_cte.sql - name a step, then use it
WITH customer_balance AS (
    SELECT customer_id,
           SUM(balance) AS total_balance
    FROM dbo.accounts
    WHERE currency = 'GBP'
    GROUP BY customer_id
)
SELECT c.segment,
       COUNT(*)                                 AS customers,
       CAST(AVG(cb.total_balance) AS DECIMAL(14,2))
                                                AS avg_balance
FROM customer_balance AS cb
INNER JOIN dbo.customers AS c
    ON cb.customer_id = c.customer_id
GROUP BY c.segment
ORDER BY avg_balance DESC;
