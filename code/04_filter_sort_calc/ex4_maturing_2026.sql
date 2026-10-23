-- ex4_maturing_2026.sql - loans that mature during 2026
SELECT TOP (5)
       loan_id,
       product,
       principal,
       origination_date AS orig_date,
       term_months      AS term,
       DATEADD(month, term_months, origination_date)
           AS maturity_date
FROM dbo.loans
WHERE DATEADD(month, term_months, origination_date)
      BETWEEN '2026-01-01' AND '2026-12-31'
ORDER BY principal DESC;

SELECT COUNT(*) AS maturing_2026
FROM dbo.loans
WHERE DATEADD(month, term_months, origination_date)
      BETWEEN '2026-01-01' AND '2026-12-31';
