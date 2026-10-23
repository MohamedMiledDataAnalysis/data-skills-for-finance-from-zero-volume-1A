SELECT product,
       COUNT(*)       AS loans,
       SUM(principal) AS principal
FROM dbo.loans
GROUP BY product
ORDER BY product;
