# ex2_balances.py — deposits by account type and currency
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("ex2-balances")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

accounts = spark.read.csv("data/csv/accounts.csv",
                          header=True, inferSchema=True)

(accounts.groupBy("account_type", "currency")
    .agg(F.count("*").alias("accounts"),
         F.format_number(F.sum("balance"), 2)
          .alias("total_balance"),
         F.sum(F.when(F.col("balance") < 0, 1).otherwise(0))
          .alias("overdrawn"))
    .orderBy("account_type", "currency")
    .show())

spark.stop()
