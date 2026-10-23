-- ex5_overdrawn.sql - sterling current accounts overdrawn
-- by more than 500 pounds
USE Northbridge;
SELECT COUNT(*) AS overdrawn
FROM dbo.accounts
WHERE account_type = 'Current' AND currency = 'GBP'
  AND balance < -500;

SELECT TOP 3 account_id, customer_id, balance
FROM dbo.accounts
WHERE account_type = 'Current' AND currency = 'GBP'
  AND balance < -500
ORDER BY balance;
