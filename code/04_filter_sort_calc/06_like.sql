-- 06_like.sql - pattern matching with wildcards
SELECT customer_id, first_name, last_name, city
FROM dbo.customers
WHERE last_name LIKE 'Wil%'
ORDER BY customer_id;

SELECT COUNT(*) AS cities_ending_on
FROM dbo.customers
WHERE city LIKE '%on';

SELECT DISTINCT category
FROM dbo.transactions
WHERE category LIKE '_e%'
ORDER BY category;
