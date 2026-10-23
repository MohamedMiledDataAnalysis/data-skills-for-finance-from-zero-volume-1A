# ex4_month_change.py — month-on-month change in card spending
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("ex4-month-change")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

txns = spark.read.csv("data/csv/transactions.csv",
                      header=True, inferSchema=True)

card = (txns
        .filter((F.col("channel") == "Card")
                & (F.col("currency") == "GBP")
                & (F.col("amount") < 0))
        .withColumn("txn_month",
                    F.date_format("txn_date", "yyyy-MM"))
        .groupBy("txn_month")
        .agg(F.round(-F.sum("amount"), 2).alias("spend")))

by_month = Window.orderBy("txn_month")
(card
    .withColumn("previous", F.lag("spend").over(by_month))
    .withColumn("change_pct",
                F.round(100 * (F.col("spend") - F.col("previous"))
                        / F.col("previous"), 1))
    .orderBy("txn_month")
    .show(12))

spark.stop()
