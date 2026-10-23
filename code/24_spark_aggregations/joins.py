# joins.py — customers, accounts and transactions together
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("northbridge-joins")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

customers = spark.read.csv("data/csv/customers.csv",
                           header=True, inferSchema=True)
accounts = spark.read.csv("data/csv/accounts.csv",
                          header=True, inferSchema=True)
txns = spark.read.csv("data/csv/transactions.csv",
                      header=True, inferSchema=True)
loans = spark.read.csv("data/csv/loans.csv",
                       header=True, inferSchema=True)

# 1. Inner join: accounts with their owner's segment
acc_cust = accounts.join(
    customers.select("customer_id", "segment", "city"),
    on="customer_id",
    how="inner",
)
print("Accounts:", accounts.count(),
      "| after inner join:", acc_cust.count())

# 2. Three tables: transactions -> accounts -> customers
txn_full = txns.join(acc_cust, on="account_id", how="inner")
print("Transactions after join:", txn_full.count())
(txn_full.groupBy("segment")
    .agg(F.count("*").alias("txns"),
         F.round(F.sum("amount"), 2).alias("net_flow"))
    .orderBy("segment")
    .show())

# 3. Left join: every customer, with loans if they have any
cust_loans = customers.join(
    loans.select("customer_id", "loan_id", "principal"),
    on="customer_id",
    how="left",
)
no_loan = cust_loans.filter(F.col("loan_id").isNull())
print("Customers without any loan:",
      no_loan.select("customer_id").distinct().count())

# 4. Broadcast hint: copy the small table to every worker
txn_bc = txns.join(F.broadcast(acc_cust), on="account_id")
print("Transactions after broadcast join:", txn_bc.count())

spark.stop()
