-- 08_integer_trap.sql - integer division gives the wrong answer
SELECT product,
       SUM(CASE WHEN status <> 'Performing' THEN 1 ELSE 0 END)
           AS arrears_count,
       COUNT(*) AS loan_count,
       SUM(CASE WHEN status <> 'Performing' THEN 1 ELSE 0 END)
           / COUNT(*) AS wrong_rate
FROM dbo.loans
GROUP BY product
ORDER BY product;

SELECT AVG(risk_rating) AS avg_rating_int,
       AVG(risk_rating * 1.0) AS avg_rating_dec,
       CAST(AVG(CAST(risk_rating AS DECIMAL(4,2)))
            AS DECIMAL(4,2)) AS avg_rating_2dp
FROM dbo.customers;
