# ex2_accounts.py - start Spark and count accounts by currency
import os
import sys

from pyspark.sql import SparkSession

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("Northbridge first Spark job")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

accounts = spark.read.csv(
    "data/csv/accounts.csv", header=True, inferSchema=True
)
print("Spark version:", spark.version)
print("Rows read:", accounts.count())
accounts.groupBy("currency").count().orderBy("currency").show()

input("Spark UI: http://localhost:4040 - press Enter to stop")
spark.stop()
