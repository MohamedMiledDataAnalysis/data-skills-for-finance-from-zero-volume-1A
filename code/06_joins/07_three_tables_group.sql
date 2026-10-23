-- 07_three_tables_group.sql - 2025 GBP card spend by segment
SELECT c.segment,
       COUNT(*)      AS txn_count,
       -SUM(t.amount) AS card_spend
FROM dbo.transactions AS t
INNER JOIN dbo.accounts AS a
    ON t.account_id = a.account_id
INNER JOIN dbo.customers AS c
    ON a.customer_id = c.customer_id
WHERE t.channel = 'Card'
  AND t.currency = 'GBP'
  AND t.amount < 0
GROUP BY c.segment
ORDER BY card_spend DESC;
