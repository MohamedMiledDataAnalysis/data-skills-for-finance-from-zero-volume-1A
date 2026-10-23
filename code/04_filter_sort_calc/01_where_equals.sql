-- 01_where_equals.sql - only SME customers
SELECT customer_id, last_name, city, segment
FROM dbo.customers
WHERE segment = 'SME'
ORDER BY customer_id;
