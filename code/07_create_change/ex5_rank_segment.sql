-- ex5_rank_segment.sql - top two borrowers in each segment
WITH borrower AS (
    SELECT l.customer_id,
           c.segment,
           SUM(l.principal) AS total_principal
    FROM dbo.loans AS l
    INNER JOIN dbo.customers AS c
        ON l.customer_id = c.customer_id
    GROUP BY l.customer_id, c.segment
),
ranked AS (
    SELECT customer_id,
           segment,
           total_principal,
           RANK() OVER (PARTITION BY segment
                        ORDER BY total_principal DESC)
               AS segment_rank
    FROM borrower
)
SELECT segment, segment_rank, customer_id, total_principal
FROM ranked
WHERE segment_rank <= 2
ORDER BY segment, segment_rank;
