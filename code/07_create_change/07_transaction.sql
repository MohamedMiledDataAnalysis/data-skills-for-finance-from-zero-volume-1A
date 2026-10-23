-- 07_transaction.sql - a safety net around a change
SELECT COUNT(*) AS rows_before
FROM dbo.loan_watchlist;

SELECT COUNT(*) AS rows_to_delete
FROM dbo.loan_watchlist
WHERE priority = 3;

BEGIN TRANSACTION;

DELETE FROM dbo.loan_watchlist
WHERE priority = 3;

SELECT COUNT(*) AS rows_inside_transaction
FROM dbo.loan_watchlist;

ROLLBACK;

SELECT COUNT(*) AS rows_after_rollback
FROM dbo.loan_watchlist;
