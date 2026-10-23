# connect_test_docker.py - the same test for SQL Server
# running in Docker (macOS and Linux)
import pyodbc

CONN = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=localhost,1433;"
    "Database=Northbridge;"
    "UID=sa;"
    "PWD=Northbridge#2026;"
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
