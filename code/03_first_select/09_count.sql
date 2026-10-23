-- 09_count.sql - how many rows does each table hold?
USE Northbridge;
SELECT COUNT(*) AS customer_rows FROM dbo.customers;
SELECT COUNT(*) AS account_rows FROM dbo.accounts;
SELECT COUNT(*) AS transaction_rows FROM dbo.transactions;
SELECT COUNT(*) AS loan_rows FROM dbo.loans;
SELECT COUNT(*) AS fx_rate_rows FROM dbo.fx_rates;
SELECT COUNT(*) AS market_price_rows FROM dbo.market_prices;
