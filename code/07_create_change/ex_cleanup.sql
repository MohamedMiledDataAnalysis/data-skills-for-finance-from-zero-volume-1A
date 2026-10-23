-- ex_cleanup.sql - remove the exercise objects
DROP VIEW IF EXISTS dbo.v_account_gbp;
DROP TABLE IF EXISTS dbo.overdrawn_accounts;
DROP TABLE IF EXISTS dbo.branch_targets;
