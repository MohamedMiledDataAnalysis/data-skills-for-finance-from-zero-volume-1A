-- 05_no_loans.sql - customers who hold no loan at all
SELECT c.customer_id,
       c.first_name,
       c.last_name,
       c.segment
FROM dbo.customers AS c
LEFT JOIN dbo.loans AS l
    ON c.customer_id = l.customer_id
WHERE l.loan_id IS NULL
ORDER BY c.customer_id;

SELECT COUNT(*) AS customers_without_loans
FROM dbo.customers AS c
LEFT JOIN dbo.loans AS l
    ON c.customer_id = l.customer_id
WHERE l.loan_id IS NULL;
