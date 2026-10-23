-- 04_update.sql - raise the priority of large 30+ DPD loans
SELECT w.watch_id, w.loan_id, w.priority, l.principal
FROM dbo.loan_watchlist AS w
INNER JOIN dbo.loans AS l
    ON w.loan_id = l.loan_id
WHERE w.priority = 3
  AND l.principal > 300000
ORDER BY w.watch_id;

UPDATE dbo.loan_watchlist
SET priority = 2,
    reason   = CONCAT(reason, N' - above 300k')
WHERE priority = 3
  AND loan_id IN (SELECT loan_id
                  FROM dbo.loans
                  WHERE principal > 300000);

SELECT watch_id, loan_id, reason, priority
FROM dbo.loan_watchlist
WHERE priority = 2
ORDER BY watch_id;
