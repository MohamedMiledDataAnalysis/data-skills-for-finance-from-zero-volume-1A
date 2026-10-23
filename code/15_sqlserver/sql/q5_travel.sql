SELECT txn_date, account_id, amount, channel
FROM dbo.transactions
WHERE category = 'Travel' AND currency = 'GBP' AND amount < -2000
ORDER BY amount;
