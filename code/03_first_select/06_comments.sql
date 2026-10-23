/* 06_comments.sql
   Author : your name
   Purpose: list the FX rates table for a first look.
*/
USE Northbridge;
SELECT TOP (4) rate_date,     -- weekday
       currency,              -- EUR or USD
       rate_per_gbp           -- units of currency per GBP 1
FROM dbo.fx_rates
ORDER BY rate_date, currency;
