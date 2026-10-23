-- ex1_mortgages.sql - how many mortgages are in the book?
USE Northbridge;
SELECT COUNT(*) AS mortgages
FROM dbo.loans
WHERE product = 'Mortgage';
