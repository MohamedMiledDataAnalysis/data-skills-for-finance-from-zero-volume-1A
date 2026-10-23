-- 09_duplication_whole.sql - the trap across the whole bank
SELECT COUNT(*)         AS joined_rows,
       SUM(l.principal) AS inflated_principal
FROM dbo.accounts AS a
INNER JOIN dbo.loans AS l
    ON a.customer_id = l.customer_id;

SELECT SUM(principal) AS true_principal
FROM dbo.loans;
