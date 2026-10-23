-- ex2_overdrawn.sql - copy overdrawn accounts into a new table
DROP TABLE IF EXISTS dbo.overdrawn_accounts;

CREATE TABLE dbo.overdrawn_accounts (
    account_id   VARCHAR(10)   NOT NULL PRIMARY KEY,
    customer_id  VARCHAR(10)   NOT NULL,
    currency     CHAR(3)       NOT NULL,
    balance      DECIMAL(14,2) NOT NULL
);

INSERT INTO dbo.overdrawn_accounts
       (account_id, customer_id, currency, balance)
SELECT account_id, customer_id, currency, balance
FROM dbo.accounts
WHERE balance < 0;

SELECT currency,
       COUNT(*)     AS accounts,
       SUM(balance) AS total_overdrawn
FROM dbo.overdrawn_accounts
GROUP BY currency
ORDER BY currency;
