-- 10_order_by.sql - sorting results
SELECT loan_id, product, principal
FROM dbo.loans
WHERE product = 'Auto'
ORDER BY principal DESC;

SELECT customer_id, segment, risk_rating, last_name
FROM dbo.customers
ORDER BY risk_rating DESC, segment ASC, last_name,
         customer_id;
