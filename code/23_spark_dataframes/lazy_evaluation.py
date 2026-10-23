# lazy_evaluation.py — transformations wait, actions run
import os
import sys
import time

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("northbridge-lazy")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

txns = spark.read.csv(
    "data/csv/transactions.csv", header=True, inferSchema=True
)

start = time.perf_counter()
fees = txns.filter(col("category") == "Fees")
fee_amounts = fees.select("transaction_id", "amount")
plan_seconds = time.perf_counter() - start
print(f"Two transformations took {plan_seconds:.3f} s")
print("Type of fee_amounts:", type(fee_amounts).__name__)

start = time.perf_counter()
n = fee_amounts.count()
run_seconds = time.perf_counter() - start
print(f"count() returned {n} rows in {run_seconds:.3f} s")

spark.stop()
