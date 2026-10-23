-- 08_view.sql - a saved query everyone can reuse
DROP VIEW IF EXISTS dbo.v_loan_summary;
GO
CREATE VIEW dbo.v_loan_summary AS
SELECT product,
       COUNT(*)                               AS loan_count,
       SUM(principal)                         AS total_principal,
       CAST(SUM(principal * interest_rate)
            / SUM(principal) AS DECIMAL(5,2)) AS wavg_rate,
       SUM(CASE WHEN status <> 'Performing'
                THEN 1 ELSE 0 END)            AS arrears_count
FROM dbo.loans
GROUP BY product;
GO
SELECT *
FROM dbo.v_loan_summary
ORDER BY total_principal DESC;
