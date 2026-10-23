-- ex2_no_accounts_txn.sql - accounts with no 2025 transaction
SELECT COUNT(*) AS silent_accounts
FROM dbo.accounts AS a
LEFT JOIN dbo.transactions AS t
    ON  a.account_id = t.account_id
    AND t.txn_date BETWEEN '2025-01-01' AND '2025-12-31'
WHERE t.transaction_id IS NULL;

SELECT a.account_type,
       COUNT(*) AS silent_accounts
FROM dbo.accounts AS a
LEFT JOIN dbo.transactions AS t
    ON  a.account_id = t.account_id
    AND t.txn_date BETWEEN '2025-01-01' AND '2025-12-31'
WHERE t.transaction_id IS NULL
GROUP BY a.account_type
ORDER BY a.account_type;
