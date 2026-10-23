-- 02_insert_values.sql - add rows one by one
INSERT INTO dbo.loan_watchlist (loan_id, reason, priority)
VALUES ('L00460', N'SME default', 1);

INSERT INTO dbo.loan_watchlist (loan_id, reason, priority)
VALUES ('L00527', N'Mortgage default', 1),
       ('L00888', N'Mortgage 90+ DPD', 2);

SELECT * FROM dbo.loan_watchlist
ORDER BY watch_id;
