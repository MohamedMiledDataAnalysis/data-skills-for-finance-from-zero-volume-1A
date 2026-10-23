-- ex1_paris_lyon.sql - higher-risk customers in Paris or Lyon
SELECT customer_id, first_name, last_name, city, risk_rating
FROM dbo.customers
WHERE city IN ('Paris', 'Lyon')
  AND risk_rating >= 4
ORDER BY risk_rating DESC, customer_id;
