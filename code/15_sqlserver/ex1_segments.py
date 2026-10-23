# ex1_segments.py - Exercise 1, customers by segment
import pyodbc

conn = pyodbc.connect(
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=localhost\\SQLEXPRESS;Database=Northbridge;"
    "Trusted_Connection=yes;TrustServerCertificate=yes;"
)
cursor = conn.cursor()
cursor.execute("""
    SELECT segment, COUNT(*) AS customers
    FROM dbo.customers
    GROUP BY segment
    ORDER BY customers DESC;
""")
for segment, customers in cursor.fetchall():
    print(f"{segment:<8}{customers:>4}")
conn.close()
