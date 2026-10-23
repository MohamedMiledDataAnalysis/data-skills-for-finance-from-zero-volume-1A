# first_query.py - connect and count the loans
import pyodbc

conn_str = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=localhost\\SQLEXPRESS;"
    "Database=Northbridge;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM dbo.loans;")
row = cursor.fetchone()
print("Loans in SQL Server:", row[0])

conn.close()
