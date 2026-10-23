-- 06_three_tables.sql - customer, account and transaction
SELECT TOP (6)
       t.transaction_id,
       t.txn_date,
       c.last_name,
       a.account_type AS type,
       t.amount,
       t.currency
FROM dbo.transactions AS t
INNER JOIN dbo.accounts AS a
    ON t.account_id = a.account_id
INNER JOIN dbo.customers AS c
    ON a.customer_id = c.customer_id
WHERE t.amount < -3000
ORDER BY t.amount, t.transaction_id;
