-- ex4_txn_counts.sql - how busy is the transactions table?
USE Northbridge;
SELECT COUNT(*)                   AS txn_rows,
       COUNT(DISTINCT account_id) AS active_accounts,
       COUNT(DISTINCT category)   AS categories,
       COUNT(DISTINCT channel)    AS channels
FROM dbo.transactions;
