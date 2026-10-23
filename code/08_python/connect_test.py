# connect_test.py - read five loans from SQL Server through
# ODBC Driver 18 (Windows, SQL Server Express)
import pyodbc

CONN = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=localhost\\SQLEXPRESS;"
    "Database=Northbridge;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)
SQL = """
SELECT TOP 5 loan_id, product, principal, status
FROM dbo.loans
ORDER BY loan_id;
"""

conn = pyodbc.connect(CONN)
for row in conn.cursor().execute(SQL):
    print(f"{row[0]}  {row[1]:<9} £{row[2]:>12,.2f}  {row[3]}")
conn.close()
