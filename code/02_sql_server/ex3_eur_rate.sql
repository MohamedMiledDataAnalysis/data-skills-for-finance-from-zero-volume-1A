-- ex3_eur_rate.sql - the last EUR rate of 2025
USE Northbridge;
SELECT TOP 1 rate_date, rate_per_gbp
FROM dbo.fx_rates
WHERE currency = 'EUR'
ORDER BY rate_date DESC;
