-- ex3_safe_delete.sql - test a delete before keeping it
SELECT COUNT(*) AS rows_before
FROM dbo.overdrawn_accounts;

SELECT COUNT(*) AS rows_to_delete
FROM dbo.overdrawn_accounts
WHERE balance > -500;

BEGIN TRANSACTION;

DELETE FROM dbo.overdrawn_accounts
WHERE balance > -500;

SELECT COUNT(*) AS rows_inside
FROM dbo.overdrawn_accounts;

ROLLBACK;

SELECT COUNT(*) AS rows_after_rollback
FROM dbo.overdrawn_accounts;
