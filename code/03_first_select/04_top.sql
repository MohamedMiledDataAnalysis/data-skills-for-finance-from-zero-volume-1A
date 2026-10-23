-- 04_top.sql - a quick look at the first five accounts
USE Northbridge;
SELECT TOP (5) account_id, customer_id, account_type,
       currency, balance
FROM dbo.accounts
ORDER BY account_id;
