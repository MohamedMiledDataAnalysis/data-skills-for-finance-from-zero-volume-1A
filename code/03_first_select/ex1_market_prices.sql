-- ex1_market_prices.sql - first look at market prices
USE Northbridge;
SELECT TOP (5) *
FROM dbo.market_prices
ORDER BY price_date, ticker;
