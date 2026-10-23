-- ex6_page3.sql - page 3 of the customer list, with tenure
-- at 30 June 2025: years crossed and completed years
SELECT customer_id,
       join_date,
       DATEDIFF(year, join_date, '2025-06-30') AS years_crossed,
       DATEDIFF(year, join_date, '2025-06-30')
         - CASE WHEN DATEADD(year,
                        DATEDIFF(year, join_date, '2025-06-30'),
                        join_date) > '2025-06-30'
                THEN 1 ELSE 0 END             AS tenure_years
FROM dbo.customers
ORDER BY customer_id
OFFSET 20 ROWS
FETCH NEXT 10 ROWS ONLY;
