-- ex2_top_customers.sql - first five customers by ID
USE Northbridge;
SELECT TOP 5 customer_id, first_name, last_name, segment
FROM dbo.customers
ORDER BY customer_id;
