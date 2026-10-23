# first_spark.py - start Spark and count Northbridge loans
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

loans = spark.read.csv(
    "data/csv/loans.csv", header=True, inferSchema=True
)
print("Spark version:", spark.version)
print("Rows read:", loans.count())
loans.groupBy("product").count().orderBy("product").show()

input("Spark UI: http://localhost:4040 - press Enter to stop")
spark.stop()
