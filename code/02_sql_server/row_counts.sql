-- row_counts.sql - check that every Northbridge table loaded
USE Northbridge;
SELECT 'customers' AS table_name, COUNT(*) AS row_count
FROM dbo.customers
UNION ALL SELECT 'accounts', COUNT(*) FROM dbo.accounts
UNION ALL SELECT 'transactions', COUNT(*) FROM dbo.transactions
UNION ALL SELECT 'loans', COUNT(*) FROM dbo.loans
UNION ALL SELECT 'fx_rates', COUNT(*) FROM dbo.fx_rates
UNION ALL SELECT 'market_prices', COUNT(*) FROM dbo.market_prices;
