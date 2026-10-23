-- 02_where_compare.sql - overdrawn accounts
SELECT account_id, customer_id, currency, balance
FROM dbo.accounts
WHERE balance < 0
ORDER BY account_id;
