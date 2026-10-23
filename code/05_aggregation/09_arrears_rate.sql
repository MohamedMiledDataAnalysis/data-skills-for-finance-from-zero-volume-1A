-- 09_arrears_rate.sql - arrears rate by product, done right
SELECT product,
       COUNT(*) AS loan_count,
       SUM(CASE WHEN status <> 'Performing' THEN 1 ELSE 0 END)
           AS arrears_count,
       CAST(100.0
            * SUM(CASE WHEN status <> 'Performing'
                       THEN 1 ELSE 0 END)
            / COUNT(*) AS DECIMAL(5,2)) AS arrears_rate_pct
FROM dbo.loans
GROUP BY product
ORDER BY arrears_rate_pct DESC;
