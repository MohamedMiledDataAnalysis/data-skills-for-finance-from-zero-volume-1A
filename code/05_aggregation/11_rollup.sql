-- 11_rollup.sql - subtotals and a grand total
SELECT COALESCE(product, 'ALL PRODUCTS') AS product_group,
       COUNT(*)                          AS loan_count,
       SUM(principal)                    AS total_principal
FROM dbo.loans
GROUP BY ROLLUP (product)
ORDER BY GROUPING(product), product_group;
