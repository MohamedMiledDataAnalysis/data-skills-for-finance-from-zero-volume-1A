SELECT category, COUNT(*) AS n, SUM(amount) AS total
FROM dbo.transactions
GROUP BY category
ORDER BY category;
