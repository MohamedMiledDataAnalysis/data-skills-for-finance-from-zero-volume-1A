/* ex6_customer_profile.sql
   One-line profile of the customer base for a briefing.
*/
USE Northbridge;
SELECT COUNT(*)                 AS customers,  -- rows
       COUNT(DISTINCT city)     AS cities, -- home cities
       COUNT(DISTINCT country)  AS countries,
       COUNT(DISTINCT segment)  AS segments,
       MIN(join_date)           AS first_joined,
       MAX(join_date)           AS last_joined
FROM dbo.customers;
