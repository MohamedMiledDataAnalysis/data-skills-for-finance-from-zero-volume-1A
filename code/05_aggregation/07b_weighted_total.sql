-- 07b_weighted_total.sql - simple and weighted rate, whole book
SELECT CAST(AVG(interest_rate) AS DECIMAL(5,2))
           AS simple_avg_rate,
       CAST(SUM(principal * interest_rate)
            / SUM(principal) AS DECIMAL(5,2))
           AS weighted_avg_rate
FROM dbo.loans;
