-- 16_applied_insert.sql - load the result into the watch list
-- Step 1: run from BEGIN TRANSACTION to the check query.
BEGIN TRANSACTION;

DELETE FROM dbo.loan_watchlist;

WITH arrears AS (
    SELECT loan_id,
           product,
           status,
           principal,
           ROW_NUMBER() OVER (PARTITION BY product
                              ORDER BY principal DESC)
               AS size_rank
    FROM dbo.loans
    WHERE status <> 'Performing'
)
INSERT INTO dbo.loan_watchlist (loan_id, reason, priority)
SELECT loan_id,
       CONCAT(product, N' ', status, N', rank ', size_rank),
       CASE WHEN status = 'Default' THEN 1 ELSE 2 END
FROM arrears
WHERE size_rank <= 3;

SELECT priority, COUNT(*) AS loans
FROM dbo.loan_watchlist
GROUP BY priority
ORDER BY priority;

-- Step 2: read the check. If it shows 6 and 6, select and
-- run COMMIT only. Otherwise select and run ROLLBACK only.
-- COMMIT;
-- ROLLBACK;
