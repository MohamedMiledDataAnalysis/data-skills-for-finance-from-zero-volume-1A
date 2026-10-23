-- 03_insert_select.sql - add every 30+ DPD mortgage at once
INSERT INTO dbo.loan_watchlist (loan_id, reason, priority)
SELECT loan_id,
       CONCAT(N'Mortgage ', status),
       3
FROM dbo.loans
WHERE product = 'Mortgage'
  AND status = '30+ DPD'
ORDER BY loan_id;

SELECT COUNT(*) AS watchlist_rows FROM dbo.loan_watchlist;

SELECT TOP (5) * FROM dbo.loan_watchlist
ORDER BY watch_id DESC;
