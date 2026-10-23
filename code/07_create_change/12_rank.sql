-- 12_rank.sql - the ten customers with the largest GBP balances
WITH customer_balance AS (
    SELECT customer_id,
           SUM(balance) AS total_balance
    FROM dbo.accounts
    WHERE currency = 'GBP'
    GROUP BY customer_id
)
SELECT TOP (10)
       customer_id,
       total_balance,
       RANK() OVER (ORDER BY total_balance DESC) AS balance_rank
FROM customer_balance
ORDER BY balance_rank;
