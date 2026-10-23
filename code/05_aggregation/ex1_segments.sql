-- ex1_segments.sql - customers and average risk by segment
SELECT segment,
       COUNT(*) AS customers,
       CAST(AVG(risk_rating * 1.0) AS DECIMAL(4,2))
           AS avg_risk_rating
FROM dbo.customers
GROUP BY segment
ORDER BY customers DESC;
