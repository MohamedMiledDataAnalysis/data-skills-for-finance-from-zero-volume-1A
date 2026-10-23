-- ex4_trap_fix.sql - GBP balances and loans by segment
-- Wrong: joins accounts and loans directly
SELECT c.segment,
       SUM(a.balance) AS gbp_balance
FROM dbo.customers AS c
INNER JOIN dbo.accounts AS a
    ON c.customer_id = a.customer_id
INNER JOIN dbo.loans AS l
    ON c.customer_id = l.customer_id
WHERE a.currency = 'GBP'
GROUP BY c.segment
ORDER BY c.segment;

-- Right: aggregate each table first, then join
SELECT c.segment,
       SUM(acc.gbp_balance)    AS gbp_balance,
       SUM(ln.total_principal) AS principal
FROM dbo.customers AS c
LEFT JOIN (SELECT customer_id,
                  SUM(balance) AS gbp_balance
           FROM dbo.accounts
           WHERE currency = 'GBP'
           GROUP BY customer_id) AS acc
    ON c.customer_id = acc.customer_id
LEFT JOIN (SELECT customer_id,
                  SUM(principal) AS total_principal
           FROM dbo.loans
           GROUP BY customer_id) AS ln
    ON c.customer_id = ln.customer_id
GROUP BY c.segment
ORDER BY c.segment;

-- Check: the true totals straight from each table
SELECT SUM(balance) AS gbp_balance_check
FROM dbo.accounts
WHERE currency = 'GBP';
