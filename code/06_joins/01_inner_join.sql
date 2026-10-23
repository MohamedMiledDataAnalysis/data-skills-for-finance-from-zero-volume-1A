-- 01_inner_join.sql - each account with its owner's name
SELECT accounts.account_id,
       accounts.customer_id,
       customers.last_name,
       accounts.account_type,
       accounts.balance
FROM dbo.accounts
INNER JOIN dbo.customers
    ON accounts.customer_id = customers.customer_id
ORDER BY accounts.account_id;
