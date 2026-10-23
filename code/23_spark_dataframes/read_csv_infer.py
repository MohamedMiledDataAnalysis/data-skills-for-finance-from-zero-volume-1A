# read_csv_infer.py — read loans.csv and let Spark guess types
import os
import sys

from pyspark.sql import SparkSession

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("northbridge-read-csv")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

loans = spark.read.csv(
    "data/csv/loans.csv", header=True, inferSchema=True
)

loans.printSchema()
loans.select("loan_id", "product", "principal",
             "status", "ltv").show(5)
print("Rows:", loans.count())
print("Number of columns:", len(loans.columns))
print("First three:", loans.columns[:3])

spark.stop()
