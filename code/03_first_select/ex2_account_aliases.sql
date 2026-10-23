-- ex2_account_aliases.sql - a readable account extract
USE Northbridge;
SELECT TOP (5)
       account_id   AS [Account],
       account_type AS [Type],
       currency     AS [Ccy],
       balance      AS [Balance]
FROM dbo.accounts
ORDER BY account_id;
