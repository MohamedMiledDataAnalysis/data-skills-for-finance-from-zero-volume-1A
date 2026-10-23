-- 16b_applied_review.sql - the committed watch list
SELECT w.priority, w.loan_id, w.reason, l.principal
FROM dbo.loan_watchlist AS w
INNER JOIN dbo.loans AS l
    ON w.loan_id = l.loan_id
ORDER BY w.priority, l.principal DESC;
