-- 15_union_vs_all.sql - UNION ALL keeps repeats, UNION drops them
SELECT customer_id, 'account' AS source
FROM dbo.accounts WHERE customer_id = 'C0002'
UNION ALL
SELECT customer_id, 'loan'
FROM dbo.loans WHERE customer_id = 'C0002'
ORDER BY source;

SELECT customer_id FROM dbo.accounts WHERE customer_id = 'C0002'
UNION
SELECT customer_id FROM dbo.loans WHERE customer_id = 'C0002'
ORDER BY customer_id;
