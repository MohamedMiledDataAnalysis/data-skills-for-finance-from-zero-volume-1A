-- 06_where_having.sql - filter rows, then filter groups
SELECT city,
       COUNT(*) AS customer_count
FROM dbo.customers
WHERE segment = 'Retail'
GROUP BY city
HAVING COUNT(*) >= 30
ORDER BY customer_count DESC;
