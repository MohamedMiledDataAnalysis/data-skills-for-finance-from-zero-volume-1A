-- ex6_union_flags.sql - one alert list from two rules
-- (the overdraft threshold is 1,000 in each account's currency)
SELECT a.customer_id,
       'Overdrawn account' AS alert,
       a.account_id        AS reference
FROM dbo.accounts AS a
WHERE a.balance < -1000
UNION ALL
SELECT l.customer_id,
       'Defaulted loan',
       l.loan_id
FROM dbo.loans AS l
WHERE l.status = 'Default'
  AND l.principal > 400000
ORDER BY customer_id, alert;
