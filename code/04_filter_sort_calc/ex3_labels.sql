-- ex3_labels.sql - readable account labels
SELECT TOP (5)
       account_id,
       CONCAT(account_id, ' (', account_type, ', ',
              currency, ')')            AS account_label,
       UPPER(LEFT(account_type, 3))      AS type_code
FROM dbo.accounts
ORDER BY account_id;
