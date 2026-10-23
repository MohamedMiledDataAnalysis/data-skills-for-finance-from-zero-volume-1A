# json_and_parquet.py — read JSON, write Parquet, read it back
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("northbridge-json-parquet")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

# loans.json is one JSON array spread over many lines
loans_json = spark.read.json("data/json/loans.json",
                             multiLine=True)
loans_json.printSchema()
print("Rows from JSON:", loans_json.count())

# A missing LTV is written null in JSON and read as NULL
print("Loans without LTV:",
      loans_json.filter(col("ltv").isNull()).count())

# Write the loans to Parquet, then read the Parquet folder
(loans_json.write
    .mode("overwrite")
    .parquet("output/loans_parquet"))

loans_pq = spark.read.parquet("output/loans_parquet")
print("Rows from Parquet:", loans_pq.count())
loans_pq.select("loan_id", "product", "principal").show(3)

spark.stop()
