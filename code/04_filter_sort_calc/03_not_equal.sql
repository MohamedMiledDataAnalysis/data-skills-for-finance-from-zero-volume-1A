-- 03_not_equal.sql - loans that are not performing
SELECT COUNT(*) AS non_performing
FROM dbo.loans
WHERE status <> 'Performing';
