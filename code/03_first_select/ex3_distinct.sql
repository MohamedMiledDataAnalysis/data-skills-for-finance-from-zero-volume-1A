-- ex3_distinct.sql - tickers, and currency/type pairs
USE Northbridge;
SELECT DISTINCT ticker
FROM dbo.market_prices
ORDER BY ticker;

SELECT DISTINCT currency, account_type
FROM dbo.accounts
ORDER BY currency, account_type;
