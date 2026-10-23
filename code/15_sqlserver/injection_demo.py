# injection_demo.py - why values go in as parameters
import pyodbc

conn = pyodbc.connect(
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=localhost\\SQLEXPRESS;Database=Northbridge;"
    "Trusted_Connection=yes;TrustServerCertificate=yes;"
)
cursor = conn.cursor()

# What a user might type into a form field
typed = "Auto' OR '1'='1"

# WRONG: the text becomes part of the SQL itself
bad_sql = ("SELECT COUNT(*) FROM dbo.loans "
           f"WHERE product = '{typed}';")
print(bad_sql)
cursor.execute(bad_sql)
print("f-string rows:", cursor.fetchone()[0])

# RIGHT: the text travels separately, as a value
cursor.execute(
    "SELECT COUNT(*) FROM dbo.loans WHERE product = ?;",
    (typed,),
)
print("parameter rows:", cursor.fetchone()[0])
conn.close()
