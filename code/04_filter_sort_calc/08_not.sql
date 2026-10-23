-- 08_not.sql - customers outside the United Kingdom
SELECT COUNT(*) AS non_uk_customers
FROM dbo.customers
WHERE NOT country = 'United Kingdom';

SELECT COUNT(*) AS not_in_list
FROM dbo.loans
WHERE product NOT IN ('Mortgage', 'SME');
