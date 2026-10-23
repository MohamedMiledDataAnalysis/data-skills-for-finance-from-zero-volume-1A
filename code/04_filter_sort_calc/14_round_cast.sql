-- 14_round_cast.sql - controlling decimals
SELECT TOP (5) loan_id,
       ROUND(principal * interest_rate / 100, 2)
           AS rounded,
       CAST(principal * interest_rate / 100
            AS DECIMAL(14,2)) AS cast_2dp,
       CAST(principal AS INT) AS principal_int
FROM dbo.loans
ORDER BY loan_id;
