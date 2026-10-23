-- 16_union_counts.sql - counting each version
SELECT COUNT(*) AS union_all_rows
FROM (SELECT customer_id FROM dbo.accounts
      UNION ALL
      SELECT customer_id FROM dbo.loans) AS u;

SELECT COUNT(*) AS union_rows
FROM (SELECT customer_id FROM dbo.accounts
      UNION
      SELECT customer_id FROM dbo.loans) AS u;
