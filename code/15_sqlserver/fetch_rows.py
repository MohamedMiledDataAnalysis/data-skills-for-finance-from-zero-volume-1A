# fetch_rows.py - read several rows with fetchall
import pyodbc

conn = pyodbc.connect(
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=localhost\\SQLEXPRESS;Database=Northbridge;"
    "Trusted_Connection=yes;TrustServerCertificate=yes;"
)
cursor = conn.cursor()

cursor.execute("""
    SELECT TOP (5) loan_id, product, principal
    FROM dbo.loans
    ORDER BY principal DESC;
""")
rows = cursor.fetchall()
print(len(rows), "rows")
for loan_id, product, principal in rows:
    print(f"{loan_id}  {product:<9}£{principal:>13,.2f}")

conn.close()
