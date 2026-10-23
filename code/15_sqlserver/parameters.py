# parameters.py - pass values with ? parameters
import pyodbc

conn = pyodbc.connect(
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=localhost\\SQLEXPRESS;Database=Northbridge;"
    "Trusted_Connection=yes;TrustServerCertificate=yes;"
)
cursor = conn.cursor()

product = "Auto"
status = "Default"
cursor.execute(
    """
    SELECT loan_id, customer_id, principal
    FROM dbo.loans
    WHERE product = ? AND status = ?
    ORDER BY loan_id;
    """,
    (product, status),
)
for loan_id, customer_id, principal in cursor.fetchall():
    print(f"{loan_id}  {customer_id}  £{principal:>10,.2f}")

conn.close()
