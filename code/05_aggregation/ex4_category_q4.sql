-- ex4_category_q4.sql - card spending by category, Q4 2025
SELECT category,
       COUNT(*)                         AS txn_count,
       -SUM(amount)                     AS spend_gbp,
       CAST(-AVG(amount) AS DECIMAL(10,2)) AS avg_spend
FROM dbo.transactions
WHERE channel = 'Card'
  AND currency = 'GBP'
  AND amount < 0
  AND txn_date >= '2025-10-01'
GROUP BY category
HAVING -SUM(amount) > 10000
ORDER BY spend_gbp DESC;
