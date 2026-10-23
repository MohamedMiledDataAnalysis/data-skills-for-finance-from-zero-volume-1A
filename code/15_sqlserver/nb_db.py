"""nb_db.py: connect to the Northbridge database on SQL Server.

Settings come from environment variables, never from the code:
    NB_SQL_SERVER    localhost\\SQLEXPRESS (default: Express),
                     localhost (Developer), localhost,1433 (Docker)
    NB_SQL_USER      SQL login, e.g. sa (leave unset on Windows)
    NB_SQL_PASSWORD  password of that login
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL


def get_engine():
    server = os.environ.get("NB_SQL_SERVER",
                            "localhost\\SQLEXPRESS")
    host, _, port = server.partition(",")
    user = os.environ.get("NB_SQL_USER")
    url = URL.create(
        "mssql+pyodbc",
        username=user,
        password=os.environ.get("NB_SQL_PASSWORD"),
        host=host,
        port=int(port) if port else None,
        database="Northbridge",
        query={
            "driver": "ODBC Driver 18 for SQL Server",
            "TrustServerCertificate": "yes",
        },
    )
    return create_engine(url, fast_executemany=True)
