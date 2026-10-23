-- 08_duplication_trap.sql - one customer, joined two ways
SELECT COUNT(*) AS account_rows
FROM dbo.accounts WHERE customer_id = 'C0010';

SELECT COUNT(*) AS loan_rows
FROM dbo.loans WHERE customer_id = 'C0010';

SELECT SUM(balance) AS true_balance
FROM dbo.accounts WHERE customer_id = 'C0010';

SELECT SUM(principal) AS true_principal
FROM dbo.loans WHERE customer_id = 'C0010';

SELECT COUNT(*)          AS joined_rows,
       SUM(a.balance)    AS wrong_balance,
       SUM(l.principal)  AS wrong_principal
FROM dbo.customers AS c
INNER JOIN dbo.accounts AS a
    ON c.customer_id = a.customer_id
INNER JOIN dbo.loans AS l
    ON c.customer_id = l.customer_id
WHERE c.customer_id = 'C0010';
