-- ex3_city_spend.sql - salary credits by customer city, 2025
SELECT c.city,
       COUNT(DISTINCT c.customer_id) AS salaried_customers,
       SUM(t.amount)                 AS salary_total
FROM dbo.transactions AS t
INNER JOIN dbo.accounts AS a
    ON t.account_id = a.account_id
INNER JOIN dbo.customers AS c
    ON a.customer_id = c.customer_id
WHERE t.category = 'Salary'
  AND t.currency = 'GBP'
GROUP BY c.city
ORDER BY salary_total DESC;
