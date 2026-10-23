# list_drivers.py - list the installed ODBC drivers
import pyodbc

for name in pyodbc.drivers():
    print(name)
