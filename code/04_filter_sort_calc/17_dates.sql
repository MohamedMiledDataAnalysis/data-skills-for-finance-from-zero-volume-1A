-- 17_dates.sql - date parts, gaps and shifts
SELECT TOP (5) loan_id,
       origination_date,
       YEAR(origination_date)    AS orig_year,
       MONTH(origination_date)   AS orig_month,
       EOMONTH(origination_date) AS month_end
FROM dbo.loans
ORDER BY loan_id;

SELECT TOP (5) loan_id,
       term_months,
       DATEDIFF(month, origination_date, '2025-12-31')
           AS months_on_book,
       DATEADD(month, term_months, origination_date)
           AS maturity_date
FROM dbo.loans
ORDER BY loan_id;
