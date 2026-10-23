-- ex2_large_outflows.sql - outflows above 5,000 in Q1 2025
SELECT transaction_id, account_id, txn_date, amount,
       currency
FROM dbo.transactions
WHERE amount < -5000
  AND txn_date BETWEEN '2025-01-01' AND '2025-03-31'
ORDER BY amount ASC, transaction_id;
