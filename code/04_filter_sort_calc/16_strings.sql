-- 16_strings.sql - building and cutting text
SELECT TOP (5) customer_id,
       CONCAT(first_name, ' ', last_name) AS full_name,
       UPPER(last_name)                   AS last_upper,
       LEFT(country, 3)                   AS country_3,
       LEN(city)                          AS city_length
FROM dbo.customers
ORDER BY customer_id;
