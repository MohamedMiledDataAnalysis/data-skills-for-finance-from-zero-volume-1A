-- 15_convert.sql - dates as UK-style text
SELECT TOP (3) loan_id,
       origination_date,
       CONVERT(VARCHAR(10), origination_date, 103)
           AS uk_date,
       CONCAT(term_months, ' months')
           AS term_text
FROM dbo.loans
ORDER BY loan_id;
