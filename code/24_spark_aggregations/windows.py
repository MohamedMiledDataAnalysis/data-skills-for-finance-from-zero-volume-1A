# windows.py — ranking and running totals with windows
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("northbridge-windows")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

loans = spark.read.csv("data/csv/loans.csv",
                       header=True, inferSchema=True)
txns = spark.read.csv("data/csv/transactions.csv",
                      header=True, inferSchema=True)

# 1. row_number: the three largest loans in each product
by_size = (Window.partitionBy("product")
           .orderBy(F.col("principal").desc()))
top3 = (loans
        .withColumn("rank_in_product",
                    F.row_number().over(by_size))
        .filter(F.col("rank_in_product") <= 3)
        .select("product", "rank_in_product", "loan_id",
                "principal"))
top3.orderBy("product", "rank_in_product").show(12)

# 2. Running total of monthly net cash flow in GBP
monthly = (
    txns.filter(F.col("currency") == "GBP")
    .withColumn("txn_month",
                F.date_format("txn_date", "yyyy-MM"))
    .groupBy("txn_month")
    .agg(F.round(F.sum("amount"), 2).alias("net_flow"))
)
running = Window.orderBy("txn_month").rowsBetween(
    Window.unboundedPreceding, Window.currentRow
)
(monthly
    .withColumn("cumulative",
                F.round(F.sum("net_flow").over(running), 2))
    .orderBy("txn_month")
    .show(12))

spark.stop()
