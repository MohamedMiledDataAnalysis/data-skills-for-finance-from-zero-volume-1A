-- arrears_check.sql - loans not performing, and their principal
USE Northbridge;
SELECT COUNT(*) AS loans_in_arrears,
       SUM(principal) AS principal_in_arrears
FROM dbo.loans
WHERE status <> 'Performing';
