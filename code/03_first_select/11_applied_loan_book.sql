-- 11_applied_loan_book.sql - first look at the loan book
USE Northbridge;

-- Step 1: how many loans?
SELECT COUNT(*) AS loan_count
FROM dbo.loans;

-- Step 2: which products and statuses exist?
SELECT DISTINCT product
FROM dbo.loans
ORDER BY product;

SELECT DISTINCT status
FROM dbo.loans
ORDER BY status;

-- Step 3: how many borrowers?
SELECT COUNT(DISTINCT customer_id) AS borrower_count
FROM dbo.loans;

-- Step 4: a readable sample for the briefing note
SELECT TOP (8)
       loan_id          AS [Loan],
       product          AS [Product],
       principal        AS [Principal (GBP)],
       interest_rate    AS [Rate %],
       status           AS [Status],
       ltv              AS [LTV %]
FROM dbo.loans
ORDER BY loan_id;
