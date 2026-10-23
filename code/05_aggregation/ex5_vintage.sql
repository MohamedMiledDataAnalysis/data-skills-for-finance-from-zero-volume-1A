-- ex5_vintage.sql - default rate by origination year
SELECT YEAR(origination_date) AS vintage,
       COUNT(*)               AS loans,
       SUM(CASE WHEN status = 'Default' THEN 1 ELSE 0 END)
                              AS defaults,
       CAST(100.0
            * SUM(CASE WHEN status = 'Default'
                       THEN 1 ELSE 0 END)
            / COUNT(*) AS DECIMAL(5,2)) AS default_rate_pct
FROM dbo.loans
GROUP BY YEAR(origination_date)
ORDER BY vintage;
