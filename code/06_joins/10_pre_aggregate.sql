-- 10_pre_aggregate.sql - aggregate first, then join
SELECT c.customer_id,
       c.last_name,
       acc.accounts,
       acc.balance,
       ln.loans,
       ln.principal
FROM dbo.customers AS c
INNER JOIN (SELECT customer_id,
                   COUNT(*)     AS accounts,
                   SUM(balance) AS balance
            FROM dbo.accounts
            GROUP BY customer_id) AS acc
    ON c.customer_id = acc.customer_id
INNER JOIN (SELECT customer_id,
                   COUNT(*)       AS loans,
                   SUM(principal) AS principal
            FROM dbo.loans
            GROUP BY customer_id) AS ln
    ON c.customer_id = ln.customer_id
WHERE c.customer_id IN ('C0005', 'C0010', 'C0020')
ORDER BY c.customer_id;
