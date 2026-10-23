-- 10_row_number.sql - number the loans of each customer
SELECT customer_id,
       loan_id,
       origination_date,
       ROW_NUMBER() OVER (PARTITION BY customer_id
                          ORDER BY origination_date)
           AS loan_seq
FROM dbo.loans
WHERE customer_id IN ('C0002', 'C0003')
ORDER BY customer_id, loan_seq;
