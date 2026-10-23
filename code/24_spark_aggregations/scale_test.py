# scale_test.py — one million synthetic transactions
import os
import sys
import time

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("northbridge-scale-test")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

N = 1_000_000

# spark.range(N) makes a DataFrame with one column, id, 0..N-1
synthetic = (
    spark.range(N)
    .withColumn("account_no",
                (F.rand(seed=2026) * 862).cast("int") + 1)
    .withColumn("amount",
                F.round((F.rand(seed=7) - 0.6) * 2000, 2))
    .withColumn("month",
                (F.rand(seed=11) * 12).cast("int") + 1)
)
synthetic.show(3)

start = time.perf_counter()
monthly = (synthetic.groupBy("month")
           .agg(F.count("*").alias("txns"),
                F.round(F.sum("amount"), 2).alias("net_flow"),
                F.countDistinct("account_no").alias("accounts"))
           .orderBy("month"))
rows = monthly.collect()
seconds = time.perf_counter() - start

for r in rows[:3]:
    print(r["month"], r["txns"], r["net_flow"], r["accounts"])
print("...")
print("Total transactions:", sum(r["txns"] for r in rows))
print(f"Aggregation took {seconds:.2f} seconds")

spark.stop()
