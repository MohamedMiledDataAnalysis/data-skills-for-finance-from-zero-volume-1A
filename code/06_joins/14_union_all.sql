-- 14_union_all.sql - GBP account balances and loans, stacked
SELECT 'Accounts (GBP)' AS side,
       COUNT(*)         AS items,
       SUM(balance)     AS amount_gbp
FROM dbo.accounts
WHERE currency = 'GBP'
UNION ALL
SELECT 'Loans',
       COUNT(*),
       SUM(principal)
FROM dbo.loans;
