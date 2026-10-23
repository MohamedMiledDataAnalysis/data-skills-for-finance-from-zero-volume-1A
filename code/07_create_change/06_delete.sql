-- 06_delete.sql - remove one row, then check
DELETE FROM dbo.loan_watchlist
WHERE loan_id = 'L00888';

SELECT COUNT(*) AS watchlist_rows FROM dbo.loan_watchlist;
