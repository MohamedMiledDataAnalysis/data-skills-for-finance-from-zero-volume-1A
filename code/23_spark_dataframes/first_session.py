# first_session.py — start Spark, print its version, stop it
import os
import sys

from pyspark.sql import SparkSession

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("northbridge-first-session")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

print("Spark version:", spark.version)
print("Application name:", spark.sparkContext.appName)
print("Master:", spark.sparkContext.master)
print("Cores available:", spark.sparkContext.defaultParallelism)

spark.stop()
