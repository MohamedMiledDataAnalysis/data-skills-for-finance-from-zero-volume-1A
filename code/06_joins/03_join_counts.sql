-- 03_join_counts.sql - row counts before and after joining
SELECT COUNT(*) AS accounts_rows FROM dbo.accounts;

SELECT COUNT(*) AS joined_rows
FROM dbo.accounts AS a
INNER JOIN dbo.customers AS c
    ON a.customer_id = c.customer_id;
