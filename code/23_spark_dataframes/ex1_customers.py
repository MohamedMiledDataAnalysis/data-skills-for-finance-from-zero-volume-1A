# ex1_customers.py — Private customers in London
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("ex1-customers")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

customers = spark.read.csv("data/csv/customers.csv",
                           header=True, inferSchema=True)
customers.printSchema()
print("Customers:", customers.count())

london_private = customers.filter(
    (col("city") == "London") & (col("segment") == "Private")
)
print("Private customers in London:", london_private.count())
london_private.select("customer_id", "first_name", "last_name",
                      "join_date").orderBy("join_date").show(5)

spark.stop()
