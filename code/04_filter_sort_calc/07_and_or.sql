-- 07_and_or.sql - combining conditions
SELECT COUNT(*) AS wrong_way
FROM dbo.loans
WHERE product = 'Mortgage'
   OR product = 'SME'
  AND status = 'Default';

SELECT COUNT(*) AS right_way
FROM dbo.loans
WHERE (product = 'Mortgage' OR product = 'SME')
  AND status = 'Default';
