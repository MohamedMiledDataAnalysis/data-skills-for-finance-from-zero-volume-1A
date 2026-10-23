-- 02_aliases.sql - the same join with table aliases
SELECT a.account_id,
       c.customer_id,
       c.last_name,
       c.segment,
       a.currency,
       a.balance
FROM dbo.accounts AS a
INNER JOIN dbo.customers AS c
    ON a.customer_id = c.customer_id
WHERE c.segment = 'Private'
ORDER BY a.balance DESC;
