# ex3_large_txns.py — keep large transactions for monitoring
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, abs as spark_abs, when
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType, DateType,
)

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("ex3-large-txns")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

txn_schema = StructType([
    StructField("transaction_id", StringType()),
    StructField("account_id", StringType()),
    StructField("txn_date", DateType()),
    StructField("amount", DoubleType()),
    StructField("currency", StringType()),
    StructField("category", StringType()),
    StructField("channel", StringType()),
])

txns = spark.read.csv("data/csv/transactions.csv",
                      header=True, schema=txn_schema)

large = (
    txns
    .filter(spark_abs(col("amount")) > 5000)
    .withColumn("direction",
                when(col("amount") < 0, "Out").otherwise("In"))
    .orderBy(spark_abs(col("amount")).desc())
)
print("Transactions above 5,000 in either direction:",
      large.count())
large.select("transaction_id", "txn_date", "amount",
               "category", "direction").show(5)

spark.stop()
