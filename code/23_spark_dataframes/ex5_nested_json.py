# ex5_nested_json.py — read nested customers.json
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, size, explode

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("ex5-nested-json")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

customers = spark.read.json("data/json/customers.json",
                            multiLine=True)
customers.printSchema()

flat = customers.select(
    "customer_id",
    "segment",
    col("address.city").alias("city"),
    size(col("accounts")).alias("n_accounts"),
)
print("Customers with 3 accounts or more:",
      flat.filter(col("n_accounts") >= 3).count())
flat.filter(col("n_accounts") >= 3).show(3)

# One row per account: explode turns each list element
# into its own row
accounts = customers.select(
    "customer_id",
    explode(col("accounts")).alias("acc"),
).select("customer_id", "acc.account_id", "acc.account_type",
         "acc.currency", "acc.balance")
print("Account rows after explode:", accounts.count())
accounts.show(4)

spark.stop()
