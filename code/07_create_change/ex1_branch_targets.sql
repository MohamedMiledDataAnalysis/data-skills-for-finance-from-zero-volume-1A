-- ex1_branch_targets.sql - a small reference table
DROP TABLE IF EXISTS dbo.branch_targets;

CREATE TABLE dbo.branch_targets (
    city              NVARCHAR(50) NOT NULL PRIMARY KEY,
    target_customers  INT          NOT NULL
                      CHECK (target_customers > 0),
    region            VARCHAR(10)  NOT NULL
);

INSERT INTO dbo.branch_targets (city, target_customers, region)
VALUES (N'London',     160, 'South'),
       (N'Manchester',  60, 'North'),
       (N'Edinburgh',   50, 'Scotland');

SELECT t.city,
       t.region,
       t.target_customers,
       COUNT(c.customer_id) AS actual_customers
FROM dbo.branch_targets AS t
LEFT JOIN dbo.customers AS c
    ON c.city = t.city
GROUP BY t.city, t.region, t.target_customers
ORDER BY t.city;
