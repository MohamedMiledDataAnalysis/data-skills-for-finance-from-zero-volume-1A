-- 07_metadata.sql - the data dictionary of dbo.loans
USE Northbridge;
SELECT COLUMN_NAME,
       DATA_TYPE,
       CHARACTER_MAXIMUM_LENGTH AS max_len,
       NUMERIC_PRECISION        AS prec,
       NUMERIC_SCALE            AS scale,
       IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'loans'
ORDER BY ORDINAL_POSITION;
