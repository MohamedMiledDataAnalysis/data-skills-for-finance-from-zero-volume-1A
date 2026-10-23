SELECT segment, COUNT(*) AS customers
FROM dbo.customers
GROUP BY segment
ORDER BY customers DESC;

SELECT account_id, account_type, currency, balance
FROM dbo.accounts
WHERE customer_id = 'C0005'
ORDER BY account_id;

SELECT loan_id, customer_id, principal, status
FROM dbo.loans
WHERE product = 'Mortgage' AND principal >= 600000
ORDER BY principal DESC;

SELECT COUNT(*) AS n FROM dbo.loans
WHERE product = 'SME' AND principal >= 600000;

SELECT channel, COUNT(*) AS n FROM dbo.transactions
GROUP BY channel ORDER BY n DESC;

SELECT rate_date, currency, rate_per_gbp FROM dbo.fx_rates;
