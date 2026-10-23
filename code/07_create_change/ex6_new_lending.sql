-- ex6_new_lending.sql - 2025 new lending, month by month,
-- with a year-to-date running total
WITH monthly AS (
    SELECT MONTH(origination_date) AS orig_month,
           COUNT(*)                AS new_loans,
           SUM(principal)          AS new_lending
    FROM dbo.loans
    WHERE origination_date >= '2025-01-01'
      AND origination_date <  '2026-01-01'
    GROUP BY MONTH(origination_date)
)
SELECT orig_month,
       new_loans,
       new_lending,
       SUM(new_lending) OVER (ORDER BY orig_month
                              ROWS UNBOUNDED PRECEDING)
           AS ytd_lending
FROM monthly
ORDER BY orig_month;
