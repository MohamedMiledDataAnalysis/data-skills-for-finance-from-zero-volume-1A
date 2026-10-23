-- 01_create_table.sql - a watch list for credit risk
DROP TABLE IF EXISTS dbo.loan_watchlist;

CREATE TABLE dbo.loan_watchlist (
    watch_id    INT           IDENTITY(1,1) PRIMARY KEY,
    loan_id     VARCHAR(10)   NOT NULL
                REFERENCES dbo.loans(loan_id),
    reason      NVARCHAR(100) NOT NULL,
    priority    TINYINT       NOT NULL
                CHECK (priority BETWEEN 1 AND 3),
    added_on    DATE          NOT NULL
                DEFAULT '2026-01-05',
    reviewed    BIT           NOT NULL DEFAULT 0
);

SELECT * FROM dbo.loan_watchlist;
