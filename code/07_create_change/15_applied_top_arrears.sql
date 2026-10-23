-- 15_applied_top_arrears.sql - the three largest arrears
-- loans per product go on the watch list
WITH arrears AS (
    SELECT loan_id,
           product,
           status,
           principal,
           ROW_NUMBER() OVER (PARTITION BY product
                              ORDER BY principal DESC)
               AS size_rank
    FROM dbo.loans
    WHERE status <> 'Performing'
)
SELECT loan_id, product, status, principal, size_rank
FROM arrears
WHERE size_rank <= 3
ORDER BY product, size_rank;
