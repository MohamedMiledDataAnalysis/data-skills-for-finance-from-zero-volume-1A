-- ex1_loans_names.sql - defaulted loans with borrower details
SELECT l.loan_id,
       c.first_name,
       c.last_name,
       c.city,
       l.product,
       l.principal
FROM dbo.loans AS l
INNER JOIN dbo.customers AS c
    ON l.customer_id = c.customer_id
WHERE l.status = 'Default'
  AND c.country = 'United Kingdom'
ORDER BY l.principal DESC;
