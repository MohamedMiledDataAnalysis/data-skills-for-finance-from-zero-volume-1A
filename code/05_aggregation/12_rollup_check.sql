-- 12_rollup_check.sql - the same totals without ROLLUP
SELECT 1              AS sort_key,
       product        AS product_group,
       COUNT(*)       AS loan_count,
       SUM(principal) AS total_principal
FROM dbo.loans
GROUP BY product
UNION ALL
SELECT 2,
       'ALL PRODUCTS',
       COUNT(*),
       SUM(principal)
FROM dbo.loans
ORDER BY sort_key, product_group;
