SELECT transaction_id, account_id, txn_date,
       amount, currency, category, channel
FROM dbo.transactions
WHERE txn_date >= '2025-03-01' AND txn_date < '2025-04-01'
  AND currency = 'GBP'
  AND ABS(amount) >= 1000
  AND category NOT IN ('Salary', 'Rent')
ORDER BY ABS(amount) DESC;
