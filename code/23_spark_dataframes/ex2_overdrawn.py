# ex2_overdrawn.py — overdrawn accounts, most overdrawn first
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("ex2-overdrawn")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

accounts = spark.read.csv("data/csv/accounts.csv",
                          header=True, inferSchema=True)

overdrawn = (accounts
             .filter(col("balance") < 0)
             .orderBy(col("balance").asc()))
print("Overdrawn accounts:", overdrawn.count())
overdrawn.select("account_id", "customer_id", "account_type",
                 "currency", "balance").show(5)

print("Overdrawn by currency:")
for ccy in ["GBP", "EUR", "USD"]:
    n = overdrawn.filter(col("currency") == ccy).count()
    print(f"  {ccy}: {n}")

spark.stop()
