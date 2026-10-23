-- 13_applied_portfolio.sql - portfolio summary for ALCO
SELECT product,
       COUNT(*)                                AS loans,
       COUNT(DISTINCT customer_id)             AS clients,
       CAST(SUM(principal) / 1000000
            AS DECIMAL(10,2))                  AS gbp_m,
       CAST(AVG(principal) AS DECIMAL(14,2))   AS avg_loan,
       CAST(SUM(principal * interest_rate)
            / SUM(principal) AS DECIMAL(5,2))  AS wa_rate,
       CAST(100.0
            * SUM(CASE WHEN status <> 'Performing'
                       THEN principal ELSE 0 END)
            / SUM(principal) AS DECIMAL(5,2))  AS arr_pct
FROM dbo.loans
WHERE origination_date < '2025-07-01'
GROUP BY product
HAVING COUNT(*) >= 100
ORDER BY gbp_m DESC;
