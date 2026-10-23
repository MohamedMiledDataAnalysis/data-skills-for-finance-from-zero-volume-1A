-- 01_aggregates.sql - five summaries of the loan book
SELECT COUNT(*)       AS loans,
       SUM(principal) AS total,
       AVG(principal) AS average,
       MIN(principal) AS smallest,
       MAX(principal) AS largest
FROM dbo.loans;
