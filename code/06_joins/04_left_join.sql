-- 04_left_join.sql - every customer, with loans if any
SELECT c.customer_id,
       c.last_name,
       c.segment,
       l.loan_id,
       l.product
FROM dbo.customers AS c
LEFT JOIN dbo.loans AS l
    ON c.customer_id = l.customer_id
WHERE c.customer_id IN ('C0001', 'C0002', 'C0003')
ORDER BY c.customer_id, l.loan_id;
