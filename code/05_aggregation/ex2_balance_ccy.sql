-- ex2_balance_ccy.sql - balances by currency and account type
SELECT currency,
       account_type,
       COUNT(*)     AS accounts,
       SUM(balance) AS total_balance,
       MIN(balance) AS lowest_balance
FROM dbo.accounts
GROUP BY currency, account_type
ORDER BY currency, account_type;
