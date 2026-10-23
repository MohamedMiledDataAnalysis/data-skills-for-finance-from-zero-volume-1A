-- 05_update_no_where.sql - what a missing WHERE does
SELECT COUNT(*) AS reviewed_before
FROM dbo.loan_watchlist
WHERE reviewed = 1;

-- Meant to mark watch_id 1 only; the WHERE line was forgotten
UPDATE dbo.loan_watchlist
SET reviewed = 1;

SELECT COUNT(*) AS reviewed_after
FROM dbo.loan_watchlist
WHERE reviewed = 1;

-- Repair: put every row back, then do the intended change
UPDATE dbo.loan_watchlist
SET reviewed = 0;

UPDATE dbo.loan_watchlist
SET reviewed = 1
WHERE watch_id = 1;

SELECT COUNT(*) AS reviewed_now
FROM dbo.loan_watchlist
WHERE reviewed = 1;
