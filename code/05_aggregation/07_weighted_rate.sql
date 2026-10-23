-- 07_weighted_rate.sql - simple and weighted average rate
SELECT product,
       CAST(AVG(interest_rate) AS DECIMAL(5,2))
           AS simple_avg_rate,
       CAST(SUM(principal * interest_rate)
            / SUM(principal) AS DECIMAL(5,2))
           AS weighted_avg_rate
FROM dbo.loans
GROUP BY product
ORDER BY product;
