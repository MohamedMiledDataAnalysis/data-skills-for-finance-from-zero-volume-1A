-- 02_choose_columns.sql - only the columns you need
USE Northbridge;
SELECT customer_id, last_name, segment, risk_rating
FROM dbo.customers;
