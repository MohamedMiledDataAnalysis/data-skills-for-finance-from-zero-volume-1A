# parquet_partitioned.py — write transactions as Parquet,
# one folder per month, then read one month back
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("northbridge-parquet")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

txns = spark.read.csv("data/csv/transactions.csv",
                      header=True, inferSchema=True)
txns = txns.withColumn("txn_month",
                       F.date_format("txn_date", "yyyy-MM"))

(txns.write
    .mode("overwrite")
    .partitionBy("txn_month")
    .parquet("output/transactions_parquet"))

folders = sorted(
    d for d in os.listdir("output/transactions_parquet")
    if d.startswith("txn_month=")
)
print("Folders written:", len(folders))
print("First:", folders[0], "| last:", folders[-1])

back = spark.read.parquet("output/transactions_parquet")
print("Rows read back:", back.count())

march = back.filter(F.col("txn_month") == "2025-03")
print("Rows in March 2025:", march.count())

spark.stop()
